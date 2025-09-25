# filepath: ui/app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="資産管理ダッシュボード")

st.title("資産管理プロトタイプ")

# モックデータ
df = pd.DataFrame({
    "date": pd.date_range("2023-01-01", periods=6, freq="M"),
    "total": [10000, 10500, 10300, 11000, 11500, 12000]
})
col1, col2 = st.columns([2,1])

with col1:
    st.subheader("総資産推移")
    fig = px.line(df, x="date", y="total", title="総資産")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("個別カード（サンプル）")
    st.write("資産A: 10,000")
    st.write("資産B: 2,000")
