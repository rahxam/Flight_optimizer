"""Routen-Optimierer.

Sucht Kombinationen aus 2-3 Zielen, Start-/Enddatum, Blocklaengen, Abflughafen und
Ticketstrategie, die Gesamtkosten gegen Erlebniswert optimal abwaegen.

Verfahren: fuer jede geordnete Zielsequenz, jedes Startdatum, jeden Abflughafen und
jede Ticketstrategie laeuft ein Dynamic-Programming ueber die Tage (Zustand =
"Ziele seq[0..i-1] fertig, Tage [0,t) gefuellt"). Das ist innerhalb des Tagesrasters
exakt: es gibt keine Aufteilung der Blocklaengen, die die Suche verpassen koennte.

Drei Zielfunktionen, ueber `objective_mode` waehlbar:

  "cheapest" (Default) - die GUENSTIGSTE Route, die noch sinnvoll ist.
      Sortiert nach Gesamtkosten pro Person; `min_score_per_day` ist die
      Sinnhaftigkeitsschwelle, unter der eine Route verworfen wird. Das
      entspricht der tatsaechlichen Entscheidungsregel: Ziele nach guenstigen
      Fluegen auswaehlen, nicht die Route vorher festlegen.
  "per_day"  - bester Kompromiss aus Kosten und Erlebniswert, laengenneutral:
      objective_per_day = (Kosten - wert_pro_punkt * Score * Reisende) / Reisetage
      Die Normierung ist notwendig, weil eine 42-Tage-Route sonst allein durch
      ihre Laenge gewinnt.
  "total"    - dasselbe als Gesamtsumme.

Anreise: der Abflughafen wird aus einem Startkontext erreicht (montafon, cottbus,
hamburg, tenerife - s. data/origins.yaml). Der Rueckweg endet immer auf Teneriffa,
ueber einen der `allowed_return_hubs`.

Urlaubstage: werden NACH dem DP verteilt, und zwar greedy nach dem Zugewinn pro
Ziel (`seasonality.vacation_gain`). Das ist bei gegebenen Blocklaengen exakt
optimal, weil der Zugewinn pro Tag konstant und das Budget global ist - aber es
ist eine Heuristik gegenueber einer gemeinsamen Optimierung von Laengen UND
Urlaubsverteilung. Der Effekt auf die Laengenwahl ist zweiter Ordnung.
"""

from __future__ import annotations

import datetime as dt
import itertools
from dataclasses import dataclass, field

from .data import load_calendar, load_destinations, load_origins, load_route_hints
from .models import Access, Block, Destination, Itinerary, Leg
from .prices import PriceBook
from .seasonality import (
    Weights,
    daily_score,
    interpolated_scores,
    is_available,
    vacation_gain,
)
from .workwindow import WorkWindow

NEG = float("-inf")
GOOD_SURF = 6.0


@dataclass
class TripConfig:
    earliest_start: dt.date = dt.date(2027, 3, 12)
    # Spaetester Abflugtag. None = nur durch latest_end und min_days begrenzt.
    # Szenarien setzen das, weil ihr Abflugfenster oft schmaler ist als das, was
    # sich aus latest_end rechnerisch ergibt.
    latest_start: dt.date | None = None
    latest_end: dt.date = dt.date(2027, 5, 10)
    min_days: int = 28
    max_days: int = 42
    travellers: int = 2
    min_destinations: int = 2
    max_destinations: int = 3
    min_block_days: int = 9
    # Muss mindestens so gross sein wie min_days, damit auch EIN Ziel fuer die
    # ganze Reise moeglich ist - das ist die guenstigste und entspannteste
    # Variante (nur ein Flugpaar, keine Umzuege) und gehoert auf den Tisch.
    max_block_days: int = 45

    # Anreise und Rueckweg
    outbound_context: str = "tenerife"
    allowed_origins: tuple[str, ...] = ()  # leer = alle aus dem Kontext erreichbaren
    allowed_return_hubs: tuple[str, ...] = ("MAD", "BCN")
    home_airport: str = "TFS"
    # "home"  = Zubringer zum Heimatflughafen direkt im Anschluss an die Langstrecke
    # "later" = die Reise endet in Europa (z.B. Familienfeier), der Heimflug kommt
    #           spaeter und steckt in post_trip_cost_eur
    return_feeder_mode: str = "home"
    ticket_strategies: tuple[str, ...] = ("separate_tickets",)

    eligible_tiers: tuple[str, ...] = ("A", "B")
    # Ziele unter dieser Arbeitsinfrastruktur taugen nicht als Standort fuer mehrere
    # Wochen - unabhaengig davon, wie viel Urlaub dort liegt. Stromausfaelle und
    # fehlendes Internet machen Arbeit nicht nur unangenehm, sondern unzuverlaessig.
    # Solche Orte gehoeren als Ausflug in einen Block (Sumbawa per Faehre von
    # Lombok), nicht als eigener Routenbaustein.
    min_work_score: float = 5.0
    include_destinations: tuple[str, ...] = ()
    exclude_destinations: tuple[str, ...] = ()
    weights: Weights = field(default_factory=Weights.balanced)
    work_window: WorkWindow = field(default_factory=WorkWindow)
    vacation_days: int = 14
    # Obergrenze je Block: Urlaub soll sich ueber die Reise VERTEILEN, nicht in
    # einem Block klumpen. Ohne diese Grenze wuerde die greedy Zuteilung den
    # ersten Block bis zum Anschlag fuellen.
    max_vacation_share_per_block: float = 0.5
    # Ziele, die Urlaubstage ZUERST bekommen, und zwar ohne die Share-Grenze.
    # Fuer Vorhaben, die nur als Urlaub funktionieren - ein 7-Tage-Trek in Nepal
    # laesst sich nicht mit drei Arbeitstagen dazwischen machen.
    vacation_priority: tuple[str, ...] = ()

    objective_mode: str = "cheapest"  # cheapest | per_day | total
    value_per_score_point_eur: float = 22.0
    # Sinnhaftigkeitsschwelle fuer "cheapest": Routen unter diesem Tagesscore
    # werden verworfen, egal wie billig sie sind.
    min_score_per_day: float = 0.0
    budget_per_person_eur: float | None = None
    travel_day_score_factor: float = 0.35
    # 3 h Eigenumstieg ohne Puffernacht: nur Umbuchungsrisiko, kein Hotel.
    self_connect_risk_eur: float = 50.0
    # Kosten, um ueberhaupt in den Startkontext zu kommen (z.B. Montafon -> Cottbus).
    # Gesamtbetrag fuer alle Reisenden, wird den Flugkosten zugeschlagen.
    pre_trip_cost_eur: float = 0.0
    # Kosten NACH der Reise (z.B. Heimflug Deutschland -> Teneriffa nach einer
    # Familienfeier). Gesamtbetrag fuer alle Reisenden.
    post_trip_cost_eur: float = 0.0
    scenario_label: str = ""
    openjaw_discount: float = 0.12
    board_bags: int = 0

    require_tropical: bool = True
    min_good_surf_days: int = 0
    budget_eur: float | None = None
    start_date_step: int = 2

    def date_grid(self) -> list[dt.date]:
        last = self.latest_end - dt.timedelta(days=self.min_days - 1)
        if self.latest_start is not None:
            last = min(last, self.latest_start)
        span = (last - self.earliest_start).days
        return [
            self.earliest_start + dt.timedelta(days=i)
            for i in range(0, max(1, span + 1), self.start_date_step)
        ]


@dataclass
class _Profile:
    score: list[float]
    avail: list[bool]
    surf: list[bool]
    vac_gain: list[float]
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
        cfg = self.cfg
        score: list[float] = []
        avail: list[bool] = []
        surf: list[bool] = []
        gain: list[float] = []
        for t in range(length):
            day = start + dt.timedelta(days=t)
            ok, _ = is_available(dest, day)
            avail.append(ok)
            if ok:
                score.append(daily_score(dest, day, cfg.weights, cfg.work_window))
                surf.append(interpolated_scores(dest, day)[1] >= GOOD_SURF)
                gain.append(vacation_gain(dest, day, cfg.weights, cfg.work_window))
            else:
                score.append(0.0)
                surf.append(False)
                gain.append(0.0)
        pref = [0.0] * (length + 1)
        blocked = [0] * (length + 1)
        for t in range(length):
            pref[t + 1] = pref[t] + score[t]
            blocked[t + 1] = blocked[t] + (0 if avail[t] else 1)
        prof = _Profile(
            score=score, avail=avail, surf=surf, vac_gain=gain, pref=pref, blocked=blocked
        )
        self._profiles[key] = prof
        return prof

    def _leg_price(self, origin: str, destination: str, day: dt.date) -> tuple[float, str]:
        key = (origin, destination, day)
        cached = self._prices.get(key)
        if cached is None:
            cached = self.pb.oneway(origin, destination, day)
            self._prices[key] = cached
        return cached

    # ------------------------------------------------------------------ #
    # Anreise und Rueckweg
    # ------------------------------------------------------------------ #
    def _access(self, hub: str, context: str) -> Access | None:
        origin = self.origins.get(hub)
        return origin.access.get(context) if origin else None

    def outbound_cost(
        self, hub: str, dest_airport: str, day: dt.date, strategy: str
    ) -> tuple[float, str] | None:
        """Gesamtkosten der Anreise ab Startkontext bis zum ersten Ziel."""
        cfg = self.cfg
        access = self._access(hub, cfg.outbound_context)
        if access is None:
            return None
        longhaul, src = self._leg_price(hub, dest_airport, day)
        if longhaul == float("inf"):
            return None

        total = longhaul * cfg.travellers
        if strategy == "through_ticket":
            if access.mode != "flight":
                return None  # ein Durchgangsticket gibt es nur mit Zubringerflug
            total += access.full_fare_eur_pp * cfg.travellers
            return total, f"{src}+through"
        total += access.total_price(cfg.travellers)
        if access.mode == "flight":
            total += cfg.self_connect_risk_eur
        return total, f"{src}+{access.mode}"

    def return_cost(
        self, last_airport: str, hub: str, day: dt.date, strategy: str
    ) -> tuple[float, str] | None:
        """Gesamtkosten des Rueckwegs vom letzten Ziel bis Teneriffa."""
        cfg = self.cfg
        access = self._access(hub, "tenerife")
        if access is None and cfg.return_feeder_mode != "later":
            return None
        longhaul, src = self._leg_price(last_airport, hub, day)
        if longhaul == float("inf"):
            return None
        # Open-Jaw: Hin und Rueck auf einem Langstreckenticket ist guenstiger
        # als zwei Einzelstrecken.
        longhaul *= 1 - cfg.openjaw_discount

        total = longhaul * cfg.travellers
        if cfg.return_feeder_mode == "later":
            # Die Reise endet in Europa; der Heimflug steckt in post_trip_cost_eur.
            return total, f"{src}+endet_in_europa"
        if strategy == "through_ticket":
            if access.mode != "flight":
                return None
            total += access.full_fare_eur_pp * cfg.travellers
            return total, f"{src}+through"
        total += access.total_price(cfg.travellers)
        if access.mode == "flight":
            total += cfg.self_connect_risk_eur
        return total, f"{src}+{access.mode}"

    def outbound_hubs(self) -> list[str]:
        cfg = self.cfg
        candidates = cfg.allowed_origins or tuple(
            h.id for h in self.origins.values() if h.reachable_from(cfg.outbound_context)
        )
        return [h for h in candidates if self._access(h, cfg.outbound_context)]

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
            if d.work < self.cfg.min_work_score:
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
        self,
        seq: tuple[Destination, ...],
        start: dt.date,
        hub: str,
        return_hub: str,
        strategy: str,
    ) -> Itinerary | None:
        cfg = self.cfg
        k = len(seq)
        max_len = min(cfg.max_days, (cfg.latest_end - start).days + 1)
        if max_len < cfg.min_days or k * cfg.min_block_days > max_len:
            return None

        vpp = cfg.value_per_score_point_eur * cfg.travellers
        profiles = [self._profile(d, start, max_len) for d in seq]

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
                    priced = self.outbound_cost(hub, dest.primary_airport, arrive_day, strategy)
                    if priced is None:
                        continue
                    arrival_cost, src = priced
                else:
                    ppp, src = self._leg_price(
                        seq[i - 1].primary_airport, dest.primary_airport, arrive_day
                    )
                    if ppp == float("inf"):
                        continue
                    arrival_cost = ppp * cfg.travellers
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
                        back[(i + 1, end)] = (i, t, arrival_cost, src)

        # cost_so_far[i][t] = reine Geldkosten zum selben Zustand wie g[i][t].
        # Im Billig-Modus wird danach optimiert, nicht nach dem Nettowert.
        best: tuple[float, float, int, float, str] | None = None
        last = seq[-1]
        for total in range(cfg.min_days, max_len + 1):
            if g[k][total] == NEG:
                continue
            back_day = start + dt.timedelta(days=total - 1)
            priced = self.return_cost(last.primary_airport, return_hub, back_day, strategy)
            if priced is None:
                continue
            cost, src = priced
            if cfg.board_bags:
                cost += self.pb.boardbag_eur() * cfg.board_bags
            net = g[k][total] - cost
            if cfg.objective_mode == "per_day":
                rank = -net / total
            else:
                # Auch im Billig-Modus waehlt das DP die Gesamtlaenge nach dem
                # Nettowert. Damit Kosten dominieren, setzt der Billig-Modus
                # value_per_score_point_eur niedrig (s. cheapest_config()); die
                # endgueltige Reihenfolge entsteht in run_all() nach Gesamtkosten.
                rank = -net
            if best is None or rank < best[0]:
                best = (rank, net, total, cost, src)

        if best is None:
            return None
        _, net, total, return_total, return_src = best
        itin = self._reconstruct(
            seq, start, total, hub, return_hub, strategy, back, net, return_total, return_src
        )
        if cfg.budget_eur is not None and itin.total_cost_eur > cfg.budget_eur:
            return None
        if cfg.budget_per_person_eur is not None and (
            itin.total_cost_eur / cfg.travellers > cfg.budget_per_person_eur
        ):
            return None
        if itin.good_surf_days < cfg.min_good_surf_days:
            return None
        if itin.score_per_day < cfg.min_score_per_day:
            return None
        return itin

    # ------------------------------------------------------------------ #
    def _reconstruct(
        self,
        seq: tuple[Destination, ...],
        start: dt.date,
        total: int,
        hub: str,
        return_hub: str,
        strategy: str,
        back: dict,
        net: float,
        return_total: float,
        return_src: str,
    ) -> Itinerary:
        cfg = self.cfg
        bounds: list[tuple[int, int, float, str]] = []
        i, t = len(seq), total
        while i > 0:
            pi, pt, cost, src = back[(i, t)]
            bounds.append((pt, t, cost, src))
            i, t = pi, pt
        bounds.reverse()

        blocks: list[Block] = []
        legs: list[Leg] = []
        flight_cost = 0.0
        estimated = 0.0
        for idx, (bt, bend, cost, src) in enumerate(bounds):
            dest = seq[idx]
            blocks.append(
                Block(
                    destination=dest,
                    start=start + dt.timedelta(days=bt),
                    end=start + dt.timedelta(days=bend - 1),
                )
            )
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

        flight_cost += return_total + cfg.pre_trip_cost_eur + cfg.post_trip_cost_eur
        if "estimate" in return_src or "unknown" in return_src:
            estimated += return_total
        legs.append(
            Leg(
                origin=seq[-1].primary_airport,
                destination=return_hub,
                date=start + dt.timedelta(days=total - 1),
                price_eur=return_total,
                kind="return",
                source=return_src,
            )
        )

        self._allocate_vacation(blocks)

        baggage = self.pb.boardbag_eur() * cfg.board_bags * len(legs)
        ground = sum(b.destination.cost_per_day_eur_pp * b.days * cfg.travellers for b in blocks)
        visas = sum(
            self.pb.visa_eur(c) for c in {b.destination.country for b in blocks}
        ) * cfg.travellers

        raw_score, good_surf = self._score_blocks(blocks)
        # Der Urlaubszugewinn steckt nicht im DP-Nettowert - hier nachtragen.
        work_only, _ = self._score_blocks(blocks, ignore_vacation=True)
        net += (raw_score - work_only) * cfg.value_per_score_point_eur * cfg.travellers

        return Itinerary(
            blocks=blocks,
            legs=legs,
            origin_hub=hub,
            ticket_strategy=strategy,
            travellers=cfg.travellers,
            flight_cost_eur=round(flight_cost, 2),
            ground_cost_eur=round(ground, 2),
            visa_cost_eur=round(visas, 2),
            baggage_cost_eur=round(baggage, 2),
            experience_score=round(raw_score, 2),
            estimated_share=round(estimated / flight_cost, 3) if flight_cost else 1.0,
            objective_eur=round(-net, 2),
            objective_per_day_eur=round(-net / total, 2),
            good_surf_days=good_surf,
            outbound_context=cfg.outbound_context,
            return_hub=return_hub,
            vacation_days=sum(b.vacation_days for b in blocks),
        )

    # ------------------------------------------------------------------ #
    def _allocate_vacation(self, blocks: list[Block]) -> None:
        """Urlaubstage dorthin, wo sie am meisten bringen (schlechtestes Arbeitsfenster)."""
        cfg = self.cfg
        budget = min(cfg.vacation_days, sum(b.days for b in blocks))
        if budget <= 0:
            return
        def mean_gain(block: Block) -> float:
            return sum(
                vacation_gain(
                    block.destination,
                    block.start + dt.timedelta(days=n),
                    cfg.weights,
                    cfg.work_window,
                )
                for n in range(block.days)
            ) / block.days

        priority = [b for b in blocks if b.destination.id in cfg.vacation_priority]
        rest = sorted(
            (b for b in blocks if b.destination.id not in cfg.vacation_priority),
            key=lambda b: -mean_gain(b),
        )
        ranked = sorted(priority, key=lambda b: -mean_gain(b)) + rest
        caps = {
            id(b): (
                b.days
                if b.destination.id in cfg.vacation_priority
                else max(1, int(b.days * cfg.max_vacation_share_per_block))
            )
            for b in blocks
        }
        for block in ranked:
            if budget <= 0:
                break
            take = min(caps[id(block)], budget)
            block.vacation_days = take
            budget -= take
        # Rest verteilen, falls die Deckel das Budget nicht aufbrauchen.
        for block in ranked:
            if budget <= 0:
                break
            extra = min(block.days - block.vacation_days, budget)
            block.vacation_days += extra
            budget -= extra

    def _score_blocks(
        self, blocks: list[Block], ignore_vacation: bool = False
    ) -> tuple[float, int]:
        cfg = self.cfg
        raw_score = 0.0
        good_surf = 0
        for b in blocks:
            # Urlaubstage auf die Tage mit dem besten Surf legen - so wuerde man es
            # auch in der Praxis machen.
            days = [b.start + dt.timedelta(days=n) for n in range(b.days)]
            if ignore_vacation or not b.vacation_days:
                vac_days: set[dt.date] = set()
            else:
                vac_days = set(
                    sorted(days, key=lambda d: -interpolated_scores(b.destination, d)[1])[
                        : b.vacation_days
                    ]
                )
            for n, day in enumerate(days):
                s = daily_score(
                    b.destination, day, cfg.weights, cfg.work_window, vacation=day in vac_days
                )
                raw_score += s * (cfg.travel_day_score_factor if n == 0 else 1.0)
                if interpolated_scores(b.destination, day)[1] >= GOOD_SURF:
                    good_surf += 1
        return raw_score, good_surf

    # ------------------------------------------------------------------ #
    def annotate(self, itin: Itinerary) -> Itinerary:
        """Haengt Warnungen an - erst fuer die Finalisten, nicht fuer alle Varianten."""
        from .workwindow import describe

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
                out.append(f"Abflugtag liegt in {event.name} - Preisspitze")
            if "EU-Abfluege" in event.affects and event.overlaps(
                itin.end - dt.timedelta(days=1), itin.end + dt.timedelta(days=1)
            ):
                out.append(f"Rueckflugtag liegt in {event.name} - Preisspitze")
        for b in itin.blocks:
            mid = b.start + dt.timedelta(days=b.days // 2)
            out.append(f"Arbeitszeit in {b.destination.region_short}: {describe(b.destination, mid, self.cfg.work_window)}")
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
        hubs = self.outbound_hubs()
        for seq in self.sequences():
            for start in self.cfg.date_grid():
                for hub in hubs:
                    for return_hub in self.cfg.allowed_return_hubs:
                        for strategy in self.cfg.ticket_strategies:
                            itin = self._solve(seq, start, hub, return_hub, strategy)
                            if itin:
                                out.append(itin)
        if self.cfg.objective_mode == "cheapest":
            out.sort(key=lambda i: (i.total_cost_eur, -i.experience_score))
        elif self.cfg.objective_mode == "per_day":
            out.sort(key=lambda i: i.objective_per_day_eur)
        else:
            out.sort(key=lambda i: i.objective_eur)
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


def cheapest_config(base: TripConfig, min_score_per_day: float = 6.5) -> TripConfig:
    """Variante von `base`, die auf "billigste noch sinnvolle Route" optimiert.

    Zwei Eingriffe: der Erlebniswert wird im DP stark abgewertet (damit die
    Blocklaengen und Flugdaten nach dem Preis gewaehlt werden), und
    `min_score_per_day` wirkt als harte Schwelle, unter der eine Route
    verworfen wird. Ohne diese Schwelle kaeme die billigste Route heraus,
    nicht die billigste brauchbare.
    """
    import dataclasses

    return dataclasses.replace(
        base,
        objective_mode="cheapest",
        value_per_score_point_eur=4.0,
        min_score_per_day=min_score_per_day,
    )
