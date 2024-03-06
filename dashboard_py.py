import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st

sns.set(style='white')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Load dataset
df = pd.read_csv("all_data.csv")

# Membuat fungsi untuk variabel
def humidity_f(df):
    humidity_v = df.groupby(['Humidity'])['Total_rental'].sum().reset_index()
    return humidity_v

def workingday_f(df):
    workingday_v = df.groupby(['Workingday'])['Total_rental'].sum().reset_index()
    return workingday_v

# Set up variables for the dataframe
humidity_plt = humidity_f(df)
workingday_plt = workingday_f(df)

# Membuat sidebar filter
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    selected_intervals = st.multiselect('Select humidity intervals:', humidity_plt['Humidity'].unique())
    day_select = st.multiselect("Filter Hari kerja", workingday_plt['Workingday'].unique(), default=workingday_plt['Workingday'].unique())

st.header(':crown: Bicycle Rental Analysis :crown:')
st.subheader(':bike: Total Customer :bike:')

columns = st.columns(1)

# Card Total Customers
with columns[0]:
    total_rental_sum = df['Total_rental'].sum()
    st.metric('Total Customer saat ini', total_rental_sum)

# Container for filter humidity
with st.container():
    st.subheader('Distribution of bicycle rentals based on time on workingday and Not workday:')

if selected_intervals:
    filter_humidity = humidity_plt[humidity_plt['Humidity'].isin(selected_intervals)]
else:
    filter_humidity = humidity_plt

# Visualize data
plt.figure(figsize=(12, 6))  
if not filter_humidity.empty:
    sns.boxplot(x='Hour', 
                y='Total_rental', 
                hue='Workingday', 
                data=df)  
    plt.title('Distribusi Penyewaan Sepeda Berdasarkan Waktu pada Hari Kerja dan Hari Libur')
    plt.xlabel('Jam (Hour)')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    plt.legend(title='Hari Kerja')
    plt.tight_layout()
    st.pyplot()
else:
    st.write("No data available for the selected intervals.")

# Container for filter customer
with st.container():
    st.subheader('Bicycle rental patterns between Workingday / Not WorkDay:')
    # Filter data based on selection
    filtered_day = df[df['Workingday'].isin(day_select)]

    # Calculate proportions based on filtered data
    workingday_plot = filtered_day.groupby('Workingday')['Total_rental'].sum().reset_index()

    # Plotting using Streamlit
    plt.figure(figsize=(12, 6))  
if not workingday_plot.empty:
    sns.lineplot(x='Hour', 
                 y='Total_rental', 
                 hue='Workingday', 
                 data=df, 
                 ci=None)  
    plt.title('Pola Penyewaan Sepeda antara Hari Kerja dan Hari Libur')
    plt.xlabel('Jam (Hour)')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    plt.legend(title='Hari Kerja')
    plt.tight_layout()
    st.pyplot()
else:
    st.write("Mohon Untuk Memilih Minimal Satu Filter")


st.caption('Copyright (c) Nadia Sofia 2024')