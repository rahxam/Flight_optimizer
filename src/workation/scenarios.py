"""Startszenarien: wie du ueberhaupt in die Reise hineinkommst - und wie du
wieder herauskommst.

Zwei harte Randbedingungen:
  * Du bist bis 06.03.2027 im Montafon (Skifahren mit den Eltern).
  * Der Geburtstag deiner Schwiegermutter ist am 06.05.2027, gefeiert wird
    voraussichtlich am Samstag 08.05. in Ostritz. Deine Freundin muss dort sein.

Der zweite Punkt ist der teurere. Endet die Reise auf Teneriffa, muss ihr fuer
die Feier noch einmal nach Deutschland und zurueck - vier Fluege, rund 880 EUR.
Endet sie stattdessen in Deutschland, entfaellt das komplett, und der
Lombok-Block rutscht zusaetzlich in die beste Zeit des Fensters. Damit der
Vergleich ehrlich ist, tragen alle Szenarien, die auf Teneriffa enden, diese
880 EUR als Nachlaufkosten.
"""


from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, replace

from .optimizer import TripConfig

# Fluege Teneriffa -> Deutschland -> Teneriffa fuer zwei Personen, wenn die
# Reise auf Teneriffa endet und die Feier in Ostritz separat angereist werden muss.
PARTY_TRIP_EUR = 880.0
PARTY_TRIP_NOTE = (
    "Zusaetzlich: Fuer die Feier am 08.05. in Ostritz noch einmal TFS -> "
    "Deutschland -> TFS, ca. 880 EUR fuer zwei Personen. Diese Variante endet "
    "auf Teneriffa, also faellt das an."
)


@dataclass(frozen=True)
class Scenario:
    key: str
    name: str
    description: str
    outbound_context: str
    allowed_origins: tuple[str, ...]
    earliest_start: dt.date
    latest_start: dt.date
    pre_trip_cost_eur: float
    pre_trip_note: str
    return_hubs: tuple[str, ...] = ("MAD", "BCN")
    return_feeder_mode: str = "home"
    post_trip_cost_eur: float = 0.0
    post_trip_note: str = ""
    hard_latest_end: dt.date | None = None

    def config(self, base: TripConfig) -> TripConfig:
        latest_end = self.hard_latest_end or min(
            base.latest_end, self.latest_start + dt.timedelta(days=base.max_days - 1)
        )
        return replace(
            base,
            outbound_context=self.outbound_context,
            allowed_origins=self.allowed_origins,
            allowed_return_hubs=self.return_hubs,
            return_feeder_mode=self.return_feeder_mode,
            earliest_start=self.earliest_start,
            latest_end=latest_end,
            pre_trip_cost_eur=self.pre_trip_cost_eur,
            post_trip_cost_eur=self.post_trip_cost_eur,
            scenario_label=self.name,
            start_date_step=1,
        )


SCENARIOS: dict[str, Scenario] = {
    "montafon_direkt": Scenario(
        key="montafon_direkt",
        name="A - Direkt ab Montafon",
        description=(
            "Am 05.03. spaet, 06.03. nachmittags oder 07.03. mit der Bahn nach "
            "Zuerich oder Muenchen und direkt nach Asien. Kein Umweg, keine "
            "Zwischenmiete - aber der Asien-Teil startet so frueh, dass Lombok "
            "noch in der Regenzeit liegt."
        ),
        outbound_context="montafon",
        allowed_origins=("ZRH", "MUC", "VIE", "STR"),
        earliest_start=dt.date(2027, 3, 5),
        latest_start=dt.date(2027, 3, 7),
        pre_trip_cost_eur=0.0,
        pre_trip_note="Bahn ab Bludenz ist in den Anreisekosten des Hubs enthalten.",
        post_trip_cost_eur=PARTY_TRIP_EUR,
        post_trip_note=PARTY_TRIP_NOTE,
    ),
    "cottbus_bruecke": Scenario(
        key="cottbus_bruecke",
        name="B - Cottbus-Bruecke (1-2 Wochen bei den Eltern)",
        description=(
            "Am 06.03. mit den Eltern nach Cottbus, dort 1-2 Wochen normal "
            "arbeiten (Unterkunft frei), dann ab BER nach Asien. Kostet keinen "
            "zusaetzlichen Flug und verschiebt den Asien-Teil genau in das "
            "Fenster, in dem Lomboks Trockenzeit beginnt."
        ),
        outbound_context="cottbus",
        allowed_origins=("BER", "MUC", "MAD"),
        earliest_start=dt.date(2027, 3, 13),
        latest_start=dt.date(2027, 3, 20),
        pre_trip_cost_eur=0.0,
        pre_trip_note="Mitfahrt mit den Eltern, Unterkunft bei der Familie - keine Zusatzkosten.",
        post_trip_cost_eur=PARTY_TRIP_EUR,
        post_trip_note=PARTY_TRIP_NOTE,
    ),
    "cottbus_lang": Scenario(
        key="cottbus_lang",
        name="B2 - Cottbus lang (3 Wochen), Abflug nach Ostern",
        description=(
            "Wie B, aber drei Wochen Cottbus: der Abflug liegt dann nach "
            "Ostern (28.03.), also hinter der teuersten Flugwoche, und der "
            "Lombok-Block faellt in die beste Saison des ganzen Fensters. "
            "Preis: Sri Lanka rutscht in das Sinhala New Year hinein."
        ),
        outbound_context="cottbus",
        allowed_origins=("BER", "MUC", "MAD"),
        earliest_start=dt.date(2027, 3, 29),
        latest_start=dt.date(2027, 3, 31),
        pre_trip_cost_eur=0.0,
        pre_trip_note="Wie B - keine Zusatzkosten, nur drei statt zwei Wochen Cottbus.",
        post_trip_cost_eur=PARTY_TRIP_EUR,
        post_trip_note=PARTY_TRIP_NOTE,
    ),
    "heim_tfs": Scenario(
        key="heim_tfs",
        name="C - Erst heim nach Teneriffa",
        description=(
            "Am 06./07.03. zurueck nach Teneriffa, dort packen und arbeiten, "
            "dann regulaer ab MAD/BCN mit Residentenrabatt. Der sauberste Weg, "
            "aber zwei zusaetzliche Fluege ab Zuerich/Muenchen."
        ),
        outbound_context="tenerife",
        allowed_origins=("MAD", "BCN"),
        earliest_start=dt.date(2027, 3, 13),
        latest_start=dt.date(2027, 3, 24),
        pre_trip_cost_eur=460.0,
        pre_trip_note="ZRH/MUC -> TFS fuer 2 Personen, ca. 230 EUR pro Person, kein Residentenrabatt.",
        post_trip_cost_eur=PARTY_TRIP_EUR,
        post_trip_note=PARTY_TRIP_NOTE,
    ),
    "hamburg_direkt": Scenario(
        key="hamburg_direkt",
        name="D - Bueroteage in Hamburg, dann ab HAM",
        description=(
            "Vom Montafon mit der Bahn nach Hamburg (deine Firma zahlt dein "
            "Ticket, ihres ca. 30 EUR mit frueh gebuchtem Flixtrain), ein paar "
            "Bueotage, dann direkt ab HAM nach Asien. Kein Umweg ueber "
            "Teneriffa - deutlich billiger als die alte Hamburg-Variante."
        ),
        outbound_context="hamburg",
        allowed_origins=("HAM",),
        earliest_start=dt.date(2027, 3, 13),
        latest_start=dt.date(2027, 3, 24),
        pre_trip_cost_eur=30.0,
        pre_trip_note=(
            "Bahn Montafon -> Hamburg: dein Ticket zahlt die Firma, ihres ca. "
            "30 EUR (Flixtrain, frueh gebucht)."
        ),
        post_trip_cost_eur=PARTY_TRIP_EUR,
        post_trip_note=PARTY_TRIP_NOTE,
    ),
    "ostritz_finale_ber": Scenario(
        key="ostritz_finale_ber",
        name="E - Ostritz-Finale (Rueckkehr nach Deutschland, ab/bis BER)",
        description=(
            "Der Geburtstag deiner Schwiegermutter am 06.05. (Feier wohl am "
            "Samstag 08.05.) ist ein harter Endtermin in Ostritz. Also die Reise "
            "so legen, dass sie in Deutschland endet statt auf Teneriffa: "
            "Rueckflug bis 06.05. nach BER, Feier, dann gemeinsam heim. Das "
            "schiebt den Lombok-Block in die absolute Bestzeit (Anfang Mai) und "
            "spart eine komplette Europa-Teneriffa-Runde."
        ),
        outbound_context="cottbus",
        allowed_origins=("BER", "MUC"),
        earliest_start=dt.date(2027, 3, 20),
        latest_start=dt.date(2027, 4, 8),
        pre_trip_cost_eur=0.0,
        pre_trip_note="Mitfahrt mit den Eltern nach Cottbus, Unterkunft bei der Familie.",
        return_hubs=("BER",),
        return_feeder_mode="later",
        post_trip_cost_eur=440.0,
        post_trip_note=(
            "Nach der Feier BER -> TFS fuer zwei Personen, ca. 220 EUR pro "
            "Person (kein Residentenrabatt ab Deutschland)."
        ),
        hard_latest_end=dt.date(2027, 5, 6),
    ),
    "ostritz_finale_ham": Scenario(
        key="ostritz_finale_ham",
        name="E2 - Ostritz-Finale mit Rueckkehr ueber Hamburg (Firmenflug)",
        description=(
            "Wie E, aber der Rueckflug geht nach HAM: Bueotage, dann den von der "
            "Firma bezahlten Flug HAM->TFS nehmen. Nur dein Ticket ist frei, "
            "ihres kostet. Der Umweg Hamburg -> Ostritz -> Teneriffa ist "
            "allerdings laestig, wenn die Feier dazwischen liegt."
        ),
        outbound_context="cottbus",
        allowed_origins=("BER", "MUC"),
        earliest_start=dt.date(2027, 3, 20),
        latest_start=dt.date(2027, 4, 8),
        pre_trip_cost_eur=0.0,
        pre_trip_note="Mitfahrt mit den Eltern nach Cottbus, Unterkunft bei der Familie.",
        return_hubs=("HAM",),
        return_feeder_mode="later",
        post_trip_cost_eur=250.0,
        post_trip_note=(
            "HAM -> TFS: dein Flug zahlt die Firma, ihrer ca. 220 EUR, plus "
            "ca. 30 EUR Bahn fuer den Umweg nach Ostritz."
        ),
        hard_latest_end=dt.date(2027, 5, 6),
    ),
}
