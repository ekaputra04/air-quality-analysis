import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load the dataset
script_dir = os.path.dirname(__file__) # Mendapatkan lokasi file .py
file_path = os.path.join(script_dir, './../data/clean/all-data.csv')
data = pd.read_csv(file_path)
data["datetime"] = pd.to_datetime(data["datetime"])

# Mengambil nilai minimum dan maksimum dari kolom 'datetime'
min_date = data["datetime"].min().date()  # Mengambil tanggal minimum
max_date = data["datetime"].max().date()  # Mengambil tanggal maksimum

# Sidebar for user input
st.sidebar.header("Filter Options")
start_date = st.sidebar.date_input("Start date", value=min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End date", value=max_date, min_value=min_date, max_value=max_date)
selected_season = st.sidebar.selectbox("Select season", options=["All", "Winter", "Spring", "Summer", "Autumn"])

# Filter data based on date range and season
filtered_data = data[(data['datetime'] >= pd.to_datetime(start_date)) & (data['datetime'] <= pd.to_datetime(end_date))]

if selected_season != "All":
    filtered_data = filtered_data[filtered_data['season'] == selected_season]

# Dashboard title
st.title("Air Quality Dashboard")

# Pertanyaan 1: Bagaimana variasi kualitas udara (PM2.5, PM10) berdasarkan musim?
st.subheader("Variasi Kualitas Udara Berdasarkan Musim (PM2.5, PM10)")
if filtered_data.empty:
    st.write("No data available for the selected range.")
else:
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    sns.boxplot(x='season', y='PM2.5', data=filtered_data, ax=ax[0])
    ax[0].set_title('PM2.5 by Season')
    sns.boxplot(x='season', y='PM10', data=filtered_data, ax=ax[1])
    ax[1].set_title('PM10 by Season')
    st.pyplot(fig)

# Pertanyaan 2: Apakah ada hubungan antara kecepatan angin (WSPM) dan konsentrasi PM2.5 di berbagai musim?
st.subheader("Hubungan antara Kecepatan Angin (WSPM) dan PM2.5 Berdasarkan Musim")
if not filtered_data.empty:
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='WSPM', y='PM2.5', hue='season', data=filtered_data, alpha=0.5, ax=ax2)
    plt.title('WSPM vs PM2.5 by Season')
    st.pyplot(fig2)

# Pertanyaan 3: Bagaimana distribusi polutan berbahaya (SO2, NO2, CO) di berbagai musim dan jam dalam sehari?
st.subheader("Distribusi Polutan Berbahaya Berdasarkan Musim dan Jam (SO2, NO2, CO)")
hourly_data = filtered_data.groupby([filtered_data['datetime'].dt.hour, 'season'])[['SO2', 'NO2', 'CO']].mean().reset_index()

if not hourly_data.empty:
    fig3, (ax3_1, ax3_2, ax3_3) = plt.subplots(1, 3, figsize=(18, 6))
    sns.lineplot(x='datetime', y='SO2', hue='season', data=hourly_data, ax=ax3_1)
    ax3_1.set_title('SO2 Distribution by Hour and Season')
    
    sns.lineplot(x='datetime', y='NO2', hue='season', data=hourly_data, ax=ax3_2)
    ax3_2.set_title('NO2 Distribution by Hour and Season')
    
    sns.lineplot(x='datetime', y='CO', hue='season', data=hourly_data, ax=ax3_3)
    ax3_3.set_title('CO Distribution by Hour and Season')
    
    st.pyplot(fig3)

# Pertanyaan 4: Bagaimana pengaruh curah hujan (RAIN) terhadap konsentrasi polutan (PM2.5, PM10)?
st.subheader("Pengaruh Curah Hujan terhadap PM2.5 dan PM10")
if not filtered_data.empty:
    fig4, (ax4_1, ax4_2) = plt.subplots(1, 2, figsize=(14, 6))
    sns.scatterplot(x='RAIN', y='PM2.5', data=filtered_data, ax=ax4_1, alpha=0.5)
    ax4_1.set_title('RAIN vs PM2.5')
    
    sns.scatterplot(x='RAIN', y='PM10', data=filtered_data, ax=ax4_2, alpha=0.5)
    ax4_2.set_title('RAIN vs PM10')
    
    st.pyplot(fig4)

# Pertanyaan 5: Apakah ada tren perubahan kualitas udara (PM2.5, PM10) dari tahun 2013 hingga 2017?
st.subheader("Tren Perubahan Kualitas Udara dari 2013 hingga 2017 (PM2.5 dan PM10)")
yearly_data = filtered_data.groupby(filtered_data['datetime'].dt.year)[['PM2.5', 'PM10']].mean().reset_index()

if not yearly_data.empty:
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='datetime', y='PM2.5', data=yearly_data, marker='o', label='PM2.5', ax=ax5, color='b')
    sns.lineplot(x='datetime', y='PM10', data=yearly_data, marker='o', label='PM10', ax=ax5, color='r')
    ax5.set_title('Tren Perubahan PM2.5 dan PM10 dari 2013 hingga 2017')
    st.pyplot(fig5)
