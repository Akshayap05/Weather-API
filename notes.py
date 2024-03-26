import streamlit as st
from sqlalchemy import create_engine
import requests
import numpy as np
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(page_title="Welcome to our Weather App", page_icon="🌎")
st.title('Welcome to our Weather App')
st.write("**Select a city from the dropdown box to explore its weather.**")

# Get weather data from API and different cities:

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

# All the cities 
    
cities = ['London', 'Manchester', 'Birmingham', 'Glasgow', 'Leeds', 'Liverpool', 'Sheffield', 'Bristol', 'Edinburgh', 'Leicester',  'York', 'Cardiff', 'Brighton', 'Coventry', 'Bath']

st.sidebar.image('logo.png', width = 10, use_column_width=True, use_container_width=True)
selected_city = st.sidebar.selectbox('Choose a city', cities)


weather_data = temperature, latitude, longitude ,condition, icon, humidity, Cloud_cover, UV_index, CO, NO2, Ozone = get_details(selected_city)

tab = st.sidebar.radio("Select Tab", ["Weather", "Air Quality"], index=0)


# Position the informaiton and image on the page:

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

# Display weather condition icon in the right column:
    
with right_hand_col:
    if weather_data:
        icon_url = "https:" + icon
        st.image(icon_url, caption='Weather Condition', use_column_width=True)


# Connect to db:
# Get database security and authorisation information from secrets.toml:
        
db_user = st.secrets["DB_USER"]
db_password = st.secrets["DB_PASSWORD"]
db_host = st.secrets["DB_HOSTS"]
db_name = st.secrets["DB_NAME"]
db_port = st.secrets["DB_PORT"]


# Connect to Database and retrieve data from weather table using query:

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

# Get weather data from the database for all cities in selected_city

data = get_data(selected_city)

# Plot average temperature of each day as a line graph:

def main():
    if tab =='Weather':
    # Calculating average temperature:
        daily_average_temp = data.groupby('date')['temperature'].mean()

    # Plot the line chart using Matplotlib
        plt.figure(figsize=(10, 6))
        plt.plot(daily_average_temp.index, daily_average_temp.values, marker='o', linestyle='-')
        plt.xlabel('Date')
        plt.ylabel('Average Temperature (°C)')
        plt.title(f'Average Temperature in {selected_city} over time')
        plt.xticks(rotation=45)
        plt.tight_layout()

    # Display the line plot in Streamlit:
        st.pyplot(plt)
main()

# Plot bar graph of air quality data (co,no2, o3):

def air_quality(selected_city):
    engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    query = f"""
            SELECT location, AVG(co) AS avg_co, AVG(no2) AS avg_no2, AVG(o3) AS avg_o3
            FROM student.weather
            WHERE location = '{selected_city}'
            GROUP BY location
            """
    air_quality = pd.read_sql(query, engine)
    return air_quality

# Get air quality data for the selected city:

pollution_dat = air_quality(selected_city)

# Display the air quality data for the selected city

if tab =='Air Quality':
    fig, ax = plt.subplots(figsize=(8, 6))
    pollution_dat.set_index('location').plot(kind='bar', ax=ax)
    plt.xlabel('Pollutant')
    plt.ylabel('Average Concentration')
    plt.title(f'Pollutant Concentration in {selected_city}')
    plt.xticks(rotation=0)
    plt.legend(loc='upper right')
    plt.tight_layout()

    st.pyplot(fig)

# To make comparison bar graph:

# Query to get air quality (pollution data):
    
def get_pollution_data_for_all_cities():
    engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    query = """
            SELECT location, AVG(co) AS avg_co, AVG(no2) AS avg_no2, AVG(o3) AS avg_o3
            FROM student.weather
            GROUP BY location
            """
    pollution_data_cities = pd.read_sql(query, engine)
    return pollution_data_cities

    # Fetch the pollutant data for all cities
pollution_data_cities = get_pollution_data_for_all_cities()


if st.button('See all cities'):
# Plot the air quality data (pollution) for all cities to compare with eachother    
    fig, ax = plt.subplots(figsize=(10, 6))
    pollution_data_cities.plot(kind='bar', x='location', ax=ax)
    plt.xlabel('City')
    plt.ylabel('Average Concentration')
    plt.title('Pollutant Comparison for All Cities')
    plt.xticks(rotation=45)
    plt.legend(loc='upper right')
    plt.tight_layout()

    st.pyplot(fig)






    