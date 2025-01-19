import pandas as pd 
import streamlit as st 
import os
import requests
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

# HTML with JavaScript to capture geolocation
def get_user_location():
    location_script = """
    <script>
    // Function to get geolocation and send it back to Streamlit
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;
                    const data = JSON.stringify({latitude, longitude});
                    // Send the data back to Streamlit
                    document.getElementById("location-data").value = data;
                    document.getElementById("send-data").click();
                },
                function(error) {
                    console.error("Error getting location: ", error.message);
                    alert("Unable to retrieve your location. Please allow location access.");
                }
            );
        } else {
            alert("Geolocation is not supported by your browser.");
        }
    }
    </script>
    <button onclick="getLocation()">Get Location</button>
    <form action="#" method="get">
        <input type="hidden" id="location-data" name="location" />
        <button id="send-data" type="submit" style="display:none;"></button>
    </form>
    """
    components.html(location_script, height=100)

# Streamlit app
st.title("Real-Time Location Capture")
st.write("Click the button below to get your current location:")

# Call JavaScript to get the location
get_user_location()

# Capture the location sent back from JavaScript
query_params = st.query_params()
if "location" in query_params:
    location_data = query_params["location"][0]
    try:
        # Parse the latitude and longitude
        location = eval(location_data)
        latitude = location.get("latitude")
        longitude = location.get("longitude")
        st.success(f"Your location: Latitude {latitude}, Longitude {longitude}")
    except:
        st.error("Error retrieving location data.")
else:
    st.info("Your location will appear here after allowing access.")
