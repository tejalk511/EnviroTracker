import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

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

import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Rectangle
import os #imoprting for image

st.set_page_config(layout="wide")

# Print installed packages
st.write("Installed packages:")
os.system('pip freeze > installed_packages.txt')

# Read and display the installed packages
with open('installed_packages.txt', 'r') as f:
    installed_packages = f.read()
st.code(installed_packages)



#for top white space removal 
#end top white space removal


#sections = st.sidebar.toggle("Sections", value=True, key="use_sections")

nav = get_nav_from_toml("pages_sections.toml")

#st.logo("logo.png")

pg = st.navigation(nav)

#add_page_title(pg)

pg.run()
