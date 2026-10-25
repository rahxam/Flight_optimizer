"""Datenmodelle fuer Ziele, Fluege und Routen."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

Date = dt.date


# --------------------------------------------------------------------------- #
# Stammdaten
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class WindowScore:
    """Saisonbewertung eines Ziels fuer ein Halbmonats-Fenster. 0-10, hoeher = besser."""

    weather: float
    surf: float
    calm: float
    note: str = ""


@dataclass
class Destination:
    id: str
    name: str
    country: str
    region_short: str
    tier: str
    airports: list[str]
    primary_airport: str
    tropical: bool
    work: float
    tz_offset_vs_madrid_winter: float
    cost_per_day_eur_pp: float
    activities: list[str]
    hub_to_base_h: float
    scores: dict[str, WindowScore]
    notes: str = ""
    hard_avoid_windows: frozenset[str] = frozenset()
    hard_avoid_reason: str = ""
    avoid_date_ranges: list[tuple[Date, Date]] = field(default_factory=list)
    avoid_date_reason: str = ""

    def blocked_on(self, day: Date) -> str | None:
        """Grund, warum dieser Tag an diesem Ziel ausgeschlossen ist - oder None."""
        for start, end in self.avoid_date_ranges:
            if start <= day <= end:
                return self.avoid_date_reason or "Sperrfenster"
        return None


@dataclass(frozen=True)
class Access:
    """Wie man einen Abflughafen aus einem bestimmten Startkontext erreicht."""

    context: str  # montafon | cottbus | hamburg | tenerife
    mode: str  # train | flight | local
    hours: float
    price_eur_pp: float
    residencia_discount: bool = False
    min_connect_h: float = 3.0
    company_covered_travellers: int = 0
    note: str = ""

    def total_price(self, travellers: int) -> float:
        """Gesamtpreis fuer alle Reisenden; von der Firma bezahlte Tickets fallen raus."""
        paying = max(0, travellers - self.company_covered_travellers)
        return self.price_eur_pp * paying

    @property
    def full_fare_eur_pp(self) -> float:
        """Preis ohne Residentenrabatt - fuer den Vergleich mit einem Durchgangsticket."""
        return self.price_eur_pp / 0.25 if self.residencia_discount else self.price_eur_pp * 1.3


@dataclass
class OriginHub:
    """Ein Abflughafen plus die Wege dorthin."""

    id: str
    name: str
    role: str
    access: dict[str, Access]
    notes: str = ""

    def reachable_from(self, context: str) -> bool:
        return context in self.access


@dataclass(frozen=True)
class CalendarEvent:
    id: str
    name: str
    start: Date
    end: Date
    affects: tuple[str, ...]
    impact: str
    note: str
    confidence: str

    def overlaps(self, start: Date, end: Date) -> bool:
        return self.start <= end and start <= self.end


# --------------------------------------------------------------------------- #
# Preise
# --------------------------------------------------------------------------- #
@dataclass
class PriceQuote:
    """Ein Flugpreis fuer eine Strecke an einem Datum (pro Person)."""

    origin: str
    destination: str
    depart_date: Date
    price_eur: float
    trip_type: str = "oneway"  # oneway | return | multicity_leg
    return_date: Date | None = None
    carrier: str = ""
    stops: int | None = None
    duration_min: int | None = None
    source: str = "estimate"  # google_flights | manual | estimate
    url: str = ""
    itinerary_id: str = ""  # fuer Multi-City-Scrapes: gruppiert Legs
    leg_index: int = 0

    @property
    def is_estimate(self) -> bool:
        return self.source == "estimate"


@dataclass
class Leg:
    """Eine geflogene Strecke in einer konkreten Route."""

    origin: str
    destination: str
    date: Date
    price_eur: float
    kind: str  # feeder | outbound | inter | return
    source: str = "estimate"
    carrier: str = ""
    note: str = ""


# --------------------------------------------------------------------------- #
# Ergebnis
# --------------------------------------------------------------------------- #
@dataclass
class Block:
    """Ein Aufenthalt an einem Ziel."""

    destination: Destination
    start: Date
    end: Date  # inklusiv
    vacation_days: int = 0

    @property
    def nights(self) -> int:
        return (self.end - self.start).days

    @property
    def days(self) -> int:
        return (self.end - self.start).days + 1

    @property
    def work_days(self) -> int:
        return self.days - self.vacation_days


@dataclass
class Itinerary:
    blocks: list[Block]
    legs: list[Leg]
    origin_hub: str
    ticket_strategy: str  # separate_tickets | through_ticket
    travellers: int
    flight_cost_eur: float
    ground_cost_eur: float
    visa_cost_eur: float
    baggage_cost_eur: float
    experience_score: float  # gewichtete Summe ueber alle Tage, hoeher = besser
    objective_eur: float  # Gesamtkosten minus monetarisierter Erlebniswert
    objective_per_day_eur: float = 0.0  # dasselbe pro Reisetag - laengenneutral
    good_surf_days: int = 0  # Tage mit interpoliertem Surf-Score >= 6
    outbound_context: str = "tenerife"
    return_hub: str = ""
    vacation_days: int = 0
    warnings: list[str] = field(default_factory=list)
    estimated_share: float = 1.0  # Anteil der Flugkosten, der auf Schaetzungen beruht

    @property
    def start(self) -> Date:
        return self.blocks[0].start

    @property
    def end(self) -> Date:
        return self.blocks[-1].end

    @property
    def total_days(self) -> int:
        return (self.end - self.start).days + 1

    @property
    def total_cost_eur(self) -> float:
        return (
            self.flight_cost_eur
            + self.ground_cost_eur
            + self.visa_cost_eur
            + self.baggage_cost_eur
        )

    @property
    def score_per_day(self) -> float:
        return self.experience_score / self.total_days

    @property
    def cost_per_day_eur(self) -> float:
        return self.total_cost_eur / self.total_days

    @property
    def label(self) -> str:
        return " -> ".join(b.destination.region_short for b in self.blocks)
