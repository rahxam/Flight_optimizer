"""Preishistorie in SQLite: ueber Monate beobachten, Bestpreise und Deals finden.

Warum eine Datenbank und nicht nur CSVs: wenn ueber Monate hinweg zweimal
taeglich dieselben 500 Strecken abgefragt werden, sind das schnell Millionen
Zeilen. Interessant sind daran drei Fragen, und alle drei brauchen Historie:

  1. Was war auf dieser Strecke an diesem Datum ueberhaupt JE zu holen?
     -> `best_prices()`. Das ist die realistische Planungsgrundlage.
  2. Ist der aktuelle Preis gut, oder nur normal?
     -> `deals()` vergleicht den neuesten Preis mit dem Median der letzten
        Wochen und meldet echte Einbrueche.
  3. Ist jetzt ein Allzeittief?
     -> `all_time_lows()`. Das ist das Kaufsignal.

Die CSVs der Scrape-Laeufe bleiben als Rohdaten liegen; diese Datenbank ist der
abgeleitete, abfragbare Zustand. `ingest_csv()` ist idempotent.
"""

from __future__ import annotations

import csv
import datetime as dt
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from .data import DATA_DIR
from .models import PriceQuote

DEFAULT_DB = DATA_DIR / "prices" / "history.sqlite3"

SCHEMA = """
CREATE TABLE IF NOT EXISTS observations (
    id            INTEGER PRIMARY KEY,
    scraped_at    TEXT NOT NULL,
    origin        TEXT NOT NULL,
    destination   TEXT NOT NULL,
    depart_date   TEXT NOT NULL,
    return_date   TEXT NOT NULL DEFAULT '',
    trip_type     TEXT NOT NULL DEFAULT 'oneway',
    price_eur     REAL NOT NULL,
    carrier       TEXT NOT NULL DEFAULT '',
    stops         INTEGER,
    duration_min  INTEGER,
    source        TEXT NOT NULL DEFAULT '',
    query_id      TEXT NOT NULL DEFAULT '',
    url           TEXT NOT NULL DEFAULT '',
    UNIQUE (scraped_at, origin, destination, depart_date, return_date,
            trip_type, price_eur, carrier)
);

CREATE INDEX IF NOT EXISTS idx_obs_route
    ON observations (origin, destination, depart_date, trip_type);
CREATE INDEX IF NOT EXISTS idx_obs_time
    ON observations (scraped_at);

CREATE TABLE IF NOT EXISTS runs (
    id          INTEGER PRIMARY KEY,
    started_at  TEXT NOT NULL,
    finished_at TEXT,
    queries     INTEGER DEFAULT 0,
    rows        INTEGER DEFAULT 0,
    status      TEXT DEFAULT 'running',
    note        TEXT DEFAULT ''
);
"""


@contextmanager
def connect(db: Path | None = None):
    path = Path(db or DEFAULT_DB)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        conn.executescript(SCHEMA)
        yield conn
        conn.commit()
    finally:
        conn.close()


# --------------------------------------------------------------------------- #
# Schreiben
# --------------------------------------------------------------------------- #
def ingest_csv(csv_path: Path, db: Path | None = None, scraped_at: str | None = None) -> int:
    """Eine Scrape-CSV in die Historie uebernehmen. Mehrfaches Einlesen ist gefahrlos."""
    csv_path = Path(csv_path)
    if not csv_path.exists():
        return 0
    stamp = scraped_at or dt.datetime.fromtimestamp(
        csv_path.stat().st_mtime, dt.timezone.utc
    ).isoformat(timespec="seconds")
    inserted = 0
    with connect(db) as conn, open(csv_path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if not (row.get("origin") and row.get("destination") and row.get("depart_date")):
                continue
            try:
                price = float(str(row["price_eur"]).replace(",", "."))
            except (KeyError, TypeError, ValueError):
                continue
            cur = conn.execute(
                """INSERT OR IGNORE INTO observations
                   (scraped_at, origin, destination, depart_date, return_date, trip_type,
                    price_eur, carrier, stops, duration_min, source, query_id, url)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    row.get("scraped_at") or stamp,
                    row["origin"].strip().upper(),
                    row["destination"].strip().upper(),
                    row["depart_date"].strip(),
                    (row.get("return_date") or "").strip(),
                    (row.get("trip_type") or "oneway").strip(),
                    price,
                    (row.get("carrier") or "").strip(),
                    int(row["stops"]) if (row.get("stops") or "").strip() else None,
                    int(row["duration_min"]) if (row.get("duration_min") or "").strip() else None,
                    (row.get("source") or "google_flights").strip(),
                    (row.get("itinerary_id") or row.get("query_id") or "").strip(),
                    (row.get("url") or "").strip(),
                ),
            )
            inserted += cur.rowcount
    return inserted


def start_run(note: str = "", db: Path | None = None) -> int:
    with connect(db) as conn:
        cur = conn.execute(
            "INSERT INTO runs (started_at, note) VALUES (?, ?)",
            (dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), note),
        )
        return int(cur.lastrowid)


def finish_run(
    run_id: int, queries: int, rows: int, status: str = "ok", db: Path | None = None
) -> None:
    with connect(db) as conn:
        conn.execute(
            """UPDATE runs SET finished_at = ?, queries = ?, rows = ?, status = ?
               WHERE id = ?""",
            (
                dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                queries,
                rows,
                status,
                run_id,
            ),
        )


# --------------------------------------------------------------------------- #
# Lesen
# --------------------------------------------------------------------------- #
@dataclass
class RouteStat:
    origin: str
    destination: str
    depart_date: str
    trip_type: str
    best_eur: float
    best_seen_at: str
    latest_eur: float
    latest_seen_at: str
    median_eur: float
    observations: int

    @property
    def latest_vs_best_pct(self) -> float:
        if not self.best_eur:
            return 0.0
        return (self.latest_eur - self.best_eur) / self.best_eur * 100

    @property
    def latest_vs_median_pct(self) -> float:
        if not self.median_eur:
            return 0.0
        return (self.latest_eur - self.median_eur) / self.median_eur * 100


_STAT_SQL = """
WITH ranked AS (
    SELECT origin, destination, depart_date, trip_type, price_eur, scraped_at,
           ROW_NUMBER() OVER (
               PARTITION BY origin, destination, depart_date, trip_type
               ORDER BY scraped_at DESC, price_eur ASC) AS recency,
           ROW_NUMBER() OVER (
               PARTITION BY origin, destination, depart_date, trip_type
               ORDER BY price_eur ASC, scraped_at ASC) AS cheapness,
           COUNT(*) OVER (
               PARTITION BY origin, destination, depart_date, trip_type) AS n,
           ROW_NUMBER() OVER (
               PARTITION BY origin, destination, depart_date, trip_type
               ORDER BY price_eur) AS price_rank
    FROM observations
    WHERE depart_date >= :min_date
)
SELECT origin, destination, depart_date, trip_type,
       MIN(CASE WHEN cheapness = 1 THEN price_eur END)   AS best_eur,
       MIN(CASE WHEN cheapness = 1 THEN scraped_at END)  AS best_seen_at,
       MIN(CASE WHEN recency  = 1 THEN price_eur END)    AS latest_eur,
       MIN(CASE WHEN recency  = 1 THEN scraped_at END)   AS latest_seen_at,
       AVG(CASE WHEN price_rank IN ((n + 1) / 2, (n + 2) / 2) THEN price_eur END)
                                                         AS median_eur,
       MAX(n)                                            AS observations
FROM ranked
GROUP BY origin, destination, depart_date, trip_type
"""


def route_stats(
    db: Path | None = None, min_date: str = "2027-01-01", min_observations: int = 1
) -> list[RouteStat]:
    with connect(db) as conn:
        rows = conn.execute(_STAT_SQL, {"min_date": min_date}).fetchall()
    out = [
        RouteStat(
            origin=r["origin"],
            destination=r["destination"],
            depart_date=r["depart_date"],
            trip_type=r["trip_type"],
            best_eur=r["best_eur"],
            best_seen_at=r["best_seen_at"],
            latest_eur=r["latest_eur"],
            latest_seen_at=r["latest_seen_at"],
            median_eur=r["median_eur"] or r["latest_eur"],
            observations=r["observations"],
        )
        for r in rows
        if r["best_eur"] is not None
    ]
    return [s for s in out if s.observations >= min_observations]


def deals(
    db: Path | None = None, min_drop_pct: float = 15.0, min_observations: int = 4
) -> list[RouteStat]:
    """Strecken, deren neuester Preis deutlich unter dem eigenen Median liegt."""
    stats = route_stats(db, min_observations=min_observations)
    hits = [s for s in stats if s.latest_vs_median_pct <= -min_drop_pct]
    return sorted(hits, key=lambda s: s.latest_vs_median_pct)


def all_time_lows(db: Path | None = None, min_observations: int = 4) -> list[RouteStat]:
    """Strecken, die gerade auf ihrem beobachteten Allzeittief stehen - das Kaufsignal."""
    stats = route_stats(db, min_observations=min_observations)
    hits = [s for s in stats if s.latest_eur <= s.best_eur + 0.01]
    return sorted(hits, key=lambda s: s.latest_vs_median_pct)


def coverage(db: Path | None = None) -> dict:
    with connect(db) as conn:
        row = conn.execute(
            """SELECT COUNT(*) AS observations,
                      COUNT(DISTINCT origin || destination || depart_date) AS route_dates,
                      MIN(scraped_at) AS first_seen,
                      MAX(scraped_at) AS last_seen
               FROM observations"""
        ).fetchone()
        runs = conn.execute(
            "SELECT COUNT(*) AS n, SUM(rows) AS rows FROM runs WHERE status = 'ok'"
        ).fetchone()
    return {
        "observations": row["observations"] or 0,
        "route_dates": row["route_dates"] or 0,
        "first_seen": row["first_seen"],
        "last_seen": row["last_seen"],
        "runs": runs["n"] or 0,
    }


def to_quotes(db: Path | None = None, mode: str = "latest") -> list[PriceQuote]:
    """Historie in Angebote fuer den PriceBook umwandeln.

    mode='latest' = was aktuell buchbar ist (Default, fuer Buchungsentscheidungen)
    mode='best'   = was je zu holen war (fuer die Frage, welche Route ueberhaupt
                    realistisch ist, wenn man geduldig beobachtet)
    """
    if mode not in ("latest", "best"):
        raise ValueError("mode muss 'latest' oder 'best' sein")
    quotes: list[PriceQuote] = []
    for stat in route_stats(db):
        price = stat.best_eur if mode == "best" else stat.latest_eur
        quotes.append(
            PriceQuote(
                origin=stat.origin,
                destination=stat.destination,
                depart_date=dt.date.fromisoformat(stat.depart_date),
                price_eur=price,
                trip_type=stat.trip_type,
                source=f"history_{mode}",
            )
        )
    return quotes
