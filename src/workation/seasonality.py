"""Saison-Scoring: Halbmonats-Fenster -> Tageswerte -> Erlebniswert."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

from .data import load_destinations
from .models import Destination


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
    """Gewichtung der Teilscores. Summe der ersten vier sollte 1.0 sein."""

    weather: float = 0.30
    surf: float = 0.30
    calm: float = 0.15
    work: float = 0.25
    # Zusatz-Terme
    tz_penalty_per_hour: float = 0.12  # Score-Abzug je Stunde Versatz zu Madrid
    tropical_bonus: float = 0.3

    @classmethod
    def surf_focused(cls) -> "Weights":
        return cls(weather=0.25, surf=0.42, calm=0.10, work=0.23, tropical_bonus=0.5)

    @classmethod
    def work_focused(cls) -> "Weights":
        return cls(weather=0.25, surf=0.15, calm=0.15, work=0.45, tz_penalty_per_hour=0.25)

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


def daily_score(dest: Destination, day: dt.date, weights: Weights) -> float:
    """Erlebniswert eines Tages an einem Ziel, 0-10."""
    weather, surf, calm = interpolated_scores(dest, day)
    score = (
        weights.weather * weather
        + weights.surf * surf
        + weights.calm * calm
        + weights.work * dest.work
    )
    # Sommerzeit ab 28.03.2027 verkleinert den Versatz zu Europa um 1 h.
    offset = dest.tz_offset_vs_madrid_winter
    if day >= dt.date(2027, 3, 28):
        offset = max(0.0, offset - 1.0)
    score -= weights.tz_penalty_per_hour * max(0.0, offset - 3.0)
    if dest.tropical:
        score += weights.tropical_bonus
    return max(0.0, score)


def is_available(dest: Destination, day: dt.date) -> tuple[bool, str]:
    """Harte Ausschluesse (Brandsaison, Lebaran-Reisewelle, ...)."""
    if window_of(day) in dest.hard_avoid_windows:
        return False, dest.hard_avoid_reason
    blocked = dest.blocked_on(day)
    if blocked:
        return False, blocked
    return True, ""


def season_table(window_keys: list[str] | None = None, weights: Weights | None = None) -> list[dict]:
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
                row[win] = round(daily_score(dest, mid, weights), 2)
        rows.append(row)
    return rows
