import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="Portfolio Scenarios Dashboard", page_icon="📊", layout="wide")

ETF_TICKERS = ["QQQ", "XLK", "XLY", "IEF", "SMH", "TLT", "SHY", "XLU", "XLP", "GLD", "DBC", "XLE", "TIP", "XLI", "XLF", "IWM", "EEM", "LQD", "VTI", "FXF", "IXUS", "BIL", "XME", "COPX", "IBIT"]

PORTFOGLI = {
    "🌟 Goldilocks Economy": ["QQQ", "XLK", "XLY", "IEF", "SMH"],
    "🔴 Recession": ["TLT", "SHY", "XLU", "XLP", "GLD"],
    "🌡️ Stagflation": ["GLD", "DBC", "XLE", "TIP", "XLU"],
    "🔄 Reflation": ["XLI", "XLF", "IWM", "EEM", "DBC"],
    "🕊️ Disinflation": ["TLT", "LQD", "QQQ", "VTI", "GLD"],
    "🌍 Dollar Weakness": ["EEM", "FXF", "GLD", "IXUS", "DBC"],
    "❄️ Deflation": ["TLT", "BIL", "SHY", "XLP", "XLU"],
    "₿ Debasement + BTC": ["GLD", "XME", "COPX", "EEM", "IBIT"],
    "💰 Debasement no BTC": ["GLD", "XME", "COPX", "EEM", "SHY"]
}

@st.cache_data(ttl=3600)
def get_etf_data(ticker, period="1y"):
    try:
        data = yf.Ticker(ticker)
        hist = data.history(period=period)
        return hist
    except:
        return None

@st.cache_data(ttl=3600)
def calc_returns(ticker):
    periods = {"1M": 30, "3M": 90, "6M": 180, "1Y": 365, "2Y": 730, "3Y": 1095, "5Y": 1825}
    returns = {}
    for name, days in periods.items():
        try:
            hist = get_etf_data(ticker, period=f"{days}d")
            if hist is not None and len(hist) > 1:
                ret = ((hist['Close'].iloc[-1] / hist['Close'].iloc[0]) - 1) * 100
                returns[name] = round(ret, 2)
            else:
                returns[name] = None
        except:
            returns[name] = None
    return returns

st.sidebar.title("📊 Portfolio Scenarios")
st.sidebar.markdown("---")

sezione = st.sidebar.radio("Sezione", ["🏠 Overview", "📈 Portafogli", "🔍 Singoli ETF", "⚖️ Confronto"])

st.sidebar.markdown("---")
portafogli_sel = st.sidebar.multiselect("Filtra portafogli", list(PORTFOGLI.keys()), default=list(PORTFOGLI.keys())[:3])
periodo = st.sidebar.selectslider("Periodo", options=["1M", "3M", "6M", "1Y", "2Y", "3Y", "5Y"], value="1Y")

if sezione == "🏠 Overview":
    st.title("🏠 Portfolio Scenarios Dashboard")
    st.markdown("### Analisi portafogli per scenari macro")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Portafogli totali", len(PORTFOGLI))
    with col2:
        st.metric("ETF monitorati", len(ETF_TICKERS))
    with col3:
        st.metric("Periodo selezionato", periodo)
    
    st.markdown("---")
    for nome, tickers in list(PORTFOGLI.items())[:3]:
        with st.expander(f"{nome}"):
            st.write(f"**ETF**: {', '.join(tickers)}")
            
elif sezione == "📈 Portafogli":
    st.title("📈 Andamento Portafogli")
    
    for nome in portafogli_sel:
        st.subheader(nome)
        tickers = PORTFOGLI[nome]
        
        fig = go.Figure()
        for ticker in tickers:
            hist = get_etf_data(ticker, period="1y")
            if hist is not None:
                normalized = (hist['Close'] / hist['Close'].iloc[0] - 1) * 100
                fig.add_trace(go.Scatter(x=hist.index, y=normalized, name=ticker, mode='lines'))
        
        fig.update_layout(title=f"Performance {nome}", xaxis_title="Data", yaxis_title="Variazione %", hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
        
elif sezione == "🔍 Singoli ETF":
    st.title("🔍 Analisi Singoli ETF")
    
    ticker_sel = st.selectbox("Seleziona ETF", ETF_TICKERS)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        hist = get_etf_data(ticker_sel, period="1y")
        if hist is not None:
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'], name=ticker_sel))
            fig.update_layout(title=f"{ticker_sel} - Candlestick", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        returns = calc_returns(ticker_sel)
        st.markdown("#### Performance")
        for period, value in returns.items():
            if value is not None:
                color = "green" if value >= 0 else "red"
                st.markdown(f"**{period}**: :{color}[{value:+.2f}%]")
                
elif sezione == "⚖️ Confronto":
    st.title("⚖️ Confronto Strategie")
    
    if len(portafogli_sel) > 0:
        fig = go.Figure()
        
        for nome in portafogli_sel:
            tickers = PORTFOGLI[nome]
            portfolio_data = []
            
            for ticker in tickers:
                hist = get_etf_data(ticker, period="1y")
                if hist is not None:
                    portfolio_data.append(hist['Close'])
            
            if portfolio_data:
                avg_portfolio = pd.concat(portfolio_data, axis=1).mean(axis=1)
                normalized = (avg_portfolio / avg_portfolio.iloc[0] - 1) * 100
                fig.add_trace(go.Scatter(x=avg_portfolio.index, y=normalized, name=nome, mode='lines'))
        
        fig.update_layout(title="Confronto Performance Portafogli", xaxis_title="Data", yaxis_title="Variazione %", hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Seleziona almeno un portafoglio dalla sidebar")

st.sidebar.markdown("---")
st.sidebar.caption("📊 Dati da Yahoo Finance")
st.sidebar.caption(f"🔄 Aggiornato: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
