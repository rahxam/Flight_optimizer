"""Startszenarien: wie du ueberhaupt in die Reise hineinkommst.

Du bist bis 06.03.2027 im Montafon. Daraus ergeben sich vier Wege, und sie
unterscheiden sich nicht nur im Preis, sondern vor allem darin, WANN der
Asien-Teil beginnt - und das entscheidet ueber die Saison vor Ort.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, replace

from .optimizer import TripConfig


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

    def config(self, base: TripConfig) -> TripConfig:
        # latest_end so setzen, dass max_days ab latest_start noch passen.
        return replace(
            base,
            outbound_context=self.outbound_context,
            allowed_origins=self.allowed_origins,
            earliest_start=self.earliest_start,
            latest_end=min(
                base.latest_end, self.latest_start + dt.timedelta(days=base.max_days - 1)
            ),
            pre_trip_cost_eur=self.pre_trip_cost_eur,
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
    ),
    "hamburg_buero": Scenario(
        key="hamburg_buero",
        name="D - Ueber Hamburg (Buerotage, Firmenflug)",
        description=(
            "Vom Montafon mit der Bahn nach Hamburg, ein paar Bueotage, dann "
            "den von der Firma bezahlten Flug HAM->TFS nehmen und ab MAD/BCN "
            "starten. Der Firmenflug deckt nur dich ab, nicht deine Freundin."
        ),
        outbound_context="tenerife",
        allowed_origins=("MAD", "BCN"),
        earliest_start=dt.date(2027, 3, 13),
        latest_start=dt.date(2027, 3, 24),
        pre_trip_cost_eur=400.0,
        pre_trip_note=(
            "Bahn Montafon -> Hamburg ca. 90 EUR pro Person (180 EUR), "
            "HAM -> TFS: dein Flug zahlt die Firma, ihrer ca. 220 EUR."
        ),
    ),
}
