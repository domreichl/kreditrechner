import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="Kreditrechner",
    layout="centered",
    initial_sidebar_state="collapsed",
)

'''
TODO: miteinrechnen: laufende Mietkosten & monatliches Sparen pro Jahr -> Veränderung



'''

st.title("Rechner für monatliches Tilgungsdarlehen")

kosten = int(st.number_input("Vorhabenskosten [€]", value=300000, min_value=100000, max_value=1000000, step=10000))
eigenmittel = int(st.number_input("Eigenmittel [€]", value=100000, min_value=0, max_value=kosten, step=10000))
zinssatz = st.slider("effektiver Zinssatz [%]", value=5.0, min_value=0.0, max_value=20.0, step=0.1)
# Effektivzins = Nominalzins + Spesen + Bereitstellungsprovisionen + Kontoführungsentgelte + Bearbeitungsgebühren + Versicherungskosten
# Achtung: Der Effektivzins erhöht sich zudem noch durch monatliche Ratenzahlung im Vergleich zur jährlichen Rate des Nominalzinses.
laufzeit = st.slider("Laufzeit in Jahren", value=20, min_value=5, max_value=35, step=5)

ratenzahlung = st.radio("Ratenzahlung", options=["vorschüssig", "nachschüssig"], index=0, horizontal=True)

anteil_eigenmittel = round(eigenmittel / kosten * 100)
finanzierungsbetrag = kosten - eigenmittel

if anteil_eigenmittel < 20:
    st.markdown(f"Achtung: Eigenmittelanteil muss über 20% liegen!")
else:
    st.markdown(f"Eigenmittelanteil: {anteil_eigenmittel}%")
st.markdown(f"Finanzierungsbetrag: {finanzierungsbetrag}€")

# TILGUNGSFORMEL lt. https://de.wikipedia.org/wiki/Annuit%C3%A4tendarlehen
m = 12
R = finanzierungsbetrag * ((1+zinssatz/100)**laufzeit * zinssatz/100) / ((1+zinssatz/100)**laufzeit - 1)
match ratenzahlung:
    case "vorschüssig":
        nenner = (m + zinssatz/2 * (m+1))
    case "nachschüssig":
        nenner = (m + zinssatz/2 * (m-1))
r = R / nenner
st.markdown(f"monatliche Tilgung: {round(r)}€")
gesamtkosten = r*m*laufzeit
st.markdown(f"Gesamtkosten: {round(gesamtkosten/1000)} Tausend €")
kreditkosten = gesamtkosten-kosten
st.markdown(f"Kreditkosten: {round(kreditkosten/1000)} Tausend €")
st.markdown(f"Kreditkostenanteil: {round(kreditkosten/gesamtkosten*100)}%")


"""
# DATA
data_dir = Path(__file__).parent / "data"
predictions = pd.read_csv(data_dir / "test_predictions.csv")
performance = pd.read_csv(data_dir / "test_metrics.csv")
trades = pd.read_csv(data_dir / "trades.csv").drop(columns=["ID"])
ts = json.load(open(data_dir / "trades_statistics.json", "r"))
backtest = pd.read_csv(data_dir / "backtest.csv")


# PREDICTIONS
st.title("Stock Price Predictions")
st.markdown(f"Last updated: {predictions['Date'].max()}")
model_selected = st.radio(
    "Choose prediction model",
    options=list(performance["Model"].unique()),
    horizontal=True,
)
ts_selected = st.selectbox("Select ISIN", list(predictions["ISIN"].unique()))
preds = predictions[predictions["Model"] == model_selected]
pr = preds[preds["ISIN"] == ts_selected].reset_index(drop=True)
st.subheader(f"Closing Prices for {ts_selected}")
fig_prices = go.Figure()
fig_prices.add_trace(
    go.Scatter(
        x=pr["Date"],
        y=pr["Price"],
        name="actual",
        line=dict(color="navy", width=5),
    )
)
fig_prices.add_trace(
    go.Scatter(
        x=pr["Date"],
        y=pr["PricePredicted"],
        name="predicted",
        line=dict(color="blueviolet", width=5),
    )
)
fig_prices.update_traces(marker={"size": 12})
fig_prices.update_layout(
    yaxis_title="Price [€]",
    xaxis=dict(title="Date", tickformat="%b %d"),
)
st.plotly_chart(fig_prices)


# MODELS
st.title("Model Performance")
st.subheader("Test Set")
metric_selected = st.radio(
    "Select metric",
    options=list(performance["Metric"].unique()),
    index=3,
    horizontal=True,
)
st.bar_chart(
    performance[performance["Metric"] == metric_selected],
    x="Model",
    y="Score",
    color="#b35300",
)
"""


# # TRADES
# st.title("Trading Statistics")
# counts = pd.DataFrame(
#     {
#         "trades": [f"{int(ts['N_TRADES'])} Trades"] * 2,
#         "count": [
#             f"{int(ts['N_TRADES_WIN'])} Wins",
#             f"{int(ts['N_TRADES_LOSS'])} Losses",
#         ],
#         "percentage": [ts["WIN_RATE"], 100 - ts["WIN_RATE"]],
#     }
# )
# st.plotly_chart(
#     px.sunburst(
#         counts,
#         path=["trades", "count"],
#         values="percentage",
#         color="count",
#         color_discrete_map={
#             "(?)": "#000000",
#             counts["count"][0]: "#00b400",
#             counts["count"][1]: "#d80000",
#         },
#     )
# )
# a1, a2, a3 = st.columns(3)
# a1.metric("Trades", f"{int(ts['N_TRADES'])}")
# a2.metric("Volume", f"{int(ts['TOTAL_VOLUME'])}€")
# a3.metric("Gross Profit", f"{ts['TOTAL_GROSS_PROFIT']}€")
# b1, b2, b3 = st.columns(3)
# b1.metric("Highest Win", f"{ts['MAX_WIN']}€")
# b2.metric("Highest Loss", f"{ts['MAX_LOSS']}€")
# b3.metric("Net Profit", f"{ts['TOTAL_NET_PROFIT']}€")
# c1, c2, c3 = st.columns(3)
# c1.metric("SQN", f"{ts['SQN']}")
# c2.metric("Fees", f"{ts['TOTAL_FEES']}€")
# c3.metric("Average Net Profit per Trade", f"{ts['AVG_PROFIT']}€")
# if st.button("Show details"):
#     st.dataframe(trades)


# # BACKTEST
# st.title("General Backtest")
# st.subheader(
#     f"Expected Profits for Weekly Long-Trading of Top ATX Stocks Initially Worth 1000€ with 1€ Transaction Cost as a Function of Model Precision"
# )
# precision = float(st.slider("Model Precision", 0.0, 1.0, 0.5, 0.05))
# bt = backtest[backtest["Model Precision"] == precision]
# st.plotly_chart(
#     px.bar(
#         bt,
#         x="Holding Weeks",
#         y="Expected Monthly Profit [€]",
#     )
# )
# st.plotly_chart(
#     px.bar(
#         bt,
#         x="Holding Weeks",
#         y="Expected Profit per Trade [€]",
#     )
# )
