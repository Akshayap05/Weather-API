import streamlit as st
import requests
import numpy as np
#import sqlalchemy
from sqlalchemy import create_engine
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

st.title('Welcome to our Weather App')
st.write("**Select a city from the side bar to explore its weather.**")


def get_details(cities):
    try:
        url = f'http://api.weatherapi.com/v1/current.json?key=787a74aa607147a19bb222554241903&q={cities}&aqi=yes'
        response = requests.get(url)
        weather = response.json()
        temperature = weather['current']['temp_c']
        condition = weather['current']['condition']['text']
        icon = weather['current']['condition']['icon']
        humidity = weather['current']['humidity']
        Cloud_cover= weather['current']['cloud']
        UV_index= weather['current']['uv']
        CO = weather['current']['air_quality']['co']
        NO2= weather['current']['air_quality']['no2']
        Ozone= weather['current']['air_quality']['o3']
        return temperature, condition, icon, humidity, Cloud_cover, UV_index, CO, NO2, Ozone
        
    except:
        return 'Error', np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN

cities = ['London', 'Manchester', 'Birmingham', 'Glasgow', 'Leeds', 'Liverpool', 'Sheffield', 'Bristol', 'Edinburgh', 'Leicester',  'York', 'Cardiff', 'Brighton', 'Coventry', 'Bath']
selected_city = st.sidebar.selectbox('Select a city', cities)

weather_data = temperature, condition, icon, humidity, Cloud_cover, UV_index, CO, NO2, Ozone = get_details(selected_city)

# Position the informaiton and the image on page:

left_col,  right_col, right_hand_col = st.columns([10,6, 4])

with left_col:

    if weather_data:
        st.title(f"{selected_city}")
        st.write(f"Temperature: {temperature}°C")
        st.write(f"Condition: {condition}")
        st.write(f"Humidity: {humidity}%")
        st.write(f"Cloud Cover: {Cloud_cover}%")
        st.write(f"UV Index: {UV_index}")
        st.write(f"CO: {CO}")
        st.write(f"NO2: {NO2}")
        st.write(F"Ozone (O3): {Ozone}")
    else:
        st.error("Failed to fetch weather data. Please try again later.")

with right_col:

    if weather_data:
        icon_url = "https:" + icon
        st.image(icon_url, caption='Weather Condition', use_column_width=True)
    
# Initialise connection to database:

dbname=st.secrets['DB_USER']
dbuser=st.secrets['DB_USER']
password=st.secrest['DB_PASSWORD']
host=st.secrets['DB_HOST']
port=st.secrets['DB_PORT']

def db_connect():
    try:
        engine = create_engine(f"postgresql://{dbuser}:{password}@{host}:{port}/{dbname}")
        query = f'SELECT * FROM weather'
        data = pd.read_sql(query, engine)
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def plot_temp(city_data):
    try:
        city_data['date'] = pd.to_datetime(city_data['date'])
        plt.figure(figsize=(10, 6))
        plt.plot(selected_city['date'], selected_city['temperature'], marker='o', linestyle='-')
        plt.title(f'Temperature Changes in {selected_city["city"].iloc[0]}')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
    except Exception as e:
        print(f"Error plotting graph: {e}")

city_weather_data = db_connect(selected_city)
if city_weather_data is not None:
    plot_temp(city_weather_data)
else:
    print("Failed to retrieve weather data for the specified city.")




 


