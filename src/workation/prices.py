"""Preis-Layer: echte Scrapes zuerst, Schaetzungen als Fallback.

CSV-Schema (data/prices/*.csv), eine Zeile pro Angebot, Preis pro Person:

    origin,destination,depart_date,return_date,trip_type,price_eur,carrier,
    stops,duration_min,source,url,itinerary_id,leg_index

Pflichtfelder: origin, destination, depart_date, price_eur.
trip_type: oneway | return | multicity_leg (Default: oneway)
Bei multicity_leg gruppiert itinerary_id die Legs; der Gesamtpreis steht in
der Zeile mit leg_index == 0 (die anderen Legs duerfen price_eur = 0 haben).
"""

from __future__ import annotations

import csv
import datetime as dt
import statistics
from collections import defaultdict
from pathlib import Path

from .data import DATA_DIR, load_route_hints
from .models import PriceQuote

PRICES_DIR = DATA_DIR / "prices"

# Aufschlag, wenn eine Strecke nur ueber einen selbst gebauten Umstieg
# geschaetzt werden kann (Risiko + zweites Ticket).
SELF_CONNECT_PENALTY_EUR = 40.0

# EU-seitige Abflughaefen - fuer die saisonalen Aufschlaege auf Schaetzpreise.
EU_HUBS = frozenset({"MAD", "BCN", "BER", "HAM", "MUC", "LIS", "TFS", "TFN"})


def _parse_date(value: str) -> dt.date | None:
    value = (value or "").strip()
    if not value:
        return None
    return dt.date.fromisoformat(value)


def load_quotes(path: Path | None = None) -> list[PriceQuote]:
    """Liest alle CSVs aus data/prices/ (oder eine konkrete Datei)."""
    files = [path] if path else sorted(PRICES_DIR.glob("*.csv"))
    quotes: list[PriceQuote] = []
    for file in files:
        if not file.exists() or file.name.startswith("_"):
            continue
        with open(file, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if not (row.get("origin") and row.get("destination")):
                    continue
                try:
                    price = float(str(row["price_eur"]).replace(",", "."))
                except (KeyError, TypeError, ValueError):
                    continue
                quotes.append(
                    PriceQuote(
                        origin=row["origin"].strip().upper(),
                        destination=row["destination"].strip().upper(),
                        depart_date=_parse_date(row["depart_date"]),
                        return_date=_parse_date(row.get("return_date", "")),
                        trip_type=(row.get("trip_type") or "oneway").strip() or "oneway",
                        price_eur=price,
                        carrier=(row.get("carrier") or "").strip(),
                        stops=int(row["stops"]) if (row.get("stops") or "").strip() else None,
                        duration_min=(
                            int(row["duration_min"]) if (row.get("duration_min") or "").strip() else None
                        ),
                        source=(row.get("source") or "manual").strip(),
                        url=(row.get("url") or "").strip(),
                        itinerary_id=(row.get("itinerary_id") or "").strip(),
                        leg_index=int(row["leg_index"]) if (row.get("leg_index") or "").strip() else 0,
                    )
                )
    return quotes


class PriceBook:
    """Preisauskunft fuer eine Strecke an einem Datum."""

    def __init__(self, quotes: list[PriceQuote] | None = None, date_tolerance_days: int = 3):
        self.quotes = quotes if quotes is not None else load_quotes()
        self.tolerance = date_tolerance_days
        self.hints = load_route_hints()
        self._by_route: dict[tuple[str, str], list[PriceQuote]] = defaultdict(list)
        for q in self.quotes:
            if q.trip_type in ("oneway", "multicity_leg") and q.depart_date:
                self._by_route[(q.origin, q.destination)].append(q)
        self._estimate_cache: dict[tuple[str, str], float | None] = {}

    # ------------------------------------------------------------------ #
    @property
    def has_real_data(self) -> bool:
        return bool(self.quotes)

    def coverage(self) -> dict[str, int]:
        return {
            "quotes": len(self.quotes),
            "routes": len(self._by_route),
            "scraped": sum(1 for q in self.quotes if q.source.startswith("google")),
        }

    # ------------------------------------------------------------------ #
    def oneway(self, origin: str, destination: str, day: dt.date) -> tuple[float, str]:
        """(Preis pro Person, Quelle) fuer eine Einzelstrecke."""
        origin, destination = origin.upper(), destination.upper()
        if origin == destination:
            return 0.0, "none"

        candidates = self._by_route.get((origin, destination), [])
        if candidates:
            near = [q for q in candidates if abs((q.depart_date - day).days) <= self.tolerance]
            if near:
                best = min(near, key=lambda q: q.price_eur)
                return best.price_eur, best.source
            # Keine Preise in Datumsnaehe: Median der Strecke als grobe Hausnummer.
            median = statistics.median(q.price_eur for q in candidates)
            return median, "scrape_median_other_dates"

        est = self.estimate_oneway(origin, destination)
        if est is None:
            return float("inf"), "unknown"
        factor, reason = self.estimate_multiplier(origin, destination, day)
        if factor != 1.0:
            return est * factor, f"estimate*{factor:.2f}({reason})"
        return est, "estimate"

    def returned(self, origin: str, destination: str, out: dt.date, back: dt.date) -> tuple[float, str]:
        """(Preis pro Person, Quelle) fuer einen Return auf derselben Strecke."""
        origin, destination = origin.upper(), destination.upper()
        hits = [
            q
            for q in self.quotes
            if q.trip_type == "return"
            and q.origin == origin
            and q.destination == destination
            and q.depart_date
            and q.return_date
            and abs((q.depart_date - out).days) <= self.tolerance
            and abs((q.return_date - back).days) <= self.tolerance
        ]
        if hits:
            best = min(hits, key=lambda q: q.price_eur)
            return best.price_eur, best.source
        for entry in self.hints.get("longhaul", []):
            if origin in entry["from"] and entry["to"] == destination and entry.get("return_eur"):
                return float(entry["return_eur"]), "estimate"
        a, sa = self.oneway(origin, destination, out)
        b, sb = self.oneway(destination, origin, back)
        if a == float("inf") or b == float("inf"):
            return float("inf"), "unknown"
        # Returns sind in der Praxis guenstiger als 2x Oneway.
        return (a + b) * 0.88, f"derived({sa}+{sb})"

    def multicity(self, legs: list[tuple[str, str, dt.date]]) -> tuple[float, str] | None:
        """Gescrapter Multi-City-Gesamtpreis, falls genau diese Legs vorliegen."""
        groups: dict[str, list[PriceQuote]] = defaultdict(list)
        for q in self.quotes:
            if q.trip_type == "multicity_leg" and q.itinerary_id:
                groups[q.itinerary_id].append(q)
        wanted = [(o.upper(), d.upper()) for o, d, _ in legs]
        best: tuple[float, str] | None = None
        for itin_id, qs in groups.items():
            qs = sorted(qs, key=lambda q: q.leg_index)
            if [(q.origin, q.destination) for q in qs] != wanted:
                continue
            if any(abs((q.depart_date - legs[i][2]).days) > self.tolerance for i, q in enumerate(qs)):
                continue
            total = sum(q.price_eur for q in qs)
            if best is None or total < best[0]:
                best = (total, f"google_flights_multicity:{itin_id}")
        return best

    # ------------------------------------------------------------------ #
    def estimate_oneway(self, origin: str, destination: str) -> float | None:
        """Schaetzung aus route_hints.yaml, notfalls ueber ein Gateway kombiniert."""
        key = (origin, destination)
        if key in self._estimate_cache:
            return self._estimate_cache[key]

        direct = self._hint_longhaul(origin, destination) or self._hint_intra(origin, destination)
        best = direct

        gateways = {e["to"] for e in self.hints.get("longhaul", [])}
        gateways |= {e["from"] for e in self.hints.get("intra_asia", [])}
        gateways |= {e["to"] for e in self.hints.get("intra_asia", [])}
        for gate in gateways:
            if gate in (origin, destination):
                continue
            first = self._hint_longhaul(origin, gate) or self._hint_intra(origin, gate)
            second = self._hint_intra(gate, destination) or self._hint_longhaul(gate, destination)
            if first is None or second is None:
                continue
            total = first + second + SELF_CONNECT_PENALTY_EUR
            if best is None or total < best:
                best = total

        self._estimate_cache[key] = best
        return best

    def _hint_longhaul(self, origin: str, destination: str) -> float | None:
        for entry in self.hints.get("longhaul", []):
            if entry["to"] == destination and origin in entry["from"]:
                return float(entry["oneway_eur"])
            # Rueckrichtung Asien -> Europa: gleiche Hausnummer annehmen.
            if entry["to"] == origin and destination in entry["from"]:
                return float(entry["oneway_eur"])
        return None

    def _hint_intra(self, origin: str, destination: str) -> float | None:
        best = None
        for entry in self.hints.get("intra_asia", []):
            if (entry["from"], entry["to"]) == (origin, destination) or (
                entry["from"],
                entry["to"],
            ) == (destination, origin):
                price = float(entry["oneway_eur"])
                best = price if best is None else min(best, price)
        return best

    def estimate_multiplier(self, origin: str, destination: str, day: dt.date) -> tuple[float, str]:
        """Saisonaler Aufschlag auf einen Schaetzpreis (1.0 = keiner).

        Mehrere zutreffende Regeln werden NICHT multipliziert, sondern es gilt die
        hoechste - sonst zaehlt derselbe Feiertag (z.B. 1. Mai, der beide Enden
        einer Strecke betrifft) doppelt.
        """
        factor, reasons = 1.0, []
        for rule in self.hints.get("estimate_multipliers", []):
            start = dt.date.fromisoformat(str(rule["start"]))
            end = dt.date.fromisoformat(str(rule["end"]))
            if not (start <= day <= end):
                continue
            scope = rule["applies_to"]
            if scope == "eu_departure":
                hit = origin in EU_HUBS
            elif scope == "eu_return":
                hit = destination in EU_HUBS
            else:
                hit = origin in scope or destination in scope
            if hit:
                factor = max(factor, float(rule["factor"]))
                reasons.append(str(rule.get("reason", "")).split(" - ")[0])
        return factor, "; ".join(reasons)

    # ------------------------------------------------------------------ #
    def boardbag_eur(self) -> float:
        return float(self.hints.get("baggage", {}).get("boardbag_eur", 0))

    def visa_eur(self, country: str) -> float:
        return float(self.hints.get("visa_eur", {}).get(country, 0))
