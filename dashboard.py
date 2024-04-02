import streamlit as st

from calc import berechne_unterjaehrige_annuitaetentilgung, berechne_mietkosten


st.set_page_config(
    page_title="Kreditrechner",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.header("Rechner für monatliches Tilgungsdarlehen")
kosten = int(
    st.number_input(
        "Kosten für Eigenheim in €",
        value=300000,
        min_value=100000,
        max_value=1000000,
        step=10000,
    )
)
eigenmittel = int(
    st.number_input(
        "Eigenmittel in €",
        value=100000,
        min_value=int(kosten * 0.2),
        max_value=kosten,
        step=10000,
    )
)
zinssatz = st.slider(
    "effektiver Zinssatz in %", value=5.0, min_value=1.0, max_value=20.0, step=0.1
)
# Effektivzins = Nominalzins + Spesen + Bereitstellungsprovisionen + Kontoführungsentgelte + Bearbeitungsgebühren + Versicherungskosten
# Achtung: Der Effektivzins erhöht sich zudem noch durch monatliche Ratenzahlung im Vergleich zur jährlichen Rate des Nominalzinses.
laufzeit = st.slider("Laufzeit in Jahren", value=20, min_value=5, max_value=35, step=5)
ratenzahlung = st.radio(
    "Ratenzahlung", options=["nachschüssig", "vorschüssig"], index=0, horizontal=True
)
finanzierungsbetrag = kosten - eigenmittel
monatliche_rate, finanzierungskosten = berechne_unterjaehrige_annuitaetentilgung(
    finanzierungsbetrag, zinssatz, laufzeit, ratenzahlung
)
kreditkosten = finanzierungskosten - finanzierungsbetrag
st.markdown(
    f":blue[Eigenmittelanteil: **{round(eigenmittel / kosten * 100)}%**]".replace(
        ",", "."
    )
)
st.markdown(
    f":blue[Gesamtkosten: **{eigenmittel + finanzierungskosten:,}€** (davon **{round(eigenmittel / kosten * 100)}%** Eigenmittel)]".replace(
        ",", "."
    )
)
st.markdown(
    f":blue[Finanzierungsbetrag: **{finanzierungsbetrag:,}€**]".replace(",", ".")
)
st.markdown(
    f":blue[Finanzierungskosten: **{finanzierungskosten:,}€** (**{monatliche_rate:,}€** monatliche Rate)]".replace(
        ",", "."
    )
)
st.markdown(
    f":blue[Kreditkosten: **{kreditkosten:,}€** (**{round(kreditkosten/finanzierungskosten*100)}%** der Finanzierungskosten)]".replace(
        ",", "."
    )
)


st.header("Rechner für Mietkosten")
startmietzins = st.number_input(
    "Startmietzins in €", value=500, min_value=400, max_value=2000, step=50
)
mietdauer = st.slider(
    "Mietdauer in Jahren", value=35, min_value=5, max_value=65, step=5
)
preissteigerung = st.slider(
    "Preissteigerung in %", value=6.0, min_value=1.0, max_value=12.0, step=0.1
)
steigerungsfrequenz = st.slider(
    "Steigerungsfrequenz in Jahren", value=3, min_value=1, max_value=10, step=1
)
mietkosten = berechne_mietkosten(
    startmietzins, mietdauer, preissteigerung, steigerungsfrequenz
)
st.markdown(f":blue[Mietkosten: **{mietkosten:,}€**]".replace(",", "."))
