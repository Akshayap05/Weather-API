import streamlit as st
from sqlalchemy import create_engine
import requests
import numpy as np
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Page title, icon, and headings:

st.set_page_config(page_title="Explore the UK's Weather", page_icon="🌎")
st.title(f'🌦️UK Weather Explorer')
#st.write("**Select a city from the dropdown box to explore its weather.**")
st.markdown("<h6 style='text-align: left;'>First select a city to explore its weather</h6>", unsafe_allow_html=True)

#with open('style.css') as f:
#    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Get weather data from API for different cities:

def get_details(cities):
    
    try:
        url = f'http://api.weatherapi.com/v1/current.json?key=787a74aa607147a19bb222554241903&q={cities}&aqi=yes'
        response = requests.get(url)
        weather = response.json()
        temperature = weather['current']['temp_c']
        condition = weather['current']['condition']['text']
        humidity = weather['current']['humidity']
        local_time = weather['location']['localtime']
        date, time = local_time.split(' ')
        feels_like = weather['current']['feelslike_c']
        CO = weather['current']['air_quality']['co']
        NO2= weather['current']['air_quality']['no2']
        Ozone= weather['current']['air_quality']['o3']
        return temperature, condition, humidity, local_time, date, time, feels_like, CO, NO2, Ozone    
    except:
        return 'Error', np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN


# Sidebar: Select box.

cities = ['London', 'Manchester', 'Birmingham', 'Glasgow', 'Leeds', 'Liverpool', 'Sheffield', 'Bristol', 'Edinburgh', 'Leicester',  'York', 'Cardiff', 'Brighton', 'Coventry', 'Bath']
selected_city = st.sidebar.selectbox('Choose a city', cities)
tab = st.sidebar.radio("Select Tab", ["Weather", "Air Quality"], index=0)


# Display metrics with center alignment, colour, padding, margin adjusted:

weather_data = temperature, condition, humidity, local_time, date, time, feels_like, CO, NO2, Ozone = get_details(selected_city)

if tab == 'Weather':
    #temperature, humidity,condition = get_details(selected_city)
    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown("<div style='padding: 10% 3% 3% 3%;  background-color: #263c52;'><h6 style='text-align: center;'>Temperature:</h6></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='padding: 10% 3% 3% 3%; margin-bottom: 10px; background-color: #263c52;'><h3 style='text-align: center;'>{temperature}°C</h3></div>", unsafe_allow_html=True)

    with a2:
        st.markdown("<div style='padding: 10% 3% 3% 3%; background-color: #263c52;'><h6 style='text-align: center;'>Humidity:</h6></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='padding: 10% 3% 3% 3%; margin-bottom: 10px; background-color: #263c52;'><h3 style='text-align: center;'>{humidity}%</h3></div>", unsafe_allow_html=True)

    with a3:
        st.markdown("<div style='padding: 10% 3% 3% 3%; background-color: #263c52;'><h6 style='text-align: center;'>Condition:</h6></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='padding: 10% 3% 3% 3%; margin-bottom: 10px; background-color: #263c52;'><h3 style='text-align: center;'>{condition}</h4></div>", unsafe_allow_html=True)

    b1, b2 = st.columns(2)
    with b1:
        st.markdown("<div style='padding: 10% 3% 3% 3%; background-color: #657796;'><h6 style='text-align: center;'>Current Time:</h6></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='padding: 10% 3% 3% 3%; margin-bottom: 10px; background-color: #657796;'><h3 style='text-align: center;'>{time}</h4></div>", unsafe_allow_html=True)
    with b2:
        st.markdown("<div style='padding: 10% 3% 3% 3%; background-color: #657796;'><h6 style='text-align: center;'>Today feels like:</h6></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='padding: 10% 3% 3% 3%; margin-bottom: 10px; background-color: #657796;'><h3 style='text-align: center;'>{feels_like}°C</h3></div>", unsafe_allow_html=True)



if tab == 'Air Quality':
    #CO, NO2, Ozone = get_details(selected_city)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div style='padding: 10% 3% 3% 3%; background-color: #263c52;'><h6 style='text-align: center;' >CO:</h5></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='padding: 10% 3% 3% 3%; margin-bottom: 10px; background-color: #263c52;'><h3 style='text-align: center;'>{CO}</h3></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div style='padding: 10% 3% 3% 3%; background-color: #263c52;'><h6 style='text-align: center;'>NO2:</h5></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='padding: 10% 3% 3% 3%; margin-bottom: 10px; background-color: #263c52;'><h3 style='text-align: center;'>{NO2}</h3></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div style='padding: 10% 3% 3% 3%; background-color: #263c52;'><h6 style='text-align: center;'>Ozone (O3):</h5></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='padding: 10% 3% 3% 3%; margin-bottom: 10px; background-color: #263c52;'><h3 style='text-align: center;'>{Ozone}</h3></div>", unsafe_allow_html=True)


# Credentials to connect to database in pagila postgresql:
        
db_user = st.secrets["DB_USER"]
db_password = st.secrets["DB_PASSWORD"]
db_host = st.secrets["DB_HOSTS"]
db_name = st.secrets["DB_NAME"]
db_port = st.secrets["DB_PORT"]

# Connect to database, get weather details through table using query:

@st.cache#(allow_output_mutation=True)
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

@st.cache   
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




