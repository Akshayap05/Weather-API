import streamlit as st
from streamlit_folium import folium_static
from sqlalchemy import create_engine
import requests
import numpy as np
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap

st.title('Welcome to our Weather App')
st.write("**Select a city from the side bar to explore its weather.**")


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

cities = ['London', 'Manchester', 'Birmingham', 'Glasgow', 'Leeds', 'Liverpool', 'Sheffield', 'Bristol', 'Edinburgh', 'Leicester',  'York', 'Cardiff', 'Brighton', 'Coventry', 'Bath']
selected_city = st.selectbox('Select a city', cities)

weather_data = temperature, latitude, longitude ,condition, icon, humidity, Cloud_cover, UV_index, CO, NO2, Ozone = get_details(selected_city)

tab = st.radio("Select Tab", ["Weather", "Air Quality"], index=0)


# Position the informaiton and the image on page:

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

# Display weather condition icon in the right column
with right_hand_col:
    if weather_data:
        icon_url = "https:" + icon
        st.image(icon_url, caption='Weather Condition', use_column_width=True)


#connect to db:
# Fetch database credentials from secrets
db_user = st.secrets["DB_USER"]
db_password = st.secrets["DB_PASSWORD"]
db_host = st.secrets["DB_HOSTS"]
db_name = st.secrets["DB_NAME"]
db_port = st.secrets["DB_PORT"]


# Retrieve data from the database

def get_data(selected_city):
    engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    query = f"""
            SELECT DISTINCT to_char(date, 'YYYY-MM-DD') AS date, location, temperature, co, no2, o3 
            FROM student.weather 
            WHERE location='{selected_city}' 
            ORDER BY date ASC
            """
    data = pd.read_sql(query, engine)
    return data

# Fetch weather data from the database
data = get_data(selected_city)

# Fetch data from the database
def main():
    if tab =='Weather':
    # Calculate average temperature of each day in the date
        daily_average_temp = data.groupby('date')['temperature'].mean()

    # Plot the line chart using Matplotlib
        plt.figure(figsize=(10, 6))
        plt.plot(daily_average_temp.index, daily_average_temp.values, marker='o', linestyle='-')
        plt.xlabel('Date')
        plt.ylabel('Average Temperature (°C)')
        plt.title(f'Average Temperature in {selected_city} over time')
        plt.xticks(rotation=45)
        plt.tight_layout()

    # Display the line plot in Streamlit
        st.pyplot(plt)
main()

# Plot bar chart for each pollutant
if tab =='Air Quality':
    fig, ax = plt.subplots(figsize=(10, 6))
    data.plot(kind='bar', x='location', ax=ax)
    plt.xlabel('Pollutant')
    plt.ylabel('Concentration')
    plt.title('Air Quality Comparison')
    plt.xticks(rotation=0)
    plt.legend(loc='upper right')
    plt.tight_layout()

    # Display the plot
    st.pyplot(fig)
    





    