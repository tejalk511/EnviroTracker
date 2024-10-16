import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Rectangle


st.set_page_config(layout="wide")
# Function to fetch AQI from AirVisual API
def fetch_aqi(city, state, country, api_key):
    url = f"https://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        aqi = data['data']['current']['pollution']['aqius']  # AQI US
        return aqi
    else:
        st.error(f"Error retrieving data: {response.status_code} - {response.json().get('data', {}).get('message', 'Unknown error')}")
        return None

# Function to determine AQI category
def get_aqi_category(aqi):
    if aqi is None:
        return 0
    if aqi <= 50:
        return 1
    elif aqi <= 100:
        return 2
    elif aqi <= 150:
        return 3
    elif aqi <= 200:
        return 4
    elif aqi <= 300:
        return 5
    elif aqi <= 400:
        return 7
    else:
        return 7

#Adding Guage chart funtions and variables 
# Gauge chart colors and values
colors_ind = ["#ee4d55", "#f36d54", "#fabd57", "#f6ee54", "#c1da64", "#72c66e", '#4dab6d']
values = [500, 400, 300, 200, 150, 100, 50, 0]
x_axis_vals = [2.64, 2.2, 1.76, 1.32, 0.88, 0.44, 0]

# Function to create the gauge chart
def map_plot(ax):
  # Draw the bars
  ax.bar(x=[0, 0.44, 0.88, 1.32, 1.76, 2.2, 2.64], width=0.5, height=0.5, bottom=2,
        linewidth=3, edgecolor="white", color=colors_ind, align="edge")
  # Annotate the labels
  plt.annotate("Hazardous", xy=(0.1, 2.1), rotation=-75, color="black", fontweight="bold")
  plt.annotate("Hazardous", xy=(0.65, 1.95), rotation=-55, color="black", fontweight="bold")
  plt.annotate("Very Unhealthy", xy=(1.19, 1.9), rotation=-32, color="black", fontweight="bold")
  plt.annotate("Unhealthy", xy=(1.67, 2.2), color="black", fontweight="bold")
  plt.annotate("Unhealthy for", xy=(2.15, 2.32), rotation=20, color="black", fontweight="bold")
  plt.annotate("Sensitive Groups", xy=(2.2, 2.2), rotation=20, color="black", fontweight="bold")
  plt.annotate("Moderate", xy=(2.52, 2.25), rotation=45, color="black", fontweight="bold")
  plt.annotate("Good", xy=(2.95, 2.25), rotation=75, color="black", fontweight="bold")
  # Annotate the values
  for loc, val in zip([0, 0.44, 0.88, 1.32, 1.76, 2.2, 2.64], values):
      plt.annotate(val, xy=(loc, 2.5), ha="right" if val <= 20 else "left")


# Create a polar plot
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(projection="polar")




# Function to calculate angle and radius for the arrow
def degree_range(n):
    start = np.linspace(0, 180, n + 1, endpoint=True)[0:-1]
    end = np.linspace(0, 180, n + 1, endpoint=True)[1::]
    mid_points = start + ((end - start) / 2.0)
    return np.c_[start, end], mid_points

def gauge(labels=['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous'], arrow=1):
    # Number of labels
    N = len(labels)
    # Check if the arrow index is valid
    if arrow > N:
        raise Exception("\n\nThe category ({}) is greater than the length\nof the labels ({})".format(arrow, N))
    # Get the range of angles and mid-points for each label
    ang_range, mid_points = degree_range(N)

    # Calculate the position for the arrow (angle in degrees)
    pos = mid_points[abs(arrow - N)]

    # Return the polar coordinates: angle in radians and a fixed radius (for the arrow)
    return np.radians(pos), 2  # Angle in radians, radius (set to 2 here)


# Main Streamlit application
#st.title("Air Quality Index (AQI) Meter", align ="center")
st.markdown("<h1 style='text-align: center;'>Air Quality Index (AQI) Meter</h1>", unsafe_allow_html=True)


# AirVisual API key (replace with your actual key)
api_key = "25b292e2-5c8f-48c5-9712-d768fa61ae0a"

# Dropdown for selecting location
locations = {
    "": ["", ""],
    "Mumbai": ["Maharashtra", "India"],
    "Delhi": ["Delhi", "India"],
    "New York": ["New York", "USA"],
    "Los Angeles": ["California", "USA"],
    "Los Angeles": ["California", "USA"],
}

# Use a markdown to create a centered div for the form


with st.form("weather_form"):
    #city = st.text_input("Enter city name")
    #submit_button = st.form_submit_button(label="Submit")
    #Input of day
    col1, colsumbit = st.columns(2)

    with col1:
        selected_city = st.selectbox("Select a city", list(locations.keys()))
        if selected_city == None:
            st.write("Input a CITY!")

    with colsumbit:
        st.write(" ")
        submit_button = st.form_submit_button(label="Get AQI")

#dividing colution space into two columns
col2, col3 = st.columns(2)
# Button to fetch AQI data
if submit_button:
    if selected_city:
        state, country = locations[selected_city]
        # Fetch AQI data
        aqi_value = fetch_aqi(selected_city, state, country, api_key)
        # Get AQI category and color
        aqi_category = get_aqi_category(aqi_value)

        #plotting graph
        with col2:
            #fig = plt.figure(figsize=(10, 10), facecolor='none')  # Set figure background to transparent
            #ax = fig.add_subplot(projection="polar")
            map_plot(ax)  # Pass the ax here
            ax.set_facecolor('none') 
            #map_plot(ax)
            angle, radius = gauge(arrow=aqi_category)
            colors_ind2 = colors_ind[::-1]
            indication = colors_ind2[(aqi_category-1)]
            # Add the arrow annotation in polar coordinates
            ax.annotate(aqi_value, xy=(angle, radius), xytext=(0, 0),
                        arrowprops=dict(arrowstyle="wedge, tail_width=0.5", color="black", shrinkA=0),
                        bbox=dict(boxstyle="circle", facecolor=indication, linewidth=1.0, linestyle ="-."),
                        fontsize=30, color="black", ha="center"
                    )
            #plt.title("Performance Gauge Chart", loc="center", pad=20, fontsize=35, fontweight="bold")
            plt.tight_layout()
            ax.set_axis_off()  #to remove plotting
            st.pyplot(fig, clear_figure="True")
        # Display a message about air quality
        with col3:
            st.write(f"**Air Quality Status:** {aqi_value} indicating {aqi_category}")
    else:
        st.error("Please select a city.")
