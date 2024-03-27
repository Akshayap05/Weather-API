import streamlit as st
from sqlalchemy import create_engine
import requests
import numpy as np
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Page Look:

st.set_page_config(page_title="Welcome to our Weather App", page_icon="🌎")
st.title('🌦️Welcome to our Weather App')
#st.write("**Select a city from the dropdown box to explore its weather.**")
st.markdown("<h6 style='text-align: left;'>Select a city from the dropdown box to explore its weather</h6>", unsafe_allow_html=True)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Get weather data from API for different cities:


def get_details(cities):
    
    try:
        url = f'http://api.weatherapi.com/v1/current.json?key=787a74aa607147a19bb222554241903&q={cities}&aqi=yes'
        response = requests.get(url)
        weather = response.json()
        temperature = weather['current']['temp_c']
        latitude = weather['location']['lat']
        longitude = weather['location']['lon']
        condition = weather['current']['condition']['text']
        icon = weather['current']['condition']['icon']
        humidity = weather['current']['humidity']
        Cloud_cover= weather['current']['cloud']
        UV_index= weather['current']['uv']
        CO = weather['current']['air_quality']['co']
        NO2= weather['current']['air_quality']['no2']
        Ozone= weather['current']['air_quality']['o3']
        return temperature, latitude, longitude, condition, icon, humidity, Cloud_cover, UV_index, CO, NO2, Ozone    
    except:
        return 'Error', np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN


# Sidebar: Logo and Select box.

#st.sidebar.image('logo.png', width = 130, use_column_width=True)
cities = ['London', 'Manchester', 'Birmingham', 'Glasgow', 'Leeds', 'Liverpool', 'Sheffield', 'Bristol', 'Edinburgh', 'Leicester',  'York', 'Cardiff', 'Brighton', 'Coventry', 'Bath']
selected_city = st.sidebar.selectbox('Choose a city', cities)
tab = st.sidebar.radio("Select Tab", ["Weather", "Air Quality"], index=0)

weather_data = temperature, latitude, longitude ,condition, icon, humidity, Cloud_cover, UV_index, CO, NO2, Ozone = get_details(selected_city)


# Add and position text to homepage using left column:





# Display metrics and image with center alignment
if tab == 'Weather':
    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown("<div style='padding: 10% 3% 3% 1%;  background-color: #0074cc;'><h6 style='text-align: center;'>Temperature</h6>", unsafe_allow_html=True)
        st.markdown(f"<div style='padding: 10% 3% 3% 1; margin-bottom: 20px; background-color: #0074cc;'><h3 style='text-align: center;'>{temperature}°C</h3>", unsafe_allow_html=True)

    with a2:
        st.markdown("<div style='padding: 10% 3% 3% 1%; background-color: #0074cc;'><h6 style='text-align: center;'>Humidity</h6>", unsafe_allow_html=True)
        st.markdown(f"<div style='padding: 10% 3% 3% 1; margin-bottom: 20px; background-color: #0074cc;'><h3 style='text-align: center;'>{humidity}%</h3>", unsafe_allow_html=True)

    with a3:
        st.markdown("<div style='padding: 10% 3% 3% 1%; background-color: #0074cc;'><h6 style='text-align: center;'>Condition</h6>", unsafe_allow_html=True)
        st.markdown(f"<div style='padding: 10% 3% 3% 1%; margin-bottom: 20px; background-color: #0074cc;'><h3 style='text-align: center;'>{condition}</h4>", unsafe_allow_html=True)
    #    icon_url = "https:" + icon
    #    st.markdown("<div style='padding: 20px; background-color: #0074cc;'><h2 style='text-align: center;'/h2>", unsafe_allow_html=True)
    #    st.image(icon_url, use_column_width='False', output_format='auto')
    #with a4:
    #    icon_url = "https:" + icon
    #    st.markdown("<h2 style='text-align: center;'/h2>", unsafe_allow_html=True)
    #    st.image(icon_url, use_column_width='False', output_format='auto')

if tab == 'Air Quality':
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.markdown("<div style='padding: 10% 3% 3% 3%; background-color: #0074cc;'><h5 style='text-align: center;'>UV Index</h5>", unsafe_allow_html=True)
        st.markdown(f"<div style='padding: 10% 3% 3% 3%; background-color: #0074cc;'><h3 style='text-align: center;'>{UV_index}</h3>", unsafe_allow_html=True)
    with b2:
        st.markdown("<div style='padding: 10% 3% 3% 3%; background-color: #0074cc;'><h5 style='text-align: center;' >CO</h5>", unsafe_allow_html=True)
        st.markdown(f"<div style='padding: 10% 3% 3% 3%; background-color: #0074cc;'><h3 style='text-align: center;'>{CO}</h3>", unsafe_allow_html=True)
    with b3:
        st.markdown("<div style='padding: 10% 3% 3% 3%; background-color: #0074cc;'><h5 style='text-align: center;'>NO2</h5>", unsafe_allow_html=True)
        st.markdown(f"<div style='padding: 10% 3% 3% 3%; background-color: #0074cc;'><h3 style='text-align: center;'>{NO2}</h3>", unsafe_allow_html=True)
    with b4:
        st.markdown("<div style='padding: 10% 3% 3% 3%; background-color: #0074cc;'><h5 style='text-align: center;'>Ozone (O3)</h5>", unsafe_allow_html=True)
        st.markdown(f"<div style='padding: 10% 3% 3% 3%; background-color: #0074cc;'><h3 style='text-align: center;'>{Ozone}</h3>", unsafe_allow_html=True)


# Credentials to connect to database in pagila postgresql:
        
db_user = st.secrets["DB_USER"]
db_password = st.secrets["DB_PASSWORD"]
db_host = st.secrets["DB_HOSTS"]
db_name = st.secrets["DB_NAME"]
db_port = st.secrets["DB_PORT"]

# Connect to database, get weather details through table using query:


def get_data(selected_city):

    try:

        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        query1 = f"""
                SELECT DISTINCT to_char(date, 'YYYY-MM-DD') AS date, location, temperature, co, no2, o3
                FROM student.weather
                WHERE location='{selected_city}'
                ORDER BY date ASC"""
        data = pd.read_sql(query1, engine)

        query2 = f"""
                SELECT DISTINCT to_char(date, 'YYYY-MM-DD') AS date, location, AVG(co) AS avg_co, AVG(no2) AS avg_no2, AVG(o3) AS avg_o3
                FROM student.weather
                WHERE location = '{selected_city}'
                GROUP BY date, location
                ORDER BY date ASC""" 
        air_quality = pd.read_sql(query2, engine)

        return data,air_quality
    except Exception as e:
        st.error(f'Error: {e}')



# Query to get air quality (pollution data):
   
def get_pollution_data_for_all_cities():

    try:
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        query3 = f"""
                SELECT location, AVG(co) AS avg_co, AVG(no2) AS avg_no2, AVG(o3) AS avg_o3
                FROM student.weather
                GROUP BY location
                """
        pollution_data_cities = pd.read_sql(query3, engine)
        return pollution_data_cities
    except Exception as e:
        st.error(f'Error: {e}')



# Graphs:

def main():
    data, air_quality = get_data(selected_city)
    pollution_data_cities = get_pollution_data_for_all_cities()
    if tab =='Weather':
    # Calculating average temperature and plot the line chart using Matplotlib
        daily_average_temp = data.groupby('date')['temperature'].mean()

        plt.figure(figsize=(10, 6))
        plt.plot(daily_average_temp.index, daily_average_temp.values, marker='o', linestyle='-')
        plt.xlabel('Date')
        plt.ylabel('Average Temperature (°C)')
        plt.title(f'Average Temperature in {selected_city} over time')
        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(plt)
    # Plot the air quality data (pollution) for all cities to compare with eachother

    # Plot the air quality data (pollution) for city selected:
    elif tab =='Air Quality':
        fig, ax = plt.subplots(figsize=(8, 6))
        air_quality.set_index('date').plot(kind='bar', ax=ax)
        plt.xlabel('Date')
        plt.ylabel('Average Concentration')
        plt.title(f'Change in Pollution levels over time in {selected_city}')
        plt.xticks(rotation=0)
        plt.legend(loc='upper right')
        plt.tight_layout()

        st.pyplot(fig)

        if st.button('See all cities'):
        
            fig, ax = plt.subplots(figsize=(10, 6))
            pollution_data_cities.plot(kind='bar', x='location', ax=ax)
            plt.xlabel('City')
            plt.ylabel('Average Concentration')
            plt.title('Pollutant Comparison for All Cities')
            plt.xticks(rotation=45)
            plt.legend(loc='upper right')
            plt.tight_layout()

            st.pyplot(fig) 
    else:
        st.error("Failed to get data.")

#data, air_quality, air_quality_all_cities = get_data(selected_city)

main()




