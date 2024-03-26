import streamlit as st
from sqlalchemy import create_engine
import requests
import numpy as np
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Page Look:

st.set_page_config(page_title="Welcome to our Weather App", page_icon="🌎")
st.title('Welcome to our Weather App')
st.write("**Select a city from the dropdown box to explore its weather.**")


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

st.sidebar.image('logo.png', width = 100)
cities = ['London', 'Manchester', 'Birmingham', 'Glasgow', 'Leeds', 'Liverpool', 'Sheffield', 'Bristol', 'Edinburgh', 'Leicester',  'York', 'Cardiff', 'Brighton', 'Coventry', 'Bath']
selected_city = st.sidebar.selectbox('Choose a city', cities)
tab = st.sidebar.radio("Select Tab", ["Weather", "Air Quality"], index=0)

weather_data = temperature, latitude, longitude ,condition, icon, humidity, Cloud_cover, UV_index, CO, NO2, Ozone = get_details(selected_city)


# Add and position text to homepage using left column:

left_col, right_col, right_hand_col = st.columns([15, 2, 8])

if tab == "Weather":
    with left_col:
        st.markdown(f"<h2>{selected_city} Weather:</h2>", unsafe_allow_html=True)
        st.write(f"Temperature: {temperature}°C")
        st.write(f"Condition: {condition}")
        st.write(f"Humidity: {humidity}%")
        st.write(f"Cloud Cover: {Cloud_cover}%")
elif tab == "Air Quality":
    with left_col:
        st.markdown(f"<h2>{selected_city} Air Quality:</h2>", unsafe_allow_html=True)
        st.write(f"UV Index: {UV_index}")
        st.write(f"CO: {CO}")
        st.write(f"NO2: {NO2}")
        st.write(f"Ozone (O3): {Ozone}")    
else:
    st.error("Failed to get data.")

# Add and position image/icon to homepage using right column:
    
with right_hand_col:
    if weather_data:
        icon_url = "https:" + icon
        st.image(icon_url, caption='Weather Condition', use_column_width=True)


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
                SELECT location, AVG(co) AS avg_co, AVG(no2) AS avg_no2, AVG(o3) AS avg_o3
                FROM student.weather
                WHERE location = '{selected_city}'
                GROUP BY location""" 
        air_quality = pd.read_sql(query2, engine)

        return data,air_quality
    except Exception as e:
        st.error(f'Error: {e}')


data = get_data(selected_city)
air_quality = get_data(selected_city)

# Query to get air quality (pollution data):
    
def get_pollution_data_for_all_cities():
    engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    query3 = """
            SELECT location, AVG(co) AS avg_co, AVG(no2) AS avg_no2, AVG(o3) AS avg_o3
            FROM student.weather
            GROUP BY location
            """
    pollution_data_cities = pd.read_sql(query3, engine)
    return pollution_data_cities

    # Fetch the pollutant data for all cities
pollution_data_cities = get_pollution_data_for_all_cities()

# Graphs:

def main():
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
    # Plot the air quality data (pollution) for city selected:
    elif tab =='Air Quality':
        fig, ax = plt.subplots(figsize=(8, 6))
        air_quality.set_index('location').plot(kind='bar', ax=ax)
        plt.xlabel('Pollutant')
        plt.ylabel('Average Concentration')
        plt.title(f'Pollutant Concentration in {selected_city}')
        plt.xticks(rotation=0)
        plt.legend(loc='upper right')
        plt.tight_layout()

        st.pyplot(fig)
    else:
        st.error("Failed to get data.")

#data, air_quality, air_quality_all_cities = get_data(selected_city)

main()
