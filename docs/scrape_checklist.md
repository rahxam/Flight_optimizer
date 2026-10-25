# Scrape-Checkliste Google Flights

294 Suchen. Bei ~6 s Pause pro Abfrage: ca. 29 Minuten automatisiert.

Automatisiert: `node scripts/scrape_google_flights.cjs data/prices/_queries.json data/prices/scraped.csv`

Manuell: Link anklicken, guenstigsten Preis ablesen, Zeile in `data/prices/manual.csv` eintragen (Schema: `data/prices/_SCHEMA.csv`).

Die `tfs`-Links kodieren die Suche direkt. Falls Google das Format aendert,
nutze die Fallback-Links (einfache Textsuche, kein Multi-City).

## Einzelticket-Vergleich Leg 1 (4)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `c001-s0` | MAD->CMB | 2027-03-16 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDTUFEcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+CMB+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `c003-s0` | MAD->CMB | 2027-03-16 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDTUFEcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+CMB+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `c004-s0` | MAD->LOP | 2027-04-01 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDTUFEcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+LOP+am+2027-04-01+oneway&curr=EUR&hl=de) |
| `c006-s0` | MAD->TRV | 2027-03-12 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDTUFEcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+TRV+am+2027-03-12+oneway&curr=EUR&hl=de) |

## Einzelticket-Vergleich Leg 2 (4)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `c001-s1` | CMB->LOP | 2027-04-07 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDdqBRIDQ01CcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+LOP+am+2027-04-07+oneway&curr=EUR&hl=de) |
| `c003-s1` | CMB->LOP | 2027-04-07 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDdqBRIDQ01CcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+LOP+am+2027-04-07+oneway&curr=EUR&hl=de) |
| `c004-s1` | LOP->CMB | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDTE9QcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+CMB+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `c006-s1` | TRV->CMB | 2027-03-21 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjFqBRIDVFJWcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TRV+nach+CMB+am+2027-03-21+oneway&curr=EUR&hl=de) |

## Einzelticket-Vergleich Leg 3 (4)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `c001-s2` | LOP->MAD | 2027-04-26 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjZqBRIDTE9QcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+MAD+am+2027-04-26+oneway&curr=EUR&hl=de) |
| `c003-s2` | LOP->CMB | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDTE9QcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+CMB+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `c004-s2` | CMB->MAD | 2027-05-10 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMTBqBRIDQ01CcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+MAD+am+2027-05-10+oneway&curr=EUR&hl=de) |
| `c006-s2` | CMB->LOP | 2027-04-09 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDlqBRIDQ01CcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+LOP+am+2027-04-09+oneway&curr=EUR&hl=de) |

## Einzelticket-Vergleich Leg 4 (2)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `c003-s3` | CMB->MAD | 2027-04-26 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjZqBRIDQ01CcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+MAD+am+2027-04-26+oneway&curr=EUR&hl=de) |
| `c006-s3` | LOP->MAD | 2027-04-22 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjJqBRIDTE9QcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+MAD+am+2027-04-22+oneway&curr=EUR&hl=de) |

## Hinflug BCN->CMB (6)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0089` | BCN->CMB | 2027-03-12 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDQkNOcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+CMB+am+2027-03-12+oneway&curr=EUR&hl=de) |
| `g0090` | BCN->CMB | 2027-03-16 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDQkNOcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+CMB+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `g0091` | BCN->CMB | 2027-03-20 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjBqBRIDQkNOcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+CMB+am+2027-03-20+oneway&curr=EUR&hl=de) |
| `g0092` | BCN->CMB | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDQkNOcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+CMB+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0093` | BCN->CMB | 2027-03-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjhqBRIDQkNOcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+CMB+am+2027-03-28+oneway&curr=EUR&hl=de) |
| `g0094` | BCN->CMB | 2027-04-01 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDQkNOcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+CMB+am+2027-04-01+oneway&curr=EUR&hl=de) |

## Hinflug BCN->HAN (6)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0122` | BCN->HAN | 2027-03-12 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDQkNOcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+HAN+am+2027-03-12+oneway&curr=EUR&hl=de) |
| `g0123` | BCN->HAN | 2027-03-16 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDQkNOcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+HAN+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `g0124` | BCN->HAN | 2027-03-20 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjBqBRIDQkNOcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+HAN+am+2027-03-20+oneway&curr=EUR&hl=de) |
| `g0125` | BCN->HAN | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDQkNOcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+HAN+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0126` | BCN->HAN | 2027-03-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjhqBRIDQkNOcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+HAN+am+2027-03-28+oneway&curr=EUR&hl=de) |
| `g0127` | BCN->HAN | 2027-04-01 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDQkNOcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+HAN+am+2027-04-01+oneway&curr=EUR&hl=de) |

## Hinflug BCN->KTM (6)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0144` | BCN->KTM | 2027-03-12 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDQkNOcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+KTM+am+2027-03-12+oneway&curr=EUR&hl=de) |
| `g0145` | BCN->KTM | 2027-03-16 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDQkNOcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+KTM+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `g0146` | BCN->KTM | 2027-03-20 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjBqBRIDQkNOcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+KTM+am+2027-03-20+oneway&curr=EUR&hl=de) |
| `g0147` | BCN->KTM | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDQkNOcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+KTM+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0148` | BCN->KTM | 2027-03-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjhqBRIDQkNOcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+KTM+am+2027-03-28+oneway&curr=EUR&hl=de) |
| `g0149` | BCN->KTM | 2027-04-01 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDQkNOcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+KTM+am+2027-04-01+oneway&curr=EUR&hl=de) |

## Hinflug BCN->KUL (6)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0100` | BCN->KUL | 2027-03-12 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDQkNOcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+KUL+am+2027-03-12+oneway&curr=EUR&hl=de) |
| `g0101` | BCN->KUL | 2027-03-16 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDQkNOcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+KUL+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `g0102` | BCN->KUL | 2027-03-20 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjBqBRIDQkNOcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+KUL+am+2027-03-20+oneway&curr=EUR&hl=de) |
| `g0103` | BCN->KUL | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDQkNOcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+KUL+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0104` | BCN->KUL | 2027-03-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjhqBRIDQkNOcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+KUL+am+2027-03-28+oneway&curr=EUR&hl=de) |
| `g0105` | BCN->KUL | 2027-04-01 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDQkNOcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+KUL+am+2027-04-01+oneway&curr=EUR&hl=de) |

## Hinflug BCN->LOP (6)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0111` | BCN->LOP | 2027-03-12 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDQkNOcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+LOP+am+2027-03-12+oneway&curr=EUR&hl=de) |
| `g0112` | BCN->LOP | 2027-03-16 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDQkNOcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+LOP+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `g0113` | BCN->LOP | 2027-03-20 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjBqBRIDQkNOcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+LOP+am+2027-03-20+oneway&curr=EUR&hl=de) |
| `g0114` | BCN->LOP | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDQkNOcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+LOP+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0115` | BCN->LOP | 2027-03-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjhqBRIDQkNOcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+LOP+am+2027-03-28+oneway&curr=EUR&hl=de) |
| `g0116` | BCN->LOP | 2027-04-01 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDQkNOcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+LOP+am+2027-04-01+oneway&curr=EUR&hl=de) |

## Hinflug BCN->MCT (6)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0155` | BCN->MCT | 2027-03-12 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDQkNOcgUSA01DVEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+MCT+am+2027-03-12+oneway&curr=EUR&hl=de) |
| `g0156` | BCN->MCT | 2027-03-16 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDQkNOcgUSA01DVEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+MCT+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `g0157` | BCN->MCT | 2027-03-20 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjBqBRIDQkNOcgUSA01DVEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+MCT+am+2027-03-20+oneway&curr=EUR&hl=de) |
| `g0158` | BCN->MCT | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDQkNOcgUSA01DVEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+MCT+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0159` | BCN->MCT | 2027-03-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjhqBRIDQkNOcgUSA01DVEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+MCT+am+2027-03-28+oneway&curr=EUR&hl=de) |
| `g0160` | BCN->MCT | 2027-04-01 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDQkNOcgUSA01DVEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+MCT+am+2027-04-01+oneway&curr=EUR&hl=de) |

## Hinflug BCN->TPE (6)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0133` | BCN->TPE | 2027-03-12 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDQkNOcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+TPE+am+2027-03-12+oneway&curr=EUR&hl=de) |
| `g0134` | BCN->TPE | 2027-03-16 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDQkNOcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+TPE+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `g0135` | BCN->TPE | 2027-03-20 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjBqBRIDQkNOcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+TPE+am+2027-03-20+oneway&curr=EUR&hl=de) |
| `g0136` | BCN->TPE | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDQkNOcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+TPE+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0137` | BCN->TPE | 2027-03-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjhqBRIDQkNOcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+TPE+am+2027-03-28+oneway&curr=EUR&hl=de) |
| `g0138` | BCN->TPE | 2027-04-01 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDQkNOcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+TPE+am+2027-04-01+oneway&curr=EUR&hl=de) |

## Hinflug BCN->TRV (6)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0166` | BCN->TRV | 2027-03-12 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDQkNOcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+TRV+am+2027-03-12+oneway&curr=EUR&hl=de) |
| `g0167` | BCN->TRV | 2027-03-16 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDQkNOcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+TRV+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `g0168` | BCN->TRV | 2027-03-20 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjBqBRIDQkNOcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+TRV+am+2027-03-20+oneway&curr=EUR&hl=de) |
| `g0169` | BCN->TRV | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDQkNOcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+TRV+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0170` | BCN->TRV | 2027-03-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjhqBRIDQkNOcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+TRV+am+2027-03-28+oneway&curr=EUR&hl=de) |
| `g0171` | BCN->TRV | 2027-04-01 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDQkNOcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+BCN+nach+TRV+am+2027-04-01+oneway&curr=EUR&hl=de) |

## Hinflug MAD->CMB (6)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0001` | MAD->CMB | 2027-03-12 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDTUFEcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+CMB+am+2027-03-12+oneway&curr=EUR&hl=de) |
| `g0002` | MAD->CMB | 2027-03-16 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDTUFEcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+CMB+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `g0003` | MAD->CMB | 2027-03-20 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjBqBRIDTUFEcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+CMB+am+2027-03-20+oneway&curr=EUR&hl=de) |
| `g0004` | MAD->CMB | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDTUFEcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+CMB+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0005` | MAD->CMB | 2027-03-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjhqBRIDTUFEcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+CMB+am+2027-03-28+oneway&curr=EUR&hl=de) |
| `g0006` | MAD->CMB | 2027-04-01 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDTUFEcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+CMB+am+2027-04-01+oneway&curr=EUR&hl=de) |

## Hinflug MAD->HAN (6)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0034` | MAD->HAN | 2027-03-12 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDTUFEcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+HAN+am+2027-03-12+oneway&curr=EUR&hl=de) |
| `g0035` | MAD->HAN | 2027-03-16 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDTUFEcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+HAN+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `g0036` | MAD->HAN | 2027-03-20 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjBqBRIDTUFEcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+HAN+am+2027-03-20+oneway&curr=EUR&hl=de) |
| `g0037` | MAD->HAN | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDTUFEcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+HAN+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0038` | MAD->HAN | 2027-03-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjhqBRIDTUFEcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+HAN+am+2027-03-28+oneway&curr=EUR&hl=de) |
| `g0039` | MAD->HAN | 2027-04-01 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDTUFEcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+HAN+am+2027-04-01+oneway&curr=EUR&hl=de) |

## Hinflug MAD->KTM (6)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0056` | MAD->KTM | 2027-03-12 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDTUFEcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+KTM+am+2027-03-12+oneway&curr=EUR&hl=de) |
| `g0057` | MAD->KTM | 2027-03-16 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDTUFEcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+KTM+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `g0058` | MAD->KTM | 2027-03-20 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjBqBRIDTUFEcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+KTM+am+2027-03-20+oneway&curr=EUR&hl=de) |
| `g0059` | MAD->KTM | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDTUFEcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+KTM+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0060` | MAD->KTM | 2027-03-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjhqBRIDTUFEcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+KTM+am+2027-03-28+oneway&curr=EUR&hl=de) |
| `g0061` | MAD->KTM | 2027-04-01 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDTUFEcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+KTM+am+2027-04-01+oneway&curr=EUR&hl=de) |

## Hinflug MAD->KUL (6)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0012` | MAD->KUL | 2027-03-12 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDTUFEcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+KUL+am+2027-03-12+oneway&curr=EUR&hl=de) |
| `g0013` | MAD->KUL | 2027-03-16 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDTUFEcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+KUL+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `g0014` | MAD->KUL | 2027-03-20 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjBqBRIDTUFEcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+KUL+am+2027-03-20+oneway&curr=EUR&hl=de) |
| `g0015` | MAD->KUL | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDTUFEcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+KUL+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0016` | MAD->KUL | 2027-03-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjhqBRIDTUFEcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+KUL+am+2027-03-28+oneway&curr=EUR&hl=de) |
| `g0017` | MAD->KUL | 2027-04-01 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDTUFEcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+KUL+am+2027-04-01+oneway&curr=EUR&hl=de) |

## Hinflug MAD->LOP (6)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0023` | MAD->LOP | 2027-03-12 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDTUFEcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+LOP+am+2027-03-12+oneway&curr=EUR&hl=de) |
| `g0024` | MAD->LOP | 2027-03-16 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDTUFEcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+LOP+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `g0025` | MAD->LOP | 2027-03-20 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjBqBRIDTUFEcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+LOP+am+2027-03-20+oneway&curr=EUR&hl=de) |
| `g0026` | MAD->LOP | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDTUFEcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+LOP+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0027` | MAD->LOP | 2027-03-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjhqBRIDTUFEcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+LOP+am+2027-03-28+oneway&curr=EUR&hl=de) |
| `g0028` | MAD->LOP | 2027-04-01 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDTUFEcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+LOP+am+2027-04-01+oneway&curr=EUR&hl=de) |

## Hinflug MAD->MCT (6)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0067` | MAD->MCT | 2027-03-12 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDTUFEcgUSA01DVEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+MCT+am+2027-03-12+oneway&curr=EUR&hl=de) |
| `g0068` | MAD->MCT | 2027-03-16 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDTUFEcgUSA01DVEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+MCT+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `g0069` | MAD->MCT | 2027-03-20 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjBqBRIDTUFEcgUSA01DVEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+MCT+am+2027-03-20+oneway&curr=EUR&hl=de) |
| `g0070` | MAD->MCT | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDTUFEcgUSA01DVEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+MCT+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0071` | MAD->MCT | 2027-03-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjhqBRIDTUFEcgUSA01DVEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+MCT+am+2027-03-28+oneway&curr=EUR&hl=de) |
| `g0072` | MAD->MCT | 2027-04-01 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDTUFEcgUSA01DVEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+MCT+am+2027-04-01+oneway&curr=EUR&hl=de) |

## Hinflug MAD->TPE (6)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0045` | MAD->TPE | 2027-03-12 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDTUFEcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+TPE+am+2027-03-12+oneway&curr=EUR&hl=de) |
| `g0046` | MAD->TPE | 2027-03-16 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDTUFEcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+TPE+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `g0047` | MAD->TPE | 2027-03-20 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjBqBRIDTUFEcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+TPE+am+2027-03-20+oneway&curr=EUR&hl=de) |
| `g0048` | MAD->TPE | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDTUFEcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+TPE+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0049` | MAD->TPE | 2027-03-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjhqBRIDTUFEcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+TPE+am+2027-03-28+oneway&curr=EUR&hl=de) |
| `g0050` | MAD->TPE | 2027-04-01 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDTUFEcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+TPE+am+2027-04-01+oneway&curr=EUR&hl=de) |

## Hinflug MAD->TRV (6)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0078` | MAD->TRV | 2027-03-12 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDTUFEcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+TRV+am+2027-03-12+oneway&curr=EUR&hl=de) |
| `g0079` | MAD->TRV | 2027-03-16 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDTUFEcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+TRV+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `g0080` | MAD->TRV | 2027-03-20 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjBqBRIDTUFEcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+TRV+am+2027-03-20+oneway&curr=EUR&hl=de) |
| `g0081` | MAD->TRV | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDTUFEcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+TRV+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0082` | MAD->TRV | 2027-03-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjhqBRIDTUFEcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+TRV+am+2027-03-28+oneway&curr=EUR&hl=de) |
| `g0083` | MAD->TRV | 2027-04-01 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDTUFEcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+TRV+am+2027-04-01+oneway&curr=EUR&hl=de) |

## Multi-City Gesamtticket (4)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `c001-mc` | MAD->CMB / CMB->LOP / LOP->MAD | 2027-03-16 / 2027-04-07 / 2027-04-26 | multicity | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDTUFEcgUSA0NNQhoaEgoyMDI3LTA0LTA3agUSA0NNQnIFEgNMT1AaGhIKMjAyNy0wNC0yNmoFEgNMT1ByBRIDTUFEQAFAAUgBmAED&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+CMB+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `c003-mc` | MAD->CMB / CMB->LOP / LOP->CMB / CMB->MAD | 2027-03-16 / 2027-04-07 / 2027-04-18 / 2027-04-26 | multicity | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDTUFEcgUSA0NNQhoaEgoyMDI3LTA0LTA3agUSA0NNQnIFEgNMT1AaGhIKMjAyNy0wNC0xOGoFEgNMT1ByBRIDQ01CGhoSCjIwMjctMDQtMjZqBRIDQ01CcgUSA01BREABQAFIAZgBAw&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+CMB+am+2027-03-16+oneway&curr=EUR&hl=de) |
| `c004-mc` | MAD->LOP / LOP->CMB / CMB->MAD | 2027-04-01 / 2027-04-23 / 2027-05-10 | multicity | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDTUFEcgUSA0xPUBoaEgoyMDI3LTA0LTIzagUSA0xPUHIFEgNDTUIaGhIKMjAyNy0wNS0xMGoFEgNDTUJyBRIDTUFEQAFAAUgBmAED&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+LOP+am+2027-04-01+oneway&curr=EUR&hl=de) |
| `c006-mc` | MAD->TRV / TRV->CMB / CMB->LOP / LOP->MAD | 2027-03-12 / 2027-03-21 / 2027-04-09 / 2027-04-22 | multicity | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDTUFEcgUSA1RSVhoaEgoyMDI3LTAzLTIxagUSA1RSVnIFEgNDTUIaGhIKMjAyNy0wNC0wOWoFEgNDTUJyBRIDTE9QGhoSCjIwMjctMDQtMjJqBRIDTE9QcgUSA01BREABQAFIAZgBAw&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+TRV+am+2027-03-12+oneway&curr=EUR&hl=de) |

## Return-Vergleich Langstrecke (4)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `c001-rt` | MAD->CMB / CMB->MAD | 2027-03-16 / 2027-04-26 | return | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDTUFEcgUSA0NNQhoaEgoyMDI3LTA0LTI2agUSA0NNQnIFEgNNQURAAUABSAGYAQE&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+CMB+am+2027-03-16+zurueck+2027-04-26&curr=EUR&hl=de) |
| `c003-rt` | MAD->CMB / CMB->MAD | 2027-03-16 / 2027-04-26 | return | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTZqBRIDTUFEcgUSA0NNQhoaEgoyMDI3LTA0LTI2agUSA0NNQnIFEgNNQURAAUABSAGYAQE&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+CMB+am+2027-03-16+zurueck+2027-04-26&curr=EUR&hl=de) |
| `c004-rt` | MAD->LOP / LOP->MAD | 2027-04-01 / 2027-05-10 | return | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDFqBRIDTUFEcgUSA0xPUBoaEgoyMDI3LTA1LTEwagUSA0xPUHIFEgNNQURAAUABSAGYAQE&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+LOP+am+2027-04-01+zurueck+2027-05-10&curr=EUR&hl=de) |
| `c006-rt` | MAD->TRV / TRV->MAD | 2027-03-12 / 2027-04-22 | return | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMTJqBRIDTUFEcgUSA1RSVhoaEgoyMDI3LTA0LTIyagUSA1RSVnIFEgNNQURAAUABSAGYAQE&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MAD+nach+TRV+am+2027-03-12+zurueck+2027-04-22&curr=EUR&hl=de) |

## Rueckflug CMB->BCN (5)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0095` | CMB->BCN | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDQ01CcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+BCN+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0096` | CMB->BCN | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDQ01CcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+BCN+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0097` | CMB->BCN | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDQ01CcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+BCN+am+2027-04-28+oneway&curr=EUR&hl=de) |
| `g0098` | CMB->BCN | 2027-05-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDNqBRIDQ01CcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+BCN+am+2027-05-03+oneway&curr=EUR&hl=de) |
| `g0099` | CMB->BCN | 2027-05-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDhqBRIDQ01CcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+BCN+am+2027-05-08+oneway&curr=EUR&hl=de) |

## Rueckflug CMB->MAD (5)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0007` | CMB->MAD | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDQ01CcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+MAD+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0008` | CMB->MAD | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDQ01CcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+MAD+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0009` | CMB->MAD | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDQ01CcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+MAD+am+2027-04-28+oneway&curr=EUR&hl=de) |
| `g0010` | CMB->MAD | 2027-05-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDNqBRIDQ01CcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+MAD+am+2027-05-03+oneway&curr=EUR&hl=de) |
| `g0011` | CMB->MAD | 2027-05-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDhqBRIDQ01CcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+MAD+am+2027-05-08+oneway&curr=EUR&hl=de) |

## Rueckflug HAN->BCN (5)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0128` | HAN->BCN | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDSEFOcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+HAN+nach+BCN+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0129` | HAN->BCN | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDSEFOcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+HAN+nach+BCN+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0130` | HAN->BCN | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDSEFOcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+HAN+nach+BCN+am+2027-04-28+oneway&curr=EUR&hl=de) |
| `g0131` | HAN->BCN | 2027-05-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDNqBRIDSEFOcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+HAN+nach+BCN+am+2027-05-03+oneway&curr=EUR&hl=de) |
| `g0132` | HAN->BCN | 2027-05-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDhqBRIDSEFOcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+HAN+nach+BCN+am+2027-05-08+oneway&curr=EUR&hl=de) |

## Rueckflug HAN->MAD (5)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0040` | HAN->MAD | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDSEFOcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+HAN+nach+MAD+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0041` | HAN->MAD | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDSEFOcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+HAN+nach+MAD+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0042` | HAN->MAD | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDSEFOcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+HAN+nach+MAD+am+2027-04-28+oneway&curr=EUR&hl=de) |
| `g0043` | HAN->MAD | 2027-05-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDNqBRIDSEFOcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+HAN+nach+MAD+am+2027-05-03+oneway&curr=EUR&hl=de) |
| `g0044` | HAN->MAD | 2027-05-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDhqBRIDSEFOcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+HAN+nach+MAD+am+2027-05-08+oneway&curr=EUR&hl=de) |

## Rueckflug KTM->BCN (5)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0150` | KTM->BCN | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDS1RNcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KTM+nach+BCN+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0151` | KTM->BCN | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDS1RNcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KTM+nach+BCN+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0152` | KTM->BCN | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDS1RNcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KTM+nach+BCN+am+2027-04-28+oneway&curr=EUR&hl=de) |
| `g0153` | KTM->BCN | 2027-05-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDNqBRIDS1RNcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KTM+nach+BCN+am+2027-05-03+oneway&curr=EUR&hl=de) |
| `g0154` | KTM->BCN | 2027-05-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDhqBRIDS1RNcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KTM+nach+BCN+am+2027-05-08+oneway&curr=EUR&hl=de) |

## Rueckflug KTM->MAD (5)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0062` | KTM->MAD | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDS1RNcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KTM+nach+MAD+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0063` | KTM->MAD | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDS1RNcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KTM+nach+MAD+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0064` | KTM->MAD | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDS1RNcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KTM+nach+MAD+am+2027-04-28+oneway&curr=EUR&hl=de) |
| `g0065` | KTM->MAD | 2027-05-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDNqBRIDS1RNcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KTM+nach+MAD+am+2027-05-03+oneway&curr=EUR&hl=de) |
| `g0066` | KTM->MAD | 2027-05-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDhqBRIDS1RNcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KTM+nach+MAD+am+2027-05-08+oneway&curr=EUR&hl=de) |

## Rueckflug KUL->BCN (5)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0106` | KUL->BCN | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDS1VMcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+BCN+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0107` | KUL->BCN | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDS1VMcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+BCN+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0108` | KUL->BCN | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDS1VMcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+BCN+am+2027-04-28+oneway&curr=EUR&hl=de) |
| `g0109` | KUL->BCN | 2027-05-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDNqBRIDS1VMcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+BCN+am+2027-05-03+oneway&curr=EUR&hl=de) |
| `g0110` | KUL->BCN | 2027-05-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDhqBRIDS1VMcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+BCN+am+2027-05-08+oneway&curr=EUR&hl=de) |

## Rueckflug KUL->MAD (5)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0018` | KUL->MAD | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDS1VMcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+MAD+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0019` | KUL->MAD | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDS1VMcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+MAD+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0020` | KUL->MAD | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDS1VMcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+MAD+am+2027-04-28+oneway&curr=EUR&hl=de) |
| `g0021` | KUL->MAD | 2027-05-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDNqBRIDS1VMcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+MAD+am+2027-05-03+oneway&curr=EUR&hl=de) |
| `g0022` | KUL->MAD | 2027-05-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDhqBRIDS1VMcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+MAD+am+2027-05-08+oneway&curr=EUR&hl=de) |

## Rueckflug LOP->BCN (5)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0117` | LOP->BCN | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDTE9QcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+BCN+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0118` | LOP->BCN | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDTE9QcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+BCN+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0119` | LOP->BCN | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDTE9QcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+BCN+am+2027-04-28+oneway&curr=EUR&hl=de) |
| `g0120` | LOP->BCN | 2027-05-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDNqBRIDTE9QcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+BCN+am+2027-05-03+oneway&curr=EUR&hl=de) |
| `g0121` | LOP->BCN | 2027-05-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDhqBRIDTE9QcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+BCN+am+2027-05-08+oneway&curr=EUR&hl=de) |

## Rueckflug LOP->MAD (5)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0029` | LOP->MAD | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDTE9QcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+MAD+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0030` | LOP->MAD | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDTE9QcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+MAD+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0031` | LOP->MAD | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDTE9QcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+MAD+am+2027-04-28+oneway&curr=EUR&hl=de) |
| `g0032` | LOP->MAD | 2027-05-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDNqBRIDTE9QcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+MAD+am+2027-05-03+oneway&curr=EUR&hl=de) |
| `g0033` | LOP->MAD | 2027-05-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDhqBRIDTE9QcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+MAD+am+2027-05-08+oneway&curr=EUR&hl=de) |

## Rueckflug MCT->BCN (5)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0161` | MCT->BCN | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDTUNUcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MCT+nach+BCN+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0162` | MCT->BCN | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDTUNUcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MCT+nach+BCN+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0163` | MCT->BCN | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDTUNUcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MCT+nach+BCN+am+2027-04-28+oneway&curr=EUR&hl=de) |
| `g0164` | MCT->BCN | 2027-05-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDNqBRIDTUNUcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MCT+nach+BCN+am+2027-05-03+oneway&curr=EUR&hl=de) |
| `g0165` | MCT->BCN | 2027-05-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDhqBRIDTUNUcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MCT+nach+BCN+am+2027-05-08+oneway&curr=EUR&hl=de) |

## Rueckflug MCT->MAD (5)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0073` | MCT->MAD | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDTUNUcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MCT+nach+MAD+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0074` | MCT->MAD | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDTUNUcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MCT+nach+MAD+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0075` | MCT->MAD | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDTUNUcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MCT+nach+MAD+am+2027-04-28+oneway&curr=EUR&hl=de) |
| `g0076` | MCT->MAD | 2027-05-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDNqBRIDTUNUcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MCT+nach+MAD+am+2027-05-03+oneway&curr=EUR&hl=de) |
| `g0077` | MCT->MAD | 2027-05-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDhqBRIDTUNUcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MCT+nach+MAD+am+2027-05-08+oneway&curr=EUR&hl=de) |

## Rueckflug TPE->BCN (5)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0139` | TPE->BCN | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDVFBFcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TPE+nach+BCN+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0140` | TPE->BCN | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDVFBFcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TPE+nach+BCN+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0141` | TPE->BCN | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDVFBFcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TPE+nach+BCN+am+2027-04-28+oneway&curr=EUR&hl=de) |
| `g0142` | TPE->BCN | 2027-05-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDNqBRIDVFBFcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TPE+nach+BCN+am+2027-05-03+oneway&curr=EUR&hl=de) |
| `g0143` | TPE->BCN | 2027-05-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDhqBRIDVFBFcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TPE+nach+BCN+am+2027-05-08+oneway&curr=EUR&hl=de) |

## Rueckflug TPE->MAD (5)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0051` | TPE->MAD | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDVFBFcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TPE+nach+MAD+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0052` | TPE->MAD | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDVFBFcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TPE+nach+MAD+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0053` | TPE->MAD | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDVFBFcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TPE+nach+MAD+am+2027-04-28+oneway&curr=EUR&hl=de) |
| `g0054` | TPE->MAD | 2027-05-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDNqBRIDVFBFcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TPE+nach+MAD+am+2027-05-03+oneway&curr=EUR&hl=de) |
| `g0055` | TPE->MAD | 2027-05-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDhqBRIDVFBFcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TPE+nach+MAD+am+2027-05-08+oneway&curr=EUR&hl=de) |

## Rueckflug TRV->BCN (5)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0172` | TRV->BCN | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDVFJWcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TRV+nach+BCN+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0173` | TRV->BCN | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDVFJWcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TRV+nach+BCN+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0174` | TRV->BCN | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDVFJWcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TRV+nach+BCN+am+2027-04-28+oneway&curr=EUR&hl=de) |
| `g0175` | TRV->BCN | 2027-05-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDNqBRIDVFJWcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TRV+nach+BCN+am+2027-05-03+oneway&curr=EUR&hl=de) |
| `g0176` | TRV->BCN | 2027-05-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDhqBRIDVFJWcgUSA0JDTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TRV+nach+BCN+am+2027-05-08+oneway&curr=EUR&hl=de) |

## Rueckflug TRV->MAD (5)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0084` | TRV->MAD | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDVFJWcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TRV+nach+MAD+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0085` | TRV->MAD | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDVFJWcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TRV+nach+MAD+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0086` | TRV->MAD | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDVFJWcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TRV+nach+MAD+am+2027-04-28+oneway&curr=EUR&hl=de) |
| `g0087` | TRV->MAD | 2027-05-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDNqBRIDVFJWcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TRV+nach+MAD+am+2027-05-03+oneway&curr=EUR&hl=de) |
| `g0088` | TRV->MAD | 2027-05-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDUtMDhqBRIDVFJWcgUSA01BREABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+TRV+nach+MAD+am+2027-05-08+oneway&curr=EUR&hl=de) |

## Zwischenflug CMB->HAN (8)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0201` | CMB->HAN | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDQ01CcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+HAN+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0202` | CMB->HAN | 2027-03-29 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjlqBRIDQ01CcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+HAN+am+2027-03-29+oneway&curr=EUR&hl=de) |
| `g0203` | CMB->HAN | 2027-04-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDNqBRIDQ01CcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+HAN+am+2027-04-03+oneway&curr=EUR&hl=de) |
| `g0204` | CMB->HAN | 2027-04-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDhqBRIDQ01CcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+HAN+am+2027-04-08+oneway&curr=EUR&hl=de) |
| `g0205` | CMB->HAN | 2027-04-13 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMTNqBRIDQ01CcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+HAN+am+2027-04-13+oneway&curr=EUR&hl=de) |
| `g0206` | CMB->HAN | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDQ01CcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+HAN+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0207` | CMB->HAN | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDQ01CcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+HAN+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0208` | CMB->HAN | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDQ01CcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+HAN+am+2027-04-28+oneway&curr=EUR&hl=de) |

## Zwischenflug CMB->KTM (8)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0217` | CMB->KTM | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDQ01CcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+KTM+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0218` | CMB->KTM | 2027-03-29 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjlqBRIDQ01CcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+KTM+am+2027-03-29+oneway&curr=EUR&hl=de) |
| `g0219` | CMB->KTM | 2027-04-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDNqBRIDQ01CcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+KTM+am+2027-04-03+oneway&curr=EUR&hl=de) |
| `g0220` | CMB->KTM | 2027-04-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDhqBRIDQ01CcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+KTM+am+2027-04-08+oneway&curr=EUR&hl=de) |
| `g0221` | CMB->KTM | 2027-04-13 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMTNqBRIDQ01CcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+KTM+am+2027-04-13+oneway&curr=EUR&hl=de) |
| `g0222` | CMB->KTM | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDQ01CcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+KTM+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0223` | CMB->KTM | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDQ01CcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+KTM+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0224` | CMB->KTM | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDQ01CcgUSA0tUTUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+KTM+am+2027-04-28+oneway&curr=EUR&hl=de) |

## Zwischenflug CMB->KUL (8)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0177` | CMB->KUL | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDQ01CcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+KUL+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0178` | CMB->KUL | 2027-03-29 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjlqBRIDQ01CcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+KUL+am+2027-03-29+oneway&curr=EUR&hl=de) |
| `g0179` | CMB->KUL | 2027-04-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDNqBRIDQ01CcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+KUL+am+2027-04-03+oneway&curr=EUR&hl=de) |
| `g0180` | CMB->KUL | 2027-04-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDhqBRIDQ01CcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+KUL+am+2027-04-08+oneway&curr=EUR&hl=de) |
| `g0181` | CMB->KUL | 2027-04-13 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMTNqBRIDQ01CcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+KUL+am+2027-04-13+oneway&curr=EUR&hl=de) |
| `g0182` | CMB->KUL | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDQ01CcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+KUL+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0183` | CMB->KUL | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDQ01CcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+KUL+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0184` | CMB->KUL | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDQ01CcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+KUL+am+2027-04-28+oneway&curr=EUR&hl=de) |

## Zwischenflug CMB->LOP (8)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0185` | CMB->LOP | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDQ01CcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+LOP+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0186` | CMB->LOP | 2027-03-29 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjlqBRIDQ01CcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+LOP+am+2027-03-29+oneway&curr=EUR&hl=de) |
| `g0187` | CMB->LOP | 2027-04-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDNqBRIDQ01CcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+LOP+am+2027-04-03+oneway&curr=EUR&hl=de) |
| `g0188` | CMB->LOP | 2027-04-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDhqBRIDQ01CcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+LOP+am+2027-04-08+oneway&curr=EUR&hl=de) |
| `g0189` | CMB->LOP | 2027-04-13 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMTNqBRIDQ01CcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+LOP+am+2027-04-13+oneway&curr=EUR&hl=de) |
| `g0190` | CMB->LOP | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDQ01CcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+LOP+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0191` | CMB->LOP | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDQ01CcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+LOP+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0192` | CMB->LOP | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDQ01CcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+LOP+am+2027-04-28+oneway&curr=EUR&hl=de) |

## Zwischenflug CMB->TRV (8)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0241` | CMB->TRV | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDQ01CcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+TRV+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0242` | CMB->TRV | 2027-03-29 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjlqBRIDQ01CcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+TRV+am+2027-03-29+oneway&curr=EUR&hl=de) |
| `g0243` | CMB->TRV | 2027-04-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDNqBRIDQ01CcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+TRV+am+2027-04-03+oneway&curr=EUR&hl=de) |
| `g0244` | CMB->TRV | 2027-04-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDhqBRIDQ01CcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+TRV+am+2027-04-08+oneway&curr=EUR&hl=de) |
| `g0245` | CMB->TRV | 2027-04-13 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMTNqBRIDQ01CcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+TRV+am+2027-04-13+oneway&curr=EUR&hl=de) |
| `g0246` | CMB->TRV | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDQ01CcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+TRV+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0247` | CMB->TRV | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDQ01CcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+TRV+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0248` | CMB->TRV | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDQ01CcgUSA1RSVkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+CMB+nach+TRV+am+2027-04-28+oneway&curr=EUR&hl=de) |

## Zwischenflug HAN->TPE (8)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0233` | HAN->TPE | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDSEFOcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+HAN+nach+TPE+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0234` | HAN->TPE | 2027-03-29 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjlqBRIDSEFOcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+HAN+nach+TPE+am+2027-03-29+oneway&curr=EUR&hl=de) |
| `g0235` | HAN->TPE | 2027-04-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDNqBRIDSEFOcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+HAN+nach+TPE+am+2027-04-03+oneway&curr=EUR&hl=de) |
| `g0236` | HAN->TPE | 2027-04-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDhqBRIDSEFOcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+HAN+nach+TPE+am+2027-04-08+oneway&curr=EUR&hl=de) |
| `g0237` | HAN->TPE | 2027-04-13 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMTNqBRIDSEFOcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+HAN+nach+TPE+am+2027-04-13+oneway&curr=EUR&hl=de) |
| `g0238` | HAN->TPE | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDSEFOcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+HAN+nach+TPE+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0239` | HAN->TPE | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDSEFOcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+HAN+nach+TPE+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0240` | HAN->TPE | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDSEFOcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+HAN+nach+TPE+am+2027-04-28+oneway&curr=EUR&hl=de) |

## Zwischenflug KUL->HAN (8)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0225` | KUL->HAN | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDS1VMcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+HAN+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0226` | KUL->HAN | 2027-03-29 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjlqBRIDS1VMcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+HAN+am+2027-03-29+oneway&curr=EUR&hl=de) |
| `g0227` | KUL->HAN | 2027-04-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDNqBRIDS1VMcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+HAN+am+2027-04-03+oneway&curr=EUR&hl=de) |
| `g0228` | KUL->HAN | 2027-04-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDhqBRIDS1VMcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+HAN+am+2027-04-08+oneway&curr=EUR&hl=de) |
| `g0229` | KUL->HAN | 2027-04-13 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMTNqBRIDS1VMcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+HAN+am+2027-04-13+oneway&curr=EUR&hl=de) |
| `g0230` | KUL->HAN | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDS1VMcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+HAN+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0231` | KUL->HAN | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDS1VMcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+HAN+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0232` | KUL->HAN | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDS1VMcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+HAN+am+2027-04-28+oneway&curr=EUR&hl=de) |

## Zwischenflug KUL->LOP (8)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0193` | KUL->LOP | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDS1VMcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+LOP+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0194` | KUL->LOP | 2027-03-29 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjlqBRIDS1VMcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+LOP+am+2027-03-29+oneway&curr=EUR&hl=de) |
| `g0195` | KUL->LOP | 2027-04-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDNqBRIDS1VMcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+LOP+am+2027-04-03+oneway&curr=EUR&hl=de) |
| `g0196` | KUL->LOP | 2027-04-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDhqBRIDS1VMcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+LOP+am+2027-04-08+oneway&curr=EUR&hl=de) |
| `g0197` | KUL->LOP | 2027-04-13 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMTNqBRIDS1VMcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+LOP+am+2027-04-13+oneway&curr=EUR&hl=de) |
| `g0198` | KUL->LOP | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDS1VMcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+LOP+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0199` | KUL->LOP | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDS1VMcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+LOP+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0200` | KUL->LOP | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDS1VMcgUSA0xPUEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+LOP+am+2027-04-28+oneway&curr=EUR&hl=de) |

## Zwischenflug KUL->TPE (8)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0257` | KUL->TPE | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDS1VMcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+TPE+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0258` | KUL->TPE | 2027-03-29 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjlqBRIDS1VMcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+TPE+am+2027-03-29+oneway&curr=EUR&hl=de) |
| `g0259` | KUL->TPE | 2027-04-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDNqBRIDS1VMcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+TPE+am+2027-04-03+oneway&curr=EUR&hl=de) |
| `g0260` | KUL->TPE | 2027-04-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDhqBRIDS1VMcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+TPE+am+2027-04-08+oneway&curr=EUR&hl=de) |
| `g0261` | KUL->TPE | 2027-04-13 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMTNqBRIDS1VMcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+TPE+am+2027-04-13+oneway&curr=EUR&hl=de) |
| `g0262` | KUL->TPE | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDS1VMcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+TPE+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0263` | KUL->TPE | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDS1VMcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+TPE+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0264` | KUL->TPE | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDS1VMcgUSA1RQRUABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+KUL+nach+TPE+am+2027-04-28+oneway&curr=EUR&hl=de) |

## Zwischenflug LOP->HAN (8)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0209` | LOP->HAN | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDTE9QcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+HAN+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0210` | LOP->HAN | 2027-03-29 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjlqBRIDTE9QcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+HAN+am+2027-03-29+oneway&curr=EUR&hl=de) |
| `g0211` | LOP->HAN | 2027-04-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDNqBRIDTE9QcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+HAN+am+2027-04-03+oneway&curr=EUR&hl=de) |
| `g0212` | LOP->HAN | 2027-04-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDhqBRIDTE9QcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+HAN+am+2027-04-08+oneway&curr=EUR&hl=de) |
| `g0213` | LOP->HAN | 2027-04-13 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMTNqBRIDTE9QcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+HAN+am+2027-04-13+oneway&curr=EUR&hl=de) |
| `g0214` | LOP->HAN | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDTE9QcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+HAN+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0215` | LOP->HAN | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDTE9QcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+HAN+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0216` | LOP->HAN | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDTE9QcgUSA0hBTkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+HAN+am+2027-04-28+oneway&curr=EUR&hl=de) |

## Zwischenflug LOP->KUL (8)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0265` | LOP->KUL | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDTE9QcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+KUL+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0266` | LOP->KUL | 2027-03-29 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjlqBRIDTE9QcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+KUL+am+2027-03-29+oneway&curr=EUR&hl=de) |
| `g0267` | LOP->KUL | 2027-04-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDNqBRIDTE9QcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+KUL+am+2027-04-03+oneway&curr=EUR&hl=de) |
| `g0268` | LOP->KUL | 2027-04-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDhqBRIDTE9QcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+KUL+am+2027-04-08+oneway&curr=EUR&hl=de) |
| `g0269` | LOP->KUL | 2027-04-13 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMTNqBRIDTE9QcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+KUL+am+2027-04-13+oneway&curr=EUR&hl=de) |
| `g0270` | LOP->KUL | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDTE9QcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+KUL+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0271` | LOP->KUL | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDTE9QcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+KUL+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0272` | LOP->KUL | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDTE9QcgUSA0tVTEABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+LOP+nach+KUL+am+2027-04-28+oneway&curr=EUR&hl=de) |

## Zwischenflug MCT->CMB (8)

| ID | Strecke | Datum | Typ | Link | Fallback |
|---|---|---|---|---|---|
| `g0249` | MCT->CMB | 2027-03-24 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjRqBRIDTUNUcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MCT+nach+CMB+am+2027-03-24+oneway&curr=EUR&hl=de) |
| `g0250` | MCT->CMB | 2027-03-29 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDMtMjlqBRIDTUNUcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MCT+nach+CMB+am+2027-03-29+oneway&curr=EUR&hl=de) |
| `g0251` | MCT->CMB | 2027-04-03 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDNqBRIDTUNUcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MCT+nach+CMB+am+2027-04-03+oneway&curr=EUR&hl=de) |
| `g0252` | MCT->CMB | 2027-04-08 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMDhqBRIDTUNUcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MCT+nach+CMB+am+2027-04-08+oneway&curr=EUR&hl=de) |
| `g0253` | MCT->CMB | 2027-04-13 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMTNqBRIDTUNUcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MCT+nach+CMB+am+2027-04-13+oneway&curr=EUR&hl=de) |
| `g0254` | MCT->CMB | 2027-04-18 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMThqBRIDTUNUcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MCT+nach+CMB+am+2027-04-18+oneway&curr=EUR&hl=de) |
| `g0255` | MCT->CMB | 2027-04-23 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjNqBRIDTUNUcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MCT+nach+CMB+am+2027-04-23+oneway&curr=EUR&hl=de) |
| `g0256` | MCT->CMB | 2027-04-28 | oneway | [Google Flights](https://www.google.com/travel/flights?tfs=GhoSCjIwMjctMDQtMjhqBRIDTUNUcgUSA0NNQkABQAFIAZgBAg&hl=de&gl=ES&curr=EUR) | [q=](https://www.google.com/travel/flights?q=Fluege+von+MCT+nach+CMB+am+2027-04-28+oneway&curr=EUR&hl=de) |
