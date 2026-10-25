"""Tests fuer Saison-Scoring, Preise, Optimierer und URL-Kodierung."""

from __future__ import annotations

import base64
import datetime as dt
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from workation.data import (  # noqa: E402
    hubs_reachable_from,
    load_calendar,
    load_destinations,
    load_origins,
)
from workation.scenarios import SCENARIOS  # noqa: E402
from workation.optimizer import Optimizer, TripConfig  # noqa: E402
from workation.prices import PriceBook  # noqa: E402
from workation.scrape.queries import grid_queries  # noqa: E402
from workation.scrape.urls import multicity_url, oneway_url  # noqa: E402
from workation.seasonality import (  # noqa: E402
    Weights,
    daily_score,
    interpolated_scores,
    is_available,
    vacation_gain,
    window_of,
)
from workation.workwindow import WorkWindow, local_window, overlap_score  # noqa: E402


# --------------------------------------------------------------------------- #
# Stammdaten
# --------------------------------------------------------------------------- #
def test_destinations_load_and_cover_all_windows():
    dests, meta = load_destinations()
    assert len(dests) >= 15
    for dest in dests.values():
        assert set(dest.scores) == set(meta["windows"]), dest.id
        for score in dest.scores.values():
            for value in (score.weather, score.surf, score.calm):
                assert 0 <= value <= 10
        assert 0 <= dest.work <= 10
        assert dest.primary_airport in dest.airports


def test_origins_and_calendar_load():
    origins, meta = load_origins()
    assert {"MAD", "BCN"} <= set(origins)
    assert "residencia_note" in meta
    events = load_calendar()
    assert any(e.id == "semana-santa-2027" for e in events)
    for event in events:
        assert event.start <= event.end


# --------------------------------------------------------------------------- #
# Saisonalitaet
# --------------------------------------------------------------------------- #
def test_window_of():
    assert window_of(dt.date(2027, 3, 15)) == "2027-03-H1"
    assert window_of(dt.date(2027, 3, 16)) == "2027-03-H2"
    assert window_of(dt.date(2027, 5, 1)) == "2027-05-H1"


def test_interpolation_is_bounded_by_neighbouring_windows():
    dests, _ = load_destinations()
    lombok = dests["ID-LOMBOK"]
    for day in (dt.date(2027, 4, 1), dt.date(2027, 4, 15), dt.date(2027, 4, 20)):
        weather, surf, calm = interpolated_scores(lombok, day)
        assert 0 <= weather <= 10 and 0 <= surf <= 10 and 0 <= calm <= 10


def test_interpolation_is_monotone_where_windows_are_monotone():
    """Lomboks Surf-Score steigt von Maerz nach Mai - die Glaettung darf das nicht brechen."""
    dests, _ = load_destinations()
    lombok = dests["ID-LOMBOK"]
    days = [dt.date(2027, 3, 20) + dt.timedelta(days=7 * i) for i in range(7)]
    surf = [interpolated_scores(lombok, d)[1] for d in days]
    assert surf == sorted(surf), surf


def test_sri_lanka_south_peaks_in_march_lombok_in_may():
    dests, _ = load_destinations()
    weights = Weights.surf_focused()
    sl = dests["LK-SOUTH"]
    lombok = dests["ID-LOMBOK"]
    assert daily_score(sl, dt.date(2027, 3, 20), weights) > daily_score(
        sl, dt.date(2027, 5, 5), weights
    )
    assert daily_score(lombok, dt.date(2027, 5, 5), weights) > daily_score(
        lombok, dt.date(2027, 3, 10), weights
    )


def test_hard_avoid_blocks_laos_in_burning_season():
    dests, _ = load_destinations()
    laos = dests["LA-LAOS"]
    ok, reason = is_available(laos, dt.date(2027, 3, 25))
    assert not ok and "Brandsaison" in reason
    assert is_available(laos, dt.date(2027, 5, 5))[0]


def test_lombok_blocked_during_lebaran_travel_wave():
    dests, _ = load_destinations()
    lombok = dests["ID-LOMBOK"]
    assert not is_available(lombok, dt.date(2027, 3, 10))[0]
    assert is_available(lombok, dt.date(2027, 3, 20))[0]


# --------------------------------------------------------------------------- #
# Arbeitszeitfenster
# --------------------------------------------------------------------------- #
def test_local_window_reflects_offset_and_dst():
    dests, _ = load_destinations()
    sl = dests["LK-SOUTH"]
    win = WorkWindow(9.0, 16.0, flex_h=0.0)
    # Winterzeit: +4,5 h -> 13:30-20:30
    assert local_window(sl, dt.date(2027, 3, 20), win) == pytest.approx((13.5, 20.5))
    # Ab 28.03. gilt Sommerzeit, der Versatz schrumpft um 1 h
    assert local_window(sl, dt.date(2027, 3, 28), win) == pytest.approx((12.5, 19.5))


def test_dst_shift_improves_work_window():
    dests, _ = load_destinations()
    lombok = dests["ID-LOMBOK"]
    win = WorkWindow(9.0, 16.0, flex_h=0.0)
    before = overlap_score(lombok, dt.date(2027, 3, 27), win)
    after = overlap_score(lombok, dt.date(2027, 3, 28), win)
    assert after > before


def test_a_late_local_start_is_rewarded_not_punished():
    """Die Nutzer bevorzugen einen spaeten lokalen Arbeitsbeginn (ca. 14:30).

    Drei Wochen praktisch getestet: erst gegen 15 Uhr anzufangen und den ganzen
    Vormittag fuer einen Ausflug zu haben, war besser als um 12:30 zu starten.
    Ein grosser Zeitversatz nach Osten ist damit ein Vorteil.
    """
    dests, _ = load_destinations()
    win = WorkWindow(9.0, 16.0, flex_h=0.0)
    day = dt.date(2027, 4, 15)
    oman = overlap_score(dests["OM-OMAN"], day, win)        # 11:00 Start
    sri = overlap_score(dests["LK-SOUTH"], day, win)        # 12:30 Start
    lombok = overlap_score(dests["ID-LOMBOK"], day, win)    # 15:00 Start
    assert lombok > sri > oman
    assert 0 <= oman <= 10 and 0 <= lombok <= 10


def test_working_past_midnight_is_still_penalised():
    """Spaeter ist besser - aber nicht beliebig spaet."""
    dests, _ = load_destinations()
    win = WorkWindow(9.0, 16.0, flex_h=0.0)
    day = dt.date(2027, 4, 15)
    # Raja Ampat (+7 h im Sommer) startet 16:00 und endet 23:00.
    raja = overlap_score(dests["ID-RAJA-AMPAT"], day, win)
    lombok = overlap_score(dests["ID-LOMBOK"], day, win)
    assert raja < lombok


def test_ideal_start_parameter_shifts_the_ranking():
    dests, _ = load_destinations()
    day = dt.date(2027, 4, 15)
    sri, lombok = dests["LK-SOUTH"], dests["ID-LOMBOK"]
    early = WorkWindow(9.0, 16.0, flex_h=0.0, ideal_local_start_h=12.5)
    late = WorkWindow(9.0, 16.0, flex_h=0.0, ideal_local_start_h=15.0)
    assert overlap_score(sri, day, early) > overlap_score(lombok, day, early)
    assert overlap_score(lombok, day, late) > overlap_score(sri, day, late)


def test_flexibility_can_only_help():
    dests, _ = load_destinations()
    lombok = dests["ID-LOMBOK"]
    day = dt.date(2027, 4, 15)
    rigid = overlap_score(lombok, day, WorkWindow(9.0, 16.0, flex_h=0.0))
    flexible = overlap_score(lombok, day, WorkWindow(9.0, 16.0, flex_h=2.0))
    assert flexible >= rigid


# --------------------------------------------------------------------------- #
# Urlaubstage
# --------------------------------------------------------------------------- #
def test_vacation_does_not_reward_bad_infrastructure():
    """Ein Urlaubstag darf ein Ziel nicht dafuer belohnen, dass man dort nicht arbeiten kann.

    Lombok und Sumbawa haben im April identische Wetter-/Surf-/Ruhe-Scores und
    unterscheiden sich nur in der Arbeitsinfrastruktur (7 vs 3). Ein Urlaubstag
    muss daher an beiden gleich viel wert sein.
    """
    dests, _ = load_destinations()
    weights = Weights.surf_focused()
    win = WorkWindow(9.0, 16.0, flex_h=1.0)
    day = dt.date(2027, 4, 20)
    lombok, sumbawa = dests["ID-LOMBOK"], dests["ID-SUMBAWA"]
    a, b = lombok.scores["2027-04-H2"], sumbawa.scores["2027-04-H2"]
    assert (a.weather, a.surf, a.calm) == (b.weather, b.surf, b.calm)
    # Lombok hat zusaetzlich die besseren Ausflugsoptionen (Rinjani, Komodo-
    # Liveaboard, Gilis), also darf sein Urlaubstag nicht schlechter sein.
    assert daily_score(lombok, day, weights, win, vacation=True) >= daily_score(
        sumbawa, day, weights, win, vacation=True
    )
    # Entscheidend: der Vorsprung kommt NICHT daher, dass Sumbawa schlechte
    # Arbeitsinfrastruktur hat. Bei gleichem activity_score waeren sie gleich.
    import dataclasses

    sumbawa_like_lombok = dataclasses.replace(
        sumbawa, activity_score=lombok.activity_score
    )
    assert daily_score(
        lombok, day, weights, win, vacation=True
    ) == pytest.approx(daily_score(sumbawa_like_lombok, day, weights, win, vacation=True))
    # Am Arbeitstag schlaegt die Infrastruktur dagegen voll durch.
    assert daily_score(lombok, day, weights, win) > daily_score(sumbawa, day, weights, win)


def test_vacation_gain_is_highest_where_the_work_window_hurts():
    dests, _ = load_destinations()
    weights = Weights.surf_focused()
    win = WorkWindow(9.0, 16.0, flex_h=1.0)
    day = dt.date(2027, 4, 20)
    # Sri Lanka: Arbeitsfenster perfekt -> Urlaub bringt dort am wenigsten.
    assert vacation_gain(dests["ID-LOMBOK"], day, weights, win) > vacation_gain(
        dests["LK-SOUTH"], day, weights, win
    )


def test_vacation_days_are_spread_across_blocks():
    cfg = TripConfig(
        outbound_context="cottbus", allowed_origins=("BER",), eligible_tiers=("A",),
        max_destinations=2, start_date_step=7, vacation_days=14,
        max_vacation_share_per_block=0.5,
    )
    results = Optimizer(cfg).run(top_n=1)
    assert results
    itin = results[0]
    assert itin.vacation_days == 14
    assert all(b.vacation_days > 0 for b in itin.blocks), "Urlaub klumpt in einem Block"
    for block in itin.blocks:
        assert block.vacation_days <= max(1, int(block.days * 0.5)) or itin.vacation_days == sum(
            b.days for b in itin.blocks
        )
        assert block.work_days + block.vacation_days == block.days


def test_low_work_destinations_are_not_usable_as_bases():
    cfg = TripConfig(min_work_score=5.0, eligible_tiers=("A", "B", "C"))
    ids = {d.id for d in Optimizer(cfg).eligible_destinations()}
    assert "ID-SUMBAWA" not in ids      # work 3
    assert "MG-MADAGASCAR" not in ids   # work 2
    assert "ID-LOMBOK" in ids           # work 7
    # Ohne die Schranke sind sie wieder dabei.
    loose = TripConfig(min_work_score=0.0, eligible_tiers=("A", "B", "C"))
    assert "ID-SUMBAWA" in {d.id for d in Optimizer(loose).eligible_destinations()}


# --------------------------------------------------------------------------- #
# Anreisekontexte
# --------------------------------------------------------------------------- #
def test_hubs_are_filtered_by_departure_context():
    assert set(hubs_reachable_from("montafon")) >= {"ZRH", "MUC"}
    assert "MAD" not in hubs_reachable_from("montafon")
    assert "BER" in hubs_reachable_from("cottbus")


def test_residencia_discount_only_on_separate_tenerife_ticket():
    origins, meta = load_origins()
    mad = origins["MAD"].access["tenerife"]
    assert mad.residencia_discount
    assert mad.min_connect_h == 3.0
    # Ohne Rabatt ist derselbe Zubringer das Vierfache - so wird ein
    # Durchgangsticket bewertet.
    assert mad.full_fare_eur_pp == pytest.approx(mad.price_eur_pp * 4)
    assert "NICHT" in meta["residencia_note"]


def test_company_covers_exactly_one_ticket_from_hamburg():
    origins, _ = load_origins()
    ham = origins["HAM"].access["tenerife"]
    assert ham.company_covered_travellers == 1
    assert ham.total_price(1) == 0.0
    assert ham.total_price(2) == pytest.approx(ham.price_eur_pp)


def test_outbound_from_montafon_uses_train_not_a_feeder_flight():
    cfg = TripConfig(
        outbound_context="montafon", allowed_origins=("ZRH",), eligible_tiers=("A",),
        max_destinations=2, start_date_step=7,
        earliest_start=dt.date(2027, 3, 5), latest_end=dt.date(2027, 4, 20),
    )
    opt = Optimizer(cfg)
    priced = opt.outbound_cost("ZRH", "CMB", dt.date(2027, 3, 7), "separate_tickets")
    assert priced is not None
    cost, source = priced
    assert source.endswith("+train")
    # Kein Self-Connect-Risiko, weil kein Zubringerflug im Spiel ist.
    longhaul, _ = opt._leg_price("ZRH", "CMB", dt.date(2027, 3, 7))
    access = opt.origins["ZRH"].access["montafon"]
    assert cost == pytest.approx(longhaul * 2 + access.price_eur_pp * 2)
    # MAD ist aus dem Montafon nicht erreichbar.
    assert opt.outbound_cost("MAD", "CMB", dt.date(2027, 3, 7), "separate_tickets") is None


def test_return_always_routes_home_via_an_allowed_hub():
    cfg = TripConfig(
        outbound_context="montafon", allowed_origins=("ZRH",),
        allowed_return_hubs=("MAD",), eligible_tiers=("A",), max_destinations=2,
        start_date_step=7, earliest_start=dt.date(2027, 3, 5),
        latest_end=dt.date(2027, 4, 20),
    )
    results = Optimizer(cfg).run(top_n=1)
    assert results
    assert results[0].return_hub == "MAD"
    assert results[0].legs[-1].destination == "MAD"


# --------------------------------------------------------------------------- #
# Szenarien
# --------------------------------------------------------------------------- #
def test_every_scenario_yields_a_feasible_route():
    base = TripConfig(
        weights=Weights.surf_focused(), eligible_tiers=("A",), max_destinations=2,
    )
    for scenario in SCENARIOS.values():
        cfg = scenario.config(base)
        results = Optimizer(cfg).run(top_n=1)
        assert results, f"{scenario.key} ohne Ergebnis"
        itin = results[0]
        assert scenario.earliest_start <= itin.start <= scenario.latest_start
        assert itin.outbound_context == scenario.outbound_context
        assert itin.origin_hub in scenario.allowed_origins


def test_scenario_pre_trip_cost_lands_in_the_total():
    base = TripConfig(
        weights=Weights.surf_focused(), eligible_tiers=("A",), max_destinations=2,
    )
    cheap = Optimizer(SCENARIOS["cottbus_bruecke"].config(base)).run(top_n=1)[0]
    pricey = Optimizer(SCENARIOS["heim_tfs"].config(base)).run(top_n=1)[0]
    assert SCENARIOS["heim_tfs"].pre_trip_cost_eur > 0
    assert pricey.total_cost_eur > cheap.total_cost_eur


# --------------------------------------------------------------------------- #
# Preise
# --------------------------------------------------------------------------- #
def test_estimate_uses_cheapest_gateway_combination():
    """Die Schaetzung muss die billigste Gateway-Kombination finden, nicht den Direkt-Hint.

    MAD->LOP: Direkt-Hint 620, via KUL 430+120+40 = 590, via Jakarta
    190+55+40 = 285. Jakarta gewinnt - und genau deshalb ist CGK als
    Transit-Gateway in den Daten (Java selbst ist als Aufenthalt ausgeschlossen).
    """
    pb = PriceBook(quotes=[])
    via_jakarta, _ = pb.oneway("MAD", "LOP", dt.date(2027, 4, 7))
    assert via_jakarta == pytest.approx(285.0)   # 190 + 55 + 40
    assert via_jakarta < 590.0


def test_scraped_price_beats_estimate_and_respects_tolerance():
    from workation.models import PriceQuote

    quotes = [
        PriceQuote("MAD", "CMB", dt.date(2027, 3, 18), 333.0, source="google_flights"),
    ]
    pb = PriceBook(quotes=quotes, date_tolerance_days=3)
    price, source = pb.oneway("MAD", "CMB", dt.date(2027, 3, 20))
    assert price == 333.0 and source == "google_flights"
    # Ausserhalb der Toleranz: Median derselben Strecke, nicht der Schaetzwert.
    price, source = pb.oneway("MAD", "CMB", dt.date(2027, 4, 30))
    assert source == "scrape_median_other_dates"


def test_seasonal_multiplier_applies_once_and_only_to_estimates():
    from workation.models import PriceQuote

    pb = PriceBook(quotes=[])
    plain, _ = pb.oneway("MAD", "CMB", dt.date(2027, 3, 16))
    easter, src = pb.oneway("MAD", "CMB", dt.date(2027, 3, 24))
    assert easter > plain and "Semana Santa" in src
    # Mehrere Regeln duerfen sich nicht multiplizieren.
    factor, _ = pb.estimate_multiplier("LOP", "MAD", dt.date(2027, 5, 1))
    assert factor == pytest.approx(1.12)
    # Echte Preise werden nicht aufgeschlagen.
    pb2 = PriceBook(
        quotes=[PriceQuote("MAD", "CMB", dt.date(2027, 3, 24), 400.0, source="google_flights")]
    )
    assert pb2.oneway("MAD", "CMB", dt.date(2027, 3, 24)) == (400.0, "google_flights")


def test_unknown_route_returns_infinity():
    pb = PriceBook(quotes=[])
    price, source = pb.oneway("MAD", "ZZZ", dt.date(2027, 4, 1))
    assert price == float("inf") and source == "unknown"


# --------------------------------------------------------------------------- #
# Optimierer
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def small_result():
    cfg = TripConfig(
        weights=Weights.surf_focused(),
        objective_mode="per_day",
        start_date_step=7,
        min_destinations=2,
        max_destinations=2,
        allowed_origins=("MAD",),
        eligible_tiers=("A",),
    )
    opt = Optimizer(cfg)
    return opt, opt.run(top_n=5)


def test_optimizer_returns_feasible_itineraries(small_result):
    opt, results = small_result
    cfg = opt.cfg
    assert results
    for itin in results:
        assert cfg.min_days <= itin.total_days <= cfg.max_days
        assert itin.start >= cfg.earliest_start
        assert itin.end <= cfg.latest_end
        assert cfg.min_destinations <= len(itin.blocks) <= cfg.max_destinations
        # Blöcke sind lückenlos und in der Reihenfolge der Sequenz.
        for prev, nxt in zip(itin.blocks, itin.blocks[1:]):
            assert nxt.start == prev.end + dt.timedelta(days=1)
        for block in itin.blocks:
            assert cfg.min_block_days <= block.days <= cfg.max_block_days
            for n in range(block.days):
                day = block.start + dt.timedelta(days=n)
                assert is_available(block.destination, day)[0]
        # Ein Flug pro Block plus Rückflug.
        assert len(itin.legs) == len(itin.blocks) + 1
        assert itin.legs[-1].kind == "return"
        assert itin.total_cost_eur > 0


def test_sri_lanka_then_lombok_is_the_leading_pair(small_result):
    """Nach Erlebniswert (objective_mode='per_day') fuehrt Suedkueste -> Lombok.

    Die saisonale Kernaussage: Sri Lankas Saison endet mit dem SW-Monsun genau
    dann, wenn Lomboks Trockenzeit beginnt. Im Billig-Modus gewinnt dagegen
    Nordvietnam, weil es schlicht guenstiger ist - das pruefen die Tests zum
    Billig-Modus separat.
    """
    _, results = small_result
    best = results[0]
    ids = [b.destination.id for b in best.blocks]
    assert ids == ["LK-SOUTH", "ID-LOMBOK"], ids
    assert best.blocks[0].start < best.blocks[1].start


def test_budget_constraint_is_enforced():
    cfg = TripConfig(
        start_date_step=14,
        max_destinations=2,
        allowed_origins=("MAD",),
        ticket_strategies=("self_transfer",),
        eligible_tiers=("A",),
        budget_eur=5000,
    )
    results = Optimizer(cfg).run(top_n=5)
    assert all(i.total_cost_eur <= 5000 for i in results)


def test_include_and_exclude_filters():
    cfg = TripConfig(
        start_date_step=14,
        max_destinations=2,
        allowed_origins=("MAD",),
        ticket_strategies=("self_transfer",),
        include_destinations=("VN-NORTH",),
        exclude_destinations=("ID-SUMBAWA",),
    )
    results = Optimizer(cfg).run(top_n=5)
    assert results
    for itin in results:
        ids = {b.destination.id for b in itin.blocks}
        assert "VN-NORTH" in ids
        assert "ID-SUMBAWA" not in ids


def test_per_day_objective_matches_total():
    cfg = TripConfig(
        start_date_step=14, max_destinations=2, allowed_origins=("MAD",),
        ticket_strategies=("self_transfer",), eligible_tiers=("A",),
    )
    for itin in Optimizer(cfg).run(top_n=3):
        assert itin.objective_per_day_eur == pytest.approx(
            itin.objective_eur / itin.total_days, abs=0.02
        )


# --------------------------------------------------------------------------- #
# Google-Flights-URLs
# --------------------------------------------------------------------------- #
def _decode_protobuf(data: bytes) -> dict:
    """Minimaler Protobuf-Reader: {feldnummer: [werte]}."""
    out: dict[int, list] = {}
    pos = 0
    while pos < len(data):
        tag, pos = _read_varint(data, pos)
        field, wire = tag >> 3, tag & 0x07
        if wire == 0:
            value, pos = _read_varint(data, pos)
        elif wire == 2:
            length, pos = _read_varint(data, pos)
            value = data[pos : pos + length]
            pos += length
        else:
            raise AssertionError(f"unerwarteter Wire-Type {wire}")
        out.setdefault(field, []).append(value)
    return out


def _read_varint(data: bytes, pos: int) -> tuple[int, int]:
    result = shift = 0
    while True:
        byte = data[pos]
        pos += 1
        result |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return result, pos
        shift += 7


def _tfs_payload(url: str) -> bytes:
    import urllib.parse

    tfs = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)["tfs"][0]
    return base64.urlsafe_b64decode(tfs + "=" * (-len(tfs) % 4))


def test_oneway_url_encodes_route_date_passengers_and_triptype():
    url = oneway_url("MAD", "CMB", dt.date(2027, 3, 18), adults=2)
    top = _decode_protobuf(_tfs_payload(url))
    legs = top[3]
    assert len(legs) == 1
    leg = _decode_protobuf(legs[0])
    assert leg[2][0] == b"2027-03-18"
    assert _decode_protobuf(leg[13][0])[2][0] == b"MAD"
    assert _decode_protobuf(leg[14][0])[2][0] == b"CMB"
    assert top[8] == [1, 1]        # zwei Erwachsene
    assert top[9] == [1]           # Economy
    assert top[19] == [2]          # Oneway


def test_multicity_url_keeps_leg_order():
    legs = [
        ("MAD", "CMB", dt.date(2027, 3, 18)),
        ("CMB", "LOP", dt.date(2027, 4, 7)),
        ("LOP", "MAD", dt.date(2027, 4, 26)),
    ]
    top = _decode_protobuf(_tfs_payload(multicity_url(legs)))
    assert top[19] == [3]  # Multicity
    decoded = []
    for raw in top[3]:
        leg = _decode_protobuf(raw)
        decoded.append(
            (
                _decode_protobuf(leg[13][0])[2][0].decode(),
                _decode_protobuf(leg[14][0])[2][0].decode(),
                leg[2][0].decode(),
            )
        )
    assert decoded == [(o, d, day.isoformat()) for o, d, day in legs]


def test_multicity_requires_two_legs():
    with pytest.raises(ValueError):
        multicity_url([("MAD", "CMB", dt.date(2027, 3, 18))])


def test_grid_queries_are_wellformed_and_deduplicated():
    queries = grid_queries(level="quick")
    assert queries
    ids = [q.id for q in queries]
    assert len(ids) == len(set(ids))
    for q in queries:
        assert q.url.startswith("https://www.google.com/travel/flights?tfs=")
        assert q.fallback_url
        for origin, destination, day in q.legs:
            assert len(origin) == 3 and len(destination) == 3
            assert dt.date.fromisoformat(day).year == 2027


# --------------------------------------------------------------------------- #
# Aktivitaets-Dimension
# --------------------------------------------------------------------------- #
def test_every_destination_has_activity_data():
    dests, _ = load_destinations()
    for dest in dests.values():
        assert 0 <= dest.activity_score <= 10, dest.id
        assert dest.multiday, dest.id


def test_activity_weight_lifts_non_surf_destinations():
    """Mit Aktivitaetsgewicht muss Nordvietnam (Surf 0, Aktivitaet 10) aufsteigen."""
    dests, _ = load_destinations()
    vietnam = dests["VN-NORTH"]
    day = dt.date(2027, 4, 10)
    win = WorkWindow(9.0, 16.0, flex_h=1.0)
    surf_profile = daily_score(vietnam, day, Weights.surf_focused(), win)
    active_profile = daily_score(vietnam, day, Weights.active(), win)
    assert active_profile > surf_profile


def test_weight_profiles_sum_to_one():
    for factory in (Weights.active, Weights.surf_focused, Weights.work_focused, Weights.balanced):
        w = factory()
        total = w.weather + w.surf + w.activity + w.calm + w.work + w.work_window
        assert total == pytest.approx(1.0), factory.__name__


# --------------------------------------------------------------------------- #
# Rueckweg-Modi und Feier-Nachlauf
# --------------------------------------------------------------------------- #
def test_return_mode_later_skips_the_home_feeder():
    cfg_home = TripConfig(
        outbound_context="cottbus", allowed_origins=("BER",), allowed_return_hubs=("BER",),
        return_feeder_mode="home", eligible_tiers=("A",), max_destinations=2,
    )
    cfg_later = TripConfig(
        outbound_context="cottbus", allowed_origins=("BER",), allowed_return_hubs=("BER",),
        return_feeder_mode="later", eligible_tiers=("A",), max_destinations=2,
    )
    day = dt.date(2027, 4, 27)
    home = Optimizer(cfg_home).return_cost("LOP", "BER", day, "separate_tickets")
    later = Optimizer(cfg_later).return_cost("LOP", "BER", day, "separate_tickets")
    assert home is not None and later is not None
    assert later[0] < home[0]
    assert later[1].endswith("+endet_in_europa")


def test_scenarios_that_end_in_europe_carry_the_flight_home():
    """Endet die Reise in Deutschland, muss der Heimflug danach mitgerechnet werden."""
    for key in ("montafon_direkt", "cottbus_bruecke", "heim_tfs", "hamburg_direkt"):
        assert SCENARIOS[key].return_feeder_mode == "home", key
        assert SCENARIOS[key].post_trip_cost_eur == 0.0, key
    for key in ("ostritz_finale_ber", "ostritz_finale_ham"):
        assert SCENARIOS[key].return_feeder_mode == "later", key
        assert SCENARIOS[key].post_trip_cost_eur > 0.0, key
    # Der Firmenflug deckt genau eine Person, also die Haelfte.
    assert SCENARIOS["ostritz_finale_ham"].post_trip_cost_eur == pytest.approx(
        SCENARIOS["ostritz_finale_ber"].post_trip_cost_eur / 2
    )


def test_ostritz_scenarios_end_before_the_party():
    base = TripConfig(weights=Weights.active(), eligible_tiers=("A",), max_destinations=2)
    for key in ("ostritz_finale_ber", "ostritz_finale_ham"):
        scenario = SCENARIOS[key]
        results = Optimizer(scenario.config(base)).run(top_n=1)
        assert results, key
        assert results[0].end <= dt.date(2027, 5, 6), key


def test_pre_and_post_trip_costs_reach_the_total():
    import dataclasses

    base = TripConfig(
        weights=Weights.active(), eligible_tiers=("A",), max_destinations=2,
        outbound_context="cottbus", allowed_origins=("BER",), start_date_step=7,
    )
    plain = Optimizer(base).run(top_n=1)[0]
    loaded = Optimizer(
        dataclasses.replace(base, pre_trip_cost_eur=100.0, post_trip_cost_eur=200.0)
    ).run(top_n=1)[0]
    assert loaded.flight_cost_eur == pytest.approx(plain.flight_cost_eur + 300.0)


# --------------------------------------------------------------------------- #
# Preishistorie
# --------------------------------------------------------------------------- #
def _write_scrape(tmp_path, name, rows, stamp):
    import csv as _csv

    path = tmp_path / name
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = _csv.writer(fh)
        writer.writerow(
            ["origin", "destination", "depart_date", "return_date", "trip_type",
             "price_eur", "carrier", "scraped_at"]
        )
        for origin, destination, day, price, carrier in rows:
            writer.writerow([origin, destination, day, "", "oneway", price, carrier, stamp])
    return path


@pytest.fixture
def history_db(tmp_path):
    from workation import history

    db = tmp_path / "h.sqlite3"
    first = _write_scrape(
        tmp_path, "a.csv",
        [("MAD", "CGK", "2027-03-17", 220, "QR"),
         ("MAD", "CGK", "2027-03-17", 260, "EK"),
         ("MAD", "CMB", "2027-03-17", 400, "QR")],
        "2026-10-18T08:00:00+00:00",
    )
    second = _write_scrape(
        tmp_path, "b.csv",
        [("MAD", "CGK", "2027-03-17", 240, "QR"),
         ("MAD", "CMB", "2027-03-17", 410, "QR")],
        "2026-10-21T08:00:00+00:00",
    )
    third = _write_scrape(
        tmp_path, "c.csv",
        [("MAD", "CGK", "2027-03-17", 175, "QR"),
         ("MAD", "CMB", "2027-03-17", 430, "QR")],
        "2026-10-25T08:00:00+00:00",
    )
    history.ingest_csv(first, db)
    history.ingest_csv(second, db)
    history.ingest_csv(third, db)
    return db


def test_ingest_is_idempotent(history_db, tmp_path):
    from workation import history

    before = history.coverage(history_db)["observations"]
    assert history.ingest_csv(tmp_path / "a.csv", history_db) == 0
    assert history.coverage(history_db)["observations"] == before


def test_route_stats_compute_best_latest_and_median(history_db):
    from workation import history

    stats = {(s.origin, s.destination): s for s in history.route_stats(history_db)}
    cgk = stats[("MAD", "CGK")]
    assert cgk.observations == 4
    assert cgk.best_eur == pytest.approx(175.0)
    assert cgk.best_seen_at.startswith("2026-10-25")
    assert cgk.latest_eur == pytest.approx(175.0)
    assert cgk.median_eur == pytest.approx(230.0)   # Median von 175/220/240/260
    assert cgk.latest_vs_median_pct < 0


def test_deals_and_lows_find_the_dropped_route(history_db):
    from workation import history

    deals = history.deals(history_db, min_drop_pct=15.0, min_observations=3)
    assert [(d.origin, d.destination) for d in deals] == [("MAD", "CGK")]
    lows = history.all_time_lows(history_db, min_observations=3)
    assert [(d.origin, d.destination) for d in lows] == [("MAD", "CGK")]
    # Die steigende Strecke darf nicht als Deal auftauchen.
    assert all(d.destination != "CMB" for d in deals)


def test_history_feeds_the_pricebook_in_both_modes(history_db):
    from workation import history

    best = {q.destination: q.price_eur for q in history.to_quotes(history_db, "best")}
    latest = {q.destination: q.price_eur for q in history.to_quotes(history_db, "latest")}
    assert best["CGK"] == pytest.approx(175.0)
    assert best["CMB"] == pytest.approx(400.0)
    assert latest["CMB"] == pytest.approx(430.0)   # zuletzt teurer als der Bestpreis
    pb = PriceBook(quotes=history.to_quotes(history_db, "best"))
    price, source = pb.oneway("MAD", "CGK", dt.date(2027, 3, 17))
    assert price == pytest.approx(175.0)
    assert source == "history_best"


def test_to_quotes_rejects_unknown_mode(history_db):
    from workation import history

    with pytest.raises(ValueError):
        history.to_quotes(history_db, "wunschpreis")


def test_vacation_priority_overrides_the_share_cap():
    """Ein 7-Tage-Trek braucht einen zusammenhaengenden Urlaubsblock."""
    base = dict(
        outbound_context="tenerife", allowed_origins=("MAD",),
        eligible_tiers=("A", "B"), min_destinations=2, max_destinations=2,
        start_date_step=7, vacation_days=16, include_destinations=("NP-NEPAL",),
        weights=Weights.active(),
    )
    without = Optimizer(TripConfig(**base)).run(top_n=1)[0]
    with_prio = Optimizer(
        TripConfig(**base, vacation_priority=("NP-NEPAL",))
    ).run(top_n=1)[0]
    nepal_without = next(b for b in without.blocks if b.destination.id == "NP-NEPAL")
    nepal_with = next(b for b in with_prio.blocks if b.destination.id == "NP-NEPAL")
    assert nepal_with.vacation_days > nepal_without.vacation_days
    assert nepal_with.vacation_days >= 7, "zu wenig fuer einen Annapurna-Trek"
    # Das Gesamtbudget bleibt eingehalten.
    assert with_prio.vacation_days <= 16


# --------------------------------------------------------------------------- #
# Billig-Modus: guenstigste noch sinnvolle Route
# --------------------------------------------------------------------------- #
def _cheap_base(**over):
    from workation.optimizer import cheapest_config

    base = TripConfig(
        weights=Weights.active(), eligible_tiers=("A",), min_destinations=1,
        max_destinations=2, start_date_step=7, vacation_days=18,
        outbound_context="tenerife", allowed_origins=("MAD",),
        **over,
    )
    return cheapest_config(base, min_score_per_day=6.0)


def test_cheapest_mode_sorts_by_total_cost():
    results = Optimizer(_cheap_base()).run(top_n=6)
    assert results
    costs = [i.total_cost_eur for i in results]
    assert costs == sorted(costs), costs


def test_a_single_destination_is_reachable_for_the_whole_trip():
    """Ein Ziel fuer 4-6 Wochen ist die guenstigste und entspannteste Variante.

    Vorher hat max_block_days (22) das verhindert, obwohl min_destinations=1
    erlaubt war - eine stille Fehlkonfiguration.
    """
    cfg = _cheap_base(min_days=35, max_days=35)
    assert cfg.max_block_days >= cfg.min_days
    results = Optimizer(cfg).run(top_n=10)
    singles = [i for i in results if len(i.blocks) == 1]
    assert singles, "keine Ein-Ziel-Route gefunden"
    best = singles[0]
    assert best.blocks[0].days == 35
    assert len(best.legs) == 2  # nur Hin- und Rueckflug
    # Und sie muss billiger sein als die beste Zwei-Ziel-Route derselben Laenge.
    doubles = [i for i in results if len(i.blocks) == 2]
    if doubles:
        assert best.total_cost_eur < min(d.total_cost_eur for d in doubles)


def test_min_score_per_day_filters_cheap_nonsense():
    loose = Optimizer(_cheap_base()).run(top_n=1)[0]
    strict_cfg = _cheap_base()
    import dataclasses

    strict_cfg = dataclasses.replace(strict_cfg, min_score_per_day=8.5)
    strict = Optimizer(strict_cfg).run(top_n=1)
    assert strict, "Schwelle 8.5 sollte noch erreichbar sein"
    assert strict[0].score_per_day >= 8.5
    assert strict[0].total_cost_eur >= loose.total_cost_eur


def test_budget_per_person_is_enforced():
    import dataclasses

    cfg = dataclasses.replace(
        _cheap_base(min_days=21, max_days=21), budget_per_person_eur=1400.0
    )
    for itin in Optimizer(cfg).run(top_n=5):
        assert itin.total_cost_eur / itin.travellers <= 1400.0


def test_measured_user_prices_replaced_the_estimates():
    """Die vom Nutzer gemessenen Preise muessen in den Daten stehen, nicht meine Schaetzung."""
    origins, _ = load_origins()
    assert origins["MAD"].access["tenerife"].price_eur_pp == 75.0   # 150 EUR Return
    assert origins["BER"].access["tenerife"].price_eur_pp == 100.0  # statt 220
    from workation.data import load_route_hints

    cgk = [
        e for e in load_route_hints()["longhaul"]
        if e["to"] == "CGK" and "MAD" in e["from"]
    ]
    assert cgk and cgk[0]["return_eur"] == 350.0


def test_living_costs_reflect_monthly_rates_for_a_couple():
    dests, _ = load_destinations()
    # Tagespreise fuer Touristen waeren 50-55; monatsweise fuer zwei Personen
    # deutlich weniger.
    assert dests["ID-LOMBOK"].cost_per_day_eur_pp <= 40
    assert dests["VN-NORTH"].cost_per_day_eur_pp <= 30
    assert dests["LK-SOUTH"].cost_per_day_eur_pp <= 40


def test_birthday_no_longer_loads_every_scenario():
    from workation.scenarios import PARTY_TRIP_EUR

    assert PARTY_TRIP_EUR == 0.0
    for key in ("montafon_direkt", "cottbus_bruecke", "heim_tfs", "hamburg_direkt"):
        assert SCENARIOS[key].post_trip_cost_eur == 0.0, key


def test_date_grid_respects_a_scenario_latest_start():
    """Ohne latest_start kann das Raster hinter das Abflugfenster laufen.

    Szenario A erlaubt nur 05.-07.03.; latest_end ergibt sich daraus als 17.04.,
    und daraus wiederum ein rechnerisch spaetester Start am 21.03. - zehn Tage
    nach dem, was das Szenario zulaesst.
    """
    base = TripConfig(weights=Weights.active(), eligible_tiers=("A",), max_destinations=2)
    cfg = SCENARIOS["montafon_direkt"].config(base)
    assert cfg.latest_start == dt.date(2027, 3, 7)
    assert max(cfg.date_grid()) <= dt.date(2027, 3, 7)
    assert min(cfg.date_grid()) == dt.date(2027, 3, 5)
