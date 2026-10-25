"""Tests fuer Saison-Scoring, Preise, Optimierer und URL-Kodierung."""

from __future__ import annotations

import base64
import datetime as dt
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from workation.data import load_calendar, load_destinations, load_origins  # noqa: E402
from workation.optimizer import Optimizer, TripConfig  # noqa: E402
from workation.prices import PriceBook  # noqa: E402
from workation.scrape.queries import grid_queries  # noqa: E402
from workation.scrape.urls import multicity_url, oneway_url  # noqa: E402
from workation.seasonality import (  # noqa: E402
    Weights,
    daily_score,
    interpolated_scores,
    is_available,
    window_of,
)


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


def test_dst_shift_reduces_timezone_penalty():
    dests, _ = load_destinations()
    lombok = dests["ID-LOMBOK"]
    # Nur der Work-Anteil, damit sich der Saison-Verlauf nicht ueberlagert; der
    # Basiswert muss positiv sein, weil daily_score bei 0 abschneidet.
    weights = Weights(weather=0.0, surf=0.0, calm=0.0, work=1.0, tropical_bonus=0.0)
    before = daily_score(lombok, dt.date(2027, 3, 27), weights)
    after = daily_score(lombok, dt.date(2027, 3, 28), weights)
    assert before > 0
    assert after == pytest.approx(before + weights.tz_penalty_per_hour)


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
