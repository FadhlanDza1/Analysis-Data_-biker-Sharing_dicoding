import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('final_df.csv')


df['dteday'] = pd.to_datetime(df['dteday'])
df['year'] = df['dteday'].dt.year
df['month'] = df['dteday'].dt.month



st.sidebar.header("🔍 Filter Data")


year_options = ["Semua Tahun"] + sorted(df['year'].unique().tolist())
selected_year = st.sidebar.selectbox("Pilih Tahun", year_options)


month_options = ["Semua Bulan"] + sorted(df['month'].unique().tolist())
selected_month = st.sidebar.selectbox("Pilih Bulan", month_options)



filtered_df = df.copy()
if selected_year != "Semua Tahun":
    filtered_df = filtered_df[filtered_df['year'] == selected_year]
if selected_month != "Semua Bulan":
    filtered_df = filtered_df[filtered_df['month'] == selected_month]

st.subheader("📈 Tren Penyewaan Sepeda (Bulan ke Bulan)")
monthly_filtered_df = df[(df['year'] == selected_year)]
monthly_trend = monthly_filtered_df.groupby(['year', 'mnth'])['cnt'].agg(
    ['sum', 'mean', 'median', 'std']
).reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=monthly_trend['mnth'], y=monthly_trend['sum'], marker='o', ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title(f"Tren Penyewaan Sepeda ({selected_year})")
st.pyplot(fig)


st.subheader("📊 Penyewaan Sepeda: Hari Kerja vs Hari Libur")

workday_trend = filtered_df.groupby('workingday')['cnt'].agg(['sum', 'mean']).reset_index()
workday_trend['workingday'] = workday_trend['workingday'].map({0: 'Hari Libur', 1: 'Hari Kerja'})

fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(data=workday_trend, x='workingday', y='sum', palette='coolwarm', ax=ax)
ax.set_xlabel("Tipe Hari")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Penyewaan Sepeda pada Hari Kerja vs Hari Libur")
st.pyplot(fig)


st.subheader("🌦️ Pengaruh Musim terhadap Penyewaan Sepeda")


season_trend = df.groupby('season')['cnt'].sum().reset_index()

fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(data=season_trend, x='season', y='cnt', palette='coolwarm', ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title(f"Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig)
