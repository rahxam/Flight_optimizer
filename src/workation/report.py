"""Markdown-Report fuer Saisontabelle und Routenvorschlaege."""

from __future__ import annotations

import datetime as dt

from .data import load_calendar, load_destinations
from .models import Itinerary
from .optimizer import Optimizer
from .seasonality import Weights, interpolated_scores, season_table

DE_MONTHS = {3: "Mrz", 4: "Apr", 5: "Mai"}


def _fmt(day: dt.date) -> str:
    return f"{day.day:02d}.{day.month:02d}."


def season_section(weights: Weights) -> str:
    _, meta = load_destinations()
    windows = meta["windows"]
    rows = season_table(weights=weights)
    def _span(window: str) -> str:
        year, month, half = window.split("-")
        if half == "H1":
            return f"{month}. 1.-15."
        last = (dt.date(int(year), int(month), 28) + dt.timedelta(days=4)).replace(
            day=1
        ) - dt.timedelta(days=1)
        return f"{month}. 16.-{last.day}."

    head = "| Ziel | Tier | Work |" + "".join(f" {_span(w)} |" for w in windows)
    sep = "|---|---|---|" + "---|" * len(windows)
    lines = [head, sep]
    best = {}
    for r in rows:
        vals = [r[w] for w in windows]
        best[r["id"]] = max([v for v in vals if v is not None], default=0)
    for r in sorted(rows, key=lambda r: -best[r["id"]]):
        cells = []
        peak = best[r["id"]]
        for w in windows:
            v = r[w]
            if v is None:
                cells.append(" **X** ")
            elif v == peak:
                cells.append(f" **{v:.1f}** ")
            else:
                cells.append(f" {v:.1f} ")
        lines.append(f"| {r['name']} | {r['tier']} | {r['work']:.0f} |" + "|".join(cells) + "|")
    return "\n".join(lines)


def itinerary_section(itin: Itinerary, index: int) -> str:
    out = [
        f"### {index}. {itin.label}",
        "",
        f"**{_fmt(itin.start)}–{_fmt(itin.end)} {itin.end.year}** · {itin.total_days} Tage · "
        f"ab **{itin.origin_hub}** · Ticketstrategie: `{itin.ticket_strategy}`",
        "",
        f"| Kennzahl | Wert |",
        f"|---|---|",
        f"| Gesamtkosten ({itin.travellers} Pers.) | **{itin.total_cost_eur:,.0f} €** |",
        f"| davon Flüge | {itin.flight_cost_eur:,.0f} € |",
        f"| davon vor Ort (Unterkunft/Essen/Mobilität) | {itin.ground_cost_eur:,.0f} € |",
        f"| Visa | {itin.visa_cost_eur:,.0f} € |",
        f"| Kosten pro Tag (beide) | {itin.cost_per_day_eur:,.0f} € |",
        f"| Erlebnis-Score pro Tag | {itin.score_per_day:.2f} / 10 |",
        f"| Tage mit Longboard-Surf (Score ≥ 6) | {itin.good_surf_days} |",
        f"| Schätzanteil der Flugpreise | {itin.estimated_share:.0%} |",
        "",
        "**Blöcke**",
        "",
        "| Zeitraum | Tage | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for b in itin.blocks:
        mid = b.start + dt.timedelta(days=b.days // 2)
        weather, surf, calm = interpolated_scores(b.destination, mid)
        out.append(
            f"| {_fmt(b.start)}–{_fmt(b.end)} | {b.days} | {b.destination.name} | "
            f"{weather:.1f} | {surf:.1f} | {calm:.1f} | {b.destination.work:.0f} | "
            f"{b.destination.cost_per_day_eur_pp:.0f} € |"
        )
    out += ["", "**Flüge**", "", "| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |", "|---|---|---|---|---|"]
    for leg in itin.legs:
        out.append(
            f"| {_fmt(leg.date)} | {leg.origin} → {leg.destination} | {leg.kind} | "
            f"{leg.price_eur:,.0f} € | `{leg.source}` |"
        )
    if itin.warnings:
        out += ["", "**Hinweise**", ""]
        out += [f"- {w}" for w in itin.warnings]
    return "\n".join(out) + "\n"


def length_tradeoff_section(opt: Optimizer, lengths: tuple[int, ...] = (28, 35, 42)) -> str:
    """Beste Route je Reiselaenge - zeigt, was eine Woche mehr oder weniger bringt."""
    base = opt.cfg
    lines = [
        "| Reiselänge | Beste Route | Zeitraum | Kosten | €/Tag | Score/Tag | Surf-Tage |",
        "|---|---|---|---|---|---|---|",
    ]
    for length in lengths:
        base.min_days, base.max_days = length, length
        opt._profiles.clear()
        results = opt.run(top_n=1)
        if not results:
            lines.append(f"| {length} Tage | – | – | – | – | – | – |")
            continue
        it = results[0]
        lines.append(
            f"| {length} Tage | {it.label} | {_fmt(it.start)}–{_fmt(it.end)} | "
            f"{it.total_cost_eur:,.0f} € | {it.cost_per_day_eur:,.0f} € | "
            f"{it.score_per_day:.2f} | {it.good_surf_days} |"
        )
    return "\n".join(lines)


def calendar_section() -> str:
    lines = ["| Datum | Ereignis | Betrifft | Impact | Hinweis |", "|---|---|---|---|---|"]
    for e in sorted(load_calendar(), key=lambda e: e.start):
        note = " ".join(e.note.split())
        if len(note) > 180:
            note = note[:177] + "…"
        flag = "" if e.confidence == "confirmed" else " *(Prognose)*"
        lines.append(
            f"| {_fmt(e.start)}–{_fmt(e.end)} | {e.name}{flag} | {', '.join(e.affects)} | "
            f"{e.impact} | {note} |"
        )
    return "\n".join(lines)


def build_report(
    opt: Optimizer,
    itineraries: list[Itinerary],
    include_tradeoff: bool = True,
) -> str:
    cfg = opt.cfg
    parts = [
        "# Workation-Routenplan 2027",
        "",
        f"*Erzeugt am {dt.date.today():%d.%m.%Y}. Reisefenster "
        f"{_fmt(cfg.earliest_start)}–{_fmt(cfg.latest_end)}, {cfg.min_days}–{cfg.max_days} Tage, "
        f"{cfg.travellers} Personen, Abflug ab {', '.join(cfg.allowed_origins)}.*",
        "",
        "## Datenlage",
        "",
    ]
    cov = opt.pb.coverage()
    if cov["quotes"]:
        parts.append(
            f"{cov['quotes']} Preisangebote auf {cov['routes']} Strecken geladen "
            f"({cov['scraped']} davon gescrapet)."
        )
    else:
        parts.append(
            "**Noch keine echten Flugpreise geladen.** Alle Flugkosten sind Schätzwerte aus "
            "`data/route_hints.yaml`. Die Saison-Logik und die Routenreihenfolge stehen damit "
            "schon, die absoluten Preise aber nicht. Sobald Scrapes in `data/prices/*.csv` "
            "liegen, rechnet derselbe Lauf mit echten Zahlen."
        )
    parts += [
        "",
        "## Saison-Matrix",
        "",
        "Gewichteter Tagesscore je Ziel und Halbmonat (0–10, höher = besser). "
        "**X** = hart ausgeschlossen. Fett = Saisonhoch des Ziels.",
        "",
        season_section(cfg.weights),
        "",
        f"*Gewichtung: Wetter {cfg.weights.weather:.0%}, Surf {cfg.weights.surf:.0%}, "
        f"Ruhe {cfg.weights.calm:.0%}, Arbeitsfähigkeit {cfg.weights.work:.0%}; "
        f"Abzug {cfg.weights.tz_penalty_per_hour:.2f}/h Zeitversatz über 3 h, "
        f"Tropen-Bonus {cfg.weights.tropical_bonus:+.1f}.*",
        "",
        "## Kalender im Reisefenster",
        "",
        calendar_section(),
        "",
    ]
    if include_tradeoff:
        parts += [
            "## Was bringt eine Woche mehr?",
            "",
            length_tradeoff_section(opt),
            "",
        ]
    parts += ["## Routenvorschläge", ""]
    for i, itin in enumerate(itineraries, 1):
        parts.append(itinerary_section(itin, i))
    return "\n".join(parts)
