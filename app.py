import plotly.express as px
import streamlit as st

from sales_calculations import load_data, total_sales, total_orders, monthly_trend

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

df = load_data("data/sales-data.csv")

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales(df):,.0f}")
col2.metric("Total Orders", f"{total_orders(df):,}")

trend = monthly_trend(df)
trend_fig = px.line(
    trend,
    x="month",
    y="total_amount",
    title="Monthly Sales Trend",
    labels={"month": "Month", "total_amount": "Sales ($)"},
    markers=True,
)
st.plotly_chart(trend_fig, use_container_width=True)
