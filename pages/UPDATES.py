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
import streamlit.components.v1 as components

# JavaScript code to get user's location
geo_location_js = """
<script>
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            window.parent.postMessage({
                lat: position.coords.latitude,
                long: position.coords.longitude
            }, "*");
        }, function() {
            alert("Geolocation is not supported by this browser.");
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
</script>
"""

# Embed JavaScript into the app
components.html(geo_location_js, height=0, width=0)

# Function to capture latitude and longitude
def get_location():
    lat = None
    long = None
    
    # JavaScript posts the location to the parent window (Streamlit app)
    st.session_state.lat = lat
    st.session_state.long = long

    return lat, long

# Trigger location capture and display
if st.button('Get Location'):
    lat, long = get_location()
    if lat and long:
        st.write(f'Latitude: {lat}, Longitude: {long}')
    else:
        st.write("Location not available.")
