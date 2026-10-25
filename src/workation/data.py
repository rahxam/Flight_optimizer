"""Laden der YAML-Stammdaten."""

from __future__ import annotations

import datetime as dt
import functools
from pathlib import Path

import yaml

from .models import Access, CalendarEvent, Destination, OriginHub, WindowScore

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def _date(value) -> dt.date:
    if isinstance(value, dt.date):
        return value
    return dt.date.fromisoformat(str(value))


def _load(name: str) -> dict:
    with open(DATA_DIR / name, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


@functools.cache
def load_destinations() -> tuple[dict[str, Destination], dict]:
    raw = _load("destinations.yaml")
    meta = raw["meta"]
    out: dict[str, Destination] = {}
    for item in raw["destinations"]:
        hard = item.get("hard_avoid") or {}
        constraints = item.get("constraints") or {}
        ranges = [
            (_date(a), _date(b)) for a, b in (constraints.get("avoid_dates") or [])
        ]
        out[item["id"]] = Destination(
            id=item["id"],
            name=item["name"],
            country=item["country"],
            region_short=item["region_short"],
            tier=item["tier"],
            airports=list(item["airports"]),
            primary_airport=item["primary_airport"],
            tropical=bool(item["tropical"]),
            work=float(item["work"]),
            tz_offset_vs_madrid_winter=float(item["tz_offset_vs_madrid_winter"]),
            cost_per_day_eur_pp=float(item["cost_per_day_eur_pp"]),
            activities=list(item.get("activities", [])),
            hub_to_base_h=float(item.get("hub_to_base_h", 1.0)),
            scores={
                win: WindowScore(
                    weather=float(s["weather"]),
                    surf=float(s["surf"]),
                    calm=float(s["calm"]),
                    note=s.get("note", ""),
                )
                for win, s in item["scores"].items()
            },
            notes=item.get("notes", "").strip(),
            hard_avoid_windows=frozenset(hard.get("windows", [])),
            hard_avoid_reason=(hard.get("reason") or "").strip(),
            avoid_date_ranges=ranges,
            avoid_date_reason=(constraints.get("avoid_reason") or "").strip(),
        )
    return out, meta


@functools.cache
def load_origins() -> tuple[dict[str, OriginHub], dict]:
    raw = _load("origins.yaml")
    out: dict[str, OriginHub] = {}
    for item in raw["origins"]:
        access = {
            context: Access(
                context=context,
                mode=spec["mode"],
                hours=float(spec["hours"]),
                price_eur_pp=float(spec["price_eur_pp"]),
                residencia_discount=bool(spec.get("residencia_discount", False)),
                min_connect_h=float(spec.get("min_connect_h", 3.0)),
                company_covered_travellers=int(spec.get("company_covered_travellers", 0)),
                note=(spec.get("note") or "").strip(),
            )
            for context, spec in item["access"].items()
        }
        out[item["id"]] = OriginHub(
            id=item["id"],
            name=item["name"],
            role=item["role"],
            access=access,
            notes=item.get("notes", "").strip(),
        )
    return out, raw["meta"]


def hubs_reachable_from(context: str) -> list[str]:
    origins, _ = load_origins()
    return [h.id for h in origins.values() if h.reachable_from(context)]


@functools.cache
def load_calendar() -> list[CalendarEvent]:
    raw = _load("calendar.yaml")
    return [
        CalendarEvent(
            id=e["id"],
            name=e["name"],
            start=_date(e["start"]),
            end=_date(e["end"]),
            affects=tuple(e.get("affects", [])),
            impact=e.get("impact", "low"),
            note=(e.get("note") or "").strip(),
            confidence=e.get("confidence", "predicted"),
        )
        for e in raw["events"]
    ]


@functools.cache
def load_route_hints() -> dict:
    return _load("route_hints.yaml")
