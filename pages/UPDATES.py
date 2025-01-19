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

get_location_script = """
<script>
const button = document.querySelector('button');

button.addEventListener("click", () => {
    navigator.geolocation.getCurrentPosition(position => {
        // Getting latitude and longitude from position object
        const { latitude, longitude } = position.coords;

        // Reverse geocoding using OpenStreetMap API
        const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`;

        fetch(url)
            .then(res => res.json())
            .then(data => {
                // Storing latitude and longitude in hidden inputs for Streamlit
                document.getElementById("latitude").value = latitude;
                document.getElementById("longitude").value = longitude;

                // Trigger input event to pass data to Streamlit
                document.getElementById("latitude").dispatchEvent(new Event("input", { bubbles: true }));
                document.getElementById("longitude").dispatchEvent(new Event("input", { bubbles: true }));
            })
            .catch(() => {
                console.log("Error fetching data from API");
            });
    });
});
</script>
"""

# Streamlit layout and display
st.title("Field Member Location App")
st.write("Please click the button to capture your location.")

# Hidden input fields to store latitude and longitude
st.markdown('<input type="text" id="latitude" style="display:none;">', unsafe_allow_html=True)
st.markdown('<input type="text" id="longitude" style="display:none;">', unsafe_allow_html=True)

# Button to trigger the geolocation request
if st.button("Get Location"):
    st.markdown(get_location_script, unsafe_allow_html=True)

# Display the latitude and longitude after they are fetched
lat = st.session_state.get("latitude", "")
long = st.session_state.get("longitude", "")

if lat and long:
    st.write(f"Latitude: {lat}")
    st.write(f"Longitude: {long}")
else:
    st.info("Click 'Get Location' and allow location access in your browser.")
