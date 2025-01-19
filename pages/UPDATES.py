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

# JavaScript code to capture geolocation
get_location_script = """
<script>
    // Function to get the geolocation data
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;
                    
                    // Updating Streamlit hidden input fields with lat and long values
                    document.getElementById("latitude").value = latitude;
                    document.getElementById("longitude").value = longitude;

                    // Trigger input event to send data to Streamlit
                    document.getElementById("latitude").dispatchEvent(new Event("input", { bubbles: true }));
                    document.getElementById("longitude").dispatchEvent(new Event("input", { bubbles: true }));
                },
                (error) => {
                    alert("Unable to retrieve your location. Please allow location access in your browser.");
                }
            );
        } else {
            alert("Geolocation is not supported by your browser.");
        }
    }

    // Call the function on button click
    getLocation();
</script>
"""

# Streamlit layout and display
st.title("Field Member LocationOO App")
st.write("Please click the button to capture your location.")

# Hidden input fields to store latitude and longitude
st.markdown('<input type="text" id="latitude" style="display:none;">', unsafe_allow_html=True)
st.markdown('<input type="text" id="longitude" style="display:none;">', unsafe_allow_html=True)

# Button to trigger the geolocation request
if st.button("Get Location"):
    # Embed the JavaScript that gets the location
    st.markdown(get_location_script, unsafe_allow_html=True)

# Display the latitude and longitude after they are fetched
lat = st.session_state.get("latitude", "")
long = st.session_state.get("longitude", "")

if lat and long:
    st.write(f"Latitude: {lat}")
    st.write(f"Longitude: {long}")
else:
    st.info("Click 'Get Location' and allow location access in your browser.")
