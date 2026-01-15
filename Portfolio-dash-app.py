import streamlit as st
import pandas as pd
import yfinance as yf
import quantstats as qs
import plotly.express as px
import tempfile, os


st.sidebar.success("Gramdev Tech💻")
st.logo("E:\data\personal\logo.png", size="large")
st.set_page_config(page_title="GramdevTech dashboard", layout="wide")


st.title("🪙Portfolio Dashboard")
st.sidebar.header("Portfolio Analysis🔎")
all_tickers= ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "BHARTIARTL.NS", "SBIN.NS", "INFY.NS", "LICI.NS", "ITC.NS", "HINDUNILVR.NS", "LT.NS", "BAJFINANCE.NS", 
                  "HCLTECH.NS", "MARUTI.NS", "SUNPHARMA.NS", "ADANIENT.NS", "TITAN.NS", "KOTAKBANK.NS", "TATAMOTORS.NS", "ONGC.NS", "AXISBANK.NS", "NTPC.NS", "ULTRACEMCO.NS",
                    "POWERGRID.NS", "COALINDIA.NS", "M&M.NS", "WIPRO.NS", "BAJAJFINSV.NS", "ADANIPORTS.NS", "JSWSTEEL.NS", "TATASTEEL.NS", "LTIM.NS", "SBILIFE.NS", "HDFCLIFE.NS", 
                    "GRASIM.NS", "TECHM.NS", "HINDALCO.NS", "DRREDDY.NS", "CIPLA.NS", "BRITANNIA.NS", "INDUSINDBK.NS", "TATACONSUM.NS", "APOLLOHOSP.NS", "EICHERMOT.NS", "DIVISLAB.NS", 
                    "NESTLEIND.NS", "BAJAJ-AUTO.NS", "HEROMOTOCO.NS", "BPCL.NS", "ASIANPAINT.NS", "ZOMATO.NS", "JIOFIN.NS", "HAL.NS", "DLF.NS", "BEL.NS", "VBL.NS", "TRENT.NS", "SIEMENS.NS",
                      "PIDILITIND.NS", "IOC.NS", "TATA_POWER.NS", "ADANIPOWER.NS", "CHOLAFIN.NS", "NAUKRI.NS", "ABB.NS", "GODREJCP.NS", "HAVELLS.NS", "BANKBARODA.NS", "GAIL.NS", "SHREECEM.NS", 
                      "TVSMOTOR.NS", "AMBUJACEM.NS", "DABUR.NS", "VEDL.NS", "INDIGO.NS", "PNB.NS", "ICICIGI.NS", "SBICARD.NS", "CANBK.NS", "BERGEPAINT.NS", "MARICO.NS", "IRCTC.NS", 
                      "BOSCHLTD.NS", "UBL.NS", "MCDOWELL-N.NS", "MOTHERSON.NS", "ICICIPRULI.NS", "PIIND.NS", "TORNTPHARM.NS", "MUTHOOTFIN.NS", "PAGEIND.NS", "LUPIN.NS", "JUBLFOOD.NS", 
                      "ALKEM.NS", "BANDHANBNK.NS", "BIOCON.NS", "ACC.NS", "AUBANK.NS", "PETRONET.NS"]
tickers = st.sidebar.multiselect(
        "Select NSE stocks:💰", options= all_tickers, default=["RELIANCE.NS", "TITAN.NS", "HDFCBANK.NS"] )
    
weights =[]
if tickers:
        st.sidebar.markdown("Assign portfolio weights")
        for t in tickers:
            w= st.sidebar.slider(f"Weight for {t}", min_value=0.0, max_value=1.0, value=round(1/len(tickers),2), step= 0.01)
            weights.append(w)
        total = sum(weights)
        if total != 1 and total != 0:
            weights = [w/total for w in weights]

start_date, end_date = st.sidebar.date_input(
        "Select date range:📆",
        value=(pd.to_datetime("2019-01-01"), pd.to_datetime("today")))
generate_btn = st.sidebar.button("Generate Analysis💡")

survey_url= "https://tinyurl.com/597mby9a"
survey_label = "Please take the survey"
st.sidebar.markdown(f"[{survey_label}]({survey_url})")
if generate_btn:
        if not tickers:
         st.error("Please select atleast one stock")
         st.stop()
        if len(tickers) != len(weights):
            st.error ("Tickers and weights mismatch")
            st.stop()
with st.spinner("🟢Fetching live data..."):
         price_data =yf.download(tickers, start=start_date, end=end_date)["Close"]
         returns= price_data.pct_change().dropna()
         
         portfolio_returns=(returns * weights).sum(axis=1)
         qs.extend_pandas()

         st.subheader("🔑 Key metrics")
         col1, col2, col3, col4= st.columns(4)
         col1.metric("Sharpe Ratio", f"{qs.stats.sharpe(portfolio_returns):.2f}")
         col2.metric("Max Drawdown", f"{qs.stats.max_drawdown(portfolio_returns)*100:.2f}%")
         col3.metric("CAGR", f"{qs.stats.cagr(portfolio_returns)*100:.2f}%")
         col4.metric("Volatility", f"{qs.stats.volatility(portfolio_returns)*100:.2f}%")

         st.subheader("⚖️Portfolio Weights")
         fig_pie =px.pie(
             names=tickers,
             values=weights,
             color_discrete_sequence=px.colors.qualitative.Pastel,
             title="Portfolio Allocation")
         st.plotly_chart(fig_pie, use_container_width=True)

         st.subheader("📚Monthly Returns")
         st.dataframe(portfolio_returns.monthly_returns().style.format("{:.2%}"))

         st.subheader("🧮Cumulative Rerturns")
         st.line_chart((1+ portfolio_returns).cumprod())

         st.subheader("📊End of Year (EOY) Returns")
         eoy_returns =portfolio_returns.resample("Y").apply(lambda x:(x+1).prod() -1)
         st.bar_chart(eoy_returns)

         with tempfile.TemporaryDirectory() as tmpd:
            report_path=os.path.join(tmpd, "portfolio_report.html")
            qs.reports.html(portfolio_returns, output=report_path, title="Portfolio Report")
            with open(report_path, "r", encoding="utf-8") as f:
                html_content=f.read()
            st.download_button(
                label="⬇️Download Full Report🔓",
                data= html_content,
                file_name="portfolio_report.html",
                mime="text/html")
            
st.success("Analysis complete ✅ ")
 
               