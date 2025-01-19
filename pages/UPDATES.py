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

# JavaScript code for prompting location access
prompt_location_script = """
<script>
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                const locationData = { latitude, longitude };

                // Pass data back to Streamlit
                const streamlitLocationData = document.getElementById("location-data");
                streamlitLocationData.textContent = JSON.stringify(locationData);
                streamlitLocationData.dispatchEvent(new Event("input", { bubbles: true }));
            },
            (error) => {
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        alert("Location access denied. Please allow location access.");
                        break;
                    case error.POSITION_UNAVAILABLE:
                        alert("Location information is unavailable.");
                        break;
                    case error.TIMEOUT:
                        alert("The request to get your location timed out.");
                        break;
                    default:
                        alert("An unknown error occurred.");
                        break;
                }
            }
        );
    } else {
        alert("Geolocation is not supported by your browser.");
    }
}
</script>
"""

# Inject JavaScript and a hidden element for location data
st.markdown(prompt_location_script, unsafe_allow_html=True)
st.markdown('<div id="location-data" style="display:none;"></div>', unsafe_allow_html=True)

# Add a button to trigger the location prompt
if st.button("Get Location"):
    st.markdown('<script>getLocation();</script>', unsafe_allow_html=True)

# Display latitude and longitude
location_data = st.session_state.get("location_data")
if location_data:
    import json
    try:
        location = json.loads(location_data)
        lat = location.get("latitude")
        long = location.get("longitude")

        # Display latitude and longitude
        st.write(f"Latitude: {lat}")
        st.write(f"Longitude: {long}")
    except json.JSONDecodeError:
        st.error("Failed to decode location data.")
else:
    st.info("Waiting for location data... Click 'Get Location' to allow access.")
