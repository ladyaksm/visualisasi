import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

# Load dataset hasil olahan
df = pd.read_csv("final_ecommerce_data.csv")

# Konversi order_purchase_timestamp ke datetime
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
df["purchase_month"] = df["order_purchase_timestamp"].dt.to_period("M")

# Hitung jumlah transaksi per kategori per bulan
category_trends = df.groupby(["purchase_month", "product_category_name_english"])["order_id"].count().reset_index()

# Ambil 5 kategori produk paling populer
top_categories = category_trends.groupby("product_category_name_english")["order_id"].sum().reset_index()
top_categories_list = top_categories.sort_values(by="order_id", ascending=False)["product_category_name_english"].head(5).tolist()

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

# 1️⃣ Visualisasi Tren Pembelian Kategori Produk Per Bulan
if menu == "Tren Pembelian Per Bulan":
    st.title("📈 Tren Pembelian Kategori Produk Per Bulan")
    
    fig, ax = plt.subplots(figsize=(14, 7))
    for category in top_categories_list:
        data = category_trends[category_trends["product_category_name_english"] == category]
        ax.plot(data["purchase_month"].astype(str), data["order_id"], marker="o", label=category)
    
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Transaksi")
    ax.set_title("Tren Pembelian Produk per Kategori dalam Beberapa Bulan Terakhir")
    ax.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(fig)

# 2️⃣ Visualisasi Kategori Produk Paling Banyak Dibeli
elif menu == "Kategori Produk Paling Banyak Dibeli":
    st.title("📊 Kategori Produk Paling Banyak Dibeli")
    top_categories = df['product_category_name_english'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_categories.values, y=top_categories.index, palette="coolwarm", ax=ax)
    ax.set_xlabel("Jumlah Produk Terjual")
    ax.set_ylabel("Kategori Produk")
    ax.set_title("Top 10 Kategori Produk")
    st.pyplot(fig)

# # 3️⃣ Visualisasi Rata-rata Harga Produk Per Kategori
elif menu == "Rata-rata Harga Produk":
    st.title("💰 Rata-rata Harga Produk Per Kategori")
    
    # Hitung rata-rata harga per kategori
    avg_price_per_category = df.groupby('product_category_name_english')['price'].mean().reset_index()
    avg_price_per_category = avg_price_per_category.sort_values(by="price", ascending=False).head(10)
    
    # Plot dengan seaborn
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=avg_price_per_category, x="price", y="product_category_name_english", palette="magma", ax=ax)
    
    ax.set_xlabel("Rata-rata Harga (IDR)")
    ax.set_ylabel("Kategori Produk")
    ax.set_title("Top 10 Kategori dengan Rata-rata Harga Tertinggi")
    
    st.pyplot(fig)

# 4️⃣ Visualisasi Hubungan Seller dan Pelanggan Berdasarkan Kota (Heatmap)
elif menu == "Hubungan Seller & Pelanggan (Heatmap)":
    st.title("🔥 Hubungan Seller & Pelanggan Berdasarkan Kota")
    
    # Buat pivot table jumlah transaksi seller-customer
    pivot_table = df.pivot_table(index="seller_city", columns="customer_city", values="order_id", aggfunc='count', fill_value=0)
    
    # Filter kota dengan transaksi terbanyak
    min_orders = 50
    filtered_pivot = pivot_table.loc[pivot_table.sum(axis=1) > min_orders, pivot_table.sum(axis=0) > min_orders]
    
    # Ambil hanya top 20 seller & customer cities
    top_seller_cities = df["seller_city"].value_counts().head(20).index
    top_customer_cities = df["customer_city"].value_counts().head(20).index
    filtered_pivot = filtered_pivot.loc[filtered_pivot.index.intersection(top_seller_cities),
                                        filtered_pivot.columns.intersection(top_customer_cities)]
    
    # Plot heatmap
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(filtered_pivot, cmap="coolwarm", linewidths=0.5, norm=mcolors.LogNorm(), ax=ax)
    ax.set_xlabel("Kota Pelanggan")
    ax.set_ylabel("Kota Seller")
    ax.set_title("Hubungan Seller dan Pelanggan Berdasarkan Kota")
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    st.pyplot(fig)

# 5️⃣ Visualisasi Kota dengan Pesanan Terbanyak
elif menu == "Kota dengan Pesanan Terbanyak":
    st.title("🏙️ Kota dengan Pesanan Terbanyak")
    city_orders = df['customer_city'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=city_orders.values, y=city_orders.index, palette="Blues_r", ax=ax)
    ax.set_xlabel("Jumlah Pesanan")
    ax.set_ylabel("Kota")
    ax.set_title("Top 10 Kota dengan Pesanan Terbanyak")
    st.pyplot(fig)

# 6️⃣ Visualisasi Distribusi Pesanan Berdasarkan Provinsi
elif menu == "Distribusi Pesanan Per Provinsi":
    st.title("🌍 Distribusi Pesanan Berdasarkan Provinsi")
    province_orders = df['customer_state'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=province_orders.index, y=province_orders.values, palette="magma", ax=ax)
    ax.set_xlabel("Provinsi")
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_title("Distribusi Pesanan Per Provinsi")
    plt.xticks(rotation=45)
    st.pyplot(fig)