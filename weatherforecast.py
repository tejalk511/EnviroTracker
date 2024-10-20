import os
from urllib import request
import pytz
import pyowm
import streamlit as st
from matplotlib import dates
from datetime import datetime, timezone
from matplotlib import pyplot as plt
import requests
from geopy.geocoders import Nominatim  #to plot map
import pandas as pd
import folium #to color map
from streamlit_folium import st_folium #map coloring
from streamlit_folium import folium_static


#st.set_page_config(layout="wide")

# List of cities with country names
cities = [
    "","New York, US", "Los Angeles, US", "London, GB", "Paris, FR", 
    "Berlin, DE", "Mumbai, IN", "Tokyo, JP", "Sydney, AU", 
    "Toronto, CA", "Cape Town, ZA", "Mumbai, India", "Kochi, India", "Bangalore, India"
]


def get_weather_data(city):
    api_key = 'a5d497b1c4b15ff85d36d4a95775e16c'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    #response = requests.get(url)
    #return response.json()
    response = requests.get(url)
    data = response.json()
    return data

def get_weather_5_days(city_name):
    api_key = 'a5d497b1c4b15ff85d36d4a95775e16c'  # Replace with your actual API key
    city = city_name.split(",")[0]  # Extract the city name from the dropdown selection
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    data = response.json()
    return data


def get_location(city_name):
    try:
        # Initialize the geocoder with a custom User-Agent
        geolocator = Nominatim(user_agent="WeatherWiseApp")
        
        # Geocode the city
        location = geolocator.geocode(city_name, timeout=10)
        
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        st.error("Geocoding request timed out. Please try again.")
        return None, None

# CSS for bordered columns (5-day weather forecast)
st.markdown("""
    <style>
    .forecast-container {
        display: flex;
        justify-content: space-around;
        gap: 20px;
    }
    .forecast-box {
        flex: 0 0 200px;  /* Fixed width for each forecast box */
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Optional shadow */
    }
    .forecast-box h4 {
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)


st.title("5 Day Weather Forecast")

with st.form("weather_form"):
    #city = st.text_input("Enter city name")
    #submit_button = st.form_submit_button(label="Submit")
    #Input of day
    col1, col2, colsumbit = st.columns(3)

    with col1:
        city=st.selectbox("NAME OF THE CITY :", cities)
        if city == None:
            st.write("Input a CITY!")

    with col2:
        unit=st.selectbox("Select Temperature Unit",("Celsius","Fahrenheit"))

    with colsumbit:
        st.write(" ")
        submit_button = st.form_submit_button(label="Submit")



#Displaying current temperature and graph
col3, col4 = st.columns(2)

# When the user submits the for
if submit_button:
    if city:
        data = get_weather_data(city)
        if data.get("cod") != 200:
                st.error(f"Error: {data.get('message', 'City not found')}")
        else:
            with col3:
                st.write(f"### Temperature in {city}")
    #st.image("https://static.streamlit.io/examples/cat.jpg")     
            
                current_temp = data['main']['temp']
                min_temp = data['main']['temp_min']
                max_temp = data['main']['temp_max']
                cloud_coverage = data['clouds']['all']
                #sunrise = datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%Y-%m-%d %H:%M:%S')
                #sunset = datetime.utcfromtimestamp(data['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S')
                sunrise = datetime.fromtimestamp(data['sys']['sunrise'], timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                sunset = datetime.fromtimestamp(data['sys']['sunset'], timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                
                # Example for forecast data
                #date = datetime.fromtimestamp(forecast['dt'], timezone.utc).strftime('%A')

                # Displaying weather information
                #st.write(f"### Weather in {city}")
                st.title(f"{current_temp}°C")
                st.write(f"**Min - Max temperature**: {min_temp}°C - {max_temp}°C")
                #st.write(f"**Max temperature**: {max_temp}°C")
                st.write(f"**Cloud coverage**: {cloud_coverage}%")
                st.write(f"**Sunrise**: {sunrise} UTC")
                st.write(f"**Sunset**: {sunset} UTC")
        

            with col4:
                # Fetching city coordinates
                #latitude, longitude = get_city_coordinates(city)
                #if latitude and longitude:
                #    st.write(f"**Map of {city}**")
                #    df = pd.DataFrame({
                #        'lat': [latitude],
                #        'lon': [longitude]
                #    })
                #    st.map(df)
                #else:
                #    st.write("City not found on map!")
                
                lat, lon = get_location(city)
                if lat and lon:
                    #st.success(f"Coordinates for {city}: Latitude = {lat}, Longitude = {lon}")
                    st.write(f"**{city}**")
                    #df = pd.DataFrame({'lat': [lat], 'lon': [lon]})
                    #map_center = [lat, lon]
                    m = folium.Map(location=[lat, lon], zoom_start=10, titles='cartodb positron')
                    folium.Marker( location=[lat, lon], popup=f"{city}: {current_temp}°C", icon=folium.Icon(color='blue', icon='info-sign')).add_to(m)
                    # Display the map in a separate column
                    #st_folium(m, width=700, height=500)
                    folium_static(m, width=500, height=300)
                else:
                    st.error(f"Could not retrieve the location for {city}. Please try a different city.")

#displaying respective graph - 
#col8 = st.column(1)

#with col8:
#   st.header("Graph of Temperature | Percipitation | Wind")


            data_5_days = get_weather_5_days(city)
            forecast_data = data_5_days['list'][::8] 
            
            st.markdown('<div class="forecast-container">', unsafe_allow_html=True)
            
            #Display of 5 Day temperature
            col8, col9, col10, col11, col12 = st.columns(5)

            columns  = [col8, col9, col10, col11, col12]
            for i, col in enumerate(columns):
                forecast = forecast_data[i]
                #date = datetime.utcfromtimestamp(forecast['dt']).strftime('%A')
                date1 = datetime.fromtimestamp(forecast['dt'], tz=timezone.utc).strftime('%A')
                date2 = datetime.fromtimestamp(forecast['dt'], tz=timezone.utc).strftime('%Y-%m-%d')
                temp = forecast['main']['temp']
                weather = forecast['weather'][0]['description'].capitalize()
                #for extracting icon 
                icon_code = forecast['weather'][0]['icon']
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

                with col:
                    st.markdown(f"""

                    <div class='forecast-box' style="background-color: white; padding: 10px; border: 5px solid navy; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
                        <h9>{date1}</h9>
                        <h4>{temp}°C</h4>
                        <img src="http://openweathermap.org/img/wn/{icon_code}@2x.png" alt="Weather icon" style="width: 100px; height: 75px;" />
                        <p>{weather}</p>
                        <h8>{date2}</h8>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.error("Please enter a city name.")

