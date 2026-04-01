import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Portfolio Scenarios Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────

PERIODI = ["1M", "3M", "6M", "1Y", "2Y", "3Y", "5Y"]

ETF_INFO = {
    "QQQ":  {"nome": "Invesco QQQ Trust", "prezzo": 584.31},
    "XLK":  {"nome": "Technology Select Sector SPDR", "prezzo": 134.91},
    "XLY":  {"nome": "Cons Disc Sel Sect SPDR", "prezzo": 109.80},
    "IEF":  {"nome": "iShares 7-10Y Treasury Bond", "prezzo": 95.04},
    "SMH":  {"nome": "VanEck Semiconductor ETF", "prezzo": 391.97},
    "TLT":  {"nome": "iShares 20Y Treasury Bond", "prezzo": 86.26},
    "SHY":  {"nome": "iShares 1-3Y Treasury Bond", "prezzo": 82.32},
    "XLU":  {"nome": "Utilities Select Sector SPDR", "prezzo": 46.11},
    "XLP":  {"nome": "Cons Staples Sel Sec SPDR", "prezzo": 81.46},
    "GLD":  {"nome": "SPDR Gold Trust", "prezzo": 437.82},
    "DBC":  {"nome": "Invesco DB Commodity Index", "prezzo": 28.68},
    "XLE":  {"nome": "Energy Select Sector SPDR", "prezzo": 58.97},
    "TIP":  {"nome": "iShares TIPS Bond ETF", "prezzo": 110.36},
    "XLI":  {"nome": "Industrial Select Sector SPDR", "prezzo": 164.43},
    "XLF":  {"nome": "Financial Sel Sec SPDR", "prezzo": 49.44},
    "IWM":  {"nome": "iShares Russell 2000 ETF", "prezzo": 249.56},
    "EEM":  {"nome": "iShares MSCI Emerging Markets", "prezzo": 57.23},
    "LQD":  {"nome": "iShares iBoxx Inv Grade Corp Bond", "prezzo": 108.66},
    "VTI":  {"nome": "Vanguard Total Stock Market", "prezzo": 323.24},
    "FXF":  {"nome": "Invesco CurrencyShares Swiss Franc", "prezzo": 111.10},
    "IXUS": {"nome": "iShares Core MSCI Total Intl Stock", "prezzo": 87.61},
    "BIL":  {"nome": "SPDR Bloomberg 1-3M T-Bill", "prezzo": 91.40},
    "XME":  {"nome": "SPDR S&P Metals & Mining", "prezzo": 109.90},
    "COPX": {"nome": "Global X Copper Miners ETF", "prezzo": 78.15},
    "IBIT": {"nome": "iShares Bitcoin Trust ETF", "prezzo": 38.64},
    "VDST": {"nome": "Vanguard US Treasury 0-1Y", "prezzo": 58.74},
    "SPY":  {"nome": "SPDR S&P 500 ETF Trust", "prezzo": None},
}

# Variazioni % per ETF: [1M, 3M, 6M, 1Y, 2Y, 3Y, 5Y]
ETF_VARS = {
    "QQQ":  [-3.91, -4.70, -4.78,  23.61,  31.32,  82.51,  76.50],
    "XLK":  [-3.32, -6.51, -6.60,  29.72,  29.19,  78.95,  95.13],
    "XLY":  [-4.87, -7.22, -7.19,  10.06,  20.32,  48.22,  26.73],
    "IEF":  [-2.14, -1.08, -1.08,  -0.38,   1.61,  -4.38, -15.92],
    "SMH":  [-3.55,  5.00,  5.55,  84.47,  71.96, 199.56, 204.87],
    "TLT":  [-3.74, -0.88, -0.86,  -5.72,  -6.80, -19.08, -37.00],
    "SHY":  [-0.59, -0.65, -0.65,  -0.19,   1.20,   0.29,  -4.51],
    "XLU":  [-2.66,  6.79,  6.59,  16.65,  41.31,  37.15,  42.58],
    "XLP":  [-8.17,  4.85,  4.83,  -0.40,   7.54,   8.47,  18.32],
    "GLD":  [-10.65, 9.93, 11.06,  52.25, 110.67, 137.25, 170.39],
    "DBC":  [11.12, 28.09, 28.07,  27.41,  24.26,  18.86,  72.36],
    "XLE":  [3.38,  29.18, 29.96,  25.47,  23.99,  36.22, 140.11],
    "TIP":  [-1.08,  0.46,  0.45,  -0.08,   3.48,   0.04, -11.85],
    "XLI":  [-8.09,  4.08,  4.18,  24.75,  31.55,  62.22,  64.43],
    "XLF":  [-3.63, -9.99,-10.22,  -0.62,  18.02,  53.49,  42.31],
    "IWM":  [-5.40,  0.31,  0.32,  25.09,  19.80,  39.83,  10.93],
    "EEM":  [-6.94,  1.76,  1.83,  30.54,  39.08,  44.74,   5.84],
    "LQD":  [-2.04, -1.36, -1.34,   0.00,   1.11,  -1.16, -16.40],
    "VTI":  [-4.68, -3.89, -3.96,  17.21,  24.47,  57.96,  52.67],
    "FXF":  [-1.96, -0.43, -0.43,  10.60,  12.91,  13.79,  14.49],
    "IXUS": [-5.25,  2.05,  2.10,  25.01,  29.41,  40.36,  21.71],
    "BIL":  [-0.02, -0.02, -0.03,  -0.02,  -0.08,  -0.11,   None],
    "XME":  [-9.96,  2.20,  2.43,  96.57,  80.67, 105.50, 169.69],
    "COPX": [-16.51, 6.97,  8.21,  98.65,  82.89,  98.75, 108.68],
    "IBIT": [-1.43,-24.15,-17.62, -20.00,  -2.79,   1.44,   None],
    "VDST": [0.44,   0.98,  0.99,   4.20,   9.41,  15.00,   None],
    "SPY":  [-4.54, -4.09, -2.09,  29.91,  26.49,  58.29,  56.94],
}

# Portafogli con ETF e variazioni medie
PORTAFOGLI = {
    "🌟 Goldilocks Economy": {
        "color": "#2ecc71",
        "etf": ["QQQ", "XLK", "XLY", "IEF", "SMH"],
        "media": [-3.56, -2.90, -2.82, 29.50, 30.88, 80.97, 77.46],
        "desc": "Crescita solida, inflazione contenuta. Tech, consumi discrezionali, semiconduttori."
    },
    "🔴 Recession": {
        "color": "#e74c3c",
        "etf": ["TLT", "SHY", "XLU", "XLP", "GLD"],
        "media": [-5.16, 4.01, 4.19, 12.52, 30.79, 32.82, 37.96],
        "desc": "Contrazione economica. Rifugi sicuri: Treasury, utility, oro, beni di prima necessità."
    },
    "🌡️ Stagflation": {
        "color": "#e67e22",
        "etf": ["GLD", "DBC", "XLE", "TIP", "XLU"],
        "media": [0.02, 14.89, 15.22, 24.34, 40.74, 45.90, 82.72],
        "desc": "Alta inflazione + bassa crescita. Commodity, energia, oro, TIPS."
    },
    "🔄 Reflation": {
        "color": "#3498db",
        "etf": ["XLI", "XLF", "IWM", "EEM", "DBC"],
        "media": [-2.59, 4.85, 4.83, 21.43, 26.54, 43.83, 39.17],
        "desc": "Ripresa con inflazione in risalita. Industriali, finanziari, small cap, emergenti."
    },
    "🕊️ Disinflation/Soft Landing": {
        "color": "#9b59b6",
        "etf": ["TLT", "LQD", "QQQ", "VTI", "GLD"],
        "media": [-5.00, -0.18, 0.02, 17.47, 32.15, 51.50, 49.24],
        "desc": "Inflazione in calo con atterraggio morbido. Bond + equity."
    },
    "🌍 Dollar Weakness / Global Rebalancing": {
        "color": "#1abc9c",
        "etf": ["EEM", "FXF", "GLD", "IXUS", "DBC"],
        "media": [-2.74, 8.28, 8.52, 29.16, 43.27, 51.00, 56.96],
        "desc": "Dollaro debole, riequilibrio globale. Emergenti, Svizzera, oro, internazionali."
    },
    "❄️ Deflation": {
        "color": "#34495e",
        "etf": ["TLT", "BIL", "SHY", "XLP", "XLU"],
        "media": [-3.03, 2.02, 1.98, 2.06, 8.65, 5.35, 3.86],
        "desc": "Prezzi in calo, bassa crescita. Massima sicurezza: T-Bill, Treasury, defensive equity."
    },
    "₿ Debasement Aggressivo (con BTC)": {
        "color": "#f39c12",
        "etf": ["GLD", "XME", "COPX", "EEM", "IBIT"],
        "media": [-9.10, -0.66, 1.18, 51.60, 62.10, 96.56, 113.65],
        "desc": "Svalutazione valutaria aggressiva. Oro, metalli, rame, BTC."
    },
    "💰 Debasement senza BTC": {
        "color": "#d35400",
        "etf": ["GLD", "XME", "COPX", "EEM", "VDST"],
        "media": [-8.72, 4.37, 4.90, 56.44, 64.54, 80.25, None],
        "desc": "Svalutazione senza esposizione crypto. Oro, metalli, rame, Treasury breve."
    },
}

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Chart_increase.svg/120px-Chart_increase.svg.png", width=60)
st.sidebar.title("📊 Portfolio Scenarios")
st.sidebar.markdown("---")

sezione = st.sidebar.radio(
    "Sezione",
    ["🏠 Overview", "📈 Portafogli nel tempo", "🔍 Singole componenti", "⚖️ Confronto strategie", "📋 Tabella dati"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Filtra portafogli**")
portafogli_sel = st.sidebar.multiselect(
    "Seleziona scenari",
    list(PORTAFOGLI.keys()),
    default=list(PORTAFOGLI.keys())
)

periodo_sel = st.sidebar.select_slider(
    "Orizzonte temporale",
    options=PERIODI,
    value="1Y"
)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def get_portafoglio_df():
    rows = []
    for nome, info in PORTAFOGLI.items():
        row = {"Portafoglio": nome, "Colore": info["color"]}
        for i, p in enumerate(PERIODI):
            row[p] = info["media"][i]
        rows.append(row)
    return pd.DataFrame(rows)

def get_etf_df():
    rows = []
    for ticker, vals in ETF_VARS.items():
        row = {"Ticker": ticker, "Nome": ETF_INFO.get(ticker, {}).get("nome", ticker)}
        for i, p in enumerate(PERIODI):
            row[p] = vals[i] if i < len(vals) else None
        rows.append(row)
    return pd.DataFrame(rows)

def colore_val(val):
    if val is None: return "gray"
    return "#2ecc71" if val >= 0 else "#e74c3c"
