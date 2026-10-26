#!/usr/bin/env bash
# Dauerbetrieb: regelmaessig einen Teil der Query-Matrix abfragen, in die
# SQLite-Historie einlesen und melden, was auffaellig ist.
#
# Bewusst eine Shell-Schleife statt cron: ein Container mit cron verschluckt
# Logs und Exitcodes, und hier soll jeder Lauf sichtbar sein.
set -uo pipefail

: "${INTERVAL_HOURS:=12}"        # Abstand zwischen zwei Laeufen
: "${QUERIES_PER_RUN:=120}"      # Suchen pro Lauf (bei 7 s Pause ca. 15 min)
: "${DELAY_SECONDS:=7}"          # Pause zwischen den Abfragen
: "${DEAL_DROP_PCT:=15}"         # ab welchem Einbruch gemeldet wird
: "${JITTER_MINUTES:=20}"        # Zufallsversatz, damit die Laeufe nicht im Takt liegen
: "${RUN_ONCE:=0}"               # 1 = nur ein Lauf, dann beenden
: "${MATRIX_ARGS:=--from-scenarios --with-candidates --calendar}"

QUERIES=/app/data/prices/_queries.json
RAW_DIR=/app/data/prices/raw
mkdir -p "$RAW_DIR"

log() { printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"; }

# Matrices from before the calendar mode have no "calendar" field - rebuild those.
if [ ! -f "$QUERIES" ] || ! grep -q '"calendar"' "$QUERIES"; then
  log "Query-Matrix fehlt oder ist veraltet, erzeuge sie neu ($MATRIX_ARGS)"
  # shellcheck disable=SC2086
  python3 /app/scripts/plan.py scrape-matrix $MATRIX_ARGS \
    || { log "FEHLER beim Erzeugen der Matrix"; exit 1; }
fi

while true; do
  STAMP=$(date -u +%Y%m%dT%H%M%SZ)
  OUT="$RAW_DIR/scrape-$STAMP.rpc.jsonl"

  log "Scrape-Lauf startet: $QUERIES_PER_RUN Suchen, $DELAY_SECONDS s Pause"
  node /app/scripts/scrape_google_flights.cjs "$QUERIES" "$OUT" \
       --shuffle --limit "$QUERIES_PER_RUN" --delay "$DELAY_SECONDS" &
  SCRAPER=$!
  # A run takes ~40 min; read in what is there every few minutes so the web
  # view fills up during the run. Ingesting the same file again is harmless.
  while kill -0 "$SCRAPER" 2>/dev/null; do
    sleep "${INGEST_EVERY_SECONDS:-300}" &
    wait $! 2>/dev/null
    [ -s "$OUT" ] && python3 /app/scripts/track.py ingest-capture "$OUT" >/dev/null 2>&1
  done
  if wait "$SCRAPER"; then
    log "Scrape fertig"
  else
    log "WARNUNG: Scraper mit Fehler beendet (abgelehnt, Captcha oder Netzproblem) - Teildaten werden trotzdem verwertet"
  fi

  if [ -s "$OUT" ]; then
    python3 /app/scripts/track.py ingest-capture "$OUT" || log "WARNUNG: Ingest fehlgeschlagen"
  else
    log "WARNUNG: keine Zeilen erfasst"
  fi

  log "--- Allzeittiefs ---"
  python3 /app/scripts/track.py lows --top 15 || true
  log "--- Preiseinbrueche (>= ${DEAL_DROP_PCT}%) ---"
  python3 /app/scripts/track.py deals --drop "$DEAL_DROP_PCT" --top 15 || true
  log "--- Stand der Historie ---"
  python3 /app/scripts/track.py status || true

  if [ "$RUN_ONCE" = "1" ]; then
    log "RUN_ONCE gesetzt - beende"
    exit 0
  fi

  JITTER=$(( RANDOM % (JITTER_MINUTES * 60 + 1) ))
  SLEEP=$(( INTERVAL_HOURS * 3600 + JITTER ))
  log "naechster Lauf in $(( SLEEP / 60 )) Minuten"
  sleep "$SLEEP"
done
