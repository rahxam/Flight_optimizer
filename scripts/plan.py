#!/usr/bin/env python3
"""CLI: Saisontabelle, Routenoptimierung, Report, Scrape-Matrix.

Beispiele:
    python3 scripts/plan.py season
    python3 scripts/plan.py optimize --profile surf --top 8
    python3 scripts/plan.py report --profile surf --out docs/routenplan.md
    python3 scripts/plan.py scrape-matrix --level standard
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from workation.optimizer import Optimizer, TripConfig  # noqa: E402
from workation.prices import PriceBook  # noqa: E402
from workation.report import build_report  # noqa: E402
from workation.scenarios import SCENARIOS  # noqa: E402
from workation.scrape.queries import (  # noqa: E402
    candidate_queries,
    grid_queries,
    scenario_queries,
    write_matrix,
)
from workation.seasonality import Weights, season_table  # noqa: E402
from workation.workwindow import WorkWindow  # noqa: E402

PROFILES = {
    "active": Weights.active,
    "surf": Weights.surf_focused,
    "work": Weights.work_focused,
    "balanced": Weights.balanced,
}


def _config(args) -> TripConfig:
    return TripConfig(
        earliest_start=dt.date.fromisoformat(args.earliest_start),
        latest_end=dt.date.fromisoformat(args.latest_end),
        min_days=args.min_days,
        max_days=args.max_days,
        travellers=args.travellers,
        min_destinations=args.min_dest,
        max_destinations=args.max_dest,
        allowed_origins=tuple(args.origins.split(",")),
        weights=PROFILES[args.profile](),
        work_window=WorkWindow(
            args.work_start, args.work_end, args.work_flex, args.ideal_local_start
        ),
        vacation_days=args.vacation_days,
        vacation_priority=tuple(x for x in args.vacation_first.split(",") if x),
        start_date_step=args.step,
        budget_eur=args.budget,
        min_good_surf_days=args.min_surf_days,
        include_destinations=tuple(x for x in args.include.split(",") if x),
        exclude_destinations=tuple(x for x in args.exclude.split(",") if x),
        board_bags=args.board_bags,
    )


def cmd_season(args) -> None:
    rows = season_table(weights=PROFILES[args.profile]())
    windows = [k for k in rows[0] if k.startswith("2027")]
    print(f"{'Ziel':<18}{'Tier':<6}" + "".join(f"{w[5:]:>10}" for w in windows))
    print("-" * (24 + 10 * len(windows)))
    for r in sorted(rows, key=lambda r: -max([v for v in (r[w] for w in windows) if v is not None] or [0])):
        cells = "".join(f"{(f'{r[w]:.2f}' if r[w] is not None else 'X'):>10}" for w in windows)
        print(f"{r['name']:<18}{r['tier']:<6}{cells}")


def _print_table(results) -> None:
    print(
        f"{'#':<3}{'Route':<36}{'Zeitraum':<14}{'d':>4}{'Hub':>5}{'Kosten':>9}"
        f"{'Flug':>8}{'€/Tag':>7}{'S/Tag':>7}{'Surf':>6}"
    )
    print("-" * 98)
    for i, it in enumerate(results, 1):
        print(
            f"{i:<3}{it.label:<36}{it.start:%d.%m}-{it.end:%d.%m}  {it.total_days:>4}"
            f"{it.origin_hub:>5}{it.total_cost_eur:>9,.0f}{it.flight_cost_eur:>8,.0f}"
            f"{it.cost_per_day_eur:>7,.0f}{it.score_per_day:>7.2f}{it.good_surf_days:>6}"
        )


def cmd_optimize(args) -> None:
    opt = Optimizer(_config(args), PriceBook())
    results = opt.run(top_n=args.top)
    if not results:
        print("Keine Route erfüllt die Vorgaben. Lockere Budget, Blocklängen oder Zieltiers.")
        return
    _print_table(results)
    print()
    for i, it in enumerate(results[: args.detail], 1):
        print(f"[{i}] {it.label}  {it.start:%d.%m.}-{it.end:%d.%m.}")
        for b in it.blocks:
            print(f"      {b.start:%d.%m.}-{b.end:%d.%m.} ({b.days:>2}d)  {b.destination.name}")
        for leg in it.legs:
            print(
                f"      ✈  {leg.date:%d.%m.}  {leg.origin}->{leg.destination:<4} "
                f"{leg.price_eur:>7,.0f} €  [{leg.source}]"
            )
        for w in it.warnings:
            print(f"      ! {w}")
        print()


def cmd_scenarios(args) -> None:
    base = _config(args)
    print(
        f"{'Szenario':<46}{'Route':<30}{'Zeitraum':<14}{'d':>4}{'ab':>5}"
        f"{'Kosten':>9}{'EUR/Tag':>9}{'S/Tag':>7}{'Surf':>6}"
    )
    print("-" * 130)
    details = []
    for scenario in SCENARIOS.values():
        opt = Optimizer(scenario.config(base), PriceBook())
        results = opt.run(top_n=1)
        if not results:
            print(f"{scenario.name:<46}keine zulaessige Route")
            continue
        it = results[0]
        print(
            f"{scenario.name:<46}{it.label:<30}{it.start:%d.%m}-{it.end:%d.%m}  "
            f"{it.total_days:>4}{it.origin_hub:>5}{it.total_cost_eur:>9,.0f}"
            f"{it.cost_per_day_eur:>9,.0f}{it.score_per_day:>7.2f}{it.good_surf_days:>6}"
        )
        details.append((scenario, it))
    print()
    for scenario, it in details:
        print(f"[{scenario.name}]")
        print(f"  {scenario.pre_trip_note}")
        if scenario.post_trip_note:
            print(f"  {scenario.post_trip_note}")
        for b in it.blocks:
            print(
                f"  {b.start:%d.%m.}-{b.end:%d.%m.} ({b.days:>2}d, davon {b.vacation_days:>2}d Urlaub)  "
                f"{b.destination.region_short}"
            )
        for leg in it.legs:
            print(
                f"  fly {leg.date:%d.%m.}  {leg.origin}->{leg.destination:<4} "
                f"{leg.price_eur:>7,.0f} EUR  [{leg.source}]"
            )
        print()


def cmd_report(args) -> None:
    opt = Optimizer(_config(args), PriceBook())
    results = opt.run(top_n=args.top)
    # length_tradeoff_section verändert die Config, daher Routen vorher einsammeln.
    text = build_report(opt, results, include_tradeoff=not args.no_tradeoff)
    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"Report geschrieben: {out}  ({len(text.splitlines())} Zeilen, {len(results)} Routen)")


def cmd_scrape_matrix(args) -> None:
    if args.from_scenarios:
        queries = scenario_queries(
            list(SCENARIOS.values()),
            gateways=[g for g in args.gateways.split(",") if g],
            adults=args.travellers,
        )
        if args.with_candidates:
            base = _config(args)
            for scenario in SCENARIOS.values():
                opt = Optimizer(scenario.config(base), PriceBook())
                queries += candidate_queries(opt.run(top_n=2), adults=args.travellers)
        write_matrix(
            queries,
            ROOT / "data" / "prices" / "_queries.json",
            ROOT / "docs" / "scrape_checklist.md",
        )
        print(f"{len(queries)} Suchen -> data/prices/_queries.json + docs/scrape_checklist.md")
        print(f"Geschätzte Laufzeit automatisiert: ~{len(queries) * 6 / 60:.0f} min")
        return
    queries = grid_queries(
        earliest_start=dt.date.fromisoformat(args.earliest_start),
        latest_start=dt.date.fromisoformat(args.latest_start),
        earliest_return=dt.date.fromisoformat(args.earliest_return),
        latest_return=dt.date.fromisoformat(args.latest_return),
        level=args.level,
        adults=args.travellers,
    )
    if args.with_candidates:
        opt = Optimizer(_config(args), PriceBook())
        queries += candidate_queries(opt.run(top_n=args.top), adults=args.travellers)
    write_matrix(
        queries,
        ROOT / "data" / "prices" / "_queries.json",
        ROOT / "docs" / "scrape_checklist.md",
    )
    print(f"{len(queries)} Suchen -> data/prices/_queries.json + docs/scrape_checklist.md")
    print(f"Geschätzte Laufzeit automatisiert: ~{len(queries) * 6 / 60:.0f} min")


def main() -> None:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--profile", choices=PROFILES, default="active")
    common.add_argument("--earliest-start", default="2027-03-12")
    common.add_argument("--latest-end", default="2027-05-10")
    common.add_argument("--min-days", type=int, default=28)
    common.add_argument("--max-days", type=int, default=42)
    common.add_argument("--travellers", type=int, default=2)
    common.add_argument("--min-dest", type=int, default=2)
    common.add_argument("--max-dest", type=int, default=3)
    common.add_argument("--origins", default="MAD,BCN")
    common.add_argument("--step", type=int, default=2, help="Raster der Startdaten in Tagen")
    common.add_argument("--budget", type=float, default=None, help="Harte Kostenobergrenze in EUR")
    common.add_argument("--min-surf-days", type=int, default=0)
    common.add_argument("--include", default="", help="Ziel-IDs, die vorkommen muessen")
    common.add_argument("--exclude", default="", help="Ziel-IDs, die ausgeschlossen sind")
    common.add_argument("--board-bags", type=int, default=0)
    common.add_argument("--top", type=int, default=10)
    common.add_argument("--work-start", type=float, default=9.0, help="Arbeitsbeginn CET")
    common.add_argument("--work-end", type=float, default=16.0, help="Arbeitsende CET")
    common.add_argument("--work-flex", type=float, default=1.0, help="Verschiebbarkeit in Stunden")
    common.add_argument(
        "--ideal-local-start",
        type=float,
        default=14.5,
        help="bevorzugter lokaler Arbeitsbeginn (14.5 = 14:30 Ortszeit)",
    )
    common.add_argument("--vacation-days", type=int, default=14)
    common.add_argument(
        "--vacation-first",
        default="",
        help="Ziel-IDs, die Urlaubstage zuerst und ohne Obergrenze bekommen "
        "(z.B. NP-NEPAL fuer einen mehrtaegigen Trek)",
    )

    p = argparse.ArgumentParser(description="Workation-Routenplaner", parents=[common])
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("season", parents=[common]).set_defaults(func=cmd_season)

    o = sub.add_parser("optimize", parents=[common])
    o.add_argument("--detail", type=int, default=3)
    o.set_defaults(func=cmd_optimize)

    r = sub.add_parser("report", parents=[common])
    r.add_argument("--out", default="docs/routenplan.md")
    r.add_argument("--no-tradeoff", action="store_true")
    r.set_defaults(func=cmd_report)

    sub.add_parser("scenarios", parents=[common]).set_defaults(func=cmd_scenarios)

    s = sub.add_parser("scrape-matrix", parents=[common])
    s.add_argument("--level", choices=["quick", "standard", "full"], default="standard")
    s.add_argument("--latest-start", default="2027-04-03")
    s.add_argument("--earliest-return", default="2027-04-18")
    s.add_argument("--latest-return", default="2027-05-10")
    s.add_argument("--with-candidates", action="store_true")
    s.add_argument(
        "--gateways",
        default="CMB,KUL,LOP,HAN,MCT",
        help="Asien-Einstiegsflughaefen, die abgefragt werden",
    )
    s.add_argument(
        "--from-scenarios",
        action="store_true",
        help="nur die Suchen, die die Startszenarien brauchen (empfohlen)",
    )
    s.set_defaults(func=cmd_scrape_matrix)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
