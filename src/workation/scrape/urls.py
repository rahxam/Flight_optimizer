"""Google-Flights-URLs bauen - inklusive Multi-City.

Google Flights kodiert die Suche im Query-Parameter ``tfs``: ein Protobuf,
base64url-kodiert. Das Schema ist nicht dokumentiert, sondern reverse-engineered
(gleiche Felder wie in der fast-flights-Bibliothek):

    Airport    { int32 kind        = 1   # 1=airport, 2=city, 3=place
                 string name       = 2 }  # IATA code or Freebase id (/m/...)
    FlightData { string date       = 2
                 repeated Airport from = 13   # several = "from any of these"
                 repeated Airport to   = 14 }
    Info       { repeated FlightData data = 3
                 repeated int32 passengers = 8   # 1=Erwachsener
                 int32 seat                = 9   # 1=Economy .. 4=First
                 int32 trip                = 19  # 1=Round, 2=Oneway, 3=Multicity
               }

Ein Leg darf mehrere Abflug- und Zielorte haben (``"MUC+FRA+TENERIFE"``) -
so sucht Google Flights selbst den guenstigsten Ein- und Ausstieg. Benannte
Orte stehen in ``PLACES``; die Kennungen stammen aus einer HAR-Aufnahme der
Google-Flights-Oberflaeche (Oktober 2026).

Weil das Schema jederzeit brechen kann, liefert jede Funktion zusaetzlich eine
``q=``-URL (natuerlichsprachige Suche) als Fallback - die ist stabil, kann aber
kein Multi-City.
"""

from __future__ import annotations

import base64
import datetime as dt
import urllib.parse

BASE = "https://www.google.com/travel/flights"

SEAT_CLASSES = {"economy": 1, "premium": 2, "business": 3, "first": 4}
TRIP_ROUND, TRIP_ONEWAY, TRIP_MULTICITY = 1, 2, 3

KIND_AIRPORT, KIND_CITY, KIND_PLACE = 1, 2, 3

# Named places (cities, islands) that cover several airports. Freebase ids and
# kinds as Google Flights sends them; captured from the UI in October 2026.
PLACES: dict[str, tuple[str, int]] = {
    "TENERIFE": ("/m/01nqb1", KIND_CITY),      # TFN + TFS
    "BERLIN": ("/m/0156q", KIND_CITY),
    "HAMBURG": ("/m/03hrz", KIND_CITY),
    "JAKARTA": ("/m/044rv", KIND_PLACE),
    "KATHMANDU": ("/m/04cx5", KIND_PLACE),
    "POKHARA": ("/m/040dx3", KIND_PLACE),
    "COLOMBO": ("/m/0fn7r", KIND_PLACE),
    "LOMBOK": ("/m/04nd9", KIND_PLACE),
    "TAIPEI": ("/m/0ftkx", KIND_PLACE),
    "KUALA_LUMPUR": ("/m/049d1", KIND_PLACE),
}
PLACE_NAMES = {mid: name for name, (mid, _) in PLACES.items()}

PLACE_SEPARATOR = "+"


# --------------------------------------------------------------------------- #
# Minimaler Protobuf-Writer (nur varint + length-delimited)
# --------------------------------------------------------------------------- #
def _varint(value: int) -> bytes:
    out = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def _tag(field: int, wire: int) -> bytes:
    return _varint((field << 3) | wire)


def _varint_field(field: int, value: int) -> bytes:
    return _tag(field, 0) + _varint(value)


def _bytes_field(field: int, payload: bytes) -> bytes:
    return _tag(field, 2) + _varint(len(payload)) + payload


def _string_field(field: int, value: str) -> bytes:
    return _bytes_field(field, value.encode("utf-8"))


def resolve_place(token: str) -> tuple[str, int]:
    """'MUC' -> airport, 'TENERIFE' -> named place, '/m/...' -> raw Freebase id."""
    token = token.strip()
    if token.startswith("/m/") or token.startswith("/g/"):
        return token, KIND_PLACE
    upper = token.upper()
    if upper in PLACES:
        return PLACES[upper]
    if len(upper) == 3 and upper.isalpha():
        return upper, KIND_AIRPORT
    raise ValueError(f"unknown place {token!r} - IATA code, PLACES key or /m/ id expected")


def split_places(spec: str | list[str] | tuple[str, ...]) -> list[str]:
    """'MUC+FRA' or ['MUC', 'FRA'] -> ['MUC', 'FRA']."""
    if isinstance(spec, str):
        return [t for t in spec.split(PLACE_SEPARATOR) if t.strip()]
    return list(spec)


def _airport(token: str) -> bytes:
    code, kind = resolve_place(token)
    return _varint_field(1, kind) + _string_field(2, code)


def _flight_data(origin, destination, day: dt.date) -> bytes:
    return (
        _string_field(2, day.isoformat())
        + b"".join(_bytes_field(13, _airport(t)) for t in split_places(origin))
        + b"".join(_bytes_field(14, _airport(t)) for t in split_places(destination))
    )


def _encode_tfs(
    legs: list[tuple[str, str, dt.date]],
    trip: int,
    adults: int = 1,
    seat: str = "economy",
) -> str:
    payload = b"".join(_bytes_field(3, _flight_data(o, d, day)) for o, d, day in legs)
    payload += b"".join(_varint_field(8, 1) for _ in range(adults))
    payload += _varint_field(9, SEAT_CLASSES.get(seat, 1))
    payload += _varint_field(19, trip)
    return base64.urlsafe_b64encode(payload).decode("ascii").rstrip("=")


# --------------------------------------------------------------------------- #
# Oeffentliche API
# --------------------------------------------------------------------------- #
def google_flights_url(
    legs: list[tuple[str, str, dt.date]],
    trip: int,
    adults: int = 2,
    seat: str = "economy",
    currency: str = "EUR",
    hl: str = "de",
    gl: str = "ES",
) -> str:
    params = {
        "tfs": _encode_tfs(legs, trip, adults, seat),
        "hl": hl,
        "gl": gl,
        "curr": currency,
    }
    return f"{BASE}?{urllib.parse.urlencode(params)}"


def oneway_url(origin: str, destination: str, day: dt.date, adults: int = 2, **kw) -> str:
    return google_flights_url([(origin, destination, day)], TRIP_ONEWAY, adults, **kw)


def roundtrip_url(
    origin: str, destination: str, out: dt.date, back: dt.date, adults: int = 2, **kw
) -> str:
    legs = [(origin, destination, out), (destination, origin, back)]
    return google_flights_url(legs, TRIP_ROUND, adults, **kw)


def multicity_url(legs: list[tuple[str, str, dt.date]], adults: int = 2, **kw) -> str:
    """Multi-City, z.B. [(MAD,CMB,18.03.), (CMB,LOP,10.04.), (LOP,MAD,28.04.)]."""
    if len(legs) < 2:
        raise ValueError("Multi-City braucht mindestens zwei Legs")
    return google_flights_url(legs, TRIP_MULTICITY, adults, **kw)


def fallback_query_url(
    origin: str, destination: str, day: dt.date, back: dt.date | None = None
) -> str:
    """Stabile, aber einfachere ``q=``-Suche (kein Multi-City)."""
    if back:
        q = f"Fluege von {origin} nach {destination} am {day:%Y-%m-%d} zurueck {back:%Y-%m-%d}"
    else:
        q = f"Fluege von {origin} nach {destination} am {day:%Y-%m-%d} oneway"
    return f"{BASE}?{urllib.parse.urlencode({'q': q, 'curr': 'EUR', 'hl': 'de'})}"
