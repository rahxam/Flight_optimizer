"""Google Flights RPC parsing, multi-place URLs and the calendar query matrix.

The fixtures are trimmed calls from a HAR recording of the Google Flights UI
(October 2026): images, extra result slots and the XSRF token removed.
"""

from __future__ import annotations

import base64
import datetime as dt
import json
import sys
import urllib.parse
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from workation import history  # noqa: E402
from workation.scrape import gf_rpc  # noqa: E402
from workation.scrape.queries import Query, calendar_queries, discovery_queries  # noqa: E402
from workation.scrape.urls import (  # noqa: E402
    KIND_AIRPORT,
    KIND_CITY,
    KIND_PLACE,
    oneway_url,
    resolve_place,
)

FIXTURES = json.loads(
    (Path(__file__).parent / "fixtures" / "gf_rpc_har_excerpt.json").read_text(encoding="utf-8")
)


def _fixture(label: str) -> dict:
    return next(f for f in FIXTURES if f["label"] == label)


def _rows(label: str) -> list[dict]:
    f = _fixture(label)
    return gf_rpc.rows_from_exchange(f["url"], f["request_body"], f["response"], "2026-10-26T05:30:00Z")


# --------------------------------------------------------------------------- #
# Requests
# --------------------------------------------------------------------------- #
def test_request_parsing_reads_trip_passengers_and_place_lists():
    req = gf_rpc.parse_request(_fixture("shopping_multicity_3legs_2pax")["request_body"])
    assert req.trip_type == "multicity"
    assert req.adults == 2
    assert [leg.date for leg in req.legs] == ["2026-11-05", "2026-11-09", "2026-11-13"]
    assert req.legs[0].origins == ["/m/01nqb1"]
    assert "CGK" in req.legs[0].destinations and "/m/0fn7r" in req.legs[0].destinations
    assert req.legs[2].origins == ["BKK"]


def test_single_leg_multicity_form_counts_as_oneway():
    req = gf_rpc.parse_request(_fixture("shopping_oneway_multi_place_2pax")["request_body"])
    assert req.trip_type == "oneway"
    assert len(req.legs) == 1


def test_place_labels_use_names_for_known_freebase_ids():
    assert gf_rpc.place_label(["/m/01nqb1", "MUC", "/m/0156q"]) == "TENERIFE+MUC+BERLIN"
    assert gf_rpc.place_label(["/m/unknown"]) == "/m/unknown"


# --------------------------------------------------------------------------- #
# Responses
# --------------------------------------------------------------------------- #
def test_shopping_results_give_airports_carrier_stops_and_per_person_price():
    rows = _rows("shopping_oneway_multi_place_2pax")
    assert rows
    cheapest = rows[0]
    # Searched "any of 5 origins -> any of 7 places"; the row names what Google picked.
    assert len(cheapest["origin"]) == 3 and len(cheapest["destination"]) == 3
    assert cheapest["trip_type"] == "oneway"
    assert cheapest["price_eur"] == 635 / 2  # response holds the total for 2 adults
    assert isinstance(cheapest["stops"], int)
    assert cheapest["duration_min"] > 0
    assert [r["price_eur"] for r in rows] == sorted(r["price_eur"] for r in rows)


def test_return_shopping_rows_carry_the_return_date():
    rows = _rows("shopping_return_multi_origin_1pax")
    assert {r["trip_type"] for r in rows} == {"return"}
    assert {r["return_date"] for r in rows} == {"2026-11-12"}
    assert rows[0]["price_eur"] == 660  # one adult: total == per person
    assert rows[0]["carrier"] == "EY"


def test_multicity_rows_put_the_ticket_price_on_leg_zero_only():
    rows = _rows("shopping_multicity_3legs_2pax")
    itineraries: dict[str, list[dict]] = {}
    for row in rows:
        itineraries.setdefault(row["itinerary_id"], []).append(row)
    for legs in itineraries.values():
        assert [r["leg_index"] for r in legs] == [0, 1, 2]
        assert legs[0]["price_eur"] > 0
        assert legs[1]["price_eur"] == 0 and legs[2]["price_eur"] == 0
        assert legs[2]["origin"] == "BKK"


@pytest.mark.parametrize(
    ("label", "source"),
    [
        ("graph_return_tenerife_cgk", "google_flights_graph"),
        ("grid_return_tenerife_cgk", "google_flights_grid"),
        ("picker_oneway_multi_origin", "google_flights_picker"),
    ],
)
def test_calendar_calls_give_one_row_per_day(label, source):
    rows = _rows(label)
    assert rows
    assert {r["source"] for r in rows} == {source}
    departs = [r["depart_date"] for r in rows]
    assert len(departs) == len(set((r["depart_date"], r["return_date"]) for r in rows))
    for r in rows:
        dt.date.fromisoformat(r["depart_date"])
        assert r["price_eur"] > 0


def test_calendar_rows_of_a_return_search_keep_trip_length():
    rows = _rows("graph_return_tenerife_cgk")
    for r in rows:
        length = dt.date.fromisoformat(r["return_date"]) - dt.date.fromisoformat(r["depart_date"])
        assert length.days == 7
    assert rows[0]["origin"] == "TENERIFE" and rows[0]["destination"] == "CGK"


def test_rejected_call_is_detected_and_yields_nothing():
    f = _fixture("rejected")
    assert gf_rpc.error_code(f["response"]) == 13
    assert gf_rpc.rows_from_exchange(f["url"], f["request_body"], f["response"], "x") == []
    assert gf_rpc.error_code(_fixture("graph_return_tenerife_cgk")["response"]) is None


def test_har_and_capture_ingest_into_history(tmp_path):
    har = {"log": {"entries": [
        {
            "startedDateTime": "2026-10-26T06:28:43.000+01:00",
            "request": {"url": f["url"] + "?rt=c", "postData": {"text": f["request_body"]},
                        "headers": [{"name": "Referer", "value": "https://www.google.com/travel/flights"}]},
            "response": {"content": {"text": f["response"]}},
        }
        for f in FIXTURES
    ] + [{"request": {"url": "https://www.google.com/log"}, "response": {"content": {}}}]}}
    har_path = tmp_path / "flights.har"
    har_path.write_text(json.dumps(har), encoding="utf-8")
    exchanges = list(gf_rpc.exchanges_from_har(har_path))
    assert len(exchanges) == len(FIXTURES)
    assert exchanges[0].scraped_at == "2026-10-26T05:28:43Z"

    db = tmp_path / "h.sqlite3"
    rows = gf_rpc.rows_from_exchanges(exchanges)
    first = history.ingest_rows(rows, db)
    # Zero-price follow-up legs are skipped; the same day at the same price from
    # two calendar views at the same moment is one observation.
    assert 0 < first <= sum(1 for r in rows if r["price_eur"] > 0)
    assert history.ingest_rows(rows, db) == 0  # idempotent

    capture = tmp_path / "run.rpc.jsonl"
    capture.write_text("\n".join(json.dumps({
        "url": f["url"], "request_body": f["request_body"], "response": f["response"],
        "scraped_at": "2026-10-27T05:00:00Z", "query_id": "k0001",
    }) for f in FIXTURES) + "\n", encoding="utf-8")
    rows = gf_rpc.rows_from_exchanges(gf_rpc.exchanges_from_capture(capture))
    assert {r["itinerary_id"] for r in rows if r["trip_type"] != "multicity_leg"} == {"k0001"}
    assert history.ingest_rows(rows, db) > 0


# --------------------------------------------------------------------------- #
# URLs with several places per leg
# --------------------------------------------------------------------------- #
def _fields(data: bytes) -> list[tuple[int, object]]:
    out, pos = [], 0
    while pos < len(data):
        key, pos = _varint(data, pos)
        field, wire = key >> 3, key & 7
        if wire == 0:
            value, pos = _varint(data, pos)
        else:
            length, pos = _varint(data, pos)
            value, pos = data[pos:pos + length], pos + length
        out.append((field, value))
    return out


def _varint(data: bytes, pos: int) -> tuple[int, int]:
    result = shift = 0
    while True:
        byte = data[pos]
        pos += 1
        result |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return result, pos
        shift += 7


def test_multi_place_leg_encodes_every_origin_with_its_kind():
    url = oneway_url("TENERIFE+MUC+BERLIN", "CMB+/m/04nd9", dt.date(2027, 3, 18))
    tfs = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)["tfs"][0]
    top = _fields(base64.urlsafe_b64decode(tfs + "=" * (-len(tfs) % 4)))
    leg = _fields(next(v for f, v in top if f == 3))
    origins = [dict(_fields(v)) for f, v in leg if f == 13]
    destinations = [dict(_fields(v)) for f, v in leg if f == 14]
    assert [(o[1], o[2]) for o in origins] == [
        (KIND_CITY, b"/m/01nqb1"), (KIND_AIRPORT, b"MUC"), (KIND_CITY, b"/m/0156q"),
    ]
    assert [(d[1], d[2]) for d in destinations] == [(KIND_AIRPORT, b"CMB"), (KIND_PLACE, b"/m/04nd9")]


def test_unknown_place_names_are_rejected():
    assert resolve_place("lombok") == ("/m/04nd9", KIND_PLACE)
    with pytest.raises(ValueError):
        resolve_place("ATLANTIS")


# --------------------------------------------------------------------------- #
# Calendar matrix
# --------------------------------------------------------------------------- #
def test_calendar_queries_cover_every_day_with_few_graph_searches():
    days = [dt.date(2027, 3, 1) + dt.timedelta(days=i) for i in range(70)]
    daily = [
        Query(id=f"s{i}", phase="scenario", trip_type="oneway",
              legs=[("MAD", "CMB", d.isoformat())])
        for i, d in enumerate(days)
    ] + [Query(id="c1", phase="candidates", trip_type="multicity",
               legs=[("MAD", "CMB", "2027-03-18"), ("CMB", "MAD", "2027-04-28")])]
    out = calendar_queries(daily)
    graphs = [q for q in out if q.calendar]
    assert len(graphs) == 2
    covered = set()
    for q in graphs:
        anchor = dt.date.fromisoformat(q.legs[0][2])
        covered |= {anchor + dt.timedelta(days=k) for k in range(-7, 53)}
    assert set(days) <= covered
    assert any(q.id == "c1" for q in out), "multi-city searches stay untouched"


def test_discovery_queries_search_all_places_at_once():
    out = discovery_queries(["MAD", "TENERIFE"], ["CMB", "LOP"])
    assert out[0].legs[0][:2] == ("MAD+TENERIFE", "CMB+LOP")
    assert out[1].legs[0][:2] == ("CMB+LOP", "MAD+TENERIFE")
    assert all(q.calendar and q.url for q in out)
    assert len(out) == 2 + 2
