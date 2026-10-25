"""Routen-Optimierer.

Sucht Kombinationen aus 2-3 Zielen, Start-/Enddatum, Blocklaengen, Abflughafen
und Ticketstrategie, die Gesamtkosten gegen Erlebniswert optimal abwaegen.

Verfahren: fuer jede geordnete Zielsequenz, jedes Startdatum, jeden Hub und
jede Ticketstrategie laeuft ein Dynamic-Programming ueber die Tage
(Zustand = "Ziele seq[0..i-1] fertig, Tage [0,t) gefuellt"). Das ist innerhalb
des Tagesrasters exakt: es gibt keine Aufteilung der Blocklaengen, die die
Suche verpassen koennte.

Zielfunktion (kleiner = besser), standardmaessig laengenneutral pro Reisetag:

    objective_per_day = (Gesamtkosten - wert_pro_punkt * Score * Reisende) / Reisetage

Warum pro Tag: eine 42-Tage-Route sammelt zwangslaeufig mehr Erlebnispunkte als
eine 28-Tage-Route. Ohne Normierung gewinnt immer die laengste Reise, was keine
Information ist - die Reiselaenge ist eine Vorgabe, keine Optimierungsgroesse.
"""

from __future__ import annotations

import datetime as dt
import itertools
from dataclasses import dataclass, field

from .data import load_calendar, load_destinations, load_origins, load_route_hints
from .models import Block, Destination, Itinerary, Leg
from .prices import PriceBook
from .seasonality import Weights, daily_score, interpolated_scores, is_available

NEG = float("-inf")
GOOD_SURF = 6.0


@dataclass
class TripConfig:
    earliest_start: dt.date = dt.date(2027, 3, 12)
    latest_end: dt.date = dt.date(2027, 5, 10)
    min_days: int = 28
    max_days: int = 42
    travellers: int = 2
    min_destinations: int = 2
    max_destinations: int = 3
    min_block_days: int = 9
    max_block_days: int = 22
    allowed_origins: tuple[str, ...] = ("MAD", "BCN")
    ticket_strategies: tuple[str, ...] = ("self_transfer", "through_ticket")
    eligible_tiers: tuple[str, ...] = ("A", "B")
    include_destinations: tuple[str, ...] = ()  # erzwingt diese Ziele in der Route
    exclude_destinations: tuple[str, ...] = ()
    weights: Weights = field(default_factory=Weights.balanced)

    # "per_day" = laengenneutral (Default), "total" = Gesamtsumme
    objective_mode: str = "per_day"
    # Monetarisierung: wie viel ist ein Score-Punkt pro Person pro Tag wert?
    value_per_score_point_eur: float = 22.0
    # Ein Umzugstag ist kein voller Urlaubstag.
    travel_day_score_factor: float = 0.35
    # Self-Transfer: Pufferuebernachtung am Hub + Risikoaufschlag (pro Richtung, total).
    self_transfer_buffer_eur: float = 120.0
    self_transfer_risk_eur: float = 50.0
    # Open-Jaw/Multi-City-Rabatt gegenueber zwei Einzeltickets (Schaetzung).
    openjaw_discount: float = 0.12
    # Boardbags auf Langstrecke (0 = vor Ort mieten, s. data/route_hints.yaml).
    board_bags: int = 0

    require_tropical: bool = True
    min_good_surf_days: int = 0
    budget_eur: float | None = None  # harte Obergrenze fuer Gesamtkosten
    start_date_step: int = 2

    def date_grid(self) -> list[dt.date]:
        span = (self.latest_end - self.earliest_start).days - self.min_days + 1
        return [
            self.earliest_start + dt.timedelta(days=i)
            for i in range(0, max(1, span + 1), self.start_date_step)
        ]


@dataclass
class _Profile:
    """Vorberechnete Tagesprofile eines Ziels ab einem Startdatum."""

    score: list[float]
    avail: list[bool]
    surf: list[bool]
    pref: list[float]
    blocked: list[int]


class Optimizer:
    def __init__(self, config: TripConfig | None = None, pricebook: PriceBook | None = None):
        self.cfg = config or TripConfig()
        self.dests, self.meta = load_destinations()
        self.origins, self.origin_meta = load_origins()
        self.hints = load_route_hints()
        self.pb = pricebook or PriceBook()
        self._profiles: dict[tuple[str, dt.date, int], _Profile] = {}
        self._prices: dict[tuple[str, str, dt.date], tuple[float, str]] = {}

    # ------------------------------------------------------------------ #
    # Caches
    # ------------------------------------------------------------------ #
    def _profile(self, dest: Destination, start: dt.date, length: int) -> _Profile:
        key = (dest.id, start, length)
        cached = self._profiles.get(key)
        if cached is not None:
            return cached
        score: list[float] = []
        avail: list[bool] = []
        surf: list[bool] = []
        for t in range(length):
            day = start + dt.timedelta(days=t)
            ok, _ = is_available(dest, day)
            avail.append(ok)
            if ok:
                score.append(daily_score(dest, day, self.cfg.weights))
                surf.append(interpolated_scores(dest, day)[1] >= GOOD_SURF)
            else:
                score.append(0.0)
                surf.append(False)
        pref = [0.0] * (length + 1)
        blocked = [0] * (length + 1)
        for t in range(length):
            pref[t + 1] = pref[t] + score[t]
            blocked[t + 1] = blocked[t] + (0 if avail[t] else 1)
        prof = _Profile(score=score, avail=avail, surf=surf, pref=pref, blocked=blocked)
        self._profiles[key] = prof
        return prof

    def _leg_price(self, origin: str, destination: str, day: dt.date) -> tuple[float, str]:
        key = (origin, destination, day)
        cached = self._prices.get(key)
        if cached is None:
            cached = self.pb.oneway(origin, destination, day)
            self._prices[key] = cached
        return cached

    def _origin_leg_price(
        self, hub: str, dest_airport: str, day: dt.date, strategy: str
    ) -> tuple[float, str, float]:
        """(Preis pro Person, Quelle, Fixkosten total) fuer die Anreise ab Teneriffa."""
        o = self.origins[hub]
        longhaul, src = self._leg_price(hub, dest_airport, day)
        if longhaul == float("inf"):
            return float("inf"), "unknown", 0.0
        if strategy == "self_transfer":
            fixed = self.cfg.self_transfer_buffer_eur + self.cfg.self_transfer_risk_eur
            return longhaul + o.self_transfer_price_eur, f"{src}+feeder", fixed
        return longhaul + o.through_ticket_feeder_eur, f"{src}+through", 0.0

    # ------------------------------------------------------------------ #
    # Kandidatenauswahl
    # ------------------------------------------------------------------ #
    def eligible_destinations(self) -> list[Destination]:
        out = []
        for d in self.dests.values():
            if d.id in self.cfg.exclude_destinations:
                continue
            if d.id in self.cfg.include_destinations:
                out.append(d)
                continue
            if d.tier not in self.cfg.eligible_tiers:
                continue
            out.append(d)
        return out

    def sequences(self) -> list[tuple[Destination, ...]]:
        pool = self.eligible_destinations()
        required = set(self.cfg.include_destinations)
        seqs: list[tuple[Destination, ...]] = []
        for n in range(self.cfg.min_destinations, self.cfg.max_destinations + 1):
            for combo in itertools.permutations(pool, n):
                countries = [d.country for d in combo]
                # Zwei gleiche Laender direkt hintereinander waeren ein
                # Inlandsumzug, kein eigener Routenbaustein.
                if any(countries[i] == countries[i + 1] for i in range(len(countries) - 1)):
                    continue
                if self.cfg.require_tropical and not any(d.tropical for d in combo):
                    continue
                if required and not required.issubset({d.id for d in combo}):
                    continue
                seqs.append(combo)
        return seqs

    # ------------------------------------------------------------------ #
    # Kern-DP
    # ------------------------------------------------------------------ #
    def _solve(
        self, seq: tuple[Destination, ...], start: dt.date, hub: str, strategy: str
    ) -> Itinerary | None:
        cfg = self.cfg
        k = len(seq)
        max_len = min(cfg.max_days, (cfg.latest_end - start).days + 1)
        if max_len < cfg.min_days or k * cfg.min_block_days > max_len:
            return None

        vpp = cfg.value_per_score_point_eur * cfg.travellers
        profiles = [self._profile(d, start, max_len) for d in seq]

        # g[i][t] = bester Nettowert, nachdem seq[0..i-1] die Tage [0,t) fuellen.
        g = [[NEG] * (max_len + 1) for _ in range(k + 1)]
        back: dict[tuple[int, int], tuple[int, int, float, str]] = {}
        g[0][0] = 0.0

        for i in range(k):
            dest = seq[i]
            prof = profiles[i]
            row_in, row_out = g[i], g[i + 1]
            for t in range(max_len):
                if row_in[t] == NEG:
                    continue
                arrive_day = start + dt.timedelta(days=t)
                if i == 0:
                    ppp, src, fixed = self._origin_leg_price(
                        hub, dest.primary_airport, arrive_day, strategy
                    )
                else:
                    ppp, src = self._leg_price(
                        seq[i - 1].primary_airport, dest.primary_airport, arrive_day
                    )
                    fixed = 0.0
                if ppp == float("inf"):
                    continue
                arrival_cost = ppp * cfg.travellers + fixed
                if cfg.board_bags:
                    arrival_cost += self.pb.boardbag_eur() * cfg.board_bags

                travel_day_loss = prof.score[t] * (1 - cfg.travel_day_score_factor)
                hi = min(cfg.max_block_days, max_len - t)
                for length in range(cfg.min_block_days, hi + 1):
                    end = t + length
                    if prof.blocked[end] - prof.blocked[t] > 0:
                        continue
                    if (k - i - 1) * cfg.min_block_days > max_len - end:
                        continue
                    value = (prof.pref[end] - prof.pref[t] - travel_day_loss) * vpp
                    ground = dest.cost_per_day_eur_pp * length * cfg.travellers
                    net = row_in[t] + value - arrival_cost - ground
                    if net > row_out[end]:
                        row_out[end] = net
                        back[(i + 1, end)] = (i, t, ppp, src)

        # Rueckflug anhaengen, beste Gesamtlaenge nach Zielfunktion waehlen.
        best: tuple[float, float, int, float, str] | None = None
        last = seq[-1]
        for total in range(cfg.min_days, max_len + 1):
            if g[k][total] == NEG:
                continue
            back_day = start + dt.timedelta(days=total - 1)
            ppp, src = self._leg_price(last.primary_airport, hub, back_day)
            if ppp == float("inf"):
                continue
            o = self.origins[hub]
            if strategy == "self_transfer":
                ppp += o.self_transfer_price_eur
                fixed = cfg.self_transfer_buffer_eur + cfg.self_transfer_risk_eur
                src = f"{src}+feeder"
            else:
                ppp += o.through_ticket_feeder_eur
                fixed = 0.0
                src = f"{src}+through"
            # Open-Jaw: Hin und Rueck auf einem Ticket ist guenstiger als zwei Einzelstrecken.
            ppp *= 1 - cfg.openjaw_discount
            cost = ppp * cfg.travellers + fixed
            if cfg.board_bags:
                cost += self.pb.boardbag_eur() * cfg.board_bags
            net = g[k][total] - cost
            rank = -net / total if cfg.objective_mode == "per_day" else -net
            if best is None or rank < best[0]:
                best = (rank, net, total, ppp, src)

        if best is None:
            return None
        _, net, total, return_ppp, return_src = best
        itin = self._reconstruct(seq, start, total, hub, strategy, back, net, return_ppp, return_src)
        if cfg.budget_eur is not None and itin.total_cost_eur > cfg.budget_eur:
            return None
        if itin.good_surf_days < cfg.min_good_surf_days:
            return None
        return itin

    # ------------------------------------------------------------------ #
    def _reconstruct(
        self,
        seq: tuple[Destination, ...],
        start: dt.date,
        total: int,
        hub: str,
        strategy: str,
        back: dict,
        net: float,
        return_ppp: float,
        return_src: str,
    ) -> Itinerary:
        cfg = self.cfg
        bounds: list[tuple[int, int, float, str]] = []
        i, t = len(seq), total
        while i > 0:
            pi, pt, ppp, src = back[(i, t)]
            bounds.append((pt, t, ppp, src))
            i, t = pi, pt
        bounds.reverse()

        blocks: list[Block] = []
        legs: list[Leg] = []
        flight_cost = 0.0
        estimated = 0.0
        for idx, (bt, bend, ppp, src) in enumerate(bounds):
            dest = seq[idx]
            blocks.append(
                Block(
                    destination=dest,
                    start=start + dt.timedelta(days=bt),
                    end=start + dt.timedelta(days=bend - 1),
                )
            )
            cost = ppp * cfg.travellers
            flight_cost += cost
            if "estimate" in src or "unknown" in src:
                estimated += cost
            legs.append(
                Leg(
                    origin=hub if idx == 0 else seq[idx - 1].primary_airport,
                    destination=dest.primary_airport,
                    date=start + dt.timedelta(days=bt),
                    price_eur=cost,
                    kind="outbound" if idx == 0 else "inter",
                    source=src,
                )
            )

        return_cost = return_ppp * cfg.travellers
        flight_cost += return_cost
        if "estimate" in return_src or "unknown" in return_src:
            estimated += return_cost
        legs.append(
            Leg(
                origin=seq[-1].primary_airport,
                destination=hub,
                date=start + dt.timedelta(days=total - 1),
                price_eur=return_cost,
                kind="return",
                source=return_src,
            )
        )

        fixed = 0.0
        if strategy == "self_transfer":
            fixed = 2 * (cfg.self_transfer_buffer_eur + cfg.self_transfer_risk_eur)
        baggage = self.pb.boardbag_eur() * cfg.board_bags * len(legs)
        ground = sum(b.destination.cost_per_day_eur_pp * b.days * cfg.travellers for b in blocks)
        visas = sum(self.pb.visa_eur(c) for c in {b.destination.country for b in blocks}) * cfg.travellers

        raw_score = 0.0
        good_surf = 0
        for b in blocks:
            for n in range(b.days):
                day = b.start + dt.timedelta(days=n)
                s = daily_score(b.destination, day, cfg.weights)
                raw_score += s * (cfg.travel_day_score_factor if n == 0 else 1.0)
                if interpolated_scores(b.destination, day)[1] >= GOOD_SURF:
                    good_surf += 1

        return Itinerary(
            blocks=blocks,
            legs=legs,
            origin_hub=hub,
            ticket_strategy=strategy,
            travellers=cfg.travellers,
            flight_cost_eur=round(flight_cost + fixed, 2),
            ground_cost_eur=round(ground, 2),
            visa_cost_eur=round(visas, 2),
            baggage_cost_eur=round(baggage, 2),
            experience_score=round(raw_score, 2),
            objective_eur=round(-net, 2),
            objective_per_day_eur=round(-net / total, 2),
            good_surf_days=good_surf,
            estimated_share=round(estimated / flight_cost, 3) if flight_cost else 1.0,
        )

    # ------------------------------------------------------------------ #
    def annotate(self, itin: Itinerary) -> Itinerary:
        """Haengt Warnungen an - erst fuer die Finalisten, nicht fuer alle Varianten."""
        out: list[str] = []
        for event in load_calendar():
            for b in itin.blocks:
                if event.overlaps(b.start, b.end) and b.destination.country in event.affects:
                    out.append(
                        f"{event.name} ({event.start:%d.%m.}-{event.end:%d.%m.}) faellt in "
                        f"{b.destination.region_short} [Impact: {event.impact}]"
                    )
            if "EU-Abfluege" in event.affects and event.overlaps(
                itin.start - dt.timedelta(days=1), itin.start + dt.timedelta(days=1)
            ):
                out.append(f"Abflugtag liegt in {event.name} - teuerste Woche ab MAD/BCN")
            if "EU-Abfluege" in event.affects and event.overlaps(
                itin.end - dt.timedelta(days=1), itin.end + dt.timedelta(days=1)
            ):
                out.append(f"Rueckflugtag liegt in {event.name} - Preisspitze")
        if itin.ticket_strategy == "self_transfer":
            hub = self.origins[itin.origin_hub]
            out.append(
                f"Self-Transfer ab {hub.id}: Residentenrabatt nutzbar, aber kein "
                f"Umsteigeschutz ({hub.min_connect_self_h:.0f} h Puffer + 1 Hotelnacht eingerechnet)"
            )
        if itin.good_surf_days:
            out.append(f"{itin.good_surf_days} Tage mit Surf-Score >= 6 (longboardtauglich)")
        else:
            out.append("Keine Tage mit gutem Longboard-Surf in dieser Route")
        weak = [b.destination.region_short for b in itin.blocks if b.destination.work <= 4]
        if weak:
            out.append(f"Schwache Arbeitsinfrastruktur: {', '.join(weak)}")
        if itin.estimated_share > 0.5:
            out.append(
                f"{itin.estimated_share:.0%} der Flugkosten sind Schaetzwerte - "
                f"mit echten Scrapes neu rechnen"
            )
        itin.warnings = sorted(set(out))
        return itin

    # ------------------------------------------------------------------ #
    def run_all(self) -> list[Itinerary]:
        out: list[Itinerary] = []
        for seq in self.sequences():
            for start in self.cfg.date_grid():
                for hub in self.cfg.allowed_origins:
                    for strategy in self.cfg.ticket_strategies:
                        itin = self._solve(seq, start, hub, strategy)
                        if itin:
                            out.append(itin)
        key = (
            (lambda i: i.objective_per_day_eur)
            if self.cfg.objective_mode == "per_day"
            else (lambda i: i.objective_eur)
        )
        out.sort(key=key)
        return out

    def run(self, top_n: int = 15) -> list[Itinerary]:
        """Beste Variante je Zielkombination, aufsteigend nach Zielfunktion."""
        seen: set[frozenset[str]] = set()
        unique: list[Itinerary] = []
        for itin in self.run_all():
            key = frozenset(b.destination.id for b in itin.blocks)
            if key in seen:
                continue
            seen.add(key)
            unique.append(self.annotate(itin))
            if len(unique) >= top_n:
                break
        return unique
