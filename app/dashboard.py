import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sales.csv")

st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# --- Sidebar filters ---
st.sidebar.title("Filters")
years = sorted(df["year"].unique())
selected_years = st.sidebar.multiselect("Year", years, default=years)

categories = sorted(df["category"].unique())
selected_cats = st.sidebar.multiselect("Category", categories, default=categories)

regions = sorted(df["region"].unique())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)

filtered = df[
    df["year"].isin(selected_years) &
    df["category"].isin(selected_cats) &
    df["region"].isin(selected_regions)
]

# --- Header ---
st.title("📊 Sales Performance Dashboard")
st.markdown("Interactive overview of sales, profit, and trends across categories, regions, and channels.")
st.divider()

# --- KPI Cards ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${filtered['revenue'].sum():,.0f}")
col2.metric("Total Profit", f"${filtered['profit'].sum():,.0f}")
col3.metric("Profit Margin", f"{filtered['profit'].sum() / filtered['revenue'].sum() * 100:.1f}%")
col4.metric("Total Orders", f"{len(filtered):,}")

st.divider()

# --- Monthly Trend ---
st.subheader("Revenue & Profit — Monthly Trend")
monthly = filtered.groupby(["year", "month_num", "month_name"])[["revenue", "profit"]].sum().reset_index()
monthly = monthly.sort_values(["year", "month_num"])
fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(x=monthly["month_name"], y=monthly["revenue"], name="Revenue", fill="tozeroy", line=dict(color="#4C78A8")))
fig_trend.add_trace(go.Scatter(x=monthly["month_name"], y=monthly["profit"], name="Profit", fill="tozeroy", line=dict(color="#54A24B")))
fig_trend.update_layout(xaxis_title="Month", yaxis_title="USD", legend=dict(orientation="h"))
st.plotly_chart(fig_trend, use_container_width=True)

# --- Category + Region ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Revenue by Category")
    cat_df = filtered.groupby("category")["revenue"].sum().reset_index().sort_values("revenue", ascending=True)
    fig_cat = px.bar(cat_df, x="revenue", y="category", orientation="h", color="revenue",
                     color_continuous_scale="Blues", labels={"revenue": "Revenue (USD)", "category": ""})
    fig_cat.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_cat, use_container_width=True)

with col_b:
    st.subheader("Revenue by Region")
    reg_df = filtered.groupby("region")["revenue"].sum().reset_index()
    fig_reg = px.pie(reg_df, names="region", values="revenue", color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_reg, use_container_width=True)

# --- Top Products + Channel ---
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Top 10 Products by Revenue")
    top_products = filtered.groupby("product")["revenue"].sum().nlargest(10).reset_index().sort_values("revenue", ascending=True)
    fig_prod = px.bar(top_products, x="revenue", y="product", orientation="h", color="revenue",
                      color_continuous_scale="Oranges", labels={"revenue": "Revenue (USD)", "product": ""})
    fig_prod.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_prod, use_container_width=True)

with col_d:
    st.subheader("Sales Channel Breakdown")
    ch_df = filtered.groupby("channel").agg(orders=("order_id", "count"), revenue=("revenue", "sum")).reset_index()
    fig_ch = px.bar(ch_df, x="channel", y=["orders", "revenue"], barmode="group",
                    color_discrete_sequence=["#4C78A8", "#F58518"],
                    labels={"value": "Count / USD", "variable": ""})
    st.plotly_chart(fig_ch, use_container_width=True)

# --- Raw Data ---
with st.expander("View Raw Data"):
    st.dataframe(filtered.sort_values("date", ascending=False).head(500), use_container_width=True)
