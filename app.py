import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# === 1. Загрузка данных ===
import os
conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'ict_analysis.db'))

df_macro = pd.read_sql("SELECT * FROM macro_ict_data", conn)
df_forecast = pd.read_sql("SELECT * FROM forecast_results", conn)
df_desc = pd.read_sql("SELECT * FROM indicator_description", conn)

# === 2. Основной заголовок ===
st.title("📊 Интерактивный анализ ИКТ и прогнозирование")

# === 3. Просмотр таблиц ===
with st.expander("📁 Показать макроэкономические данные"):
    st.dataframe(df_macro)

with st.expander("📈 Прогноз SARIMAX"):
    st.dataframe(df_forecast)

with st.expander("🧾 Описание показателей"):
    st.dataframe(df_desc)

# === 4. Визуализация временного ряда ИКТ ===
st.subheader("Динамика ИКТ-услуг с 2010 по 2024")
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df_macro["year"], y=df_macro["ict_services"],
                          mode='lines+markers', name='ИКТ-услуги'))
fig1.update_layout(xaxis_title="Год", yaxis_title="ИКТ (трлн руб.)")
st.plotly_chart(fig1)

# === 5. Прогноз SARIMAX (график с доверительными интервалами) ===
st.subheader("Прогноз ИКТ-услуг по SARIMAX (2025–2029)")
df_forecast = df_forecast[df_forecast["model_type"] == "SARIMAX"]

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df_forecast["year"], y=df_forecast["forecast_value"],
                          mode='lines+markers', name='Прогноз'))
fig2.add_trace(go.Scatter(x=df_forecast["year"], y=df_forecast["lower_bound"],
                          line=dict(dash='dot'), name='Нижняя граница'))
fig2.add_trace(go.Scatter(x=df_forecast["year"], y=df_forecast["upper_bound"],
                          line=dict(dash='dot'), name='Верхняя граница'))
fig2.update_layout(xaxis_title="Год", yaxis_title="ИКТ (трлн руб.)")
st.plotly_chart(fig2)

# === 6. Интерактивный ввод пользовательского сценария ===
st.subheader("📌 Пользовательский сценарий: рассчитай свой прогноз")
col1, col2 = st.columns(2)
with col1:
    inf = st.number_input("Инфляция (%)", value=7.0)
    gdp = st.number_input("ВВП (трлн руб.)", value=150.0)
with col2:
    unemp = st.number_input("Безработица (%)", value=4.5)
    rnd = st.number_input("НИОКР (% от ВВП)", value=1.0)

# === 7. Прогноз по регрессионной модели ===
coef = {
    'const': -9587.10,
    'inflation': 59.54,
    'gdp': 43.45,
    'unemployment': 94.29,
    'rnd': 7968.23
}
ict_pred = (
    coef['const']
    + coef['inflation'] * inf
    + coef['gdp'] * gdp
    + coef['unemployment'] * unemp
    + coef['rnd'] * rnd
)
st.success(f"Прогноз объёма ИКТ-услуг: {ict_pred:.2f} трлн руб.")
