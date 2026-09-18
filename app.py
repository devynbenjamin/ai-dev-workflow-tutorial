import plotly.express as px
import streamlit as st

from sales_calculations import (
    load_data,
    total_sales,
    total_orders,
    monthly_trend,
    sales_by_category,
    sales_by_region,
)

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
st.plotly_chart(trend_fig, width="stretch")

category_col, region_col = st.columns(2)

category_data = sales_by_category(df)
category_fig = px.bar(
    category_data,
    x="category",
    y="total_amount",
    title="Sales by Category",
    labels={"category": "Category", "total_amount": "Sales ($)"},
    category_orders={"category": list(category_data["category"])},
)
category_col.plotly_chart(category_fig, width="stretch")

region_data = sales_by_region(df)
region_fig = px.bar(
    region_data,
    x="region",
    y="total_amount",
    title="Sales by Region",
    labels={"region": "Region", "total_amount": "Sales ($)"},
    category_orders={"region": list(region_data["region"])},
)
region_col.plotly_chart(region_fig, width="stretch")
