"""Parse Google Flights' internal RPC traffic into price rows.

The Flights UI talks to ``FlightsFrontendService`` over form-encoded POSTs
(``f.req``) and answers with a chunked JSON stream. Four calls carry prices:

    GetShoppingResults  flight list for one search (offers with carrier,
                        stops, duration and the airports actually used)
    GetCalendarGraph    "Preisgrafik": cheapest price per departure day over
                        ~60 days, for a fixed trip length
    GetCalendarGrid     "Datumsraster": departure x return matrix (7 x 7)
    GetCalendarPicker   prices shown in the date picker

Requests cannot be replayed outside the browser: every call carries a
BotGuard token (``x-goog-batchexecute-bgr``) bound to the request body. So the
scraper lets the page make the calls and records them; this module only
reads what was recorded - from the scraper's JSONL capture or from a HAR file
exported in a normal browser.

All prices in the responses are totals for all passengers. Rows written here
carry the price per person, as the CSV schema in ``prices.py`` requires.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator

from .urls import PLACE_NAMES, PLACE_SEPARATOR

SERVICE = "FlightsFrontendService"
SHOPPING = "GetShoppingResults"
CALENDAR_CALLS = {
    "GetCalendarGraph": "google_flights_graph",
    "GetCalendarGrid": "google_flights_grid",
    "GetCalendarPicker": "google_flights_picker",
}
PRICED_CALLS = {SHOPPING, *CALENDAR_CALLS}

TRIP_TYPES = {1: "return", 2: "oneway", 3: "multicity"}


# --------------------------------------------------------------------------- #
# Wire format
# --------------------------------------------------------------------------- #
def rpc_name(url: str) -> str:
    return urllib.parse.urlparse(url).path.rsplit("/", 1)[-1]


def is_priced_call(url: str) -> bool:
    return SERVICE in url and rpc_name(url) in PRICED_CALLS


def decode_stream(text: str) -> list:
    """Split the ``)]}'`` + length-prefixed chunk stream into JSON values.

    The length prefixes count UTF-16 units, so they are not used to slice;
    each chunk is read with ``raw_decode`` instead.
    """
    if text.startswith(")]}'"):
        text = text[4:]
    decoder = json.JSONDecoder()
    chunks, pos, n = [], 0, len(text)
    while pos < n:
        while pos < n and text[pos] in " \r\n":
            pos += 1
        if pos >= n:
            break
        newline = text.find("\n", pos)
        if newline < 0 or not text[pos:newline].strip().isdigit():
            break
        value, pos = decoder.raw_decode(text, newline + 1)
        chunks.append(value)
    return chunks


def payloads(text: str) -> list:
    """The decoded ``wrb.fr`` payloads of a response (empty ones skipped)."""
    out = []
    for chunk in decode_stream(text):
        for item in chunk if isinstance(chunk, list) else []:
            if isinstance(item, list) and len(item) > 2 and item[0] == "wrb.fr" and item[2]:
                out.append(json.loads(item[2]))
    return out


def error_code(text: str) -> int | None:
    """Google's error code if the call was rejected (13 = BotGuard said no)."""
    for chunk in decode_stream(text):
        for item in chunk if isinstance(chunk, list) else []:
            if (
                isinstance(item, list) and len(item) > 5 and item[0] == "wrb.fr"
                and not item[2] and isinstance(item[5], list) and item[5]
            ):
                return item[5][0]
    return None


# --------------------------------------------------------------------------- #
# Request: what was searched
# --------------------------------------------------------------------------- #
@dataclass
class SearchLeg:
    origins: list[str]
    destinations: list[str]
    date: str = ""


@dataclass
class SearchRequest:
    trip_type: str
    adults: int
    legs: list[SearchLeg] = field(default_factory=list)


def _place_list(raw) -> list[str]:
    # [[["MUC", 0], ["/m/0156q", 4]]] -> ["MUC", "/m/0156q"]
    try:
        return [p[0] for p in raw[0] if p and isinstance(p[0], str)]
    except (TypeError, IndexError):
        return []


def parse_request(body: str) -> SearchRequest | None:
    form = urllib.parse.parse_qs(body or "")
    if "f.req" not in form:
        return None
    try:
        inner = json.loads(json.loads(form["f.req"][0])[1])
        spec = inner[1]
    except (ValueError, TypeError, IndexError):
        return None
    passengers = spec[6] if len(spec) > 6 and spec[6] else [1]
    legs = []
    for raw in (spec[13] if len(spec) > 13 and spec[13] else []):
        legs.append(
            SearchLeg(
                origins=_place_list(raw[0]),
                destinations=_place_list(raw[1]),
                date=raw[6] if len(raw) > 6 and isinstance(raw[6], str) else "",
            )
        )
    trip_type = TRIP_TYPES.get(spec[2], "oneway")
    if trip_type == "multicity" and len(legs) == 1:
        trip_type = "oneway"  # the UI sends 3 for a multi-city form with one leg left
    return SearchRequest(
        trip_type=trip_type,
        adults=max(int(passengers[0] or 1), 1),
        legs=legs,
    )


def place_label(codes: list[str]) -> str:
    """['MUC', '/m/01nqb1'] -> 'MUC+TENERIFE' - readable and stable as a key."""
    return PLACE_SEPARATOR.join(PLACE_NAMES.get(c, c) for c in codes)


# --------------------------------------------------------------------------- #
# Responses
# --------------------------------------------------------------------------- #
@dataclass
class Offer:
    price_total: float
    carrier: str
    origin: str
    destination: str
    depart_date: str
    stops: int
    duration_min: int | None
    flights: str


def _iso(parts) -> str:
    try:
        return dt.date(*parts[:3]).isoformat()
    except (TypeError, ValueError):
        return ""


def _offer(item) -> Offer | None:
    try:
        info, fare = item[0], item[1]
        price = fare[0][1] if fare and fare[0] else None
    except (TypeError, IndexError):
        return None
    if not price or not isinstance(info, list) or len(info) < 10:
        return None
    segments = info[2] or []
    numbers = [f"{s[22][0]}{s[22][1]}" for s in segments if len(s) > 22 and s[22]]
    return Offer(
        price_total=float(price),
        carrier=info[0] or "",
        origin=info[3] or "",
        destination=info[6] or "",
        depart_date=_iso(info[4]) if info[4] else "",
        stops=max(len(segments) - 1, 0),
        duration_min=info[9] if isinstance(info[9], int) else None,
        flights="|".join(numbers),
    )


def shopping_offers(text: str) -> list[Offer]:
    """All distinct offers of a GetShoppingResults stream.

    Slots 2 and 3 of each payload hold the "best" and the "other" flights; the
    stream repeats them as results come in, so offers are deduplicated by
    flight numbers and price.
    """
    seen: dict[tuple, Offer] = {}
    for payload in payloads(text):
        for slot in (2, 3):
            block = payload[slot] if len(payload) > slot else None
            if not block or not block[0]:
                continue
            for item in block[0]:
                offer = _offer(item)
                if offer:
                    seen.setdefault((offer.flights, offer.origin, offer.price_total), offer)
    return sorted(seen.values(), key=lambda o: o.price_total)


def calendar_prices(text: str) -> list[tuple[str, str, float]]:
    """(depart, return or '', total price) per day from any calendar call."""
    cells: dict[tuple[str, str], float] = {}
    for payload in payloads(text):
        for cell in (payload[1] if len(payload) > 1 and payload[1] else []):
            try:
                depart, back, price = cell[0], cell[1] or "", cell[2][0][1]
            except (TypeError, IndexError):
                continue
            if depart and price:
                cells[(depart, back)] = float(price)
    return [(d, r, p) for (d, r), p in sorted(cells.items())]


# --------------------------------------------------------------------------- #
# Exchange -> CSV rows (schema of prices.py plus scraped_at)
# --------------------------------------------------------------------------- #
def _row(**kw) -> dict:
    row = {
        "origin": "", "destination": "", "depart_date": "", "return_date": "",
        "trip_type": "oneway", "price_eur": "", "carrier": "", "stops": "",
        "duration_min": "", "source": "", "url": "", "itinerary_id": "",
        "leg_index": 0, "scraped_at": "",
    }
    row.update(kw)
    return row


def rows_from_exchange(
    url: str,
    request_body: str,
    response_text: str,
    scraped_at: str,
    query_id: str = "",
    page_url: str = "",
    max_offers: int = 10,
) -> list[dict]:
    """Turn one recorded RPC call into price rows (price per person)."""
    name = rpc_name(url)
    request = parse_request(request_body)
    if name not in PRICED_CALLS or not request or not request.legs or not response_text:
        return []
    adults = request.adults
    first, last = request.legs[0], request.legs[-1]
    common = {"scraped_at": scraped_at, "url": page_url}

    if name in CALENDAR_CALLS:
        if request.trip_type == "multicity":
            return []  # calendar prices of multi-city searches have no clear route key
        return [
            _row(
                origin=place_label(first.origins),
                destination=place_label(first.destinations),
                depart_date=depart,
                return_date=back if request.trip_type == "return" else "",
                trip_type=request.trip_type,
                price_eur=round(total / adults, 2),
                source=CALENDAR_CALLS[name],
                itinerary_id=query_id,
                **common,
            )
            for depart, back, total in calendar_prices(response_text)
        ]

    rows = []
    for n, offer in enumerate(shopping_offers(response_text)[:max_offers]):
        per_person = round(offer.price_total / adults, 2)
        base = dict(
            carrier=offer.carrier, stops=offer.stops,
            duration_min=offer.duration_min if offer.duration_min is not None else "",
            source="google_flights_rpc", **common,
        )
        if request.trip_type == "multicity":
            # Price is for the whole ticket; it goes on leg 0, the other legs
            # are listed with 0 so prices.PriceBook can match the itinerary.
            key = query_id or hashlib.sha1(request_body.encode()).hexdigest()[:8]
            itin = f"{key}-{n}"
            rows.append(_row(
                origin=offer.origin, destination=offer.destination,
                depart_date=offer.depart_date or first.date, trip_type="multicity_leg",
                price_eur=per_person, itinerary_id=itin, leg_index=0, **base,
            ))
            for i, leg in enumerate(request.legs[1:], start=1):
                rows.append(_row(
                    origin=place_label(leg.origins), destination=place_label(leg.destinations),
                    depart_date=leg.date, trip_type="multicity_leg", price_eur=0,
                    itinerary_id=itin, leg_index=i, scraped_at=scraped_at, url=page_url,
                    source="google_flights_rpc",
                ))
            continue
        rows.append(_row(
            origin=offer.origin, destination=offer.destination,
            depart_date=offer.depart_date or first.date,
            return_date=last.date if request.trip_type == "return" else "",
            trip_type=request.trip_type, price_eur=per_person,
            itinerary_id=query_id, leg_index=n, **base,
        ))
    return rows


# --------------------------------------------------------------------------- #
# Sources: scraper capture (JSONL) and browser HAR export
# --------------------------------------------------------------------------- #
@dataclass
class Exchange:
    url: str
    request_body: str
    response_text: str
    scraped_at: str
    query_id: str = ""
    page_url: str = ""


def _utc_stamp(value: str) -> str:
    try:
        stamp = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value
    return stamp.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def exchanges_from_har(path: Path) -> Iterator[Exchange]:
    with open(path, encoding="utf-8") as fh:
        har = json.load(fh)
    for entry in har.get("log", {}).get("entries", []):
        request = entry.get("request", {})
        url = request.get("url", "")
        if not is_priced_call(url):
            continue
        referer = next(
            (h["value"] for h in request.get("headers", []) if h.get("name", "").lower() == "referer"),
            "",
        )
        yield Exchange(
            url=url,
            request_body=(request.get("postData") or {}).get("text", ""),
            response_text=(entry.get("response", {}).get("content") or {}).get("text", "") or "",
            scraped_at=_utc_stamp(entry.get("startedDateTime", "")),
            page_url=referer,
        )


def exchanges_from_capture(path: Path) -> Iterator[Exchange]:
    """JSONL written by scripts/scrape_google_flights.cjs, one call per line."""
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            yield Exchange(
                url=rec["url"],
                request_body=rec.get("request_body", ""),
                response_text=rec.get("response", ""),
                scraped_at=rec.get("scraped_at", ""),
                query_id=rec.get("query_id", ""),
                page_url=rec.get("page_url", ""),
            )


def rows_from_exchanges(exchanges: Iterable[Exchange]) -> list[dict]:
    rows = []
    for ex in exchanges:
        rows += rows_from_exchange(
            ex.url, ex.request_body, ex.response_text, ex.scraped_at, ex.query_id, ex.page_url
        )
    return rows
