import streamlit as st
import requests
import numpy as np
#import sqlalchemy
from sqlalchemy import create_engine
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

#def db_connect():
#    try:
#        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
#        query = f'SELECT * FROM weather' 
#        data = pd.read_sql(query, engine)
#        return data
#    except Exception as e:
#        st.error(f'Error: {e}')



# Connect to the database and fetch data
#weather_data = db_connect()

# Display the fetched data
#if weather_data is not None:
#    st.write(weather_data)
#else:
#    st.error("Failed to get weather data.")


def db_connect(selected_city):
    try:
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        query = f"SELECT date, temperature FROM weather WHERE location = '{selected_city}'"
        data = pd.read_sql(query, engine)
        return data
    except Exception as e:
        st.error(f'Error: {e}')

# Fetch data from the database
data = db_connect(selected_city)

# Ensure that the data DataFrame contains the necessary columns (date and temperature)
# Convert 'date' column to datetime format
data['date'] = pd.to_datetime(data['date'])

# Plot scatter plot with markers for temperature changes over time
if data is not None:
    fig, ax = plt.subplots()
    ax.scatter(data['date'], data['temperature'])
    ax.plot(data['date'], data['temperature'], linestyle='-', color='blue')  # Connect scatter points
    ax.set_title(f'Temperature changes in {selected_city} over time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature')
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.error("Failed to get weather data from the database.")



