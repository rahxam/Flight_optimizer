#!/usr/bin/env python3
"""Preis-Tracking: Scrapes in die Historie einlesen, Bestpreise und Deals zeigen.

Gedacht fuer den Dauerbetrieb: regelmaessig scrapen, hier einlesen, und ueber
Wochen beobachten, was auf den relevanten Strecken wirklich zu holen ist.

    python3 scripts/track.py ingest data/prices/raw/scrape-2026-10-25.csv
    python3 scripts/track.py ingest-all          # alles aus data/prices/raw/
    python3 scripts/track.py status
    python3 scripts/track.py best --top 30
    python3 scripts/track.py deals --drop 15
    python3 scripts/track.py lows
    python3 scripts/track.py plan --price-mode best
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from workation import history  # noqa: E402
from workation.optimizer import Optimizer, TripConfig  # noqa: E402
from workation.prices import PriceBook  # noqa: E402
from workation.scenarios import SCENARIOS  # noqa: E402
from workation.seasonality import Weights  # noqa: E402

RAW_DIR = ROOT / "data" / "prices" / "raw"


def cmd_ingest(args) -> None:
    total = 0
    for path in args.paths:
        n = history.ingest_csv(Path(path), args.db)
        print(f"{path}: {n} neue Beobachtungen")
        total += n
    print(f"Gesamt: {total}")


def cmd_ingest_all(args) -> None:
    files = sorted(RAW_DIR.glob("*.csv"))
    if not files:
        print(f"Keine CSVs in {RAW_DIR}")
        return
    total = 0
    for path in files:
        n = history.ingest_csv(path, args.db)
        if n:
            print(f"{path.name}: {n} neue Beobachtungen")
        total += n
    print(f"{len(files)} Dateien, {total} neue Beobachtungen")


def cmd_status(args) -> None:
    cov = history.coverage(args.db)
    print(f"Beobachtungen      : {cov['observations']:,}")
    print(f"Strecke x Datum    : {cov['route_dates']:,}")
    print(f"Erste Messung      : {cov['first_seen'] or '-'}")
    print(f"Letzte Messung     : {cov['last_seen'] or '-'}")
    print(f"Abgeschlossene Laeufe: {cov['runs']}")
    if not cov["observations"]:
        print("\nNoch keine Daten. Erst scrapen, dann 'ingest-all'.")


def _print_stats(stats, limit: int) -> None:
    if not stats:
        print("Keine Treffer.")
        return
    print(
        f"{'Strecke':<12}{'Abflug':<12}{'Bestpreis':>10}{'gesehen':>12}"
        f"{'aktuell':>9}{'Median':>8}{'vs Med':>8}{'n':>5}"
    )
    print("-" * 84)
    for s in stats[:limit]:
        print(
            f"{s.origin + '->' + s.destination:<12}{s.depart_date:<12}"
            f"{s.best_eur:>10,.0f}{s.best_seen_at[:10]:>12}{s.latest_eur:>9,.0f}"
            f"{s.median_eur:>8,.0f}{s.latest_vs_median_pct:>7.0f}%{s.observations:>5}"
        )


def cmd_best(args) -> None:
    stats = sorted(history.route_stats(args.db), key=lambda s: s.best_eur)
    _print_stats(stats, args.top)


def cmd_deals(args) -> None:
    stats = history.deals(args.db, min_drop_pct=args.drop, min_observations=args.min_obs)
    print(f"Strecken mindestens {args.drop:.0f}% unter ihrem eigenen Median:\n")
    _print_stats(stats, args.top)


def cmd_lows(args) -> None:
    stats = history.all_time_lows(args.db, min_observations=args.min_obs)
    print("Strecken auf dem beobachteten Allzeittief (Kaufsignal):\n")
    _print_stats(stats, args.top)


def cmd_plan(args) -> None:
    """Szenarienvergleich mit den Preisen aus der Historie."""
    quotes = history.to_quotes(args.db, mode=args.price_mode)
    if not quotes:
        print("Keine Historie vorhanden - es wird mit Schaetzwerten gerechnet.")
    pb = PriceBook(quotes=quotes)
    base = TripConfig(
        weights=Weights.active(),
        eligible_tiers=("A", "B"),
        max_destinations=args.max_dest,
        vacation_days=args.vacation_days,
    )
    print(
        f"Preisquelle: {args.price_mode} ({len(quotes)} Strecken aus der Historie)\n"
    )
    print(
        f"{'Szenario':<58}{'Route':<28}{'Zeitraum':<14}{'d':>4}"
        f"{'Kosten':>9}{'EUR/Tag':>9}{'Schaetz':>9}"
    )
    print("-" * 128)
    for scenario in SCENARIOS.values():
        results = Optimizer(scenario.config(base), pb).run(top_n=1)
        if not results:
            print(f"{scenario.name:<58}keine zulaessige Route")
            continue
        it = results[0]
        print(
            f"{scenario.name:<58}{it.label:<28}{it.start:%d.%m}-{it.end:%d.%m}  "
            f"{it.total_days:>4}{it.total_cost_eur:>9,.0f}{it.cost_per_day_eur:>9,.0f}"
            f"{1 - it.estimated_share:>5.0%}"
        )
    print(
        "\n'Schaetz' = Anteil der Flugkosten aus Schaetzwerten. Der Rest sind "
        "gemessene Preise\nplus feste Posten (Bahn, Zubringer mit Residentenrabatt, "
        "Feier-Nachlauf)."
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Preis-Tracking und Historie")
    p.add_argument("--db", default=None, help="Pfad zur SQLite-Datei")
    sub = p.add_subparsers(dest="cmd", required=True)

    i = sub.add_parser("ingest")
    i.add_argument("paths", nargs="+")
    i.set_defaults(func=cmd_ingest)

    sub.add_parser("ingest-all").set_defaults(func=cmd_ingest_all)
    sub.add_parser("status").set_defaults(func=cmd_status)

    b = sub.add_parser("best")
    b.add_argument("--top", type=int, default=25)
    b.set_defaults(func=cmd_best)

    d = sub.add_parser("deals")
    d.add_argument("--drop", type=float, default=15.0)
    d.add_argument("--min-obs", type=int, default=4)
    d.add_argument("--top", type=int, default=25)
    d.set_defaults(func=cmd_deals)

    low = sub.add_parser("lows")
    low.add_argument("--min-obs", type=int, default=4)
    low.add_argument("--top", type=int, default=25)
    low.set_defaults(func=cmd_lows)

    pl = sub.add_parser("plan")
    pl.add_argument("--price-mode", choices=["latest", "best"], default="latest")
    pl.add_argument("--max-dest", type=int, default=2)
    pl.add_argument("--vacation-days", type=int, default=18)
    pl.set_defaults(func=cmd_plan)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
