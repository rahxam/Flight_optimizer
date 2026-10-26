#!/usr/bin/env node
/**
 * Google-Flights-Scraper (Playwright/Chromium).
 *
 *   node scripts/scrape_google_flights.cjs data/prices/_queries.json out.rpc.jsonl
 *   node scripts/scrape_google_flights.cjs --verify            # eine Suche pruefen
 *
 * The page is loaded like in a normal browser, and the scraper records the
 * Flights RPCs the page makes itself (GetShoppingResults, GetCalendarGraph,
 * GetCalendarGrid, GetCalendarPicker) into a JSONL file. Those calls cannot be
 * replayed directly: each carries a BotGuard token bound to its body. Parsing
 * happens in Python (src/workation/scrape/gf_rpc.py):
 *
 *   python3 scripts/track.py ingest-capture out.rpc.jsonl
 *
 * Flags:
 *   --limit N     nur N Suchen in diesem Lauf (fuer kurze, regelmaessige Laeufe)
 *   --shuffle     Reihenfolge zufaellig - ueber viele Laeufe deckt das alles ab
 *   --resume      Suchen ueberspringen, die in der Ziel-Datei schon stehen
 *   --delay S     Pause zwischen Abfragen in Sekunden (Default 6)
 *   --graph       zusaetzlich die Preisgrafik oeffnen (~60 Abflugtage pro Suche);
 *                 Suchen mit "calendar": true in der Matrix tun das immer
 *   --headed      sichtbarer Browser
 *
 * Schreibt inkrementell: ein Abbruch verliert nichts.
 *
 * WICHTIG: Google Flights hat keine offizielle API. Scraping verstoesst gegen die
 * ToS und die Seitenstruktur aendert sich ohne Vorwarnung. Fuer eine private
 * Reiseplanung in kleinem Volumen vertretbar - halte die Rate niedrig. Wenn
 * Google mehrere Suchen hintereinander ablehnt, bricht das Skript ab, statt
 * weiterzuhaemmern.
 */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const CONSENT_LABELS = ['Alle akzeptieren', 'Accept all', 'Ich stimme zu', 'I agree', 'Alle ablehnen'];
const GRAPH_LABELS = [/^Preisgrafik/i, /^Price graph/i];
const GRID_LABELS = [/^Datumsraster/i, /^Date grid/i];
const PRICED_RPC = /FlightsFrontendService\/(GetShoppingResults|GetCalendarGraph|GetCalendarGrid|GetCalendarPicker)/;
// Headless Chromium announces itself as "HeadlessChrome"; Google answers that
// with error 13 on most searches. A regular desktop UA avoids it.
const USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
  + '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36';
const MAX_BLOCKED_IN_A_ROW = 3;

const rpcName = (url) => url.split('?')[0].split('/').pop();
// Error 13 = the request was rejected (BotGuard); Google still answers 200.
const isRejected = (text) => /^\[\["wrb\.fr",null,null,null,null,\[13\b/m.test(text);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

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

// Runs inside the page: hands the response text of every finished Flights RPC
// (XHR or fetch) to window.__gfCapture. The page streams these responses, and
// Chromium drops the body before the DevTools protocol can read it - so it is
// taken from the page itself. The request body comes from Playwright, which
// has it reliably (the page sends it as FormData, not as a string).
const CAPTURE_HOOK = `(() => {
  const PRICED = ${PRICED_RPC.toString()};
  const send = (url, text) => { try { window.__gfCapture({ url, text: text || '' }); } catch (e) {} };
  const open = XMLHttpRequest.prototype.open;
  const xsend = XMLHttpRequest.prototype.send;
  XMLHttpRequest.prototype.open = function (method, url, ...rest) {
    this.__gfUrl = String(url);
    return open.call(this, method, url, ...rest);
  };
  XMLHttpRequest.prototype.send = function (body) {
    const url = this.__gfUrl ? new URL(this.__gfUrl, location.href).href : '';
    if (PRICED.test(url)) {
      this.addEventListener('loadend', () => send(url, this.responseText));
    }
    return xsend.call(this, body);
  };
  const origFetch = window.fetch;
  window.fetch = async function (input, init) {
    const response = await origFetch.apply(this, arguments);
    const url = typeof input === 'string' ? input : (input && input.url) || '';
    if (PRICED.test(url)) {
      response.clone().text().then((t) => send(new URL(url, location.href).href, t)).catch(() => {});
    }
    return response;
  };
})();`;

/** Records every priced RPC of a page; returns the list it appends to. */
async function recordRpcs(page, query, scrapedAt) {
  const calls = [];
  const bodies = new Map();
  page.on('request', (request) => {
    if (PRICED_RPC.test(request.url())) bodies.set(request.url(), request.postData() || '');
  });
  await page.exposeFunction('__gfCapture', ({ url, text }) => {
    const body = bodies.get(url) || '';
    calls.push({
      name: rpcName(url),
      text,
      record: {
        url,
        request_body: body,
        response: text,
        scraped_at: scrapedAt,
        query_id: query.id || '',
        page_url: query.url,
      },
    });
  });
  await page.addInitScript(CAPTURE_HOOK);
  return calls;
}

async function waitForCall(calls, name, from, timeout) {
  const deadline = Date.now() + timeout;
  while (Date.now() < deadline) {
    const hit = calls.slice(from).find((c) => c.name === name);
    if (hit) return hit;
    await sleep(250);
  }
  return null;
}

/** Clicks a calendar button (price graph / date grid) and waits for its RPC. */
async function openCalendar(page, calls, labels, rpc, opts) {
  for (const label of labels) {
    const btn = page.getByRole('button', { name: label });
    if (!(await btn.count())) continue;
    let hit = null;
    // A rejected calendar call (error 13) usually goes through on a second click.
    for (let attempt = 0; attempt < 2 && (!hit || isRejected(hit.text)); attempt += 1) {
      const from = calls.length;
      try {
        await btn.first().click({ timeout: 5000 });
      } catch {
        return hit;
      }
      hit = await waitForCall(calls, rpc, from, opts.timeout / 2);
      await page.keyboard.press('Escape').catch(() => {});
      await page.waitForTimeout(800 + attempt * 2500);
    }
    return hit;
  }
  return null;
}

async function scrapeOne(page, query, opts, scrapedAt) {
  const calls = await recordRpcs(page, query, scrapedAt);
  let shopping = null;
  for (let attempt = 0; attempt < 3; attempt += 1) {
    const from = calls.length;
    if (attempt === 0) {
      await page.goto(query.url, { waitUntil: 'domcontentloaded', timeout: opts.timeout });
      await dismissConsent(page);
    } else {
      await page.waitForTimeout(4000 + Math.random() * 4000);
      await page.reload({ waitUntil: 'domcontentloaded', timeout: opts.timeout });
    }
    shopping = await waitForCall(calls, 'GetShoppingResults', from, opts.timeout);
    if (shopping && !isRejected(shopping.text)) break;
    if (!shopping) {
      const body = await page.innerText('body').catch(() => '');
      if (/captcha|ungew(ö|oe)hnlichen Datenverkehr|unusual traffic|sorry\/index/i.test(body)) {
        throw new Error('CAPTCHA');
      }
    }
  }
  const blocked = !shopping || isRejected(shopping.text);
  const result = { blocked, readBack: await readBackRoute(page), graph: null, grid: null };

  if (!blocked) {
    // Results stream in; give the page a moment to finish the list.
    await page.waitForTimeout(2500);
    if (opts.graph || query.calendar) {
      result.graph = await openCalendar(page, calls, GRAPH_LABELS, 'GetCalendarGraph', opts);
      if (query.trip_type === 'return') {
        result.grid = await openCalendar(page, calls, GRID_LABELS, 'GetCalendarGrid', opts);
      }
    }
  }
  result.records = calls.filter((c) => c.record && c.text).map((c) => c.record);
  return result;
}

function describe(result) {
  if (result.blocked) return 'von Google abgelehnt';
  const parts = [];
  for (const rec of result.records) {
    const name = rpcName(rec.url).replace('GetCalendar', 'Kalender ').replace('GetShoppingResults', 'Liste');
    parts.push(`${name} ${isRejected(rec.response) ? 'abgelehnt' : `${Math.round(rec.response.length / 1024)} KB`}`);
  }
  return parts.join(', ') || 'keine Antwort';
}

async function newContext(browser) {
  return browser.newContext({
    locale: 'de-DE',
    timezoneId: 'Atlantic/Canary',
    viewport: { width: 1440, height: 1000 },
    userAgent: USER_AGENT,
  });
}

async function main() {
  const args = process.argv.slice(2);
  const flags = new Set(args.filter((a) => a.startsWith('--')));
  const getOpt = (name, fallback) => {
    const i = args.indexOf(`--${name}`);
    return i >= 0 && args[i + 1] ? args[i + 1] : fallback;
  };
  const valued = new Set(['--limit', '--delay']);
  const positional = args.filter((a, i) => !a.startsWith('--') && !valued.has(args[i - 1]));

  const opts = {
    timeout: 45000,
    delay: parseFloat(getOpt('delay', '6')) * 1000,
    limit: parseInt(getOpt('limit', '0'), 10),
    headless: !flags.has('--headed'),
    shuffle: flags.has('--shuffle'),
    resume: flags.has('--resume'),
    graph: flags.has('--graph'),
  };
  const launch = {
    headless: opts.headless,
    // Full Chromium in its new headless mode instead of the stripped
    // chromium-headless-shell Playwright uses by default - the shell is what
    // BotGuard recognises most easily.
    channel: 'chromium',
    args: ['--disable-blink-features=AutomationControlled'],
  };
  const startedAt = new Date().toISOString().replace(/\.\d+Z$/, 'Z');

  if (flags.has('--verify')) {
    const url = positional[0] || 'https://www.google.com/travel/flights?tfs='
      + 'GhoSCjIwMjctMDMtMThqBRIDTUFEcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR';
    const browser = await chromium.launch(launch);
    const page = await (await newContext(browser)).newPage();
    const result = await scrapeOne(page, { url, trip_type: 'oneway' }, { ...opts, graph: true }, startedAt);
    console.log('Google hat verstanden:', result.readBack || '(keine Eingabefelder gelesen)');
    console.log('Mitgeschnitten:', describe(result));
    const out = positional[1];
    if (out) {
      fs.writeFileSync(out, result.records.map((r) => JSON.stringify(r)).join('\n') + '\n');
      console.log(`Rohdaten in ${out} - auswerten mit: python3 scripts/track.py ingest-capture ${out}`);
    }
    console.log('\nPruefe, ob die Strecke oben der erwarteten entspricht. Wenn nicht,');
    console.log('ist die tfs-Kodierung in src/workation/scrape/urls.py veraltet.');
    await browser.close();
    return;
  }

  const queriesPath = positional[0] || 'data/prices/_queries.json';
  const outPath = positional[1] || 'data/prices/scraped.rpc.jsonl';
  const queries = JSON.parse(fs.readFileSync(queriesPath, 'utf8'));

  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  const done = new Set();
  if (opts.resume && fs.existsSync(outPath)) {
    for (const line of fs.readFileSync(outPath, 'utf8').split('\n')) {
      try { done.add(JSON.parse(line).query_id); } catch { /* leere Zeile */ }
    }
  }

  const browser = await chromium.launch(launch);
  const context = await newContext(browser);

  let calls = 0;
  let processed = 0;
  let blockedInARow = 0;
  let firstReadBack = '';
  const todo = queries.filter((q) => !done.has(q.id));
  if (opts.shuffle) {
    for (let i = todo.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [todo[i], todo[j]] = [todo[j], todo[i]];
    }
  }
  const slice = opts.limit > 0 ? todo.slice(0, opts.limit) : todo;
  console.log(
    `${queries.length} Suchen in der Matrix, ${slice.length} in diesem Lauf` +
    (opts.shuffle ? ' (zufaellige Auswahl)' : '') + '.'
  );

  let aborted = false;
  for (const query of slice) {
    processed += 1;
    const page = await context.newPage();
    const label = query.legs.map((l) => `${l[0]}->${l[1]} ${l[2]}`).join(' / ');
    try {
      const result = await scrapeOne(page, query, opts, startedAt);
      if (!firstReadBack && result.readBack) {
        firstReadBack = result.readBack;
        console.log(`  [Selbsttest] Google verstand die erste Suche als: ${result.readBack}`);
      }
      if (result.records.length) {
        fs.appendFileSync(outPath, result.records.map((r) => JSON.stringify(r)).join('\n') + '\n');
        calls += result.records.length;
      }
      console.log(`  [${processed}/${slice.length}] ${query.id} ${label} -> ${describe(result)}`);
      blockedInARow = result.blocked ? blockedInARow + 1 : 0;
      if (blockedInARow >= MAX_BLOCKED_IN_A_ROW) {
        console.error(`\nABBRUCH: Google hat ${blockedInARow} Suchen hintereinander abgelehnt.`);
        console.error('Der naechste Lauf versucht es wieder; bei Dauerablehnung --delay erhoehen.');
        aborted = true;
      }
    } catch (err) {
      if (err.message === 'CAPTCHA') {
        console.error('\nABBRUCH: Google zeigt ein Captcha. Warte ein paar Stunden, erhoehe --delay');
        console.error('oder erfasse die restlichen Preise manuell (data/prices/manual.csv).');
        aborted = true;
      } else {
        console.error(`  [${processed}/${slice.length}] ${query.id} ${label} -> FEHLER: ${err.message}`);
      }
    } finally {
      await page.close();
    }
    if (aborted) break;
    await sleep(opts.delay * (0.75 + Math.random() * 0.5));
  }

  await browser.close();
  console.log(`\nFertig: ${calls} mitgeschnittene Abfragen in ${outPath}`);
  console.log(`Weiter mit: python3 scripts/track.py ingest-capture ${outPath}`);
  if (aborted) process.exitCode = 2;
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
