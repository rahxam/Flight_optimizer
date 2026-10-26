#!/usr/bin/env python3
"""Read-only web view of the price history.

Serves the same evaluations as scripts/track.py (status, all-time lows, deals,
best prices, scenarios) as one HTML page, plus the docs as plain text. Standard
library only, so it runs from the tracker image without extra packages.

Authentication is not handled here: the page is meant to sit behind a reverse
proxy with forward auth (Traefik + Authentik on the Unraid box).

    python3 scripts/web.py --port 8080
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import os
import sys
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from workation import history  # noqa: E402
from workation.optimizer import Optimizer, TripConfig  # noqa: E402
from workation.prices import PriceBook  # noqa: E402
from workation.scenarios import SCENARIOS  # noqa: E402
from workation.seasonality import Weights  # noqa: E402

DOCS_DIR = ROOT / "docs"
RAW_DIR = ROOT / "data" / "prices" / "raw"
DOCS = ("strategie", "routenplan", "seasonality")


# --------------------------------------------------------------------------- #
# Scenario comparison (slow: ~30 s per price mode), cached per history state
# --------------------------------------------------------------------------- #
class ScenarioCache:
    """Recomputes the scenario table in the background when the history changes."""

    def __init__(self, db: Path | None):
        self.db = db
        self.lock = threading.Lock()
        self.key: str | None = None
        self.rows: dict[str, list[dict]] = {}
        self.computed_at: str | None = None
        self.busy = False
        self.error: str | None = None

    def _state_key(self) -> str:
        cov = history.coverage(self.db)
        return f"{cov['observations']}|{cov['last_seen']}"

    def refresh_if_stale(self) -> None:
        try:
            key = self._state_key()
        except Exception as exc:  # noqa: BLE001 - surface any DB problem on the page
            self.error = str(exc)
            return
        with self.lock:
            if self.busy or key == self.key:
                return
            self.busy = True
        threading.Thread(target=self._compute, args=(key,), daemon=True).start()

    def _compute(self, key: str) -> None:
        try:
            rows = {mode: self._plan(mode) for mode in ("latest", "best")}
            with self.lock:
                self.rows, self.key, self.error = rows, key, None
                self.computed_at = dt.datetime.now().strftime("%d.%m.%Y %H:%M")
        except Exception as exc:  # noqa: BLE001
            with self.lock:
                self.error = str(exc)
        finally:
            with self.lock:
                self.busy = False

    def _plan(self, mode: str) -> list[dict]:
        pb = PriceBook(quotes=history.to_quotes(self.db, mode=mode))
        base = TripConfig(
            weights=Weights.active(),
            eligible_tiers=("A", "B"),
            max_destinations=2,
            vacation_days=18,
        )
        out = []
        for scenario in SCENARIOS.values():
            results = Optimizer(scenario.config(base), pb).run(top_n=1)
            if not results:
                out.append({"scenario": scenario.name, "route": None})
                continue
            it = results[0]
            out.append(
                {
                    "scenario": scenario.name,
                    "route": it.label,
                    "period": f"{it.start:%d.%m.}–{it.end:%d.%m.}",
                    "days": it.total_days,
                    "cost": it.total_cost_eur,
                    "per_day": it.cost_per_day_eur,
                    "measured": 1 - it.estimated_share,
                }
            )
        return out


# --------------------------------------------------------------------------- #
# HTML
# --------------------------------------------------------------------------- #
CSS = """
:root { color-scheme: light dark; --muted: #6b7280; --line: #d1d5db; --good: #15803d; --bad: #b91c1c; }
body { font: 15px/1.45 system-ui, sans-serif; margin: 0 auto; max-width: 1100px; padding: 1.5rem; }
h1 { font-size: 1.4rem; margin: 0 0 .25rem; }
h2 { font-size: 1.1rem; margin: 2rem 0 .5rem; }
p.note, .muted { color: var(--muted); font-size: .85rem; }
.cards { display: flex; flex-wrap: wrap; gap: .75rem; margin: 1rem 0; }
.card { border: 1px solid var(--line); border-radius: 8px; padding: .6rem .9rem; min-width: 9rem; }
.card b { display: block; font-size: 1.25rem; }
table { border-collapse: collapse; width: 100%; font-variant-numeric: tabular-nums; }
th, td { padding: .3rem .5rem; border-bottom: 1px solid var(--line); text-align: left; white-space: nowrap; }
td.n, th.n { text-align: right; }
.down { color: var(--good); } .up { color: var(--bad); }
nav a { margin-right: 1rem; }
pre { white-space: pre-wrap; font: 13px/1.5 ui-monospace, monospace; }
"""


def _page(title: str, body: str) -> bytes:
    return (
        "<!doctype html><html lang='de'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        f"<title>{html.escape(title)}</title><style>{CSS}</style></head><body>"
        f"{body}</body></html>"
    ).encode()


def _eur(value: float) -> str:
    return f"{value:,.0f} €".replace(",", ".")


def _stats_table(stats: list[history.RouteStat], limit: int) -> str:
    if not stats:
        return "<p class='muted'>Keine Treffer.</p>"
    rows = []
    for s in stats[:limit]:
        pct = s.latest_vs_median_pct
        cls = "down" if pct < 0 else "up" if pct > 0 else ""
        rows.append(
            "<tr>"
            f"<td>{html.escape(s.origin)} → {html.escape(s.destination)}</td>"
            f"<td>{html.escape(s.depart_date)}</td>"
            f"<td>{'Hin und zurück' if s.trip_type == 'return' else 'einfach'}</td>"
            f"<td class='n'>{_eur(s.best_eur)}</td>"
            f"<td>{html.escape((s.best_seen_at or '')[:10])}</td>"
            f"<td class='n'>{_eur(s.latest_eur)}</td>"
            f"<td class='n'>{_eur(s.median_eur)}</td>"
            f"<td class='n {cls}'>{pct:+.0f} %</td>"
            f"<td class='n'>{s.observations}</td>"
            "</tr>"
        )
    head = (
        "<tr><th>Strecke</th><th>Abflug</th><th>Art</th><th class='n'>Bestpreis</th>"
        "<th>gesehen</th><th class='n'>aktuell</th><th class='n'>Median</th>"
        "<th class='n'>vs. Median</th><th class='n'>n</th></tr>"
    )
    return f"<table>{head}{''.join(rows)}</table>"


def _scenario_table(cache: ScenarioCache, mode: str) -> str:
    rows = cache.rows.get(mode)
    if rows is None:
        return "<p class='muted'>Wird berechnet … (dauert etwa eine Minute, Seite neu laden)</p>"
    out = []
    for r in rows:
        if r["route"] is None:
            out.append(
                f"<tr><td>{html.escape(r['scenario'])}</td>"
                "<td colspan='6' class='muted'>keine zulässige Route</td></tr>"
            )
            continue
        out.append(
            f"<tr><td>{html.escape(r['scenario'])}</td><td>{html.escape(r['route'])}</td>"
            f"<td>{r['period']}</td><td class='n'>{r['days']}</td>"
            f"<td class='n'>{_eur(r['cost'])}</td><td class='n'>{_eur(r['per_day'])}</td>"
            f"<td class='n'>{r['measured']:.0%}</td></tr>"
        )
    head = (
        "<tr><th>Szenario</th><th>Route</th><th>Zeitraum</th><th class='n'>Tage</th>"
        "<th class='n'>Kosten</th><th class='n'>€/Tag</th><th class='n'>gemessen</th></tr>"
    )
    return f"<table>{head}{''.join(out)}</table>"


def _recent_scrapes(limit: int = 8) -> str:
    files = sorted(RAW_DIR.glob("scrape-*.csv"), reverse=True)[:limit]
    if not files:
        return "<p class='muted'>Noch kein Scrape-Lauf.</p>"
    items = []
    for f in files:
        try:
            lines = max(sum(1 for _ in f.open(encoding="utf-8")) - 1, 0)
        except OSError:
            lines = 0
        when = dt.datetime.fromtimestamp(f.stat().st_mtime).strftime("%d.%m.%Y %H:%M")
        items.append(f"<tr><td>{when}</td><td class='n'>{lines}</td></tr>")
    return (
        "<table><tr><th>Lauf beendet</th><th class='n'>Preise</th></tr>"
        f"{''.join(items)}</table>"
    )


def render_index(db: Path | None, cache: ScenarioCache) -> bytes:
    cache.refresh_if_stale()
    cov = history.coverage(db)
    stats = history.route_stats(db)
    lows = history.all_time_lows(db)
    deals = history.deals(db)

    def card(label: str, value: str) -> str:
        return f"<div class='card'><span class='muted'>{label}</span><b>{value}</b></div>"

    last = (cov["last_seen"] or "–")[:16].replace("T", " ")
    nav = " ".join(f"<a href='/docs/{d}'>{d}.md</a>" for d in DOCS)
    note = ""
    if not cov["observations"]:
        note = (
            "<p class='note'>Noch keine gemessenen Preise. Der Tracker läuft alle "
            "12 Stunden; bis dahin rechnen die Szenarien mit Schätzwerten.</p>"
        )
    scen_note = f"Berechnet {cache.computed_at}" if cache.computed_at else ""
    if cache.busy and cache.computed_at:
        scen_note += " · wird gerade neu berechnet"
    if cache.error:
        scen_note += f" · Fehler: {html.escape(cache.error)}"

    body = f"""
<h1>Workation-Flugpreise</h1>
<nav class='muted'>Doku: {nav}</nav>
<div class='cards'>
  {card("Beobachtungen", f"{cov['observations']:,}".replace(",", "."))}
  {card("Strecke × Datum", f"{cov['route_dates']:,}".replace(",", "."))}
  {card("Letzte Messung", html.escape(last))}
  {card("Allzeittiefs", str(len(lows)))}
  {card("Preiseinbrüche", str(len(deals)))}
</div>
{note}
<h2>Allzeittiefs – Kaufsignal</h2>
<p class='note'>Strecken, deren neuester Preis dem niedrigsten je gesehenen entspricht (ab 4 Messungen).</p>
{_stats_table(lows, 25)}
<h2>Preiseinbrüche</h2>
<p class='note'>Neuester Preis mindestens 15 % unter dem eigenen Median (ab 4 Messungen).</p>
{_stats_table(deals, 25)}
<h2>Szenarien mit aktuellen Preisen</h2>
<p class='note'>„Soll ich jetzt buchen?“ – rechnet mit dem jeweils neuesten Preis. {scen_note}</p>
{_scenario_table(cache, "latest")}
<h2>Szenarien mit Bestpreisen</h2>
<p class='note'>„Was ist erreichbar, wenn ich geduldig beobachte?“ – rechnet mit dem besten je gesehenen Preis.</p>
{_scenario_table(cache, "best")}
<h2>Günstigste gesehene Preise</h2>
{_stats_table(sorted(stats, key=lambda s: s.best_eur), 40)}
<h2>Letzte Scrape-Läufe</h2>
{_recent_scrapes()}
"""
    return _page("Workation-Flugpreise", body)


def render_doc(name: str) -> bytes | None:
    if name not in DOCS:
        return None
    path = DOCS_DIR / f"{name}.md"
    if not path.exists():
        return None
    text = html.escape(path.read_text(encoding="utf-8"))
    return _page(f"{name}.md", f"<p><a href='/'>← Übersicht</a></p><pre>{text}</pre>")


# --------------------------------------------------------------------------- #
# Server
# --------------------------------------------------------------------------- #
def make_handler(db: Path | None, cache: ScenarioCache):
    class Handler(BaseHTTPRequestHandler):
        server_version = "workation-web"

        def _send(self, status: HTTPStatus, body: bytes, ctype: str = "text/html; charset=utf-8"):
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):  # noqa: N802 - http.server API
            path = self.path.split("?", 1)[0]
            if path == "/healthz":
                return self._send(HTTPStatus.OK, b"ok", "text/plain")
            if path == "/":
                try:
                    return self._send(HTTPStatus.OK, render_index(db, cache))
                except Exception as exc:  # noqa: BLE001
                    msg = _page("Fehler", f"<pre>{html.escape(repr(exc))}</pre>")
                    return self._send(HTTPStatus.INTERNAL_SERVER_ERROR, msg)
            if path.startswith("/docs/"):
                body = render_doc(path.removeprefix("/docs/"))
                if body:
                    return self._send(HTTPStatus.OK, body)
            self._send(HTTPStatus.NOT_FOUND, _page("404", "<p>Nicht gefunden.</p>"))

        def log_message(self, fmt, *args):  # one line per request, no noise from health checks
            if not self.path.startswith("/healthz"):
                sys.stderr.write(f"[{time.strftime('%Y-%m-%dT%H:%M:%S')}] {fmt % args}\n")

    return Handler


def main() -> None:
    p = argparse.ArgumentParser(description="Read-only web view of the price history")
    p.add_argument("--host", default=os.environ.get("WEB_HOST", "0.0.0.0"))
    p.add_argument("--port", type=int, default=int(os.environ.get("WEB_PORT", "8080")))
    p.add_argument("--db", default=None, help="path to the SQLite file")
    args = p.parse_args()

    db = Path(args.db) if args.db else None
    cache = ScenarioCache(db)
    cache.refresh_if_stale()
    server = ThreadingHTTPServer((args.host, args.port), make_handler(db, cache))
    print(f"listening on {args.host}:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
