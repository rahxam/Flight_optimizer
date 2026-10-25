# Workation-Routenplaner 2027

Planungswerkzeug für eine 4–6-wöchige Workation zwischen Mitte März und Anfang Mai 2027,
für 2 Personen, ab Teneriffa. Es verbindet drei Dinge, die man sonst getrennt betrachtet:

1. **Saisonalität** – wann ist welches Ziel wirklich gut (Wetter, Longboard-Welle, Feiertage)?
2. **Flugpreise** – echte Google-Flights-Daten, inklusive Multi-City und Open-Jaw.
3. **Arbeitsrealität** – Internet und Coworking, und vor allem: wo landet die
   Pflicht-Arbeitszeit 09–16 Uhr deutscher Zeit vor Ort?

Daraus sucht der Optimierer Routen über 2–3 Ziele und sagt, wann welcher Block
wie lang sein soll – und wohin die Urlaubstage gehören.

## Kernergebnis (Stand: nur Schätzpreise)

**Cottbus-Brücke → Sri Lanka Südküste → Lombok Süd.** Am 06.03. von Montafon
mit den Eltern nach Cottbus, dort knapp zwei Wochen arbeiten, am **17.03. ab BER**
nach Colombo, **Sri Lanka 17.03.–07.04.**, **Lombok 08.04.–27.04.**, zurück über
Madrid. Ca. **7.220 € für zwei Personen** (172 €/Tag).

Die beiden Ziele laufen saisonal gegenläufig: Sri Lankas Südküste ist im März auf
dem Höhepunkt und endet Ende April mit dem SW-Monsun, Lombok startet genau dann
seine Trockenzeit. Und sie ergänzen sich auch bei der Arbeitszeit: in Sri Lanka
heißt 09–16 Uhr deutscher Zeit 12:30–19:30 Ortszeit (Morgen frei zum Surfen,
Abend frei), in Lombok 15:00–22:00. Darum gehen die Urlaubstage überwiegend nach
Lombok – 18/4 Arbeits-/Urlaubstage in Sri Lanka, 10/10 in Lombok.

Szenarienvergleich, Wochenplan und offene Punkte: [`docs/strategie.md`](docs/strategie.md).
Routen im Detail: [`docs/routenplan.md`](docs/routenplan.md).
Begründung je Ziel mit Quellen: [`docs/seasonality.md`](docs/seasonality.md).

## Schnellstart

```bash
# Startszenarien vergleichen (Montafon direkt / Cottbus / Teneriffa / Hamburg)
python3 scripts/plan.py scenarios --profile surf --max-dest 2

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

Wichtige Schalter:

```bash
--work-start 9 --work-end 16 --work-flex 1   # Pflicht-Arbeitszeit (deutsche Zeit)
--vacation-days 14                           # Urlaubsbudget, wird verteilt
--origins ZRH,MUC                            # Abflughäfen
--budget 6500                                # harte Kostenobergrenze
--include LK-SOUTH --exclude ID-LOMBOK        # Ziele erzwingen/ausschließen
```

`--work-flex` ist der wirksamste Hebel: bei 2 h Flexibilität wird Lombok von
15:00–22:00 auf 13:00–20:00 Ortszeit verschoben, und das Ranking ändert sich.

## Flugpreise beschaffen

Das Projekt rechnet ohne echte Preise mit Schätzwerten aus `data/route_hints.yaml`
und markiert jede Zahl entsprechend. Mit echten Preisen wird daraus eine belastbare
Rechnung. Zwei Wege:

**A) Automatisiert scrapen** (braucht Node + Playwright, läuft lokal, nicht in einer
Cloud-Session mit eingeschränktem Netz):

```bash
# 1. Query-Matrix erzeugen (521 Suchen, genau die der Startszenarien)
python3 scripts/plan.py scrape-matrix --from-scenarios --with-candidates

# 2. Erst prüfen, ob Google die URL-Kodierung noch versteht
node scripts/scrape_google_flights.cjs --verify --headed

# 3. Dann scrapen (inkrementell, Neustart überspringt Erledigtes)
node scripts/scrape_google_flights.cjs data/prices/_queries.json data/prices/scraped.csv --delay 7

# 4. Neu rechnen
python3 scripts/plan.py report --profile surf
```

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
data/destinations.yaml   17 Ziele mit Halbmonats-Scores, Kosten, Arbeitsfähigkeit
data/origins.yaml        12 Abflughäfen mit Anreise je Startkontext
                         (montafon / cottbus / hamburg / tenerife)
data/calendar.yaml       Feiertage und Preistreiber im Reisefenster
data/route_hints.yaml    Schätzpreise, Visa, Gepäck, saisonale Preisaufschläge
data/prices/*.csv        Echte Preise (gescrapet oder manuell) – haben Vorrang
src/workation/           seasonality · workwindow · prices · optimizer ·
                         scenarios · report · scrape
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
