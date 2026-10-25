# Workation-Routenplan 2027

*Erzeugt am 25.10.2026. Reisefenster 12.03.–10.05., 28–42 Tage, 2 Personen, Abflug ab MAD, BCN.*

## Datenlage

**Noch keine echten Flugpreise geladen.** Alle Flugkosten sind Schätzwerte aus `data/route_hints.yaml`. Die Saison-Logik und die Routenreihenfolge stehen damit schon, die absoluten Preise aber nicht. Sobald Scrapes in `data/prices/*.csv` liegen, rechnet derselbe Lauf mit echten Zahlen.

## Saison-Matrix

Gewichteter Tagesscore je Ziel und Halbmonat (0–10, höher = besser). **X** = hart ausgeschlossen. Fett = Saisonhoch des Ziels.

| Ziel | Tier | Work | 03. 1.-15. | 03. 16.-31. | 04. 1.-15. | 04. 16.-30. | 05. 1.-15. |
|---|---|---|---|---|---|---|---|
| Lombok | A | 7 | 7.5 | 7.8 | 8.5 | 9.0 | **9.2** |
| SL Süd | A | 8 | **9.0** | **9.0** | 8.6 | 8.3 | 7.6 |
| Taiwan | B | 10 | 8.0 | 8.0 | **8.1** | 8.0 | 7.7 |
| N-Vietnam | A | 9 | 7.1 | 7.3 | 7.6 | **7.7** | 7.5 |
| Sumbawa | B | 3 | 6.2 | 6.4 | 7.0 | 7.5 | **7.6** |
| W-Sumatra | C | 4 | 6.5 | 6.6 | 7.0 | 7.4 | **7.4** |
| SL Ost | B | 5 | 6.4 | 6.6 | 6.8 | 7.1 | **7.4** |
| Madagaskar | C | 2 | 5.7 | 5.9 | 6.3 | 6.9 | **7.3** |
| Oman | B | 7 | **7.1** | **7.1** | 6.9 | 6.5 | 6.1 |
| Kerala | B | 6 | **7.0** | 6.9 | 6.4 | 6.1 | 6.2 |
| Penang/Langkawi | B | 9 | 6.8 | 6.8 | **6.9** | 6.7 | 6.6 |
| Nepal | B | 5 | 6.8 | **6.9** | 6.9 | 6.8 | 6.5 |
| Cherating | C | 5 | **6.5** | 6.5 | 6.3 | 6.0 | 5.9 |
| Raja Ampat | C | 3 | 6.1 | 6.1 | **6.2** | 6.0 | 5.7 |
| Andamanen | C | 3 | **6.1** | **6.1** | 5.9 | 5.8 | 5.6 |
| Kambodscha | C | 6 | **5.9** | 5.8 | 5.5 | 5.4 | 5.6 |
| Laos | D | 4 | **X** | **X** | **X** | **X** | **5.9** |

*Gewichtung: Wetter 20%, Surf 18%, Ruhe 7%, Arbeitsinfrastruktur 16%, Arbeitszeitfenster 17%; Tropen-Bonus +0.4.*

## Arbeitszeitfenster vor Ort

Pflicht-Arbeitszeit 9:00–16:00 deutscher Zeit, verschiebbar um ±1 h. Stand 15.04.2027 (Sommerzeit). Der freie Morgen ist für Surfer ein Gewinn, der verlorene Abend der Preis.

| Ziel | Score | Arbeitszeit vor Ort |
|---|---|---|
| Lombok | 10.0 | 08:30-15:30 CET = 14:30-21:30 vor Ort (+6.0 h); 8.5 h freier Vormittag; Fenster um -0.5 h verschoben |
| Sumbawa | 10.0 | 08:30-15:30 CET = 14:30-21:30 vor Ort (+6.0 h); 8.5 h freier Vormittag; Fenster um -0.5 h verschoben |
| W-Sumatra | 10.0 | 09:30-16:30 CET = 14:30-21:30 vor Ort (+5.0 h); 8.5 h freier Vormittag; Fenster um +0.5 h verschoben |
| Penang/Langkawi | 10.0 | 08:30-15:30 CET = 14:30-21:30 vor Ort (+6.0 h); 8.5 h freier Vormittag; Fenster um -0.5 h verschoben |
| Cherating | 10.0 | 08:30-15:30 CET = 14:30-21:30 vor Ort (+6.0 h); 8.5 h freier Vormittag; Fenster um -0.5 h verschoben |
| N-Vietnam | 10.0 | 09:30-16:30 CET = 14:30-21:30 vor Ort (+5.0 h); 8.5 h freier Vormittag; Fenster um +0.5 h verschoben |
| Taiwan | 10.0 | 08:30-15:30 CET = 14:30-21:30 vor Ort (+6.0 h); 8.5 h freier Vormittag; Fenster um -0.5 h verschoben |
| Kambodscha | 10.0 | 09:30-16:30 CET = 14:30-21:30 vor Ort (+5.0 h); 8.5 h freier Vormittag; Fenster um +0.5 h verschoben |
| Laos | 10.0 | 09:30-16:30 CET = 14:30-21:30 vor Ort (+5.0 h); 8.5 h freier Vormittag; Fenster um +0.5 h verschoben |
| Nepal | 9.6 | 10:00-17:00 CET = 13:45-20:45 vor Ort (+3.8 h); 7.8 h freier Vormittag; Fenster um +1.0 h verschoben |
| SL Süd | 9.5 | 10:00-17:00 CET = 13:30-20:30 vor Ort (+3.5 h); 7.5 h freier Vormittag; Fenster um +1.0 h verschoben |
| SL Ost | 9.5 | 10:00-17:00 CET = 13:30-20:30 vor Ort (+3.5 h); 7.5 h freier Vormittag; Fenster um +1.0 h verschoben |
| Kerala | 9.5 | 10:00-17:00 CET = 13:30-20:30 vor Ort (+3.5 h); 7.5 h freier Vormittag; Fenster um +1.0 h verschoben |
| Andamanen | 9.5 | 10:00-17:00 CET = 13:30-20:30 vor Ort (+3.5 h); 7.5 h freier Vormittag; Fenster um +1.0 h verschoben |
| Raja Ampat | 9.4 | 08:00-15:00 CET = 15:00-22:00 vor Ort (+7.0 h); 9.0 h freier Vormittag; Fenster um -1.0 h verschoben |
| Oman | 8.8 | 10:00-17:00 CET = 12:00-19:00 vor Ort (+2.0 h); 6.0 h freier Vormittag; Fenster um +1.0 h verschoben |
| Madagaskar | 8.2 | 10:00-17:00 CET = 11:00-18:00 vor Ort (+1.0 h); 5.0 h freier Vormittag; Fenster um +1.0 h verschoben |

## Kalender im Reisefenster

| Datum | Ereignis | Betrifft | Impact | Hinweis |
|---|---|---|---|---|
| 08.02.–09.03. | Ramadan 2027 *(Prognose)* | Oman, Malaysia, Indonesien | medium | Endet VOR dem geplanten Reisebeginn. Relevant nur, wenn du vor dem 10.03. in Oman/Malaysia/Indonesien startest (Restaurants tagsueber geschlossen). |
| 15.02.–20.04. | Brandsaison Festland-SO-Asien | Laos, Nord-Thailand, Nord-Vietnam, Kambodscha | high | PM2.5-Belastung in Nord-Laos/Nord-Thailand regelmaessig AQI 150-300+. Nord-Vietnam ist weniger betroffen als Laos, aber Hanoi hat im Maerz eigene Smog-Episoden (AQI 150+). Live … |
| 09.03.–14.03. | Eid al-Fitr / Idul Fitri / Hari Raya *(Prognose)* | Indonesien, Malaysia, Oman | high | Groesster Preistreiber in Indonesien/Malaysia. Die Mudik-/Lebaran-Reisewelle laeuft ca. 5 Tage davor bis 7 Tage danach: Inlandsfluege (z.B. nach LOP) und Faehren sind teuer und … |
| 21.03.–29.03. | Semana Santa / Ostern (Spanien + EU) | Spanien, Deutschland, EU-Abfluege | high | Ostersonntag 2027 = 28.03. Gruendonnerstag 25.03. und Karfreitag 26.03. sind in Spanien Feiertage. Langstreckenabfluege ab MAD/BCN sowie die Kanaren-Zubringer (TFS/TFN -> MAD/BC… |
| 28.03.–28.03. | EU-Sommerzeit beginnt | Spanien, Deutschland | low | Ab 28.03. verschiebt sich die Uhr in Spanien auf UTC+2. Alle Zeitversaetze zu Asien schrumpfen um 1 h -> Calls mit Europa werden leichter. |
| 01.04.–15.05. | Indonesien: Trockenzeit/Passat setzt ein | Indonesien | high | SO-Passat dreht offshore an Lomboks Sued-/Westkueste. Ab Mitte April zuverlaessig saubere Vormittage. Je spaeter im Fenster, desto besser. |
| 13.04.–15.04. | Sinhala & Tamil New Year (Sri Lanka) | Sri Lanka | high | Das Land steht 3-4 Tage still: Laeden, Coworking und viele Restaurants zu, Busse/Zuege ueberfuellt, Inlandspreise hoch. Entweder vorher weiterfliegen oder bewusst als Kultur-Erl… |
| 13.04.–16.04. | Khmer / Lao / Thai New Year | Kambodscha, Laos | high | Landesweite Schliessungen, Reisewellen, Preisspitzen. |
| 25.04.–20.05. | Sri Lanka: SW-Monsun setzt ein | Sri Lanka | high | Der Wind dreht: Suedkueste wird onshore/choppy, Ostkueste (Arugam Bay) beginnt zu laufen. Harte Deadline fuer den Suedkuesten-Block. |
| 29.04.–05.05. | 1. Mai / Golden Week-Vorlauf | Taiwan, Malaysia, Indonesien, Vietnam | medium | Regionale Feiertage -> Rueckflugpreise ab Asien leicht erhoeht. |
| 30.04.–03.05. | Vietnam: Reunification Day + Labour Day | Vietnam | medium | Langes Wochenende, starke Inlandsreisewelle (Sapa/Ha Giang/Kuesten voll, Hotelpreise +50-100%). Fuer die Ha-Giang-Runde vorher einplanen. |

## Was bringt eine Woche mehr?

| Reiselänge | Beste Route | Zeitraum | Kosten | €/Tag | Score/Tag | Surf-Tage |
|---|---|---|---|---|---|---|
| 28 Tage | N-Vietnam -> Lombok | 13.04.–10.05. | 4,854 € | 173 € | 8.21 | 19 |
| 35 Tage | SL Süd -> Lombok | 18.03.–21.04. | 5,984 € | 171 € | 8.51 | 35 |
| 42 Tage | SL Süd -> Lombok | 12.03.–22.04. | 6,744 € | 161 € | 8.59 | 42 |

## Routenvorschläge

### 1. SL Süd -> Lombok

**12.03.–22.04. 2027** · 42 Tage · ab **MAD** (Anreise aus `tenerife`) · zurück über **MAD** · `separate_tickets`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **6,744 €** |
| davon Flüge | 2,194 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 4,400 € |
| Visa | 150 € |
| Kosten pro Tag (beide) | 161 € |
| Erlebnis-Score pro Tag | 8.59 / 10 |
| Urlaubstage (verteilt) | 18 von 42 |
| Tage mit Longboard-Surf (Score ≥ 6) | 42 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Arbeit/Urlaub | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|---|
| 12.03.–31.03. | 20 | 13 / 7 | Sri Lanka Suedkueste (Weligama / Ahangama / Hiriketiya / Dikwella) | 9.0 | 9.0 | 6.0 | 8 | 55 € |
| 01.04.–22.04. | 22 | 11 / 11 | Lombok Sued (Kuta / Gerupuk / Tanjung Aan / Mawi) | 8.2 | 8.2 | 8.0 | 7 | 50 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 12.03. | MAD → CMB | outbound | 920 € | `estimate+flight` |
| 01.04. | CMB → LOP | inter | 580 € | `estimate` |
| 22.04. | LOP → MAD | return | 694 € | `estimate+flight` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 42 Tage mit Surf-Score >= 6 (longboardtauglich)
- Arbeitszeit in Lombok: 08:30-15:30 CET = 14:30-21:30 vor Ort (+6.0 h); 8.5 h freier Vormittag; Fenster um -0.5 h verschoben
- Arbeitszeit in SL Süd: 10:00-17:00 CET = 14:30-21:30 vor Ort (+4.5 h); 8.5 h freier Vormittag; Fenster um +1.0 h verschoben
- Indonesien: Trockenzeit/Passat setzt ein (01.04.-15.05.) faellt in Lombok [Impact: high]

### 2. N-Vietnam -> Lombok

**01.04.–10.05. 2027** · 40 Tage · ab **MAD** (Anreise aus `tenerife`) · zurück über **MAD** · `separate_tickets`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **5,784 €** |
| davon Flüge | 2,214 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 3,460 € |
| Visa | 110 € |
| Kosten pro Tag (beide) | 145 € |
| Erlebnis-Score pro Tag | 8.07 / 10 |
| Urlaubstage (verteilt) | 18 von 40 |
| Tage mit Longboard-Surf (Score ≥ 6) | 22 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Arbeit/Urlaub | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|---|
| 01.04.–18.04. | 18 | 11 / 7 | Nordvietnam (Hanoi / Ha Giang / Sapa / Cao Bang / Ba Be) | 9.0 | 0.0 | 7.6 | 9 | 35 € |
| 19.04.–10.05. | 22 | 11 / 11 | Lombok Sued (Kuta / Gerupuk / Tanjung Aan / Mawi) | 9.0 | 9.0 | 8.0 | 7 | 50 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 01.04. | MAD → HAN | outbound | 1,000 € | `estimate+flight` |
| 19.04. | HAN → LOP | inter | 520 € | `estimate` |
| 10.05. | LOP → MAD | return | 694 € | `estimate+flight` |

**Hinweise**

- 1. Mai / Golden Week-Vorlauf (29.04.-05.05.) faellt in Lombok [Impact: medium]
- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 22 Tage mit Surf-Score >= 6 (longboardtauglich)
- Arbeitszeit in Lombok: 08:30-15:30 CET = 14:30-21:30 vor Ort (+6.0 h); 8.5 h freier Vormittag; Fenster um -0.5 h verschoben
- Arbeitszeit in N-Vietnam: 09:30-16:30 CET = 14:30-21:30 vor Ort (+5.0 h); 8.5 h freier Vormittag; Fenster um +0.5 h verschoben
- Indonesien: Trockenzeit/Passat setzt ein (01.04.-15.05.) faellt in Lombok [Impact: high]

### 3. SL Süd -> N-Vietnam -> Lombok

**16.03.–26.04. 2027** · 42 Tage · ab **MAD** (Anreise aus `tenerife`) · zurück über **MAD** · `separate_tickets`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **6,924 €** |
| davon Flüge | 2,654 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 4,070 € |
| Visa | 200 € |
| Kosten pro Tag (beide) | 165 € |
| Erlebnis-Score pro Tag | 8.24 / 10 |
| Urlaubstage (verteilt) | 18 von 42 |
| Tage mit Longboard-Surf (Score ≥ 6) | 33 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Arbeit/Urlaub | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|---|
| 16.03.–29.03. | 14 | 7 / 7 | Sri Lanka Suedkueste (Weligama / Ahangama / Hiriketiya / Dikwella) | 9.0 | 9.0 | 6.0 | 8 | 55 € |
| 30.03.–07.04. | 9 | 7 / 2 | Nordvietnam (Hanoi / Ha Giang / Sapa / Cao Bang / Ba Be) | 8.9 | 0.0 | 8.0 | 9 | 35 € |
| 08.04.–26.04. | 19 | 10 / 9 | Lombok Sued (Kuta / Gerupuk / Tanjung Aan / Mawi) | 8.9 | 8.9 | 8.0 | 7 | 50 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 16.03. | MAD → CMB | outbound | 920 € | `estimate+flight` |
| 30.03. | CMB → HAN | inter | 520 € | `estimate` |
| 08.04. | HAN → LOP | inter | 520 € | `estimate` |
| 26.04. | LOP → MAD | return | 694 € | `estimate+flight` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 33 Tage mit Surf-Score >= 6 (longboardtauglich)
- Arbeitszeit in Lombok: 08:30-15:30 CET = 14:30-21:30 vor Ort (+6.0 h); 8.5 h freier Vormittag; Fenster um -0.5 h verschoben
- Arbeitszeit in N-Vietnam: 09:30-16:30 CET = 14:30-21:30 vor Ort (+5.0 h); 8.5 h freier Vormittag; Fenster um +0.5 h verschoben
- Arbeitszeit in SL Süd: 10:00-17:00 CET = 14:30-21:30 vor Ort (+4.5 h); 8.5 h freier Vormittag; Fenster um +1.0 h verschoben
- Indonesien: Trockenzeit/Passat setzt ein (01.04.-15.05.) faellt in Lombok [Impact: high]

### 4. Lombok -> SL Ost

**01.04.–10.05. 2027** · 40 Tage · ab **MAD** (Anreise aus `tenerife`) · zurück über **MAD** · `separate_tickets`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **6,146 €** |
| davon Flüge | 2,176 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 3,820 € |
| Visa | 150 € |
| Kosten pro Tag (beide) | 154 € |
| Erlebnis-Score pro Tag | 7.94 / 10 |
| Urlaubstage (verteilt) | 18 von 40 |
| Tage mit Longboard-Surf (Score ≥ 6) | 39 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Arbeit/Urlaub | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|---|
| 01.04.–22.04. | 22 | 11 / 11 | Lombok Sued (Kuta / Gerupuk / Tanjung Aan / Mawi) | 8.2 | 8.2 | 8.0 | 7 | 50 € |
| 23.04.–10.05. | 18 | 11 / 7 | Sri Lanka Ostkueste (Arugam Bay) | 8.0 | 6.9 | 7.1 | 5 | 45 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 01.04. | MAD → LOP | outbound | 770 € | `estimate+flight` |
| 23.04. | LOP → CMB | inter | 580 € | `estimate` |
| 10.05. | CMB → MAD | return | 826 € | `estimate+flight` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 39 Tage mit Surf-Score >= 6 (longboardtauglich)
- Arbeitszeit in Lombok: 08:30-15:30 CET = 14:30-21:30 vor Ort (+6.0 h); 8.5 h freier Vormittag; Fenster um -0.5 h verschoben
- Arbeitszeit in SL Ost: 10:00-17:00 CET = 13:30-20:30 vor Ort (+3.5 h); 7.5 h freier Vormittag; Fenster um +1.0 h verschoben
- Indonesien: Trockenzeit/Passat setzt ein (01.04.-15.05.) faellt in Lombok [Impact: high]
- Sri Lanka: SW-Monsun setzt ein (25.04.-20.05.) faellt in SL Ost [Impact: high]

### 5. SL Süd -> N-Vietnam

**12.03.–22.04. 2027** · 42 Tage · ab **MAD** (Anreise aus `tenerife`) · zurück über **MAD** · `separate_tickets`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **6,217 €** |
| davon Flüge | 2,337 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 3,740 € |
| Visa | 140 € |
| Kosten pro Tag (beide) | 148 € |
| Erlebnis-Score pro Tag | 7.79 / 10 |
| Urlaubstage (verteilt) | 18 von 42 |
| Tage mit Longboard-Surf (Score ≥ 6) | 20 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Arbeit/Urlaub | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|---|
| 12.03.–31.03. | 20 | 10 / 10 | Sri Lanka Suedkueste (Weligama / Ahangama / Hiriketiya / Dikwella) | 9.0 | 9.0 | 6.0 | 8 | 55 € |
| 01.04.–22.04. | 22 | 14 / 8 | Nordvietnam (Hanoi / Ha Giang / Sapa / Cao Bang / Ba Be) | 9.0 | 0.0 | 7.8 | 9 | 35 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 12.03. | MAD → CMB | outbound | 920 € | `estimate+flight` |
| 01.04. | CMB → HAN | inter | 520 € | `estimate` |
| 22.04. | HAN → MAD | return | 897 € | `estimate+flight` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 20 Tage mit Surf-Score >= 6 (longboardtauglich)
- Arbeitszeit in N-Vietnam: 09:30-16:30 CET = 14:30-21:30 vor Ort (+5.0 h); 8.5 h freier Vormittag; Fenster um +0.5 h verschoben
- Arbeitszeit in SL Süd: 10:00-17:00 CET = 14:30-21:30 vor Ort (+4.5 h); 8.5 h freier Vormittag; Fenster um +1.0 h verschoben

### 6. Nepal -> Lombok

**01.04.–10.05. 2027** · 40 Tage · ab **MAD** (Anreise aus `tenerife`) · zurück über **MAD** · `separate_tickets`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **6,044 €** |
| davon Flüge | 2,434 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 3,460 € |
| Visa | 150 € |
| Kosten pro Tag (beide) | 151 € |
| Erlebnis-Score pro Tag | 7.81 / 10 |
| Urlaubstage (verteilt) | 18 von 40 |
| Tage mit Longboard-Surf (Score ≥ 6) | 22 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Arbeit/Urlaub | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|---|
| 01.04.–18.04. | 18 | 11 / 7 | Nepal (Kathmandu / Pokhara / Annapurna / Langtang) | 8.6 | 0.0 | 6.0 | 5 | 35 € |
| 19.04.–10.05. | 22 | 11 / 11 | Lombok Sued (Kuta / Gerupuk / Tanjung Aan / Mawi) | 9.0 | 9.0 | 8.0 | 7 | 50 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 01.04. | MAD → KTM | outbound | 1,040 € | `estimate+flight` |
| 19.04. | KTM → LOP | inter | 700 € | `estimate` |
| 10.05. | LOP → MAD | return | 694 € | `estimate+flight` |

**Hinweise**

- 1. Mai / Golden Week-Vorlauf (29.04.-05.05.) faellt in Lombok [Impact: medium]
- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 22 Tage mit Surf-Score >= 6 (longboardtauglich)
- Arbeitszeit in Lombok: 08:30-15:30 CET = 14:30-21:30 vor Ort (+6.0 h); 8.5 h freier Vormittag; Fenster um -0.5 h verschoben
- Arbeitszeit in Nepal: 10:00-17:00 CET = 13:45-20:45 vor Ort (+3.8 h); 7.8 h freier Vormittag; Fenster um +1.0 h verschoben
- Indonesien: Trockenzeit/Passat setzt ein (01.04.-15.05.) faellt in Lombok [Impact: high]

### 7. SL Süd -> Nepal -> Lombok

**16.03.–26.04. 2027** · 42 Tage · ab **MAD** (Anreise aus `tenerife`) · zurück über **MAD** · `separate_tickets`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **7,004 €** |
| davon Flüge | 2,694 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 4,070 € |
| Visa | 240 € |
| Kosten pro Tag (beide) | 167 € |
| Erlebnis-Score pro Tag | 8.11 / 10 |
| Urlaubstage (verteilt) | 18 von 42 |
| Tage mit Longboard-Surf (Score ≥ 6) | 33 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Arbeit/Urlaub | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|---|
| 16.03.–29.03. | 14 | 7 / 7 | Sri Lanka Suedkueste (Weligama / Ahangama / Hiriketiya / Dikwella) | 9.0 | 9.0 | 6.0 | 8 | 55 € |
| 30.03.–07.04. | 9 | 7 / 2 | Nepal (Kathmandu / Pokhara / Annapurna / Langtang) | 9.0 | 0.0 | 6.1 | 5 | 35 € |
| 08.04.–26.04. | 19 | 10 / 9 | Lombok Sued (Kuta / Gerupuk / Tanjung Aan / Mawi) | 8.9 | 8.9 | 8.0 | 7 | 50 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 16.03. | MAD → CMB | outbound | 920 € | `estimate+flight` |
| 30.03. | CMB → KTM | inter | 380 € | `estimate` |
| 08.04. | KTM → LOP | inter | 700 € | `estimate` |
| 26.04. | LOP → MAD | return | 694 € | `estimate+flight` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 33 Tage mit Surf-Score >= 6 (longboardtauglich)
- Arbeitszeit in Lombok: 08:30-15:30 CET = 14:30-21:30 vor Ort (+6.0 h); 8.5 h freier Vormittag; Fenster um -0.5 h verschoben
- Arbeitszeit in Nepal: 10:00-17:00 CET = 13:45-20:45 vor Ort (+3.8 h); 7.8 h freier Vormittag; Fenster um +1.0 h verschoben
- Arbeitszeit in SL Süd: 10:00-17:00 CET = 14:30-21:30 vor Ort (+4.5 h); 8.5 h freier Vormittag; Fenster um +1.0 h verschoben
- Indonesien: Trockenzeit/Passat setzt ein (01.04.-15.05.) faellt in Lombok [Impact: high]

### 8. Kerala -> SL Süd -> Lombok

**12.03.–22.04. 2027** · 42 Tage · ab **MAD** (Anreise aus `tenerife`) · zurück über **MAD** · `separate_tickets`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **6,844 €** |
| davon Flüge | 2,494 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 4,130 € |
| Visa | 220 € |
| Kosten pro Tag (beide) | 163 € |
| Erlebnis-Score pro Tag | 8.01 / 10 |
| Urlaubstage (verteilt) | 18 von 42 |
| Tage mit Longboard-Surf (Score ≥ 6) | 33 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Arbeit/Urlaub | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|---|
| 12.03.–20.03. | 9 | 7 / 2 | Kerala / Varkala / Kovalam | 5.0 | 3.0 | 8.0 | 6 | 40 € |
| 21.03.–31.03. | 11 | 6 / 5 | Sri Lanka Suedkueste (Weligama / Ahangama / Hiriketiya / Dikwella) | 8.7 | 8.7 | 5.4 | 8 | 55 € |
| 01.04.–22.04. | 22 | 11 / 11 | Lombok Sued (Kuta / Gerupuk / Tanjung Aan / Mawi) | 8.2 | 8.2 | 8.0 | 7 | 50 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 12.03. | MAD → TRV | outbound | 1,000 € | `estimate+flight` |
| 21.03. | TRV → CMB | inter | 220 € | `estimate` |
| 01.04. | CMB → LOP | inter | 580 € | `estimate` |
| 22.04. | LOP → MAD | return | 694 € | `estimate+flight` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 33 Tage mit Surf-Score >= 6 (longboardtauglich)
- Arbeitszeit in Kerala: 10:00-17:00 CET = 14:30-21:30 vor Ort (+4.5 h); 8.5 h freier Vormittag; Fenster um +1.0 h verschoben
- Arbeitszeit in Lombok: 08:30-15:30 CET = 14:30-21:30 vor Ort (+6.0 h); 8.5 h freier Vormittag; Fenster um -0.5 h verschoben
- Arbeitszeit in SL Süd: 10:00-17:00 CET = 14:30-21:30 vor Ort (+4.5 h); 8.5 h freier Vormittag; Fenster um +1.0 h verschoben
- Indonesien: Trockenzeit/Passat setzt ein (01.04.-15.05.) faellt in Lombok [Impact: high]
