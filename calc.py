def berechne_unterjaehrige_annuitaetentilgung(
    finanzierungsbetrag: int,
    effektivzins_pct: float,
    laufzeit: int,
    ratenzahlungstyp: str,
    m: int = 12,
) -> tuple[float]:
    # https://de.wikipedia.org/wiki/Annuit%C3%A4tendarlehen
    i = effektivzins_pct / 100
    R = finanzierungsbetrag * ((1 + i) ** laufzeit * i) / ((1 + i) ** laufzeit - 1)
    match ratenzahlungstyp:
        case "nachschüssig":
            nenner = m + i / 2 * (m - 1)
        case "vorschüssig":
            nenner = m + i / 2 * (m + 1)
    r = R / nenner  # monatliche Rate
    return r, r * m * laufzeit


def berechne_mietkosten(
    startmietzins: int,
    mietdauer: int,
    preissteigerung_pct: float,
    steigerungsfrequenz: int,
    m: int = 12,
) -> float:
    n_steigerungen = mietdauer / steigerungsfrequenz - 1
    basiskosten = startmietzins * mietdauer * m
    q = 1 + preissteigerung_pct / 100
    mietkosten = basiskosten * q**n_steigerungen
    return mietkosten
