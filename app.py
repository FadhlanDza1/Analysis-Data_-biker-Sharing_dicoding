import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("final_dataset.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])
    df["month"] = df["dteday"].dt.month
    df["year"] = df["dteday"].dt.year
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun", df["year"].unique())
selected_month = st.sidebar.selectbox("Pilih Bulan", df["month"].unique())

filtered_df = df[(df["year"] == selected_year) & (df["month"] == selected_month)]

st.title("📊 Dashboard Penyewaan Sepeda")

# Grafik Penyewaan Sepeda per Bulan
st.subheader("📅 Penyewaan Sepeda per Bulan")
monthly_data = df[df["year"] == selected_year].groupby("month")["cnt"].sum()
fig, ax = plt.subplots()
sns.lineplot(x=monthly_data.index, y=monthly_data.values, marker="o", ax=ax, color='b')
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_xticks(range(1, 13))
st.pyplot(fig)

# Grafik Perbandingan Hari Kerja vs Libur
st.subheader("🏢 Perbandingan Penyewaan: Hari Kerja vs Libur")
fig, ax = plt.subplots()
sns.barplot(x=["Libur", "Hari Kerja"], y=filtered_df.groupby("workingday")["cnt"].mean(), palette=["lightblue", "lightsalmon"], ax=ax)
ax.set_xlabel("Hari Kerja (1) vs Libur (0)")
ax.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig)

# Grafik Pengaruh Musim terhadap Penyewaan
st.subheader("🌦️ Pengaruh Musim terhadap Penyewaan Sepeda")
fig, ax = plt.subplots()
sns.barplot(x=df['season'], y=df["cnt"], palette="coolwarm", ci=None, ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

st.subheader("📋 Data Penyewaan Sepeda")
st.write(filtered_df)
