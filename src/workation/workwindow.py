"""Arbeitszeitfenster: was die 09:00-16:00-Pflicht vor Ort bedeutet.

Die Arbeitszeit ist in deutscher/oesterreichischer Zeit vorgegeben (CET, ab
28.03.2027 CEST) - dieselbe Zone wie Madrid. Entscheidend fuer eine Workation ist
nicht der Zeitversatz als Zahl, sondern WOHIN das Fenster vor Ort faellt:

    Sri Lanka  (+3,5 h im Sommer)  ->  12:30-19:30  Morgen frei, Abend knapp
    Lombok     (+6 h im Sommer)    ->  15:00-22:00  Morgen lang frei, Abend weg
    Oman       (+2 h im Sommer)    ->  11:00-18:00  nahezu europaeischer Alltag

Ein langer freier Morgen ist fuer Surfer ein Gewinn, nicht nur ein Trost: die
offshore-Vormittage in Lombok und Sri Lanka liegen genau dort. Der Preis sind die
Abende. Das Modell bewertet beides getrennt.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

from .models import Destination

# EU-Sommerzeit 2027 beginnt am 28.03.
DST_START = dt.date(2027, 3, 28)

# Bewertungsparameter (Score-Punkte je Stunde)
EVENING_FROM = 19.0       # ab hier gilt der Abend als verloren
NIGHT_FROM = 22.0         # ab hier ist es Nachtarbeit
MORNING_FROM = 6.0        # ab wann ein freier Morgen zaehlt
PENALTY_EVENING = 1.5
PENALTY_NIGHT = 0.8       # zusaetzlich zur Abendstrafe
PENALTY_EARLY = 1.2       # Arbeitsbeginn vor 07:00 lokal
EARLY_BEFORE = 7.0
BONUS_MORNING = 0.4
BONUS_MORNING_CAP_H = 3.0


@dataclass(frozen=True)
class WorkWindow:
    """Pflicht-Arbeitszeit in der Heimatzone (CET/CEST)."""

    start_h: float = 9.0
    end_h: float = 16.0
    flex_h: float = 1.0  # wie weit das Fenster verschoben werden darf

    @property
    def hours(self) -> float:
        return self.end_h - self.start_h


def utc_offset_vs_home(dest: Destination, day: dt.date) -> float:
    """Stunden, die das Ziel der Heimatzone voraus ist (DST-bereinigt)."""
    offset = dest.tz_offset_vs_madrid_winter
    if day >= DST_START:
        offset -= 1.0
    return offset


def local_window(dest: Destination, day: dt.date, window: WorkWindow, shift: float = 0.0) -> tuple[float, float]:
    """Das Arbeitsfenster in Ortszeit, optional um `shift` Stunden verschoben."""
    offset = utc_offset_vs_home(dest, day)
    return window.start_h + shift + offset, window.end_h + shift + offset


def _score_for_shift(start: float, end: float) -> float:
    score = 10.0
    evening = max(0.0, end - EVENING_FROM) - max(0.0, start - EVENING_FROM)
    score -= PENALTY_EVENING * evening
    night = max(0.0, end - NIGHT_FROM) - max(0.0, start - NIGHT_FROM)
    score -= PENALTY_NIGHT * night
    early = max(0.0, EARLY_BEFORE - start) - max(0.0, EARLY_BEFORE - end)
    score -= PENALTY_EARLY * early
    free_morning = min(max(0.0, start - MORNING_FROM), BONUS_MORNING_CAP_H)
    score += BONUS_MORNING * free_morning
    return max(0.0, min(10.0, score))


def overlap_score(dest: Destination, day: dt.date, window: WorkWindow) -> float:
    """0-10, hoeher = besser. Nutzt die beste erlaubte Verschiebung des Fensters."""
    best = 0.0
    steps = int(window.flex_h * 2)
    for i in range(-steps, steps + 1):
        shift = i * 0.5
        start, end = local_window(dest, day, window, shift)
        best = max(best, _score_for_shift(start, end))
    return best


def best_shift(dest: Destination, day: dt.date, window: WorkWindow) -> float:
    """Die Fensterverschiebung (in Stunden Heimatzeit), die am besten passt."""
    best, best_shift_h = -1.0, 0.0
    steps = int(window.flex_h * 2)
    for i in range(-steps, steps + 1):
        shift = i * 0.5
        start, end = local_window(dest, day, window, shift)
        score = _score_for_shift(start, end)
        if score > best:
            best, best_shift_h = score, shift
    return best_shift_h


def _hhmm(value: float) -> str:
    value %= 24.0
    hours = int(value)
    minutes = int(round((value - hours) * 60))
    if minutes == 60:
        hours, minutes = hours + 1, 0
    return f"{hours:02d}:{minutes:02d}"


def describe(dest: Destination, day: dt.date, window: WorkWindow) -> str:
    """Menschenlesbare Zeile fuer den Report."""
    shift = best_shift(dest, day, window)
    start, end = local_window(dest, day, window, shift)
    offset = utc_offset_vs_home(dest, day)
    home = (
        f"{_hhmm(window.start_h + shift)}-{_hhmm(window.end_h + shift)}"
        if shift
        else f"{_hhmm(window.start_h)}-{_hhmm(window.end_h)}"
    )
    free_morning = max(0.0, start - MORNING_FROM)
    evening_lost = max(0.0, end - EVENING_FROM)
    bits = [f"{home} CET = {_hhmm(start)}-{_hhmm(end)} vor Ort (+{offset:.1f} h)"]
    if free_morning >= 1:
        bits.append(f"{free_morning:.1f} h freier Morgen")
    if evening_lost >= 0.5:
        bits.append(f"{evening_lost:.1f} h Abend weg")
    if shift:
        bits.append(f"Fenster um {shift:+.1f} h verschoben")
    return "; ".join(bits)
