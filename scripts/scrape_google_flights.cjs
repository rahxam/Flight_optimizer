#!/usr/bin/env node
/**
 * Google-Flights-Scraper (Playwright/Chromium).
 *
 *   node scripts/scrape_google_flights.cjs data/prices/_queries.json data/prices/scraped.csv
 *   node scripts/scrape_google_flights.cjs --verify            # eine Suche pruefen
 *   node scripts/scrape_google_flights.cjs <json> <csv> --headed --limit 20 --delay 7
 *
 * Schreibt inkrementell: ein Abbruch verliert nichts, ein Neustart ueberspringt,
 * was schon in der CSV steht.
 *
 * WICHTIG: Google Flights hat keine offizielle API. Scraping verstoesst gegen die
 * ToS und die Seitenstruktur aendert sich ohne Vorwarnung. Fuer eine private
 * Reiseplanung in kleinem Volumen vertretbar - halte die Rate niedrig. Bei einem
 * Captcha bricht das Skript ab, statt weiterzuhaemmern.
 */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const CSV_HEADER = [
  'origin', 'destination', 'depart_date', 'return_date', 'trip_type', 'price_eur',
  'carrier', 'stops', 'duration_min', 'source', 'url', 'itinerary_id', 'leg_index',
].join(',');

const CONSENT_LABELS = ['Alle akzeptieren', 'Accept all', 'Ich stimme zu', 'I agree', 'Alle ablehnen'];
const CARRIER_RE = new RegExp(
  '^(Qatar Airways|Emirates|Turkish Airlines|Etihad Airways|Iberia|AirAsia X?|Air Asia|' +
  'Singapore Airlines|SriLankan Airlines|Vietnam Airlines|Malaysia Airlines|Lufthansa|KLM|' +
  'Air France|Oman Air|IndiGo|Thai Airways|Thai AirAsia|China Southern|China Airlines|' +
  'China Eastern|EVA Air|Garuda Indonesia|Scoot|Batik Air|VietJet Air|Air India|Gulf Air|' +
  'Saudia|Etihad|Swiss|Austrian|Vueling|Ryanair|Binter.*|Canaryfly|Air Europa|Royal Jordanian|' +
  'Himalaya Airlines|Nepal Airlines|Cathay Pacific|Korean Air|Japan Airlines|ANA|Sichuan Airlines)$'
);

function parsePrice(line) {
  const m = line.match(/(?:€|EUR)\s*([\d., \s]{2,12})|([\d., \s]{2,12})\s*(?:€|EUR)/);
  if (!m) return null;
  let raw = (m[1] || m[2] || '').replace(/[\s  ]/g, '');
  if (raw.includes(',') && raw.includes('.')) {
    raw = raw.lastIndexOf(',') > raw.lastIndexOf('.')
      ? raw.replace(/\./g, '').replace(',', '.')
      : raw.replace(/,/g, '');
  } else if (raw.includes(',')) {
    const dec = raw.split(',').pop();
    raw = dec.length === 2 ? raw.replace(',', '.') : raw.replace(/,/g, '');
  } else if (raw.includes('.')) {
    const dec = raw.split('.').pop();
    if (dec.length === 3) raw = raw.replace(/\./g, '');
  }
  const value = parseFloat(raw);
  return Number.isFinite(value) ? value : null;
}

function parseDuration(text) {
  const m = text.match(/(\d+)\s*(?:h|Std\.?)(?:[^\d]{0,4}(\d+)\s*(?:m|Min\.?))?/i);
  if (!m) return '';
  const total = parseInt(m[1], 10) * 60 + (m[2] ? parseInt(m[2], 10) : 0);
  return total > 0 ? String(total) : '';
}

function parseStops(text) {
  if (/\b(Nonstop|Direkt(flug)?|Direct)\b/i.test(text)) return '0';
  const m = text.match(/(\d+)\s*(?:Zwischenstopp|Stopps?|stops?)/i);
  return m ? m[1] : '';
}

function csvEscape(value) {
  const s = value === null || value === undefined ? '' : String(value);
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

async function dismissConsent(page) {
  for (const label of CONSENT_LABELS) {
    try {
      const btn = page.getByRole('button', { name: label });
      if (await btn.count()) {
        await btn.first().click({ timeout: 4000 });
        await page.waitForTimeout(1200);
        return;
      }
    } catch { /* weiter zum naechsten Label */ }
  }
}

/** Liest zurueck, welche Strecke Google aus dem tfs-Parameter verstanden hat. */
async function readBackRoute(page) {
  try {
    const values = await page.$$eval(
      'input[aria-label], div[role="combobox"] input',
      (nodes) => nodes.map((n) => n.value).filter(Boolean).slice(0, 6)
    );
    return values.join(' | ');
  } catch {
    return '';
  }
}

async function scrapeOne(page, query, opts) {
  await page.goto(query.url, { waitUntil: 'domcontentloaded', timeout: opts.timeout });
  await dismissConsent(page);
  try {
    await page.waitForSelector('li[class*="pIav2d"], ul li div[role="button"], [aria-label*="€"]',
      { timeout: opts.timeout });
  } catch {
    await page.waitForTimeout(6000);
  }
  const body = await page.innerText('body');
  if (/captcha|ungew(ö|oe)hnlichen Datenverkehr|unusual traffic|sorry\/index/i.test(body)) {
    throw new Error('CAPTCHA');
  }
  const readBack = await readBackRoute(page);

  const lines = body.split('\n').map((l) => l.trim()).filter(Boolean);
  const offers = [];
  const window = [];
  for (const line of lines) {
    window.push(line);
    if (window.length > 14) window.shift();
    const price = parsePrice(line);
    if (price === null || price < 40 || price > 25000) continue;
    const context = window.join('\n');
    const carrier = window.slice().reverse().find((w) => CARRIER_RE.test(w)) || '';
    offers.push({
      price_eur: price,
      carrier,
      stops: parseStops(context),
      duration_min: parseDuration(context),
    });
    if (offers.length >= opts.maxOffers) break;
  }
  return { offers, readBack };
}

async function main() {
  const args = process.argv.slice(2);
  const flags = new Set(args.filter((a) => a.startsWith('--')));
  const positional = args.filter((a) => !a.startsWith('--'));
  const getOpt = (name, fallback) => {
    const i = args.indexOf(`--${name}`);
    return i >= 0 && args[i + 1] ? args[i + 1] : fallback;
  };

  const opts = {
    timeout: 45000,
    maxOffers: parseInt(getOpt('max-offers', '6'), 10),
    delay: parseFloat(getOpt('delay', '6')) * 1000,
    limit: parseInt(getOpt('limit', '0'), 10),
    headless: !flags.has('--headed'),
  };

  if (flags.has('--verify')) {
    const url = positional[0] || 'https://www.google.com/travel/flights?tfs='
      + 'GhoSCjIwMjctMDMtMThqBRIDTUFEcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR';
    const browser = await chromium.launch({ headless: opts.headless });
    const page = await browser.newContext({ locale: 'de-DE', timezoneId: 'Atlantic/Canary' })
      .then((c) => c.newPage());
    const { offers, readBack } = await scrapeOne(page, { url }, opts);
    console.log('Google hat verstanden:', readBack || '(keine Eingabefelder gelesen)');
    console.log('Gefundene Angebote:', JSON.stringify(offers, null, 2));
    console.log('\nPruefe, ob die Strecke oben der erwarteten entspricht. Wenn nicht,');
    console.log('ist die tfs-Kodierung in src/workation/scrape/urls.py veraltet.');
    await browser.close();
    return;
  }

  const queriesPath = positional[0] || 'data/prices/_queries.json';
  const outPath = positional[1] || 'data/prices/scraped.csv';
  const queries = JSON.parse(fs.readFileSync(queriesPath, 'utf8'));

  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  const done = new Set();
  if (fs.existsSync(outPath)) {
    const text = fs.readFileSync(outPath, 'utf8').split('\n').slice(1);
    for (const row of text) {
      const cells = row.split(',');
      if (cells.length > 12) done.add(cells[11] || `${cells[0]}|${cells[1]}|${cells[2]}|${cells[4]}`);
    }
  } else {
    fs.writeFileSync(outPath, CSV_HEADER + '\n');
  }

  const browser = await chromium.launch({ headless: opts.headless });
  const context = await browser.newContext({
    locale: 'de-DE',
    timezoneId: 'Atlantic/Canary',
    viewport: { width: 1440, height: 1000 },
  });

  let written = 0;
  let processed = 0;
  let firstReadBack = '';
  const todo = queries.filter((q) => !done.has(q.id));
  const slice = opts.limit > 0 ? todo.slice(0, opts.limit) : todo;
  console.log(`${queries.length} Suchen in der Matrix, ${slice.length} offen.`);

  for (const query of slice) {
    processed += 1;
    const page = await context.newPage();
    const label = query.legs.map((l) => `${l[0]}->${l[1]} ${l[2]}`).join(' / ');
    try {
      const { offers, readBack } = await scrapeOne(page, query, opts);
      if (!firstReadBack) {
        firstReadBack = readBack;
        console.log(`  [Selbsttest] Google verstand die erste Suche als: ${readBack || '?'}`);
      }
      const rows = offers.map((o, i) => [
        query.legs[0][0],
        query.trip_type === 'return' ? query.legs[0][1] : query.legs[0][1],
        query.legs[0][2],
        query.trip_type === 'return' ? query.legs[query.legs.length - 1][2] : '',
        query.trip_type,
        o.price_eur,
        o.carrier,
        o.stops,
        o.duration_min,
        'google_flights',
        query.url,
        query.id,
        i,
      ].map(csvEscape).join(','));
      if (rows.length) {
        fs.appendFileSync(outPath, rows.join('\n') + '\n');
        written += rows.length;
      }
      const cheapest = offers.length ? Math.min(...offers.map((o) => o.price_eur)) : null;
      console.log(
        `  [${processed}/${slice.length}] ${query.id} ${label} -> ` +
        (cheapest === null ? 'keine Preise gefunden' : `ab ${cheapest} € (${offers.length} Angebote)`)
      );
    } catch (err) {
      if (err.message === 'CAPTCHA') {
        console.error('\nABBRUCH: Google zeigt ein Captcha. Warte ein paar Stunden, erhoehe --delay');
        console.error('oder erfasse die restlichen Preise manuell (data/prices/manual.csv).');
        await page.close();
        break;
      }
      console.error(`  [${processed}/${slice.length}] ${query.id} ${label} -> FEHLER: ${err.message}`);
    } finally {
      await page.close();
    }
    await new Promise((r) => setTimeout(r, opts.delay * (0.75 + Math.random() * 0.5)));
  }

  await browser.close();
  console.log(`\nFertig: ${written} Preiszeilen in ${outPath}`);
  console.log('Weiter mit: python3 scripts/plan.py report --profile surf');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
