"""Google-Flights-Scraper auf Basis des vorinstallierten Playwright-Chromium.

Hinweise, bevor du das laufen laesst:
  * Google Flights hat keine offizielle API; Scraping verstoesst gegen die ToS
    und die Seitenstruktur aendert sich ohne Vorwarnung. Fuer eine private
    Reiseplanung in kleinem Volumen ist das vertretbar, fuer mehr nicht.
  * Halte die Abfragerate niedrig (Default: 4-8 s Pause). Bei Captchas/429
    bricht der Scraper ab, statt stur weiterzulaufen.
  * Alternative ohne eigenen Browser: SerpApi (bezahlt) oder die Preise von
    Hand in eine CSV nach dem Schema in data/prices/_SCHEMA.csv eintragen.
"""

from __future__ import annotations

import csv
import datetime as dt
import random
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from .urls import TRIP_MULTICITY, TRIP_ONEWAY, TRIP_ROUND, google_flights_url

PRICE_RE = re.compile(r"(\d[\d\s.,]{1,9})\s*(?:€|EUR)|(?:€|EUR)\s*(\d[\d\s.,]{1,9})")
DURATION_RE = re.compile(r"(?:(\d+)\s*(?:h|Std))(?:[^\d]{0,4}(\d+)\s*(?:m|Min))?", re.I)
STOPS_RE = re.compile(r"(Nonstop|Direkt|(\d+)\s*(?:Stopp|Zwischenstopp|stop))", re.I)


@dataclass
class ScrapeResult:
    origin: str
    destination: str
    depart_date: str
    return_date: str
    trip_type: str
    price_eur: float
    carrier: str
    stops: int | None
    duration_min: int | None
    source: str
    url: str
    itinerary_id: str
    leg_index: int


def _parse_price(text: str) -> float | None:
    match = PRICE_RE.search(text)
    if not match:
        return None
    raw = (match.group(1) or match.group(2) or "").strip()
    raw = raw.replace(" ", "").replace(" ", "").replace("\xa0", "")
    # Deutsche Notation: 1.234,56 -> 1234.56 ; englische: 1,234.56
    if "," in raw and "." in raw:
        raw = raw.replace(".", "").replace(",", ".") if raw.rfind(",") > raw.rfind(".") else raw.replace(",", "")
    elif "," in raw:
        raw = raw.replace(",", "." if len(raw.split(",")[-1]) == 2 else "")
    else:
        raw = raw.replace(".", "") if raw.count(".") == 1 and len(raw.split(".")[-1]) == 3 else raw
    try:
        return float(raw)
    except ValueError:
        return None


def _parse_duration(text: str) -> int | None:
    match = DURATION_RE.search(text)
    if not match:
        return None
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    return hours * 60 + minutes or None


def _parse_stops(text: str) -> int | None:
    match = STOPS_RE.search(text)
    if not match:
        return None
    if match.group(2):
        return int(match.group(2))
    return 0


class GoogleFlightsScraper:
    def __init__(
        self,
        headless: bool = True,
        min_delay: float = 4.0,
        max_delay: float = 8.0,
        timeout_ms: int = 45_000,
        max_offers_per_query: int = 6,
        locale: str = "de-DE",
        currency: str = "EUR",
    ):
        self.headless = headless
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.timeout_ms = timeout_ms
        self.max_offers = max_offers_per_query
        self.locale = locale
        self.currency = currency
        self._pw = None
        self._browser = None
        self._context = None

    # ------------------------------------------------------------------ #
    def __enter__(self) -> "GoogleFlightsScraper":
        from playwright.sync_api import sync_playwright

        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch(headless=self.headless)
        self._context = self._browser.new_context(
            locale=self.locale,
            timezone_id="Atlantic/Canary",
            viewport={"width": 1440, "height": 1000},
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
            ),
        )
        return self

    def __exit__(self, *exc) -> None:
        for obj in (self._context, self._browser):
            if obj:
                obj.close()
        if self._pw:
            self._pw.stop()

    # ------------------------------------------------------------------ #
    def _accept_consent(self, page) -> None:
        for label in ("Alle akzeptieren", "Accept all", "Ich stimme zu", "I agree"):
            try:
                btn = page.get_by_role("button", name=label)
                if btn.count():
                    btn.first.click(timeout=4000)
                    page.wait_for_timeout(1200)
                    return
            except Exception:
                continue

    def _fetch(self, url: str) -> str:
        page = self._context.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
            self._accept_consent(page)
            # Ergebnisliste abwarten; Google rendert sie als <li> in einer Rolle "list".
            try:
                page.wait_for_selector("li[class*='pIav2d'], ul li div[role='button']", timeout=self.timeout_ms)
            except Exception:
                page.wait_for_timeout(5000)
            body = page.inner_text("body")
            if re.search(r"captcha|ungewoehnlichen Datenverkehr|unusual traffic", body, re.I):
                raise RuntimeError(
                    "Google zeigt ein Captcha / blockt den Traffic. Scraper anhalten, "
                    "Pause erhoehen oder Preise manuell erfassen."
                )
            return body
        finally:
            page.close()

    # ------------------------------------------------------------------ #
    def scrape(
        self,
        legs: list[tuple[str, str, dt.date]],
        trip_type: str,
        adults: int = 2,
        itinerary_id: str = "",
    ) -> list[ScrapeResult]:
        trip = {"oneway": TRIP_ONEWAY, "return": TRIP_ROUND, "multicity": TRIP_MULTICITY}[trip_type]
        url = google_flights_url(legs, trip, adults=adults, currency=self.currency)
        body = self._fetch(url)

        results: list[ScrapeResult] = []
        # Jede Ergebniszeile enthaelt Dauer, Stopps und Preis - wir schneiden
        # den Text an den Preisvorkommen und lesen den Kontext davor aus.
        lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
        window: list[str] = []
        for line in lines:
            window.append(line)
            if len(window) > 14:
                window.pop(0)
            price = _parse_price(line)
            if price is None or not (40 <= price <= 20_000):
                continue
            context = "\n".join(window)
            carrier = next(
                (
                    w
                    for w in window
                    if re.fullmatch(
                        r"(Qatar Airways|Emirates|Turkish Airlines|Etihad.*|Iberia|AirAsia|"
                        r"Singapore Airlines|SriLankan.*|Vietnam Airlines|Malaysia Airlines|"
                        r"Lufthansa|KLM|Air France|Oman Air|IndiGo|Thai.*|China.*|EVA Air|"
                        r"Garuda.*|Scoot|Batik Air|Vietjet.*)",
                        w.strip(),
                    )
                ),
                "",
            )
            results.append(
                ScrapeResult(
                    origin=legs[0][0],
                    destination=legs[-1][1] if trip_type == "return" else legs[0][1],
                    depart_date=legs[0][2].isoformat(),
                    return_date=legs[-1][2].isoformat() if trip_type == "return" else "",
                    trip_type=trip_type,
                    price_eur=price,
                    carrier=carrier,
                    stops=_parse_stops(context),
                    duration_min=_parse_duration(context),
                    source="google_flights",
                    url=url,
                    itinerary_id=itinerary_id,
                    leg_index=0,
                )
            )
            if len(results) >= self.max_offers:
                break

        time.sleep(random.uniform(self.min_delay, self.max_delay))
        return results

    # ------------------------------------------------------------------ #
    def scrape_matrix(self, queries: list[dict], out_csv: Path) -> int:
        """Arbeitet eine Query-Matrix ab und schreibt inkrementell in die CSV."""
        fields = list(ScrapeResult.__dataclass_fields__)
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        existing = set()
        if out_csv.exists():
            with open(out_csv, newline="", encoding="utf-8") as fh:
                for row in csv.DictReader(fh):
                    existing.add((row["origin"], row["destination"], row["depart_date"], row["trip_type"]))
        written = 0
        with open(out_csv, "a", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields)
            if out_csv.stat().st_size == 0:
                writer.writeheader()
            for query in queries:
                legs = [(o, d, dt.date.fromisoformat(day)) for o, d, day in query["legs"]]
                key = (legs[0][0], legs[0][1], legs[0][2].isoformat(), query["trip_type"])
                if key in existing and query["trip_type"] != "multicity":
                    continue
                try:
                    for res in self.scrape(
                        legs,
                        query["trip_type"],
                        adults=query.get("adults", 2),
                        itinerary_id=query.get("id", ""),
                    ):
                        writer.writerow(asdict(res))
                        written += 1
                    fh.flush()
                except RuntimeError:
                    raise
                except Exception as exc:  # einzelne Query darf den Lauf nicht killen
                    print(f"  ! {key}: {type(exc).__name__}: {exc}")
        return written
