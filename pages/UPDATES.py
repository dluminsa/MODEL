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

# JavaScript code to get user's geolocation
geo_location_js = """
<script>
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            window.parent.postMessage({
                lat: position.coords.latitude,
                long: position.coords.longitude
            }, "*");
        }, function(error) {
            window.parent.postMessage({
                error: error.message
            }, "*");
        });
    } else {
        window.parent.postMessage({
            error: "Geolocation is not supported by this browser."
        }, "*");
    }
</script>
"""

# Embed JavaScript into the app
components.html(geo_location_js, height=0, width=0)

# Function to capture latitude and longitude
def get_location():
    lat = None
    long = None

    # Get values from JavaScript
    if "lat" in st.session_state and "long" in st.session_state:
        lat = st.session_state["lat"]
        long = st.session_state["long"]

    return lat, long

# Trigger location capture and display
if st.button("Get Location"):
    # Capture location
    st.session_state["lat"] = None
    st.session_state["long"] = None
    components.html(geo_location_js, height=0, width=0)  # Re-trigger JavaScript

    lat, long = get_location()
    if lat and long:
        st.write(f"Latitude: {lat}, Longitude: {long}")
    else:
        st.write("Location not available.")
