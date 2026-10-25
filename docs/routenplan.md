# Workation-Routenplan 2027

*Erzeugt am 25.10.2026. Reisefenster 12.03.–10.05., 28–42 Tage, 2 Personen, Abflug ab MAD, BCN.*

## Datenlage

**Noch keine echten Flugpreise geladen.** Alle Flugkosten sind Schätzwerte aus `data/route_hints.yaml`. Die Saison-Logik und die Routenreihenfolge stehen damit schon, die absoluten Preise aber nicht. Sobald Scrapes in `data/prices/*.csv` liegen, rechnet derselbe Lauf mit echten Zahlen.

## Saison-Matrix

Gewichteter Tagesscore je Ziel und Halbmonat (0–10, höher = besser). **X** = hart ausgeschlossen. Fett = Saisonhoch des Ziels.

| Ziel | Tier | Work | 03. 1.-15. | 03. 16.-31. | 04. 1.-15. | 04. 16.-30. | 05. 1.-15. |
|---|---|---|---|---|---|---|---|
| SL Süd | A | 8 | **9.3** | **9.3** | 8.9 | 8.4 | 7.3 |
| Lombok | A | 7 | 6.5 | 6.9 | 7.9 | 8.7 | **8.9** |
| Sumbawa | B | 3 | 6.1 | 6.4 | 7.3 | 8.0 | **8.3** |
| W-Sumatra | C | 4 | 6.2 | 6.3 | 7.2 | 7.8 | **7.9** |
| SL Ost | B | 5 | 5.9 | 6.2 | 6.6 | 7.2 | **7.8** |
| Madagaskar | C | 2 | 5.0 | 5.3 | 6.2 | 7.0 | **7.6** |
| Taiwan | B | 10 | **6.9** | 6.9 | 6.8 | 6.6 | 6.2 |
| Kerala | B | 6 | **6.6** | 6.3 | 5.8 | 5.4 | 5.6 |
| Cherating | C | 5 | **6.5** | 6.3 | 6.0 | 5.5 | 5.3 |
| Oman | B | 7 | **5.8** | **5.8** | 5.6 | 5.2 | 4.8 |
| N-Vietnam | A | 9 | 4.9 | 5.1 | 5.7 | **5.8** | 5.5 |
| Penang/Langkawi | B | 9 | 5.4 | 5.5 | **5.7** | 5.5 | 5.4 |
| Andamanen | C | 3 | **5.6** | **5.6** | 5.5 | 5.3 | 5.2 |
| Nepal | B | 5 | 5.0 | 5.1 | **5.1** | 5.0 | 4.7 |
| Kambodscha | C | 6 | **4.6** | 4.5 | 4.4 | 4.3 | 4.6 |
| Laos | D | 4 | **X** | **X** | **X** | **X** | **4.4** |
| Raja Ampat | C | 3 | 4.1 | 4.1 | **4.4** | 4.1 | 3.8 |

*Gewichtung: Wetter 22%, Surf 36%, Ruhe 8%, Arbeitsinfrastruktur 16%, Arbeitszeitfenster 18%; Tropen-Bonus +0.5.*

## Arbeitszeitfenster vor Ort

Pflicht-Arbeitszeit 9:00–16:00 deutscher Zeit, verschiebbar um ±1 h. Stand 15.04.2027 (Sommerzeit). Der freie Morgen ist für Surfer ein Gewinn, der verlorene Abend der Preis.

| Ziel | Score | Arbeitszeit vor Ort |
|---|---|---|
| SL Süd | 10.0 | 08:00-15:00 CET = 11:30-18:30 vor Ort (+3.5 h); 5.5 h freier Morgen; Fenster um -1.0 h verschoben |
| SL Ost | 10.0 | 08:00-15:00 CET = 11:30-18:30 vor Ort (+3.5 h); 5.5 h freier Morgen; Fenster um -1.0 h verschoben |
| Kerala | 10.0 | 08:00-15:00 CET = 11:30-18:30 vor Ort (+3.5 h); 5.5 h freier Morgen; Fenster um -1.0 h verschoben |
| Andamanen | 10.0 | 08:00-15:00 CET = 11:30-18:30 vor Ort (+3.5 h); 5.5 h freier Morgen; Fenster um -1.0 h verschoben |
| Nepal | 10.0 | 08:00-15:00 CET = 11:45-18:45 vor Ort (+3.8 h); 5.8 h freier Morgen; Fenster um -1.0 h verschoben |
| Oman | 10.0 | 08:00-15:00 CET = 10:00-17:00 vor Ort (+2.0 h); 4.0 h freier Morgen; Fenster um -1.0 h verschoben |
| Madagaskar | 10.0 | 08:00-15:00 CET = 09:00-16:00 vor Ort (+1.0 h); 3.0 h freier Morgen; Fenster um -1.0 h verschoben |
| W-Sumatra | 9.7 | 08:00-15:00 CET = 13:00-20:00 vor Ort (+5.0 h); 7.0 h freier Morgen; 1.0 h Abend weg; Fenster um -1.0 h verschoben |
| N-Vietnam | 9.7 | 08:00-15:00 CET = 13:00-20:00 vor Ort (+5.0 h); 7.0 h freier Morgen; 1.0 h Abend weg; Fenster um -1.0 h verschoben |
| Kambodscha | 9.7 | 08:00-15:00 CET = 13:00-20:00 vor Ort (+5.0 h); 7.0 h freier Morgen; 1.0 h Abend weg; Fenster um -1.0 h verschoben |
| Laos | 9.7 | 08:00-15:00 CET = 13:00-20:00 vor Ort (+5.0 h); 7.0 h freier Morgen; 1.0 h Abend weg; Fenster um -1.0 h verschoben |
| Lombok | 8.2 | 08:00-15:00 CET = 14:00-21:00 vor Ort (+6.0 h); 8.0 h freier Morgen; 2.0 h Abend weg; Fenster um -1.0 h verschoben |
| Sumbawa | 8.2 | 08:00-15:00 CET = 14:00-21:00 vor Ort (+6.0 h); 8.0 h freier Morgen; 2.0 h Abend weg; Fenster um -1.0 h verschoben |
| Penang/Langkawi | 8.2 | 08:00-15:00 CET = 14:00-21:00 vor Ort (+6.0 h); 8.0 h freier Morgen; 2.0 h Abend weg; Fenster um -1.0 h verschoben |
| Cherating | 8.2 | 08:00-15:00 CET = 14:00-21:00 vor Ort (+6.0 h); 8.0 h freier Morgen; 2.0 h Abend weg; Fenster um -1.0 h verschoben |
| Taiwan | 8.2 | 08:00-15:00 CET = 14:00-21:00 vor Ort (+6.0 h); 8.0 h freier Morgen; 2.0 h Abend weg; Fenster um -1.0 h verschoben |
| Raja Ampat | 6.7 | 08:00-15:00 CET = 15:00-22:00 vor Ort (+7.0 h); 9.0 h freier Morgen; 3.0 h Abend weg; Fenster um -1.0 h verschoben |

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
| 28 Tage | SL Süd -> Lombok | 09.04.–06.05. | 5,718 € | 204 € | 8.39 | 28 |
| 35 Tage | SL Süd -> Lombok | 18.03.–21.04. | 6,548 € | 187 € | 8.59 | 35 |
| 42 Tage | SL Süd -> Lombok | 16.03.–26.04. | 7,248 € | 173 € | 8.67 | 42 |

## Routenvorschläge

### 1. SL Süd -> Lombok

**16.03.–26.04. 2027** · 42 Tage · ab **MAD** (Anreise aus `tenerife`) · zurück über **MAD** · `separate_tickets`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **7,248 €** |
| davon Flüge | 2,678 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 4,420 € |
| Visa | 150 € |
| Kosten pro Tag (beide) | 173 € |
| Erlebnis-Score pro Tag | 8.67 / 10 |
| Urlaubstage (verteilt) | 14 von 42 |
| Tage mit Longboard-Surf (Score ≥ 6) | 42 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Arbeit/Urlaub | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|---|
| 16.03.–06.04. | 22 | 18 / 4 | Sri Lanka Suedkueste (Weligama / Ahangama / Hiriketiya / Dikwella) | 8.8 | 8.8 | 5.5 | 8 | 55 € |
| 07.04.–26.04. | 20 | 10 / 10 | Lombok Sued (Kuta / Gerupuk / Tanjung Aan / Mawi) | 8.9 | 8.9 | 8.0 | 7 | 50 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 16.03. | MAD → CMB | outbound | 920 € | `estimate+flight` |
| 07.04. | CMB → LOP | inter | 580 € | `estimate` |
| 26.04. | LOP → MAD | return | 1,178 € | `estimate+flight` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 42 Tage mit Surf-Score >= 6 (longboardtauglich)
- Arbeitszeit in Lombok: 08:00-15:00 CET = 14:00-21:00 vor Ort (+6.0 h); 8.0 h freier Morgen; 2.0 h Abend weg; Fenster um -1.0 h verschoben
- Arbeitszeit in SL Süd: 08:00-15:00 CET = 12:30-19:30 vor Ort (+4.5 h); 6.5 h freier Morgen; 0.5 h Abend weg; Fenster um -1.0 h verschoben
- Indonesien: Trockenzeit/Passat setzt ein (01.04.-15.05.) faellt in Lombok [Impact: high]

### 2. Lombok -> SL Ost

**01.04.–10.05. 2027** · 40 Tage · ab **MAD** (Anreise aus `tenerife`) · zurück über **MAD** · `separate_tickets`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **6,696 €** |
| davon Flüge | 2,726 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 3,820 € |
| Visa | 150 € |
| Kosten pro Tag (beide) | 167 € |
| Erlebnis-Score pro Tag | 7.99 / 10 |
| Urlaubstage (verteilt) | 14 von 40 |
| Tage mit Longboard-Surf (Score ≥ 6) | 39 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Arbeit/Urlaub | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|---|
| 01.04.–22.04. | 22 | 11 / 11 | Lombok Sued (Kuta / Gerupuk / Tanjung Aan / Mawi) | 8.2 | 8.2 | 8.0 | 7 | 50 € |
| 23.04.–10.05. | 18 | 15 / 3 | Sri Lanka Ostkueste (Arugam Bay) | 8.0 | 6.9 | 7.1 | 5 | 45 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 01.04. | MAD → LOP | outbound | 1,320 € | `estimate+flight` |
| 23.04. | LOP → CMB | inter | 580 € | `estimate` |
| 10.05. | CMB → MAD | return | 826 € | `estimate+flight` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 39 Tage mit Surf-Score >= 6 (longboardtauglich)
- Arbeitszeit in Lombok: 08:00-15:00 CET = 14:00-21:00 vor Ort (+6.0 h); 8.0 h freier Morgen; 2.0 h Abend weg; Fenster um -1.0 h verschoben
- Arbeitszeit in SL Ost: 08:00-15:00 CET = 11:30-18:30 vor Ort (+3.5 h); 5.5 h freier Morgen; Fenster um -1.0 h verschoben
- Indonesien: Trockenzeit/Passat setzt ein (01.04.-15.05.) faellt in Lombok [Impact: high]
- Sri Lanka: SW-Monsun setzt ein (25.04.-20.05.) faellt in SL Ost [Impact: high]

### 3. SL Süd -> N-Vietnam

**12.03.–22.04. 2027** · 42 Tage · ab **MAD** (Anreise aus `tenerife`) · zurück über **MAD** · `separate_tickets`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **6,297 €** |
| davon Flüge | 2,337 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 3,820 € |
| Visa | 140 € |
| Kosten pro Tag (beide) | 150 € |
| Erlebnis-Score pro Tag | 7.16 / 10 |
| Urlaubstage (verteilt) | 14 von 42 |
| Tage mit Longboard-Surf (Score ≥ 6) | 22 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Arbeit/Urlaub | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|---|
| 12.03.–02.04. | 22 | 11 / 11 | Sri Lanka Suedkueste (Weligama / Ahangama / Hiriketiya / Dikwella) | 9.0 | 9.0 | 6.0 | 8 | 55 € |
| 03.04.–22.04. | 20 | 17 / 3 | Nordvietnam (Hanoi / Ha Giang / Sapa / Cao Bang / Ba Be) | 9.0 | 0.0 | 7.9 | 9 | 35 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 12.03. | MAD → CMB | outbound | 920 € | `estimate+flight` |
| 03.04. | CMB → HAN | inter | 520 € | `estimate` |
| 22.04. | HAN → MAD | return | 897 € | `estimate+flight` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 22 Tage mit Surf-Score >= 6 (longboardtauglich)
- Arbeitszeit in N-Vietnam: 08:00-15:00 CET = 13:00-20:00 vor Ort (+5.0 h); 7.0 h freier Morgen; 1.0 h Abend weg; Fenster um -1.0 h verschoben
- Arbeitszeit in SL Süd: 08:00-15:00 CET = 12:30-19:30 vor Ort (+4.5 h); 6.5 h freier Morgen; 0.5 h Abend weg; Fenster um -1.0 h verschoben

### 4. SL Süd -> Kerala

**12.03.–11.04. 2027** · 31 Tage · ab **MAD** (Anreise aus `tenerife`) · zurück über **MAD** · `separate_tickets`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **5,337 €** |
| davon Flüge | 2,037 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 3,140 € |
| Visa | 160 € |
| Kosten pro Tag (beide) | 172 € |
| Erlebnis-Score pro Tag | 7.62 / 10 |
| Urlaubstage (verteilt) | 14 von 31 |
| Tage mit Longboard-Surf (Score ≥ 6) | 22 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Arbeit/Urlaub | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|---|
| 12.03.–02.04. | 22 | 11 / 11 | Sri Lanka Suedkueste (Weligama / Ahangama / Hiriketiya / Dikwella) | 9.0 | 9.0 | 6.0 | 8 | 55 € |
| 03.04.–11.04. | 9 | 6 / 3 | Kerala / Varkala / Kovalam | 4.4 | 2.4 | 8.0 | 6 | 40 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 12.03. | MAD → CMB | outbound | 920 € | `estimate+flight` |
| 03.04. | CMB → TRV | inter | 220 € | `estimate` |
| 11.04. | TRV → MAD | return | 897 € | `estimate+flight` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 22 Tage mit Surf-Score >= 6 (longboardtauglich)
- Arbeitszeit in Kerala: 08:00-15:00 CET = 11:30-18:30 vor Ort (+3.5 h); 5.5 h freier Morgen; Fenster um -1.0 h verschoben
- Arbeitszeit in SL Süd: 08:00-15:00 CET = 12:30-19:30 vor Ort (+4.5 h); 6.5 h freier Morgen; 0.5 h Abend weg; Fenster um -1.0 h verschoben

### 5. N-Vietnam -> Lombok

**01.04.–10.05. 2027** · 40 Tage · ab **MAD** (Anreise aus `tenerife`) · zurück über **MAD** · `separate_tickets`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **6,268 €** |
| davon Flüge | 2,698 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 3,460 € |
| Visa | 110 € |
| Kosten pro Tag (beide) | 157 € |
| Erlebnis-Score pro Tag | 7.24 / 10 |
| Urlaubstage (verteilt) | 14 von 40 |
| Tage mit Longboard-Surf (Score ≥ 6) | 22 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Arbeit/Urlaub | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|---|
| 01.04.–18.04. | 18 | 15 / 3 | Nordvietnam (Hanoi / Ha Giang / Sapa / Cao Bang / Ba Be) | 9.0 | 0.0 | 7.6 | 9 | 35 € |
| 19.04.–10.05. | 22 | 11 / 11 | Lombok Sued (Kuta / Gerupuk / Tanjung Aan / Mawi) | 9.0 | 9.0 | 8.0 | 7 | 50 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 01.04. | MAD → HAN | outbound | 1,000 € | `estimate+flight` |
| 19.04. | HAN → LOP | inter | 520 € | `estimate` |
| 10.05. | LOP → MAD | return | 1,178 € | `estimate+flight` |

**Hinweise**

- 1. Mai / Golden Week-Vorlauf (29.04.-05.05.) faellt in Lombok [Impact: medium]
- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 22 Tage mit Surf-Score >= 6 (longboardtauglich)
- Arbeitszeit in Lombok: 08:00-15:00 CET = 14:00-21:00 vor Ort (+6.0 h); 8.0 h freier Morgen; 2.0 h Abend weg; Fenster um -1.0 h verschoben
- Arbeitszeit in N-Vietnam: 08:00-15:00 CET = 13:00-20:00 vor Ort (+5.0 h); 7.0 h freier Morgen; 1.0 h Abend weg; Fenster um -1.0 h verschoben
- Indonesien: Trockenzeit/Passat setzt ein (01.04.-15.05.) faellt in Lombok [Impact: high]

### 6. SL Süd -> Nepal

**12.03.–11.04. 2027** · 31 Tage · ab **MAD** (Anreise aus `tenerife`) · zurück über **MAD** · `separate_tickets`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **5,462 €** |
| davon Flüge | 2,232 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 3,050 € |
| Visa | 180 € |
| Kosten pro Tag (beide) | 176 € |
| Erlebnis-Score pro Tag | 7.52 / 10 |
| Urlaubstage (verteilt) | 14 von 31 |
| Tage mit Longboard-Surf (Score ≥ 6) | 22 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Arbeit/Urlaub | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|---|
| 12.03.–02.04. | 22 | 11 / 11 | Sri Lanka Suedkueste (Weligama / Ahangama / Hiriketiya / Dikwella) | 9.0 | 9.0 | 6.0 | 8 | 55 € |
| 03.04.–11.04. | 9 | 6 / 3 | Nepal (Kathmandu / Pokhara / Annapurna / Langtang) | 9.0 | 0.0 | 6.4 | 5 | 35 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 12.03. | MAD → CMB | outbound | 920 € | `estimate+flight` |
| 03.04. | CMB → KTM | inter | 380 € | `estimate` |
| 11.04. | KTM → MAD | return | 932 € | `estimate+flight` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 22 Tage mit Surf-Score >= 6 (longboardtauglich)
- Arbeitszeit in Nepal: 08:00-15:00 CET = 11:45-18:45 vor Ort (+3.8 h); 5.8 h freier Morgen; Fenster um -1.0 h verschoben
- Arbeitszeit in SL Süd: 08:00-15:00 CET = 12:30-19:30 vor Ort (+4.5 h); 6.5 h freier Morgen; 0.5 h Abend weg; Fenster um -1.0 h verschoben
