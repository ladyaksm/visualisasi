import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

# Load dataset hasil olahan
df = pd.read_csv("main_data.csv")

# Konversi order_purchase_timestamp ke datetime
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
df["purchase_month"] = df["order_purchase_timestamp"].dt.to_period("M")

# Sidebar Navigation
st.sidebar.title("📊 Dashboard E-Commerce")
menu = st.sidebar.radio("Pilih Visualisasi:", [
    "Tren Pembelian Per Bulan",
    "Kategori Produk Paling Banyak Dibeli",
    "Rata-rata Harga Produk",
    "Hubungan Seller & Pelanggan (Heatmap)",
    "Kota dengan Pesanan Terbanyak",
    "Distribusi Pesanan Per Provinsi"
])

# Filtering Interaktif
st.sidebar.header("🔍 Filter Data")
start_date = st.sidebar.date_input("Tanggal Mulai", df["order_purchase_timestamp"].min().date())
end_date = st.sidebar.date_input("Tanggal Akhir", df["order_purchase_timestamp"].max().date())
selected_category = st.sidebar.selectbox("Pilih Kategori Produk", ["Semua"] + sorted(df["product_category_name_english"].dropna().unique()))
selected_cities = st.sidebar.multiselect("Pilih Kota Pelanggan", df["customer_city"].unique())

# Terapkan filter pada dataset
filtered_df = df[(df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) &
                 (df["order_purchase_timestamp"] <= pd.to_datetime(end_date))]
if selected_category != "Semua":
    filtered_df = filtered_df[filtered_df["product_category_name_english"] == selected_category]
if selected_cities:
    filtered_df = filtered_df[filtered_df["customer_city"].isin(selected_cities)]

# 1️⃣ Visualisasi Tren Pembelian Kategori Produk Per Bulan
if menu == "Tren Pembelian Per Bulan":
    st.title("📈 Tren Pembelian Kategori Produk Per Bulan")
    category_trends = filtered_df.groupby(["purchase_month", "product_category_name_english"]) \
                              ["order_id"].count().reset_index()
    top_categories_list = category_trends.groupby("product_category_name_english")["order_id"].sum() \
                                    .sort_values(ascending=False).head(5).index.tolist()
    
    fig, ax = plt.subplots(figsize=(14, 7))
    for category in top_categories_list:
        data = category_trends[category_trends["product_category_name_english"] == category]
        ax.plot(data["purchase_month"].astype(str), data["order_id"], marker="o", label=category)
    
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Transaksi")
    ax.set_title("Tren Pembelian Produk per Kategori")
    ax.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(fig)

# 2️⃣ Visualisasi Kategori Produk Paling Banyak Dibeli
elif menu == "Kategori Produk Paling Banyak Dibeli":
    st.title("📊 Kategori Produk Paling Banyak Dibeli")
    top_categories = filtered_df['product_category_name_english'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_categories.values, y=top_categories.index, palette="coolwarm", ax=ax)
    ax.set_xlabel("Jumlah Produk Terjual")
    ax.set_ylabel("Kategori Produk")
    ax.set_title("Top 10 Kategori Produk")
    st.pyplot(fig)

# 3️⃣ Visualisasi Rata-rata Harga Produk Per Kategori
elif menu == "Rata-rata Harga Produk":
    st.title("💰 Rata-rata Harga Produk Per Kategori")
    avg_price_per_category = filtered_df.groupby('product_category_name_english')['price'].mean().reset_index()
    avg_price_per_category = avg_price_per_category.sort_values(by="price", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=avg_price_per_category, x="price", y="product_category_name_english", palette="magma", ax=ax)
    ax.set_xlabel("Rata-rata Harga (IDR)")
    ax.set_ylabel("Kategori Produk")
    ax.set_title("Top 10 Kategori dengan Rata-rata Harga Tertinggi")
    st.pyplot(fig)

# 4️⃣ Hubungan Seller dan Pelanggan (Heatmap)
elif menu == "Hubungan Seller & Pelanggan (Heatmap)":
    st.title("🔥 Hubungan Seller & Pelanggan Berdasarkan Kota")
    pivot_table = filtered_df.pivot_table(index="seller_city", columns="customer_city", values="order_id", aggfunc='count', fill_value=0)
    min_orders = 50
    filtered_pivot = pivot_table.loc[pivot_table.sum(axis=1) > min_orders, pivot_table.sum(axis=0) > min_orders]
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(filtered_pivot, cmap="coolwarm", linewidths=0.5, norm=mcolors.LogNorm(), ax=ax)
    ax.set_xlabel("Kota Pelanggan")
    ax.set_ylabel("Kota Seller")
    ax.set_title("Hubungan Seller dan Pelanggan Berdasarkan Kota")
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    st.pyplot(fig)

# 5️⃣ Kota dengan Pesanan Terbanyak
elif menu == "Kota dengan Pesanan Terbanyak":
    st.title("🏙️ Kota dengan Pesanan Terbanyak")
    city_orders = filtered_df['customer_city'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=city_orders.values, y=city_orders.index, palette="viridis", ax=ax)
    ax.set_xlabel("Jumlah Pesanan")
    ax.set_ylabel("Kota")
    ax.set_title("Top 10 Kota dengan Pesanan Terbanyak")
    st.pyplot(fig)

# 6️⃣ Distribusi Pesanan Per Provinsi
elif menu == "Distribusi Pesanan Per Provinsi":
    st.title("🌍 Distribusi Pesanan Berdasarkan Provinsi")
    province_orders = filtered_df['customer_state'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=province_orders.index, y=province_orders.values, palette="coolwarm", ax=ax)
    ax.set_xlabel("Provinsi")
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_title("Distribusi Pesanan Per Provinsi")
    plt.xticks(rotation=45)
    st.pyplot(fig)
