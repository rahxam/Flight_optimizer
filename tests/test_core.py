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


def test_work_window_ranks_destinations_by_evening_loss():
    dests, _ = load_destinations()
    win = WorkWindow(9.0, 16.0, flex_h=1.0)
    day = dt.date(2027, 4, 15)
    oman = overlap_score(dests["OM-OMAN"], day, win)
    sri = overlap_score(dests["LK-SOUTH"], day, win)
    lombok = overlap_score(dests["ID-LOMBOK"], day, win)
    assert oman == pytest.approx(sri)       # beide verlieren keinen Abend
    assert sri > lombok                      # Lombok kostet 2 h Abend
    assert 0 <= lombok <= 10


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
    assert daily_score(lombok, day, weights, win, vacation=True) == pytest.approx(
        daily_score(sumbawa, day, weights, win, vacation=True)
    )
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
    pb = PriceBook(quotes=[])
    direct, _ = pb.oneway("MAD", "LOP", dt.date(2027, 4, 7))
    # MAD->KUL (430) + KUL->LOP (120) + 40 Umsteigeaufschlag = 590 < 620 Direkt-Hint
    assert direct == pytest.approx(590.0)


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
        start_date_step=7,
        max_destinations=2,
        allowed_origins=("MAD",),
        ticket_strategies=("self_transfer",),
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
    """Die saisonale Kernaussage: Südküste zuerst, Lombok danach."""
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
