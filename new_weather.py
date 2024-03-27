import streamlit as st
from sqlalchemy import create_engine
import requests
import numpy as np
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Page Look:

st.set_page_config(page_title="Welcome to our Weather App", page_icon="🌎", layout="wide")
st.title('🌦️Welcome to our Weather App')
st.write("**Select a city from the dropdown box to explore its weather.**")

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
selected_city = st.selectbox('Choose a city', cities)
#tab = st.radio("Select Tab", ["Weather", "Air Quality"], index=0)

weather_data = temperature, latitude, longitude ,condition, icon, humidity, Cloud_cover, UV_index, CO, NO2, Ozone = get_details(selected_city)


# Add and position text to homepage using left column:

a1, a2, a3, a4 = st.columns(4)

a1, a2, a3, a4 = st.columns(4)

# Display metrics and image with center alignment
with a1:
    st.markdown("<h2 style='text-align: center;'>Temperature</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>{temperature}°C</p>", unsafe_allow_html=True)

with a2:
    st.markdown("<h2 style='text-align: center;'>Humidity</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>{humidity}%</p>", unsafe_allow_html=True)

with a3:
    st.markdown("<h2 style='text-align: center;'>Condition</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>{condition}</p>", unsafe_allow_html=True)

with a4:
    icon_url = "https:" + icon
    st.markdown("<h2 style='text-align: center;'/h2>", unsafe_allow_html=True)
    st.image(icon_url, use_column_width='False', output_format='auto')




