"""Query-Matrix: welche Google-Flights-Suchen genau gescrapet werden muessen.

Zwei Phasen:

  Phase 1 "grid"      - Preisentdeckung. Alle plausiblen Langstrecken-Gateways
                        x Abflugdaten, dazu die Intra-Asien-Verbindungen.
                        Ergebnis: wo sind Ein- und Ausstieg guenstig?
  Phase 2 "candidates"- Multi-City-Tickets fuer die konkreten Routen, die der
                        Optimierer aus Phase 1 als Favoriten ausspuckt.
                        Open-Jaw/Multi-City ist oft 10-20% guenstiger als zwei
                        Einzeltickets - das laesst sich nur direkt messen.
"""

from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass, field
from pathlib import Path

from ..models import Itinerary
from .urls import TRIP_MULTICITY, TRIP_ONEWAY, TRIP_ROUND, fallback_query_url, google_flights_url

# Langstrecken-Gateways, die als Ein-/Ausstieg in Frage kommen.
GATEWAYS = ["CMB", "KUL", "LOP", "HAN", "TPE", "KTM", "MCT", "TRV"]

# Verbindungen zwischen den Zielen, die der Optimierer braucht.
INTRA_ROUTES = [
    ("CMB", "KUL"), ("CMB", "LOP"), ("KUL", "LOP"), ("CMB", "HAN"),
    ("LOP", "HAN"), ("CMB", "KTM"), ("KUL", "HAN"), ("HAN", "TPE"),
    ("CMB", "TRV"), ("MCT", "CMB"), ("KUL", "TPE"), ("LOP", "KUL"),
]

LEVELS = {
    "quick":    {"out_step": 5, "ret_step": 6, "mid_step": 7, "gateways": ["CMB", "KUL", "LOP", "MCT"], "hubs": ["MAD"]},
    "standard": {"out_step": 4, "ret_step": 5, "mid_step": 5, "gateways": GATEWAYS, "hubs": ["MAD", "BCN"]},
    "full":     {"out_step": 2, "ret_step": 3, "mid_step": 3, "gateways": GATEWAYS, "hubs": ["MAD", "BCN", "BER", "HAM", "TFS"]},
}


@dataclass
class Query:
    id: str
    phase: str
    trip_type: str  # oneway | return | multicity
    legs: list[tuple[str, str, str]]  # (origin, dest, ISO-Datum)
    adults: int = 2
    purpose: str = ""
    url: str = field(default="")
    fallback_url: str = field(default="")

    def build_urls(self) -> "Query":
        parsed = [(o, d, dt.date.fromisoformat(day)) for o, d, day in self.legs]
        trip = {"oneway": TRIP_ONEWAY, "return": TRIP_ROUND, "multicity": TRIP_MULTICITY}[
            self.trip_type
        ]
        self.url = google_flights_url(parsed, trip, adults=self.adults)
        o, d, day = parsed[0]
        back = parsed[-1][2] if self.trip_type == "return" else None
        self.fallback_url = fallback_query_url(o, d, day, back)
        return self

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "phase": self.phase,
            "trip_type": self.trip_type,
            "legs": [list(leg) for leg in self.legs],
            "adults": self.adults,
            "purpose": self.purpose,
            "url": self.url,
            "fallback_url": self.fallback_url,
        }


def _dates(start: dt.date, end: dt.date, step: int) -> list[dt.date]:
    out, day = [], start
    while day <= end:
        out.append(day)
        day += dt.timedelta(days=step)
    return out


def grid_queries(
    earliest_start: dt.date = dt.date(2027, 3, 13),
    latest_start: dt.date = dt.date(2027, 4, 3),
    earliest_return: dt.date = dt.date(2027, 4, 18),
    latest_return: dt.date = dt.date(2027, 5, 10),
    level: str = "standard",
    adults: int = 2,
) -> list[Query]:
    cfg = LEVELS[level]
    out_dates = _dates(earliest_start, latest_start, cfg["out_step"])
    ret_dates = _dates(earliest_return, latest_return, cfg["ret_step"])
    mid_dates = _dates(
        earliest_start + dt.timedelta(days=12), latest_return - dt.timedelta(days=10), cfg["mid_step"]
    )

    queries: list[Query] = []
    n = 0
    for hub in cfg["hubs"]:
        for gate in cfg["gateways"]:
            for day in out_dates:
                n += 1
                queries.append(
                    Query(
                        id=f"g{n:04d}",
                        phase="grid",
                        trip_type="oneway",
                        legs=[(hub, gate, day.isoformat())],
                        adults=adults,
                        purpose=f"Hinflug {hub}->{gate}",
                    ).build_urls()
                )
            for day in ret_dates:
                n += 1
                queries.append(
                    Query(
                        id=f"g{n:04d}",
                        phase="grid",
                        trip_type="oneway",
                        legs=[(gate, hub, day.isoformat())],
                        adults=adults,
                        purpose=f"Rueckflug {gate}->{hub}",
                    ).build_urls()
                )
    for a, b in INTRA_ROUTES:
        if a not in cfg["gateways"] or b not in cfg["gateways"]:
            continue
        for day in mid_dates:
            n += 1
            queries.append(
                Query(
                    id=f"g{n:04d}",
                    phase="grid",
                    trip_type="oneway",
                    legs=[(a, b, day.isoformat())],
                    adults=adults,
                    purpose=f"Zwischenflug {a}->{b}",
                ).build_urls()
            )
    return queries


def scenario_queries(
    scenarios: list,
    gateways: list[str] | None = None,
    return_hubs: tuple[str, ...] = ("MAD", "BCN"),
    return_window: tuple[dt.date, dt.date] = (dt.date(2027, 4, 15), dt.date(2027, 5, 12)),
    return_step: int = 3,
    adults: int = 2,
) -> list[Query]:
    """Genau die Suchen, die die Startszenarien brauchen.

    Weil die Abflugfenster der Szenarien klein sind (3-8 Tage), wird dort jeder
    Tag abgefragt - gerade bei Flugpreisen entscheidet oft ein einzelner Tag.
    """
    gateways = gateways or ["CMB", "KUL", "LOP", "HAN", "MCT", "TPE", "KTM"]
    queries: list[Query] = []
    n = 0
    seen: set[tuple] = set()
    for scenario in scenarios:
        days = _dates(scenario.earliest_start, scenario.latest_start, 1)
        for hub in scenario.allowed_origins:
            for gate in gateways:
                for day in days:
                    key = (hub, gate, day.isoformat(), "oneway")
                    if key in seen:
                        continue
                    seen.add(key)
                    n += 1
                    queries.append(
                        Query(
                            id=f"s{n:04d}",
                            phase="scenario",
                            trip_type="oneway",
                            legs=[(hub, gate, day.isoformat())],
                            adults=adults,
                            purpose=f"Hinflug {scenario.key}: {hub}->{gate}",
                        ).build_urls()
                    )
    for hub in return_hubs:
        for gate in gateways:
            for day in _dates(return_window[0], return_window[1], return_step):
                key = (gate, hub, day.isoformat(), "oneway")
                if key in seen:
                    continue
                seen.add(key)
                n += 1
                queries.append(
                    Query(
                        id=f"s{n:04d}",
                        phase="scenario",
                        trip_type="oneway",
                        legs=[(gate, hub, day.isoformat())],
                        adults=adults,
                        purpose=f"Rueckflug {gate}->{hub}",
                    ).build_urls()
                )
    mid = _dates(dt.date(2027, 3, 25), dt.date(2027, 4, 28), 4)
    for a, b in INTRA_ROUTES:
        if a not in gateways or b not in gateways:
            continue
        for day in mid:
            key = (a, b, day.isoformat(), "oneway")
            if key in seen:
                continue
            seen.add(key)
            n += 1
            queries.append(
                Query(
                    id=f"s{n:04d}",
                    phase="scenario",
                    trip_type="oneway",
                    legs=[(a, b, day.isoformat())],
                    adults=adults,
                    purpose=f"Zwischenflug {a}->{b}",
                ).build_urls()
            )
    return queries


def candidate_queries(itineraries: list[Itinerary], adults: int = 2) -> list[Query]:
    """Multi-City-Suchen fuer konkrete Routenvorschlaege, plus Vergleichs-Einzeltickets."""
    queries: list[Query] = []
    seen: set[tuple] = set()
    for idx, itin in enumerate(itineraries, 1):
        legs = [(leg.origin, leg.destination, leg.date.isoformat()) for leg in itin.legs]
        key = tuple(legs)
        if key in seen:
            continue
        seen.add(key)
        label = itin.label
        queries.append(
            Query(
                id=f"c{idx:03d}-mc",
                phase="candidates",
                trip_type="multicity",
                legs=legs,
                adults=adults,
                purpose=f"Multi-City Gesamtticket: {label}",
            ).build_urls()
        )
        # Vergleich: dieselbe Route als Einzeltickets.
        for j, leg in enumerate(legs):
            queries.append(
                Query(
                    id=f"c{idx:03d}-s{j}",
                    phase="candidates",
                    trip_type="oneway",
                    legs=[leg],
                    adults=adults,
                    purpose=f"Einzelticket-Vergleich Leg {j + 1}: {label}",
                ).build_urls()
            )
        # Und als klassischer Return auf der Langstrecke (falls Start=Ende-Hub).
        if legs[0][0] == legs[-1][1]:
            queries.append(
                Query(
                    id=f"c{idx:03d}-rt",
                    phase="candidates",
                    trip_type="return",
                    legs=[
                        (legs[0][0], legs[0][1], legs[0][2]),
                        (legs[0][1], legs[0][0], legs[-1][2]),
                    ],
                    adults=adults,
                    purpose=f"Return-Vergleich Langstrecke: {label}",
                ).build_urls()
            )
    return queries


def write_matrix(queries: list[Query], json_path: Path, markdown_path: Path | None = None) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps([q.to_dict() for q in queries], indent=2, ensure_ascii=False), encoding="utf-8"
    )
    if markdown_path is None:
        return

    by_purpose: dict[str, list[Query]] = {}
    for q in queries:
        by_purpose.setdefault(q.purpose.split(":")[0], []).append(q)

    lines = [
        "# Scrape-Checkliste Google Flights",
        "",
        f"{len(queries)} Suchen. Bei ~6 s Pause pro Abfrage: ca. "
        f"{len(queries) * 6 / 60:.0f} Minuten automatisiert.",
        "",
        "Automatisiert: `node scripts/scrape_google_flights.cjs data/prices/_queries.json "
        "data/prices/scraped.csv`",
        "",
        "Manuell: Link anklicken, guenstigsten Preis ablesen, Zeile in "
        "`data/prices/manual.csv` eintragen (Schema: `data/prices/_SCHEMA.csv`).",
        "",
        "Die `tfs`-Links kodieren die Suche direkt. Falls Google das Format aendert,",
        "nutze die Fallback-Links (einfache Textsuche, kein Multi-City).",
        "",
    ]
    for purpose, group in sorted(by_purpose.items()):
        lines.append(f"## {purpose} ({len(group)})")
        lines.append("")
        lines.append("| ID | Strecke | Datum | Typ | Link | Fallback |")
        lines.append("|---|---|---|---|---|---|")
        for q in group:
            route = " / ".join(f"{o}->{d}" for o, d, _ in q.legs)
            dates = " / ".join(day for _, _, day in q.legs)
            lines.append(
                f"| `{q.id}` | {route} | {dates} | {q.trip_type} | "
                f"[Google Flights]({q.url}) | [q=]({q.fallback_url}) |"
            )
        lines.append("")
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text("\n".join(lines), encoding="utf-8")
