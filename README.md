# Workation-Routenplaner 2027

Planungswerkzeug für eine 4–6-wöchige Workation zwischen Mitte März und Anfang Mai 2027,
für 2 Personen, ab Teneriffa. Es verbindet drei Dinge, die man sonst getrennt betrachtet:

1. **Saisonalität** – wann ist welches Ziel wirklich gut (Wetter, Longboard-Welle, Feiertage)?
2. **Flugpreise** – echte Google-Flights-Daten, inklusive Multi-City und Open-Jaw.
3. **Ausflüge** – Canyoning, Rafting, Trekking, Mehrtages-Bootstouren, nicht nur Surf.
4. **Arbeitsrealität** – Internet und Coworking, und vor allem: wo landet die
   Pflicht-Arbeitszeit 09–16 Uhr deutscher Zeit vor Ort? Ein späterer lokaler
   Start ist dabei ein Vorteil, kein Nachteil.

Daraus sucht der Optimierer Routen über 2–3 Ziele und sagt, wann welcher Block
wie lang sein soll – und wohin die Urlaubstage gehören. Dazu kommt ein
Dauerbetrieb-Teil, der über Monate Flugpreise beobachtet und Preiseinbrüche
meldet.

## Kernergebnis (Stand: nur Schätzpreise)

**Sri Lanka Südküste → Flores/Komodo → Lombok Süd, 18.03.–28.04.2027, je 14 Tage.**

| Posten | für zwei | pro Person |
|---|---|---|
| Flüge (MAD→CMB, CMB→LBJ, LBJ→LOP, LOP→MAD) | 2.562 € | **1.281 €** |
| vor Ort, 42 Tage | 3.994 € | 1.997 € |
| Visa | 160 € | 80 € |
| **Gesamt** | **6.716 €** | 3.358 € |

Score 8,24/Tag, 28 Tage mit longboardtauglicher Welle, drei Regionen mit je
mehreren Standorten. Das Flugbudget von 1.500 € pro Person ist damit nicht die
bindende Grenze.

Die Saison-Logik: Sri Lankas Südküste ist im März auf dem Höhepunkt und endet
Ende April mit dem SW-Monsun; Flores beginnt Anfang April seine Trockenzeit mit
der besten Tauchsicht; Lombok dreht Mitte April auf offshore. Jedes Ziel wird in
seinem eigenen Saisonfenster besucht.

Alternativen: **Flores/Komodo → Lombok** (nur 811 € Flug pro Person, 5.102 €
gesamt — eine Indonesien-Reise mit einem Inlandsflug in der Mitte),
**SL Süd → Nordvietnam → Lombok** (dichteste Ausflugsliste, kein Surf im
Vietnam-Block), **SL Süd → SL Ost → Lombok** (billigste Drei-Ziel-Variante,
Umzug innerhalb Sri Lankas per Auto).

Szenarienvergleich, Wochenplan und offene Punkte: [`docs/strategie.md`](docs/strategie.md).
Routen im Detail: [`docs/routenplan.md`](docs/routenplan.md).
Begründung je Ziel mit Quellen: [`docs/seasonality.md`](docs/seasonality.md).

## Schnellstart

```bash
# Routen suchen, ohne Ziele vorzugeben, mit Flugbudget als Grenze
python3 scripts/plan.py optimize --min-dest 2 --max-dest 3 --max-block 14 \
    --flight-budget-pp 1500 --vacation-days 18 --top 10

# Reine Preissuche: günstigste noch sinnvolle Routen je Reiselänge
python3 scripts/plan.py discover --min-score 6.5 --lengths 28,35,42

# Startszenarien vergleichen (Montafon direkt / Cottbus / Teneriffa / Hamburg)
python3 scripts/plan.py scenarios --profile active --max-dest 2

# Saisontabelle aller Ziele
python3 scripts/plan.py season --profile surf

# Routen frei optimieren
python3 scripts/plan.py optimize --profile surf --top 8 --detail 2

# Vollständigen Report schreiben
python3 scripts/plan.py report --profile surf --out docs/routenplan.md

# Tests
python3 -m pytest tests/ -q
```

Profile: `surf` (Longboard-Fokus), `balanced`, `work` (Arbeitsfähigkeit zuerst).

Profil `active` ist der Standard: Ausflüge wiegen mehr als Surf, weil nicht jeden
Tag gesurft werden soll.

Wichtige Schalter:

```bash
--work-start 9 --work-end 16 --work-flex 1   # Pflicht-Arbeitszeit (deutsche Zeit)
--ideal-local-start 14.5                      # bevorzugter lokaler Arbeitsbeginn
--vacation-days 18                            # Urlaubsbudget, wird verteilt
--origins ZRH,MUC                             # Abflughäfen
--budget 6500                                 # harte Kostenobergrenze
--include NP-NEPAL --exclude ID-LOMBOK        # Ziele erzwingen/ausschließen
--max-dest 3                                  # auch Drei-Ziel-Routen (langsam, ~3 min)
```

`--ideal-local-start` ist der wirksamste Hebel. Bei 14.5 (Standard) gewinnen
Ziele mit großem Zeitversatz nach Osten, weil der Vormittag frei bleibt; bei 12.5
kippt es zurück Richtung Sri Lanka und Oman.

## Dauerbetrieb: Preise über Monate beobachten

```bash
docker compose up -d --build        # alle 12 h ein Scrape-Lauf, Historie in SQLite
docker compose logs -f flight-tracker
```

Der Container arbeitet pro Lauf die Kalender-Matrix ab (gut 90 Suchen, siehe
unten), schneidet die Antworten von Google Flights mit, liest sie in eine
SQLite-Historie ein und meldet Allzeittiefs und Preiseinbrüche ins Log. Pro
Suche öffnet er die Preisgrafik, eine Seite liefert damit ~60 Abflugtage plus
die Angebotsliste. Lehnt Google mehrere Suchen hintereinander ab, bricht der
Lauf ab und der nächste versucht es wieder.

Auswerten:

```bash
python3 scripts/track.py status                 # Umfang der Historie
python3 scripts/track.py lows                   # Allzeittiefs = Kaufsignal
python3 scripts/track.py deals --drop 20         # Einbrüche gegen den eigenen Median
python3 scripts/track.py best --top 30           # günstigste je gesehene Preise
python3 scripts/track.py plan --price-mode best  # Szenarien mit echten Preisen
```

`--price-mode best` beantwortet „welche Route ist erreichbar, wenn ich geduldig
beobachte", `--price-mode latest` beantwortet „soll ich jetzt buchen".

Dieselben Auswertungen gibt es als Webseite (`scripts/web.py`, Dienst
`flight-web`, lokal auf http://127.0.0.1:8080): Allzeittiefs, Preiseinbrüche,
Szenarien mit aktuellen und mit Bestpreisen, günstigste Preise und die letzten
Läufe. Die Szenarien rechnet die Seite im Hintergrund neu, sobald neue Preise
in der Historie stehen (gut eine Minute). Eine eigene Anmeldung hat sie nicht;
nach außen nur hinter einem Proxy mit Login stellen. Auf dem Unraid läuft sie
als `flights.hartig.es` hinter Authentik.

Einstellbar in `docker-compose.yml`: `INTERVAL_HOURS`, `QUERIES_PER_RUN`,
`DELAY_SECONDS`, `DEAL_DROP_PCT`.

## Flugpreise beschaffen

Das Projekt rechnet ohne echte Preise mit Schätzwerten aus `data/route_hints.yaml`
und markiert jede Zahl entsprechend. Mit echten Preisen wird daraus eine belastbare
Rechnung. Drei Wege:

**A) Automatisiert scrapen** (braucht Node + Playwright, läuft lokal, nicht in einer
Cloud-Session mit eingeschränktem Netz):

```bash
# 1. Query-Matrix erzeugen. --calendar bündelt die Einzeltage jeder Strecke zu
#    Preisgrafik-Suchen und ergänzt Entdeckungssuchen über alle Abflugorte und
#    Ziele auf einmal ("MAD+BER+…" -> "CMB+KUL+…"): ~90 statt ~760 Suchen.
python3 scripts/plan.py scrape-matrix --from-scenarios --with-candidates --calendar

# 2. Erst prüfen, ob Google die URL-Kodierung noch versteht
node scripts/scrape_google_flights.cjs --verify --headed

# 3. Dann scrapen (inkrementell, --resume überspringt Erledigtes)
node scripts/scrape_google_flights.cjs data/prices/_queries.json data/prices/scraped.rpc.jsonl --delay 7
python3 scripts/track.py ingest-capture data/prices/scraped.rpc.jsonl

# 4. Neu rechnen
python3 scripts/plan.py report --profile surf
```

Der Scraper liest keinen Seitentext, sondern die Antworten der internen
Google-Flights-Schnittstelle (`GetShoppingResults`, `GetCalendarGraph`,
`GetCalendarGrid`, `GetCalendarPicker`), ausgewertet in
`src/workation/scrape/gf_rpc.py`. Nachbauen lassen sich diese Aufrufe nicht:
jeder trägt ein BotGuard-Token, das an den Inhalt gebunden ist. Darum lädt
Playwright die Seite und schneidet mit, was die Seite selbst abfragt. Google
liefert Gesamtpreise für alle Reisenden; gespeichert wird der Preis pro Person.

Ein Leg darf mehrere Orte haben: `MUC+FRA+TENERIFE` (IATA-Codes oder benannte
Orte aus `PLACES` in `src/workation/scrape/urls.py`). Bei solchen Suchen steht
in der Angebotsliste der Flughafen, den Google gewählt hat; die Kalenderpreise
laufen unter dem zusammengesetzten Namen.

**C) Aus dem eigenen Browser** – auf Google Flights suchen, Preisgrafik,
Datumsraster und Datumswähler nach Belieben öffnen, dann in den Entwicklertools
(Netzwerk) „Alle als HAR speichern“ und einlesen:

```bash
python3 scripts/track.py ingest-har ~/Downloads/www.google.com.har [--csv data/prices/har.csv]
```

Eingelesen werden nur die vier Preis-Aufrufe; die HAR-Datei selbst enthält
Cookies und gehört nicht ins Repo. Mit `--csv` landen die Zeilen zusätzlich
als CSV, die der Optimierer direkt liest (nötig für Multi-City-Tickets).

**B) Manuell** – `docs/scrape_checklist.md` enthält alle Suchen als klickbare
Google-Flights-Links. Preise ablesen und als CSV nach dem Schema in
`data/prices/_SCHEMA.csv` in `data/prices/manual.csv` eintragen. Der Optimierer
liest alle `data/prices/*.csv` automatisch ein.

Google Flights hat keine offizielle API. Der Scraper nutzt den
reverse-engineerten `tfs`-Parameter (base64-kodiertes Protobuf) und kann brechen,
wenn Google das Format ändert – darum der `--verify`-Modus und die
`q=`-Fallback-Links in der Checkliste. Halte die Abfragerate niedrig.

## Wie der Optimierer rechnet

Für jede geordnete Zielsequenz, jedes Startdatum, jeden Abflughafen und jede
Ticketstrategie läuft ein Dynamic Programming über die Reisetage. Zustand:
„Ziele 1..i sind abgearbeitet, Tage 0..t sind verplant". Damit ist die Aufteilung
der Blocklängen innerhalb des Tagesrasters exakt optimal, nicht geraten.

Zielfunktion, kleiner ist besser:

```
objective_per_day = (Gesamtkosten − wert_pro_punkt × Tagesscore × Reisende) / Reisetage
```

Die Normierung pro Tag ist wichtig: ohne sie gewinnt immer die längste Reise,
weil sie mehr Erlebnispunkte sammelt. Die Reiselänge ist aber eine Vorgabe,
keine Optimierungsgröße. `value_per_score_point_eur` (Standard 22 €) ist der
Umrechnungskurs zwischen Geld und Erlebnis – die einzige wirklich subjektive
Zahl im Modell. Hoch = Qualität zählt mehr, niedrig = Preis zählt mehr.

Harte Nebenbedingungen: Reisefenster, Reiselänge 28–42 Tage, Blocklänge 9–22 Tage,
mindestens ein tropisches Ziel, keine zwei gleichen Länder hintereinander,
Arbeitsinfrastruktur ≥ 5 für einen Standort, optional Budgetgrenze und
Mindestanzahl Surftage. Gesperrte Zeitfenster (Brandsaison Laos,
Lebaran-Reisewelle Indonesien) schließen Tage komplett aus.

**Urlaubstage** werden nach dem DP greedy verteilt, nach dem Zugewinn pro Ziel –
und ein Urlaubstag zählt nicht „Arbeit = 10/10", sondern verteilt das Gewicht der
beiden Arbeitsterme auf Wetter/Surf/Ruhe um. Sonst würde ein Ziel dafür belohnt,
dass man dort nicht arbeiten kann. Eine Obergrenze pro Block (Standard 50 %)
sorgt dafür, dass sich der Urlaub über die Reise verteilt statt zu klumpen. Das
ist bei gegebenen Blocklängen exakt, gegenüber einer gemeinsamen Optimierung von
Längen und Urlaub aber eine Heuristik.

## Struktur

```
data/destinations.yaml   17 Ziele mit Halbmonats-Scores, Kosten, Arbeitsfähigkeit,
                         Ausflugsbewertung und konkreten Mehrtagestouren
data/origins.yaml        12 Abflughäfen mit Anreise je Startkontext
                         (montafon / cottbus / hamburg / tenerife)
data/calendar.yaml       Feiertage und Preistreiber im Reisefenster
data/route_hints.yaml    Schätzpreise, Visa, Gepäck, saisonale Preisaufschläge
data/prices/*.csv        Echte Preise (gescrapet oder manuell) – haben Vorrang
src/workation/           seasonality · workwindow · prices · history ·
                         optimizer · scenarios · report · scrape
scripts/track.py         Preishistorie: ingest, best, deals, lows, plan
Dockerfile + compose     Dauerbetrieb mit regelmäßigen Scrape-Läufen
scripts/plan.py          CLI
scripts/scrape_google_flights.cjs  Scraper (Node/Playwright)
docs/                    Report, Saison-Begründungen, Strategie, Scrape-Checkliste
```

## Was noch offen ist

- **Wo startet die zweite Person?** Das Modell nimmt an, dass beide ab demselben
  Flughafen fliegen. Reist sie stattdessen von Teneriffa aus an, braucht sie ein
  eigenes Ticket, und der Szenarienvergleich kann kippen. Größter offener Posten.
- **Verschiebbarkeit der Arbeitszeit.** Standard ist 1 h. Bei 2 h entschärft sich
  das Lombok-Problem fast vollständig, bei 0 h sollte Lombok kürzer werden.
- **Islamische Feiertage 2027** sind Mondsichtungs-Prognosen (Eid al-Fitr
  ~10.03.2027). Vor der Buchung erneut prüfen.
- **Alle Flugpreise** sind bis zum ersten Scrape Schätzwerte.

Geklärt: Der 75%-Residentenrabatt gilt **nicht** auf Tickets mit internationalem
Anschluss. Der Kanaren-Zubringer wird deshalb immer separat gebucht, mit 3 h
Umstiegszeit – so rechnet das Modell jetzt.
