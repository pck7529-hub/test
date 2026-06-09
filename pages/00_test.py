import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="Global Top 10 Market Cap Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 글로벌 시가총액 Top 10 최근 1년 변화")
st.caption("Yahoo Finance 데이터 기반 · Plotly 시각화 · Streamlit Cloud 배포 가능")

# 2026년 6월 기준 CompaniesMarketCap 상위 10개 기업
TOP10 = {
    "NVIDIA": "NVDA",
    "Apple": "AAPL",
    "Alphabet": "GOOG",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "TSMC": "TSM",
    "Broadcom": "AVGO",
    "Saudi Aramco": "2222.SR",
    "Tesla": "TSLA",
    "Meta Platforms": "META",
}

@st.cache_data(ttl=60 * 60)
def get_price_data(tickers, period="1y"):
    data = yf.download(
        tickers=list(tickers.values()),
        period=period,
        interval="1d",
        auto_adjust=True,
        progress=False,
        group_by="ticker",
        threads=True
    )

    price_frames = []

    for company, ticker in tickers.items():
        try:
            if len(tickers) == 1:
                close = data["Close"]
            else:
                close = data[ticker]["Close"]

            temp = pd.DataFrame({
                "Date": close.index,
                "Company": company,
                "Ticker": ticker,
                "Close": close.values
            })

            price_frames.append(temp)

        except Exception as e:
            st.warning(f"{company}({ticker}) 가격 데이터를 가져오지 못했습니다: {e}")

    return pd.concat(price_frames, ignore_index=True)


@st.cache_data(ttl=60 * 60)
def get_shares_outstanding(tickers):
    rows = []

    for company, ticker in tickers.items():
        shares = None
        current_market_cap = None

        try:
            stock = yf.Ticker(ticker)

            # fast_info가 가장 빠르지만 종목에 따라 누락될 수 있음
            try:
                shares = stock.fast_info.get("shares")
                current_market_cap = stock.fast_info.get("market_cap")
            except Exception:
                pass

            # fallback
            if shares is None:
                info = stock.info
                shares = info.get("sharesOutstanding")
                current_market_cap = info.get("marketCap")

            rows.append({
                "Company": company,
                "Ticker": ticker,
                "Shares": shares,
                "Current Market Cap": current_market_cap
            })

        except Exception as e:
            rows.append({
                "Company": company,
                "Ticker": ticker,
                "Shares": np.nan,
                "Current Market Cap": np.nan
            })
            st.warning(f"{company}({ticker}) 발행주식수 데이터를 가져오지 못했습니다: {e}")

    return pd.DataFrame(rows)


with st.sidebar:
    st.header("⚙️ 설정")

    selected_companies = st.multiselect(
        "표시할 기업 선택",
        options=list(TOP10.keys()),
        default=list(TOP10.keys())
    )

    chart_mode = st.radio(
        "차트 방식",
        ["시가총액", "1년 수익률 지수화", "주가"],
        index=0
    )

    show_table = st.checkbox("최근 데이터 표 보기", value=True)

    st.markdown("---")
    st.info(
        "과거 시가총액은 `과거 종가 × 현재 발행주식수`로 계산한 근사값입니다. "
        "자사주 매입, 증자, 주식분할 등에 따라 실제 과거 시가총액과 차이가 날 수 있습니다."
    )


if not selected_companies:
    st.warning("왼쪽 사이드바에서 기업을 1개 이상 선택하세요.")
    st.stop()

selected_tickers = {k: TOP10[k] for k in selected_companies}

with st.spinner("Yahoo Finance에서 데이터를 불러오는 중입니다..."):
    price_df = get_price_data(selected_tickers)
    shares_df = get_shares_outstanding(selected_tickers)

df = price_df.merge(shares_df, on=["Company", "Ticker"], how="left")
df["Market Cap"] = df["Close"] * df["Shares"]
df = df.dropna(subset=["Close"])

# 지수화: 시작일 = 100
df["Indexed"] = df.groupby("Company")["Close"].transform(lambda x: x / x.iloc[0] * 100)

latest = (
    df.sort_values("Date")
    .groupby("Company")
    .tail(1)
    .sort_values("Market Cap", ascending=False)
)

col1, col2, col3, col4 = st.columns(4)

total_cap = latest["Market Cap"].sum()
best_company = latest.sort_values("Indexed", ascending=False).iloc[0]
worst_company = latest.sort_values("Indexed", ascending=True).iloc[0]

col1.metric("선택 기업 수", f"{len(selected_companies)}개")
col2.metric("합산 시가총액", f"${total_cap / 1e12:,.2f}T")
col3.metric("1년 최고 상승", best_company["Company"], f"{best_company['Indexed'] - 100:.1f}%")
col4.metric("1년 최저 상승", worst_company["Company"], f"{worst_company['Indexed'] - 100:.1f}%")

st.markdown("## 📊 최근 1년 변화")

if chart_mode == "시가총액":
    fig = px.line(
        df,
        x="Date",
        y="Market Cap",
        color="Company",
        hover_data={
            "Ticker": True,
            "Market Cap": ":,.0f",
            "Close": ":.2f",
            "Date": True
        },
        title="글로벌 시가총액 Top 10 최근 1년 시가총액 변화"
    )
    fig.update_yaxes(title="Market Cap, USD", tickprefix="$")
    fig.update_layout(hovermode="x unified")

elif chart_mode == "1년 수익률 지수화":
    fig = px.line(
        df,
        x="Date",
        y="Indexed",
        color="Company",
        hover_data={
            "Ticker": True,
            "Indexed": ":.2f",
            "Close": ":.2f",
            "Date": True
        },
        title="최근 1년 주가 변화 지수화, 시작일 = 100"
    )
    fig.add_hline(y=100, line_dash="dash")
    fig.update_yaxes(title="Index, Start = 100")
    fig.update_layout(hovermode="x unified")

else:
    fig = px.line(
        df,
        x="Date",
        y="Close",
        color="Company",
        hover_data={
            "Ticker": True,
            "Close": ":.2f",
            "Date": True
        },
        title="최근 1년 주가 변화"
    )
    fig.update_yaxes(title="Adjusted Close Price")
    fig.update_layout(hovermode="x unified")

st.plotly_chart(fig, use_container_width=True)

st.markdown("## 🏆 최신 시가총액 순위")

bar_fig = px.bar(
    latest,
    x="Company",
    y="Market Cap",
    text=latest["Market Cap"].apply(lambda x: f"${x/1e12:.2f}T"),
    title="선택 기업 최신 시가총액 비교"
)
bar_fig.update_yaxes(title="Market Cap, USD", tickprefix="$")
bar_fig.update_xaxes(title="")
bar_fig.update_traces(textposition="outside")
st.plotly_chart(bar_fig, use_container_width=True)

if show_table:
    st.markdown("## 📋 최신 데이터")

    table = latest[[
        "Company",
        "Ticker",
        "Close",
        "Market Cap",
        "Indexed"
    ]].copy()

    table["Close"] = table["Close"].map(lambda x: f"${x:,.2f}")
    table["Market Cap"] = table["Market Cap"].map(lambda x: f"${x/1e12:,.3f}T")
    table["1Y Change"] = latest["Indexed"].map(lambda x: f"{x - 100:.2f}%")
    table = table.drop(columns=["Indexed"])

    st.dataframe(table, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption(
    "주의: 투자 조언이 아닙니다. Yahoo Finance 데이터 지연·누락 가능성이 있으며, "
    "과거 시가총액은 현재 발행주식수를 기준으로 한 근사값입니다."
)
