# Workation-Routenplan 2027

*Erzeugt am 25.10.2026. Reisefenster 12.03.–10.05., 28–42 Tage, 2 Personen, Abflug ab MAD, BCN.*

## Datenlage

**Noch keine echten Flugpreise geladen.** Alle Flugkosten sind Schätzwerte aus `data/route_hints.yaml`. Die Saison-Logik und die Routenreihenfolge stehen damit schon, die absoluten Preise aber nicht. Sobald Scrapes in `data/prices/*.csv` liegen, rechnet derselbe Lauf mit echten Zahlen.

## Saison-Matrix

Gewichteter Tagesscore je Ziel und Halbmonat (0–10, höher = besser). **X** = hart ausgeschlossen. Fett = Saisonhoch des Ziels.

| Ziel | Tier | Work | 03. 1.-15. | 03. 16.-31. | 04. 1.-15. | 04. 16.-30. | 05. 1.-15. |
|---|---|---|---|---|---|---|---|
| SL Süd | A | 8 | **8.8** | **8.8** | 8.5 | 7.9 | 6.7 |
| Lombok | A | 7 | 5.9 | 6.3 | 7.4 | 8.2 | **8.5** |
| Sumbawa | B | 3 | 5.3 | 5.6 | 6.5 | 7.3 | **7.6** |
| SL Ost | B | 5 | 4.7 | 5.0 | 5.7 | 6.4 | **7.1** |
| W-Sumatra | C | 4 | 5.2 | 5.4 | 6.2 | 6.9 | **7.0** |
| Madagaskar | C | 2 | 3.8 | 4.1 | 5.1 | 6.1 | **6.8** |
| Taiwan | B | 10 | **6.6** | 6.5 | 6.3 | 6.0 | 5.5 |
| Cherating | C | 5 | **5.8** | 5.6 | 5.1 | 4.5 | 4.3 |
| Kerala | B | 6 | **5.6** | 5.3 | 4.8 | 4.3 | 4.6 |
| Oman | B | 7 | **5.0** | **5.0** | 4.8 | 4.3 | 3.8 |
| Penang/Langkawi | B | 9 | 4.7 | 4.8 | **4.9** | 4.6 | 4.5 |
| N-Vietnam | A | 9 | 4.0 | 4.3 | 4.8 | **4.8** | 4.6 |
| Andamanen | C | 3 | 4.3 | 4.3 | **4.3** | 4.1 | 4.0 |
| Nepal | B | 5 | 3.7 | 3.8 | **4.0** | 3.8 | 3.5 |
| Kambodscha | C | 6 | **3.5** | 3.4 | 3.1 | 2.9 | 3.3 |
| Raja Ampat | C | 3 | **3.3** | **3.3** | **3.3** | 3.0 | 2.6 |
| Laos | D | 4 | **X** | **X** | **X** | **X** | **3.0** |

*Gewichtung: Wetter 25%, Surf 42%, Ruhe 10%, Arbeitsfähigkeit 23%; Abzug 0.12/h Zeitversatz über 3 h, Tropen-Bonus +0.5.*

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
| 28 Tage | SL Süd -> Lombok | 14.03.–10.04. | 6,038 € | 216 € | 8.00 | 28 |
| 35 Tage | SL Süd -> Lombok | 18.03.–21.04. | 6,778 € | 194 € | 8.12 | 35 |
| 42 Tage | SL Süd -> Lombok | 16.03.–26.04. | 7,478 € | 178 € | 8.15 | 42 |

## Routenvorschläge

### 1. SL Süd -> Lombok

**16.03.–26.04. 2027** · 42 Tage · ab **MAD** · Ticketstrategie: `self_transfer`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **7,478 €** |
| davon Flüge | 2,908 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 4,420 € |
| Visa | 150 € |
| Kosten pro Tag (beide) | 178 € |
| Erlebnis-Score pro Tag | 8.15 / 10 |
| Tage mit Longboard-Surf (Score ≥ 6) | 42 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|
| 16.03.–06.04. | 22 | Sri Lanka Suedkueste (Weligama / Ahangama / Hiriketiya / Dikwella) | 8.8 | 8.8 | 5.5 | 8 | 55 € |
| 07.04.–26.04. | 20 | Lombok Sued (Kuta / Gerupuk / Tanjung Aan / Mawi) | 8.9 | 8.9 | 8.0 | 7 | 50 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 16.03. | MAD → CMB | outbound | 870 € | `estimate+feeder` |
| 07.04. | CMB → LOP | inter | 580 € | `estimate` |
| 26.04. | LOP → MAD | return | 1,118 € | `estimate+feeder` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 42 Tage mit Surf-Score >= 6 (longboardtauglich)
- Indonesien: Trockenzeit/Passat setzt ein (01.04.-15.05.) faellt in Lombok [Impact: high]
- Self-Transfer ab MAD: Residentenrabatt nutzbar, aber kein Umsteigeschutz (4 h Puffer + 1 Hotelnacht eingerechnet)

### 2. SL Süd -> Sumbawa

**16.03.–26.04. 2027** · 42 Tage · ab **MAD** · Ticketstrategie: `self_transfer`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **7,278 €** |
| davon Flüge | 2,908 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 4,220 € |
| Visa | 150 € |
| Kosten pro Tag (beide) | 173 € |
| Erlebnis-Score pro Tag | 7.73 / 10 |
| Tage mit Longboard-Surf (Score ≥ 6) | 42 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|
| 16.03.–06.04. | 22 | Sri Lanka Suedkueste (Weligama / Ahangama / Hiriketiya / Dikwella) | 8.8 | 8.8 | 5.5 | 8 | 55 € |
| 07.04.–26.04. | 20 | Sumbawa (Lakey Peak / Maluk / Scar Reef) | 8.9 | 8.9 | 8.0 | 3 | 45 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 16.03. | MAD → CMB | outbound | 870 € | `estimate+feeder` |
| 07.04. | CMB → LOP | inter | 580 € | `estimate` |
| 26.04. | LOP → MAD | return | 1,118 € | `estimate+feeder` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 42 Tage mit Surf-Score >= 6 (longboardtauglich)
- Indonesien: Trockenzeit/Passat setzt ein (01.04.-15.05.) faellt in Sumbawa [Impact: high]
- Schwache Arbeitsinfrastruktur: Sumbawa
- Self-Transfer ab MAD: Residentenrabatt nutzbar, aber kein Umsteigeschutz (4 h Puffer + 1 Hotelnacht eingerechnet)

### 3. SL Süd -> Lombok -> SL Ost

**16.03.–26.04. 2027** · 42 Tage · ab **MAD** · Ticketstrategie: `self_transfer`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **7,616 €** |
| davon Flüge | 3,136 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 4,330 € |
| Visa | 150 € |
| Kosten pro Tag (beide) | 181 € |
| Erlebnis-Score pro Tag | 7.68 / 10 |
| Tage mit Longboard-Surf (Score ≥ 6) | 36 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|
| 16.03.–06.04. | 22 | Sri Lanka Suedkueste (Weligama / Ahangama / Hiriketiya / Dikwella) | 8.8 | 8.8 | 5.5 | 8 | 55 € |
| 07.04.–17.04. | 11 | Lombok Sued (Kuta / Gerupuk / Tanjung Aan / Mawi) | 8.2 | 8.2 | 8.0 | 7 | 50 € |
| 18.04.–26.04. | 9 | Sri Lanka Ostkueste (Arugam Bay) | 7.6 | 5.1 | 8.0 | 5 | 45 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 16.03. | MAD → CMB | outbound | 870 € | `estimate+feeder` |
| 07.04. | CMB → LOP | inter | 580 € | `estimate` |
| 18.04. | LOP → CMB | inter | 580 € | `estimate` |
| 26.04. | CMB → MAD | return | 766 € | `estimate+feeder` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 36 Tage mit Surf-Score >= 6 (longboardtauglich)
- Indonesien: Trockenzeit/Passat setzt ein (01.04.-15.05.) faellt in Lombok [Impact: high]
- Self-Transfer ab MAD: Residentenrabatt nutzbar, aber kein Umsteigeschutz (4 h Puffer + 1 Hotelnacht eingerechnet)
- Sri Lanka: SW-Monsun setzt ein (25.04.-20.05.) faellt in SL Ost [Impact: high]

### 4. Lombok -> SL Ost

**01.04.–10.05. 2027** · 40 Tage · ab **MAD** · Ticketstrategie: `self_transfer`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **6,926 €** |
| davon Flüge | 2,956 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 3,820 € |
| Visa | 150 € |
| Kosten pro Tag (beide) | 173 € |
| Erlebnis-Score pro Tag | 7.36 / 10 |
| Tage mit Longboard-Surf (Score ≥ 6) | 39 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|
| 01.04.–22.04. | 22 | Lombok Sued (Kuta / Gerupuk / Tanjung Aan / Mawi) | 8.2 | 8.2 | 8.0 | 7 | 50 € |
| 23.04.–10.05. | 18 | Sri Lanka Ostkueste (Arugam Bay) | 8.0 | 6.9 | 7.1 | 5 | 45 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 01.04. | MAD → LOP | outbound | 1,270 € | `estimate+feeder` |
| 23.04. | LOP → CMB | inter | 580 € | `estimate` |
| 10.05. | CMB → MAD | return | 766 € | `estimate+feeder` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 39 Tage mit Surf-Score >= 6 (longboardtauglich)
- Indonesien: Trockenzeit/Passat setzt ein (01.04.-15.05.) faellt in Lombok [Impact: high]
- Self-Transfer ab MAD: Residentenrabatt nutzbar, aber kein Umsteigeschutz (4 h Puffer + 1 Hotelnacht eingerechnet)
- Sri Lanka: SW-Monsun setzt ein (25.04.-20.05.) faellt in SL Ost [Impact: high]

### 5. SL Süd -> Sumbawa -> SL Ost

**16.03.–26.04. 2027** · 42 Tage · ab **MAD** · Ticketstrategie: `self_transfer`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **7,506 €** |
| davon Flüge | 3,136 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 4,220 € |
| Visa | 150 € |
| Kosten pro Tag (beide) | 179 € |
| Erlebnis-Score pro Tag | 7.46 / 10 |
| Tage mit Longboard-Surf (Score ≥ 6) | 36 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|
| 16.03.–06.04. | 22 | Sri Lanka Suedkueste (Weligama / Ahangama / Hiriketiya / Dikwella) | 8.8 | 8.8 | 5.5 | 8 | 55 € |
| 07.04.–17.04. | 11 | Sumbawa (Lakey Peak / Maluk / Scar Reef) | 8.2 | 8.2 | 8.0 | 3 | 45 € |
| 18.04.–26.04. | 9 | Sri Lanka Ostkueste (Arugam Bay) | 7.6 | 5.1 | 8.0 | 5 | 45 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 16.03. | MAD → CMB | outbound | 870 € | `estimate+feeder` |
| 07.04. | CMB → LOP | inter | 580 € | `estimate` |
| 18.04. | LOP → CMB | inter | 580 € | `estimate` |
| 26.04. | CMB → MAD | return | 766 € | `estimate+feeder` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 36 Tage mit Surf-Score >= 6 (longboardtauglich)
- Indonesien: Trockenzeit/Passat setzt ein (01.04.-15.05.) faellt in Sumbawa [Impact: high]
- Schwache Arbeitsinfrastruktur: Sumbawa
- Self-Transfer ab MAD: Residentenrabatt nutzbar, aber kein Umsteigeschutz (4 h Puffer + 1 Hotelnacht eingerechnet)
- Sri Lanka: SW-Monsun setzt ein (25.04.-20.05.) faellt in SL Ost [Impact: high]

### 6. Kerala -> SL Süd -> Lombok

**12.03.–22.04. 2027** · 42 Tage · ab **MAD** · Ticketstrategie: `self_transfer`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **7,638 €** |
| davon Flüge | 3,208 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 4,210 € |
| Visa | 220 € |
| Kosten pro Tag (beide) | 182 € |
| Erlebnis-Score pro Tag | 7.38 / 10 |
| Tage mit Longboard-Surf (Score ≥ 6) | 33 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|
| 12.03.–20.03. | 9 | Kerala / Varkala / Kovalam | 5.0 | 3.0 | 8.0 | 6 | 40 € |
| 21.03.–08.04. | 19 | Sri Lanka Suedkueste (Weligama / Ahangama / Hiriketiya / Dikwella) | 8.9 | 8.9 | 5.9 | 8 | 55 € |
| 09.04.–22.04. | 14 | Lombok Sued (Kuta / Gerupuk / Tanjung Aan / Mawi) | 9.0 | 9.0 | 8.0 | 7 | 50 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 12.03. | MAD → TRV | outbound | 950 € | `estimate+feeder` |
| 21.03. | TRV → CMB | inter | 220 € | `estimate` |
| 09.04. | CMB → LOP | inter | 580 € | `estimate` |
| 22.04. | LOP → MAD | return | 1,118 € | `estimate+feeder` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 33 Tage mit Surf-Score >= 6 (longboardtauglich)
- Indonesien: Trockenzeit/Passat setzt ein (01.04.-15.05.) faellt in Lombok [Impact: high]
- Self-Transfer ab MAD: Residentenrabatt nutzbar, aber kein Umsteigeschutz (4 h Puffer + 1 Hotelnacht eingerechnet)

### 7. SL Süd -> N-Vietnam -> Lombok

**12.03.–22.04. 2027** · 42 Tage · ab **MAD** · Ticketstrategie: `self_transfer`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **7,698 €** |
| davon Flüge | 3,368 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 4,130 € |
| Visa | 200 € |
| Kosten pro Tag (beide) | 183 € |
| Erlebnis-Score pro Tag | 7.41 / 10 |
| Tage mit Longboard-Surf (Score ≥ 6) | 33 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|
| 12.03.–31.03. | 20 | Sri Lanka Suedkueste (Weligama / Ahangama / Hiriketiya / Dikwella) | 9.0 | 9.0 | 6.0 | 8 | 55 € |
| 01.04.–09.04. | 9 | Nordvietnam (Hanoi / Ha Giang / Sapa / Cao Bang / Ba Be) | 8.7 | 0.0 | 8.0 | 9 | 35 € |
| 10.04.–22.04. | 13 | Lombok Sued (Kuta / Gerupuk / Tanjung Aan / Mawi) | 9.0 | 9.0 | 8.0 | 7 | 50 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 12.03. | MAD → CMB | outbound | 870 € | `estimate+feeder` |
| 01.04. | CMB → HAN | inter | 520 € | `estimate` |
| 10.04. | HAN → LOP | inter | 520 € | `estimate` |
| 22.04. | LOP → MAD | return | 1,118 € | `estimate+feeder` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 33 Tage mit Surf-Score >= 6 (longboardtauglich)
- Indonesien: Trockenzeit/Passat setzt ein (01.04.-15.05.) faellt in Lombok [Impact: high]
- Self-Transfer ab MAD: Residentenrabatt nutzbar, aber kein Umsteigeschutz (4 h Puffer + 1 Hotelnacht eingerechnet)

### 8. SL Süd -> Kerala -> SL Ost

**16.03.–26.04. 2027** · 42 Tage · ab **MAD** · Ticketstrategie: `self_transfer`

| Kennzahl | Wert |
|---|---|
| Gesamtkosten (2 Pers.) | **6,739 €** |
| davon Flüge | 2,449 € |
| davon vor Ort (Unterkunft/Essen/Mobilität) | 4,130 € |
| Visa | 160 € |
| Kosten pro Tag (beide) | 160 € |
| Erlebnis-Score pro Tag | 6.91 / 10 |
| Tage mit Longboard-Surf (Score ≥ 6) | 26 |
| Schätzanteil der Flugpreise | 100% |

**Blöcke**

| Zeitraum | Tage | Ziel | Wetter | Surf | Ruhe | Work | €/Tag/Pers |
|---|---|---|---|---|---|---|---|
| 16.03.–06.04. | 22 | Sri Lanka Suedkueste (Weligama / Ahangama / Hiriketiya / Dikwella) | 8.8 | 8.8 | 5.5 | 8 | 55 € |
| 07.04.–15.04. | 9 | Kerala / Varkala / Kovalam | 3.7 | 2.0 | 8.0 | 6 | 40 € |
| 16.04.–26.04. | 11 | Sri Lanka Ostkueste (Arugam Bay) | 7.6 | 5.3 | 8.0 | 5 | 45 € |

**Flüge**

| Datum | Strecke | Art | Preis (2 Pers.) | Quelle |
|---|---|---|---|---|
| 16.03. | MAD → CMB | outbound | 870 € | `estimate+feeder` |
| 07.04. | CMB → TRV | inter | 220 € | `estimate` |
| 16.04. | TRV → CMB | inter | 253 € | `estimate*1.15(Sinhala & Tamil New Year)` |
| 26.04. | CMB → MAD | return | 766 € | `estimate+feeder` |

**Hinweise**

- 100% der Flugkosten sind Schaetzwerte - mit echten Scrapes neu rechnen
- 26 Tage mit Surf-Score >= 6 (longboardtauglich)
- Self-Transfer ab MAD: Residentenrabatt nutzbar, aber kein Umsteigeschutz (4 h Puffer + 1 Hotelnacht eingerechnet)
- Sri Lanka: SW-Monsun setzt ein (25.04.-20.05.) faellt in SL Ost [Impact: high]
