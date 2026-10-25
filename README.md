# Workation-Routenplaner 2027

Planungswerkzeug für eine 4–6-wöchige Workation zwischen Mitte März und Anfang Mai 2027,
für 2 Personen, ab Teneriffa. Es verbindet drei Dinge, die man sonst getrennt betrachtet:

1. **Saisonalität** – wann ist welches Ziel wirklich gut (Wetter, Longboard-Welle, Feiertage)?
2. **Flugpreise** – echte Google-Flights-Daten, inklusive Multi-City und Open-Jaw.
3. **Arbeitsfähigkeit** – Internet, Coworking, Zeitzonen-Überlappung mit Europa.

Daraus sucht der Optimierer Routen über 2–3 Ziele und sagt, wann welcher Block
wie lang sein soll.

## Kernergebnis (Stand: nur Schätzpreise)

**Sri Lanka Südküste → Lombok Süd**, Abflug Mitte März, Rückflug Ende April.
Die beiden Ziele laufen saisonal gegenläufig: Sri Lankas Südküste ist im März auf
dem Höhepunkt und endet Ende April mit dem SW-Monsun, Lombok startet genau dann
seine Trockenzeit. Beide sind tropisch, beide longboardtauglich, beide mit
brauchbarem Coworking. Details und Alternativen: [`docs/routenplan.md`](docs/routenplan.md),
Begründung je Ziel: [`docs/seasonality.md`](docs/seasonality.md),
konkreter Urlaubs-/Arbeitsplan: [`docs/strategie.md`](docs/strategie.md).

## Schnellstart

```bash
# Saisontabelle aller Ziele
python3 scripts/plan.py season --profile surf

# Routen optimieren
python3 scripts/plan.py optimize --profile surf --top 8 --detail 2

# Vollständigen Report schreiben
python3 scripts/plan.py report --profile surf --out docs/routenplan.md

# Tests
python3 -m pytest tests/ -q
```

Profile: `surf` (Longboard-Fokus), `balanced`, `work` (Arbeitsfähigkeit/Zeitzone zuerst).

## Flugpreise beschaffen

Das Projekt rechnet ohne echte Preise mit Schätzwerten aus `data/route_hints.yaml`
und markiert jede Zahl entsprechend. Mit echten Preisen wird daraus eine belastbare
Rechnung. Zwei Wege:

**A) Automatisiert scrapen** (braucht Node + Playwright, läuft lokal, nicht in einer
Cloud-Session mit eingeschränktem Netz):

```bash
# 1. Query-Matrix erzeugen (294 Suchen bei --level standard)
python3 scripts/plan.py scrape-matrix --level standard --with-candidates

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
optional Budgetgrenze und Mindestanzahl Surftage. Gesperrte Zeitfenster
(Brandsaison Laos, Lebaran-Reisewelle Indonesien) schließen Tage komplett aus.

## Struktur

```
data/destinations.yaml   17 Ziele mit Halbmonats-Scores, Kosten, Arbeitsfähigkeit
data/origins.yaml        Abflughäfen + Teneriffa-Zubringer + Residentenrabatt-Logik
data/calendar.yaml       Feiertage und Preistreiber im Reisefenster
data/route_hints.yaml    Schätzpreise, Visa, Gepäck, saisonale Preisaufschläge
data/prices/*.csv        Echte Preise (gescrapet oder manuell) – haben Vorrang
src/workation/           seasonality · prices · optimizer · report · scrape
scripts/plan.py          CLI
scripts/scrape_google_flights.cjs  Scraper (Node/Playwright)
docs/                    Report, Saison-Begründungen, Strategie, Scrape-Checkliste
```

## Was noch offen ist

- **Residentenrabatt bei internationalen Anschlüssen.** Der 75%-Rabatt gilt für
  Kanaren↔Peninsula. Ob er auf einem durchgehenden Ticket TFS-MAD-CMB greift,
  ist nicht belegt. Das Modell rechnet deshalb beide Varianten (`self_transfer`
  mit Rabatt und Umsteigerisiko, `through_ticket` ohne Rabatt mit Umsteigeschutz).
  Vor der Buchung bei Iberia/Binter direkt prüfen.
- **Islamische Feiertage 2027** sind Mondsichtungs-Prognosen (Eid al-Fitr
  ~10.03.2027). Vor der Buchung erneut prüfen.
- **Alle Flugpreise** sind bis zum ersten Scrape Schätzwerte.
