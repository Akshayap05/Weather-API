import streamlit as st
import requests
import numpy as np
#import sqlalchemy
#from sqlalchemy import create_engine
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
#from dotenv import load_dotenv
#import os

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
        st.error("Failed to get data.")

with right_col:

    if weather_data:
        icon_url = "https:" + icon
        st.image(icon_url, caption='Weather Condition', use_column_width=True)



#connect to db:
from sqlalchemy import create_engine        
  
db_user = st.secrets["DB_USER"]
db_password = st.secrets["DB_PASSWORD"]
db_hosts = st.secrets["DB_HOSTS"]
db_name = st.secrets["DB_NAME"]
db_port = st.secrets["DB_PORT"]

from sqlalchemy import create_engine
import streamlit as st
import pandas as pd

# Fetch database credentials from secrets
db_user = st.secrets["DB_USER"]
db_password = st.secrets["DB_PASSWORD"]
db_host = st.secrets["DB_HOSTS"]
db_name = st.secrets["DB_NAME"]
db_port = st.secrets["DB_PORT"]

import psycopg2

# Define a function to connect to the database
def connect_to_database():
    try:
        connection = psycopg2.connect(
            dbname="db_user",
            user="db_password",
            password="db_host",
            host="db_name",
            port="db_port"
        )
        return connection
    except psycopg2.Error as e:
        print("Unable to connect to the database.")
        print(e)
        return None

# Define a function to fetch weather data from the database
def fetch_weather_data(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT timestamp, temperature FROM weather_data ORDER BY timestamp")
        weather_data = cursor.fetchall()
        cursor.close()
        return weather_data
    except psycopg2.Error as e:
        print("Error fetching weather data from the database.")
        print(e)
        return None

# Define a function to organize weather data by day
def organize_by_day(weather_data):
    organized_data = {}
    for timestamp, temperature in weather_data:
        day = timestamp.date()
        if day not in organized_data:
            organized_data[day] = []
        organized_data[day].append((timestamp, temperature))
    return organized_data

# Define a function to plot weather data for each day
def plot_weather_data(organized_data):
    for day, data in organized_data.items():
        timestamps, temperatures = zip(*data)
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, temperatures, marker='o', linestyle='-')
        plt.title(f"Weather Changes on {day}")
        plt.xlabel("Time")
        plt.ylabel("Temperature (°C)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

# Define the main function to execute the script
def main():
    # Connect to the database
    connection = connect_to_database()
    if connection is not None:
        # Fetch weather data
        weather_data = fetch_weather_data(connection)
        if weather_data is not None:
            # Organize weather data by day
            organized_data = organize_by_day(weather_data)
            # Plot weather data for each day
            plot_weather_data(organized_data)
        # Close the database connection
        connection.close()
    else:
        print("Exiting script.")

# Execute the main function when the script is run
if __name__ == "__main__":
    main()