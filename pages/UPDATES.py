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

# JavaScript code to get exact geolocation
get_location_script = """
<script>
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                // Pass latitude and longitude to Streamlit
                const streamlitLatitude = document.getElementById("latitude");
                const streamlitLongitude = document.getElementById("longitude");
                
                streamlitLatitude.value = latitude;
                streamlitLongitude.value = longitude;

                streamlitLatitude.dispatchEvent(new Event("input", { bubbles: true }));
                streamlitLongitude.dispatchEvent(new Event("input", { bubbles: true }));
            },
            (error) => {
                alert("Error getting location: " + error.message);
            }
        );
    } else {
        alert("Geolocation is not supported by your browser.");
    }
}
</script>
"""

# Add the JavaScript and hidden fields to the Streamlit app
st.markdown(get_location_script, unsafe_allow_html=True)
st.markdown('<input type="text" id="latitude" style="display:none;">', unsafe_allow_html=True)
st.markdown('<input type="text" id="longitude" style="display:none;">', unsafe_allow_html=True)

# Add a button to trigger the location prompt
if st.button("Get Location"):
    st.markdown('<script>getLocation();</script>', unsafe_allow_html=True)

# Capture latitude and longitude
lat = st.session_state.get("latitude", "")
long = st.session_state.get("longitude", "")

# Display latitude and longitude
if lat and long:
    st.write(f"Latitude: {lat}")
    st.write(f"Longitude: {long}")
else:
    st.info("Click 'Get Location' and allow location access in your browser.")
