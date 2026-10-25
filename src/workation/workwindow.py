"""Arbeitszeitfenster: was die 09:00-16:00-Pflicht vor Ort bedeutet.

Die Arbeitszeit ist in deutscher/oesterreichischer Zeit vorgegeben (CET, ab
28.03.2027 CEST) - dieselbe Zone wie Madrid. Entscheidend fuer eine Workation ist
nicht der Zeitversatz als Zahl, sondern WOHIN das Fenster vor Ort faellt:

    Oman       (+2 h im Sommer)    ->  11:00-18:00  kaum freier Vormittag
    Sri Lanka  (+3,5 h im Sommer)  ->  12:30-19:30  halber Vormittag frei
    Nordvietnam(+5 h im Sommer)    ->  14:00-21:00
    Lombok     (+6 h im Sommer)    ->  15:00-22:00  ganzer Vormittag frei

WICHTIG - das Modell bewertet einen SPAETEN lokalen Arbeitsbeginn als Vorteil,
nicht als Nachteil. Die Nutzer haben das drei Wochen praktisch getestet: erst
gegen 15 Uhr anzufangen und den ganzen Vormittag fuer eine Bootstour oder einen
Ausflug zu haben, war ein Gewinn - und besser als um 12:30 zu starten. Ein
Ganztagesausflug braucht einen ganzen Vormittag, kein halbes Zeitfenster.

Bewertet wird deshalb der Abstand zu einem bevorzugten lokalen Arbeitsbeginn
(`ideal_local_start_h`, Standard 14:30). Zu frueh kostet Vormittag und wird
moderat bestraft, zu spaet frisst den Abend und wird staerker bestraft; Arbeit
nach 23 Uhr zusaetzlich hart. Damit wird ein grosser Zeitversatz nach Osten zum
Vorteil, solange der Arbeitstag vor Mitternacht endet.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

from .models import Destination

# EU-Sommerzeit 2027 beginnt am 28.03.
DST_START = dt.date(2027, 3, 28)

# Bewertungsparameter (Score-Punkte je Stunde Abweichung)
PENALTY_TOO_EARLY = 0.5   # je Stunde, die der lokale Start vor dem Ideal liegt
PENALTY_TOO_LATE = 1.2    # je Stunde danach - der Abend ist knapper als der Morgen
NIGHT_FROM = 23.0         # Arbeit danach ist zusaetzlich teuer
PENALTY_NIGHT = 1.5
MORNING_FROM = 6.0        # ab hier zaehlt freie Vormittagszeit als nutzbar


@dataclass(frozen=True)
class WorkWindow:
    """Pflicht-Arbeitszeit in der Heimatzone (CET/CEST)."""

    start_h: float = 9.0
    end_h: float = 16.0
    flex_h: float = 1.0  # wie weit das Fenster verschoben werden darf
    ideal_local_start_h: float = 14.5  # bevorzugter lokaler Arbeitsbeginn

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


def _score_for_shift(start: float, end: float, ideal_start: float) -> float:
    score = 10.0
    if start < ideal_start:
        score -= PENALTY_TOO_EARLY * (ideal_start - start)
    else:
        score -= PENALTY_TOO_LATE * (start - ideal_start)
    night = max(0.0, end - NIGHT_FROM) - max(0.0, start - NIGHT_FROM)
    score -= PENALTY_NIGHT * night
    return max(0.0, min(10.0, score))


def overlap_score(dest: Destination, day: dt.date, window: WorkWindow) -> float:
    """0-10, hoeher = besser. Nutzt die beste erlaubte Verschiebung des Fensters."""
    best = 0.0
    steps = int(window.flex_h * 2)
    for i in range(-steps, steps + 1):
        shift = i * 0.5
        start, end = local_window(dest, day, window, shift)
        best = max(best, _score_for_shift(start, end, window.ideal_local_start_h))
    return best


def best_shift(dest: Destination, day: dt.date, window: WorkWindow) -> float:
    """Die Fensterverschiebung (in Stunden Heimatzeit), die am besten passt."""
    best, best_shift_h = -1.0, 0.0
    steps = int(window.flex_h * 2)
    for i in range(-steps, steps + 1):
        shift = i * 0.5
        start, end = local_window(dest, day, window, shift)
        score = _score_for_shift(start, end, window.ideal_local_start_h)
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
    night = max(0.0, end - NIGHT_FROM)
    bits = [f"{home} CET = {_hhmm(start)}-{_hhmm(end)} vor Ort (+{offset:.1f} h)"]
    if free_morning >= 1:
        bits.append(f"{free_morning:.1f} h freier Vormittag")
    if night >= 0.5:
        bits.append(f"{night:.1f} h nach 23 Uhr")
    if shift:
        bits.append(f"Fenster um {shift:+.1f} h verschoben")
    return "; ".join(bits)
