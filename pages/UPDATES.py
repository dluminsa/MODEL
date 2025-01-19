import pandas as pd 
import streamlit as st 
import os
import gspread
from pathlib import Path
import random
import plotly.express as px
import plotly.graph_objects as go
import traceback
import geocoder
import time
from streamlit_gsheets import GSheetsConnection
from datetime import datetime 

st.set_page_config(
    page_title = 'NS TRACKER',
    page_icon =":bar_chart"
    )
import json
def get_location():
    try:
        # You can use any geolocation API. Here we're using ip-api as an example
        response = requests.get('http://ip-api.com/json')
        data = response.json()
        lat = data['lat']
        long = data['lon']
        return lat, long
    except Exception as e:
        st.error(f"Error retrieving location: {e}")
        return None, None

# Streamlit App Layout
st.title("Get Your Location")

# Button to fetch the location
if st.button("Get Location"):
    lat, long = get_location()
    
    if lat and long:
        st.session_state.lat = lat
        st.session_state.long = long
        st.write(f"Latitude: {lat}, Longitude: {long}")
    else:
        st.write("Location not available.")
