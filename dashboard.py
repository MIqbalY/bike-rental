import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image

# Load data
main_df = pd.read_csv("main_data.csv")
def create_daily_df(df):
    daily_df = df.groupby(by="dteday").agg({
        "cnt": "sum"
    })
    return daily_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="season").cnt.sum().reset_index()
    byseason_df['season'] = pd.Categorical(byseason_df['season'], ["Springer", "Summer", "Fall", "Winter"])
    return byseason_df

def create_byweather_df(df):
    byweather_df = df.groupby(by="weathersit").cnt.sum().reset_index()
    byweather_df['weathersit'] = pd.Categorical(byweather_df['weathersit'], ["Clear", "Cloudy", "Light Rain/Snow", "Thunderstorm/Blizard"])
    return byweather_df

def create_avghours_df(df):
    avghours_df = df.groupby(by="workingday").hr.mean().reset_index()
    avghours_df['workingday'] = pd.Categorical(avghours_df['workingday'], ["Work Day", "Weekend/Holiday"])
    return avghours_df

def create_casual_df(df):
    casual_df = df.groupby(by="yr").casual.sum().reset_index()
    casual_df['yr'] = pd.Categorical(casual_df['yr'], ["2011", "2012"])
    return casual_df

def create_registered_df(df):
    registered_df = df.groupby(by="yr").registered.sum().reset_index()
    registered_df['yr'] = pd.Categorical(registered_df['yr'], ["2011", "2012"])
    return registered_df

#Membuat DataFrame
daily_df = create_daily_df(main_df)
byseason_df = create_byseason_df(main_df)
byweather_df = create_byweather_df(main_df)
avghours_df = create_avghours_df(main_df)
casual_df = create_casual_df(main_df)
registered_df = create_registered_df(main_df)

# Header
col1, col2 = st.columns(2)
with col1:
    st.write(
        """
        # Rental Sepeda Pak Eko
        #### Statistik dan Data 2011-2012
        """
    )

with col2:
    image = Image.open('542278 (1).png')
    st.image(image)

tab1, tab2 = st.tabs(["Statistik", "Data"])

with tab1:
    # Grafik Daily Basis
    st.subheader('Sewa per Hari')
    datetime_columns = ["dteday"]
    main_df.sort_values(by="dteday")
    main_df.reset_index(inplace=True)
    for column in datetime_columns:
        main_df[column] = pd.to_datetime(main_df[column])
    min_date = main_df["dteday"].min()
    max_date = main_df["dteday"].max()
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    main_df = main_df[(main_df["dteday"] >= str(start_date)) &
                     (main_df["dteday"] <= str(end_date))]
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(
        main_df["dteday"],
        main_df["cnt"],
        linewidth=2,
        marker='o'
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=18)
    st.pyplot(fig)
    st.line_chart(daily_df)

    # Grafik Order by Season and Weathersite
    col3, col4 = st.columns(2)
    with col3:
        st.subheader('Jumlah sewa berdasarkan Musim')
        st.bar_chart(byseason_df)

    with col4:
        st.subheader('Jumlah sewa berdasarkan Cuaca')
        st.bar_chart(byweather_df)

    # Grafik Persentase berdasarkan hari dan jam
    st.subheader('Persentase jumlah sewa berdasarkan Hari')
    fig = px.pie(main_df, names='weekday', values='cnt')
    st.plotly_chart(fig)

    st.subheader('Persentase jumlah sewa berdasarkan jam sewa')
    fig = px.pie(main_df, names='hr', values='cnt')
    st.plotly_chart(fig)

    # Grafik Rerata Sewa Hari Kerja/Libur
    st.subheader('Rerata jam sewa berdasarkan Hari kerja dan Akhir Pekan/Libur')
    st.bar_chart(avghours_df)

    # Grafik Customer Growth
    st.markdown("<h3 style='text-align: center; color: white;'>Pertumbuhan Pelanggan</h3>", unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        st.markdown("<h3 style='text-align: center; color: white;'>Kasual</h3>", unsafe_allow_html=True)
        st.bar_chart(casual_df)

    with col6:
        st.markdown("<h3 style='text-align: center; color: white;'>Terdaftar</h3>", unsafe_allow_html=True)
        st.bar_chart(registered_df)

st.markdown("<h3 style='text-align: left; color: white;'> </h3>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: left; color: white;'> </h3>", unsafe_allow_html=True)
st.caption('Copyright (c) 2023 miqbalyusuf. All Right Reserved')

with tab2:
    st.title('Bike-sharing-dataset')
    st.dataframe(main_df)
    st.markdown(
        """
        Use of this dataset in publications must be cited to the following publication:
        [1] Fanaee-T, Hadi, and Gama, Joao, "Event labeling combining ensemble detectors and background knowledge", 
        Progress in Artificial Intelligence (2013): pp. 1-15, Springer Berlin Heidelberg, doi:10.1007/s13748-013-0040-3.
        """
    )