import streamlit as st

from calc import berechne_unterjaehrige_annuitaetentilgung, berechne_mietkosten


st.set_page_config(
    page_title="Kreditrechner",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.header("Rechner für monatliches Tilgungsdarlehen")
st.subheader("Eingaben")
kosten = int(
    st.number_input(
        "Vorhabenskosten [€]",
        value=300000,
        min_value=100000,
        max_value=1000000,
        step=10000,
    )
)
eigenmittel = int(
    st.number_input(
        "Eigenmittel [€]",
        value=100000,
        min_value=int(kosten * 0.2),
        max_value=kosten,
        step=10000,
    )
)
zinssatz = st.slider(
    "effektiver Zinssatz [%]", value=5.0, min_value=1.0, max_value=20.0, step=0.1
)
# Effektivzins = Nominalzins + Spesen + Bereitstellungsprovisionen + Kontoführungsentgelte + Bearbeitungsgebühren + Versicherungskosten
# Achtung: Der Effektivzins erhöht sich zudem noch durch monatliche Ratenzahlung im Vergleich zur jährlichen Rate des Nominalzinses.
laufzeit = st.slider("Laufzeit in Jahren", value=20, min_value=5, max_value=35, step=5)
ratenzahlung = st.radio(
    "Ratenzahlung", options=["nachschüssig", "vorschüssig"], index=0, horizontal=True
)
st.subheader("Berechnung")
anteil_eigenmittel = round(eigenmittel / kosten * 100)
finanzierungsbetrag = kosten - eigenmittel
monatliche_rate, finanzierungskosten = berechne_unterjaehrige_annuitaetentilgung(
    finanzierungsbetrag, zinssatz, laufzeit, ratenzahlung
)
kreditkosten = finanzierungskosten - finanzierungsbetrag
st.markdown(f"Eigenmittelanteil: {anteil_eigenmittel}%")
st.markdown(f"monatliche Rate: {round(monatliche_rate)}€")
st.markdown(f"Finanzierungsbetrag: {round(finanzierungsbetrag/1000)} Tausend €")
st.markdown(f"Finanzierungskosten: {round(finanzierungskosten/1000)} Tausend €")
st.markdown(f"Kreditkosten: {round(kreditkosten/1000)} Tausend €")
st.markdown(f"Kreditkostenanteil: {round(kreditkosten/finanzierungskosten*100)}%")


st.header("Rechner für Mietkosten")
st.subheader("Eingaben")
startmietzins = st.number_input(
    "Startmietzins [€]", value=500, min_value=400, max_value=2000, step=50
)
mietdauer = st.slider(
    "Mietdauer in Jahren", value=45, min_value=5, max_value=65, step=5
)
preissteigerung = st.slider(
    "Preissteigerung [%]", value=2.0, min_value=1.0, max_value=10.0, step=0.1
)
steigerungsfrequenz = st.slider(
    "Steigerungsfrequenz in Jahren", value=3, min_value=1, max_value=10, step=1
)
st.subheader("Berechnung")
mietkosten = berechne_mietkosten(
    startmietzins, mietdauer, preissteigerung, steigerungsfrequenz
)
st.markdown(f"Mietkosten für {mietdauer} Jahre: {round(mietkosten/1000)} Tausend €")
