"""Saison-Scoring: Halbmonats-Fenster -> Tageswerte -> Erlebniswert."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

from .data import load_destinations
from .models import Destination
from .workwindow import WorkWindow, overlap_score


def window_of(day: dt.date) -> str:
    """Halbmonats-Fenster-Key fuer einen Tag, z.B. '2027-04-H2'."""
    half = "H1" if day.day <= 15 else "H2"
    return f"{day.year}-{day.month:02d}-{half}"


def _window_bounds(key: str) -> tuple[dt.date, dt.date]:
    year, month, half = key.split("-")
    year, month = int(year), int(month)
    if half == "H1":
        return dt.date(year, month, 1), dt.date(year, month, 15)
    last = (dt.date(year, month, 28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
    return dt.date(year, month, 16), last


@dataclass(frozen=True)
class Weights:
    """Gewichtung der Teilscores. Die Summe der sechs Gewichte sollte 1.0 sein.

    weather     = trocken/angenehm
    surf        = Longboard-taugliche Welle
    activity    = Vielfalt von Ganztages- und Mehrtagesausfluegen
    calm        = keine Crowds, keine Feiertagsstillstaende
    work        = Arbeitsinfrastruktur (Internet, Coworking, Strom)
    work_window = wie gut die Pflicht-Arbeitszeit vor Ort liegt (s. workwindow.py)
    """

    weather: float = 0.20
    surf: float = 0.18
    activity: float = 0.18
    calm: float = 0.08
    work: float = 0.18
    work_window: float = 0.18
    tropical_bonus: float = 0.3

    @classmethod
    def active(cls) -> "Weights":
        """Default: aktiv unterwegs, Surfen ist eine Option von mehreren."""
        return cls(
            weather=0.20, surf=0.18, activity=0.22, calm=0.07,
            work=0.16, work_window=0.17, tropical_bonus=0.4,
        )

    @classmethod
    def surf_focused(cls) -> "Weights":
        return cls(
            weather=0.20, surf=0.32, activity=0.13, calm=0.06,
            work=0.14, work_window=0.15, tropical_bonus=0.5,
        )

    @classmethod
    def work_focused(cls) -> "Weights":
        return cls(
            weather=0.18, surf=0.10, activity=0.14, calm=0.08,
            work=0.25, work_window=0.25, tropical_bonus=0.2,
        )

    @classmethod
    def balanced(cls) -> "Weights":
        return cls()


def interpolated_scores(dest: Destination, day: dt.date) -> tuple[float, float, float]:
    """(weather, surf, calm) fuer einen Tag, linear zwischen Fenstermitten geglaettet.

    Ohne Glaettung wuerde ein Umzug ueber eine Fenstergrenze einen Sprung erzeugen
    und die Optimierung auf die Fenstergrenzen hin verzerren.
    """
    key = window_of(day)
    cur = dest.scores.get(key)
    if cur is None:
        # Ausserhalb des modellierten Fensters: neutral-pessimistisch bewerten.
        return 0.0, 0.0, 5.0

    lo, hi = _window_bounds(key)
    mid = lo + (hi - lo) / 2
    keys = sorted(dest.scores)
    idx = keys.index(key)

    if day <= mid:
        neighbour = dest.scores[keys[idx - 1]] if idx > 0 else cur
        span = (mid - lo).days or 1
        t = 0.5 * (1 - (mid - day).days / span)  # 0.0 am Fensteranfang -> 0.5 in der Mitte
    else:
        neighbour = dest.scores[keys[idx + 1]] if idx + 1 < len(keys) else cur
        span = (hi - mid).days or 1
        t = 0.5 * (1 - (day - mid).days / span)

    blend = lambda a, b: b * (1 - t) + a * t  # noqa: E731
    return (
        blend(neighbour.weather, cur.weather),
        blend(neighbour.surf, cur.surf),
        blend(neighbour.calm, cur.calm),
    )


DEFAULT_WINDOW = WorkWindow()


def daily_score(
    dest: Destination,
    day: dt.date,
    weights: Weights,
    window: WorkWindow | None = None,
    vacation: bool = False,
) -> float:
    """Erlebniswert eines Tages an einem Ziel, 0-10.

    An einem Urlaubstag entfallen die beiden Arbeitsterme, und das Gewicht wird
    auf Wetter/Surf/Ruhe UMVERTEILT - nicht durch Vollwert ersetzt. Der
    Unterschied ist wichtig: wuerde man `work = 10` setzen, wuerde ein Ziel mit
    schlechter Infrastruktur dafuer belohnt, dass es schlecht ist (Sumbawa haette
    den groessten "Urlaubsgewinn" und wuerde dadurch zum Favoriten). So bemisst
    sich ein Urlaubstag ausschliesslich an den eigenen Qualitaeten des Ortes.
    """
    weather, surf, calm = interpolated_scores(dest, day)
    if vacation:
        # An einem Urlaubstag zaehlt vor allem, was man unternehmen kann.
        experience = weights.weather + weights.surf + weights.activity + weights.calm
        total = experience + weights.work + weights.work_window
        scale = (total / experience) if experience else 0.0
        score = scale * (
            weights.weather * weather
            + weights.surf * surf
            + weights.activity * dest.activity_score
            + weights.calm * calm
        )
    else:
        work_window = overlap_score(dest, day, window or DEFAULT_WINDOW)
        score = (
            weights.weather * weather
            + weights.surf * surf
            + weights.activity * dest.activity_score
            + weights.calm * calm
            + weights.work * dest.work
            + weights.work_window * work_window
        )
    if dest.tropical:
        score += weights.tropical_bonus
    return max(0.0, score)


def vacation_gain(
    dest: Destination, day: dt.date, weights: Weights, window: WorkWindow | None = None
) -> float:
    """Wie viel ein Urlaubstag an diesem Ziel mehr wert ist als ein Arbeitstag."""
    return daily_score(dest, day, weights, window, vacation=True) - daily_score(
        dest, day, weights, window, vacation=False
    )


def is_available(dest: Destination, day: dt.date) -> tuple[bool, str]:
    """Harte Ausschluesse (Brandsaison, Lebaran-Reisewelle, ...)."""
    if window_of(day) in dest.hard_avoid_windows:
        return False, dest.hard_avoid_reason
    blocked = dest.blocked_on(day)
    if blocked:
        return False, blocked
    return True, ""


def season_table(
    window_keys: list[str] | None = None,
    weights: Weights | None = None,
    work_window: WorkWindow | None = None,
) -> list[dict]:
    """Uebersichtstabelle aller Ziele x Fenster - fuer den Report."""
    dests, meta = load_destinations()
    weights = weights or Weights.balanced()
    windows = window_keys or meta["windows"]
    rows = []
    for dest in dests.values():
        row: dict = {"id": dest.id, "name": dest.region_short, "tier": dest.tier, "work": dest.work}
        for win in windows:
            lo, hi = _window_bounds(win)
            mid = lo + (hi - lo) / 2
            if win in dest.hard_avoid_windows:
                row[win] = None
            else:
                row[win] = round(daily_score(dest, mid, weights, work_window), 2)
        rows.append(row)
    return rows
