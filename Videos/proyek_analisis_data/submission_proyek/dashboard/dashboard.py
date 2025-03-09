
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static

# Load dataset yang sudah dibersihkan
@st.cache_data
def load_data():
    file_path = "final_ecommerce_data.csv"
    df = pd.read_csv(file_path, parse_dates=["order_purchase_timestamp"])
    return df

df = load_data()

# Sidebar - Filter Data
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Start Date", df["order_purchase_timestamp"].min())
end_date = st.sidebar.date_input("End Date", df["order_purchase_timestamp"].max())

# Filter berdasarkan tanggal
filtered_df = df[(df["order_purchase_timestamp"] >= pd.Timestamp(start_date)) & 
                 (df["order_purchase_timestamp"] <= pd.Timestamp(end_date))]

# ** Overview**
st.title("📊 E-Commerce Dashboard")
st.subheader("Ringkasan Data")
col1, col2, col3 = st.columns(3)
col1.metric("Total Order", f"{filtered_df['order_id'].nunique():,}")
col2.metric("Total Revenue", f"${filtered_df['price'].sum():,.2f}")
col3.metric("Total Customers", f"{filtered_df['customer_id'].nunique():,}")

# ** Tren Penjualan**
st.subheader("📈 Tren Penjualan per Bulan")
filtered_df.loc[:, "order_month"] = filtered_df["order_purchase_timestamp"].dt.to_period("M")
sales_trend = filtered_df.groupby("order_month")["order_id"].count().reset_index()

# Convert period ke string biar seaborn bisa baca
sales_trend["order_month"] = sales_trend["order_month"].astype(str)

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=sales_trend, x="order_month", y="order_id", marker="o", ax=ax)
plt.xticks(rotation=45)
plt.xlabel("Bulan")
plt.ylabel("Jumlah Order")
plt.title("Tren Penjualan dari Waktu ke Waktu")
st.pyplot(fig)

# ** Peta Lokasi Seller & Pelanggan**
st.subheader("📍 Distribusi Order Berdasarkan Wilayah")

state_counts = filtered_df["customer_state"].value_counts().reset_index()
state_counts.columns = ["State", "Jumlah Order"]

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=state_counts, x="Jumlah Order", y="State", palette="coolwarm", ax=ax)
plt.xlabel("Jumlah Order")
plt.ylabel("Provinsi Pelanggan")
plt.title("Distribusi Order Berdasarkan Wilayah")
st.pyplot(fig)

st.write("📌 **Grafik menunjukkan distribusi jumlah order berdasarkan provinsi pelanggan.**")



