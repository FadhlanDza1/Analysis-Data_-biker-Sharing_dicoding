import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv('Dasbord/final_df.csv')

# Konversi tanggal
df['dteday'] = pd.to_datetime(df['dteday'])
df['year'] = df['dteday'].dt.year
df['month'] = df['dteday'].dt.month

# Sidebar filter
st.sidebar.header("🔍 Filter Data")

year_options = ["Semua Tahun"] + sorted(df['year'].unique().tolist())
selected_year = st.sidebar.selectbox("Pilih Tahun", year_options)

month_options = ["Semua Bulan"] + sorted(df['month'].unique().tolist())
selected_month = st.sidebar.selectbox("Pilih Bulan", month_options)

# Filter dataset
filtered_df = df.copy()
if selected_year != "Semua Tahun":
    filtered_df = filtered_df[filtered_df['year'] == selected_year]
if selected_month != "Semua Bulan":
    filtered_df = filtered_df[filtered_df['month'] == selected_month]

# Hitung minggu dalam bulan
filtered_df['week_in_month'] = (filtered_df['dteday'].dt.day - 1) // 7 + 1

# Plot berdasarkan filter
if selected_month == "Semua Bulan":
    # Jika semua bulan dipilih → Tampilkan tren bulanan
    st.subheader("📈 Tren Penyewaan Sepeda (Bulan ke Bulan)")
    monthly_trend = filtered_df.groupby(['year', 'month'])['cnt'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=monthly_trend, x='month', y='cnt', marker='o', hue='year', ax=ax)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.set_title(f"Tren Penyewaan Sepeda ({selected_year})")
    st.pyplot(fig)

else:
    # Jika bulan spesifik dipilih → Tampilkan tren mingguan dalam bulan itu
    st.subheader(f"📆 Tren Penyewaan Sepeda per Minggu ({selected_year} - {selected_month})")
    weekly_trend = filtered_df.groupby(['year', 'month', 'week_in_month'])['cnt'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=weekly_trend, x='week_in_month', y='cnt', marker='o', hue='year', ax=ax)
    ax.set_xticks(weekly_trend['week_in_month'].unique())  # Pastikan sumbu x hanya menampilkan minggu yang ada
    ax.set_xlabel("Minggu ke- dalam Bulan")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.set_title(f"Tren Penyewaan Sepeda ({selected_year} - {selected_month})")
    st.pyplot(fig)


st.subheader("📊 Penyewaan Sepeda: Hari Kerja vs Hari Libur")

workday_trend = filtered_df.groupby('workingday')['cnt'].agg(['sum', 'mean']).reset_index()
workday_trend['workingday'] = workday_trend['workingday'].map({0: 'Hari Libur', 1: 'Hari Kerja'})

fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(data=workday_trend, x='workingday', y='mean', palette='coolwarm', ax=ax)
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
