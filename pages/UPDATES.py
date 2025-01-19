import pandas as pd 
import streamlit as st 

from datetime import datetime 

import streamlit as st
import streamlit.components.v1 as components

# HTML/JavaScript component for getting browser geolocation
geolocation_html = """
<script>
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    document.getElementById("output").value = `${lat},${lon}`;
    // Send the location to Streamlit
    const data = { lat: lat, lon: lon };
    window.parent.postMessage({ type: 'geolocation', data: data }, '*');
}

function showError(error) {
    alert("Error retrieving geolocation.");
}

getLocation();
</script>
<input id="output" type="text" readonly>
"""

# Function to handle message from JS
def on_message(event):
    if event['type'] == 'geolocation':
        lat, lon = event['data']['lat'], event['data']['lon']
        st.session_state.latitude = lat
        st.session_state.longitude = lon

# Render the HTML/JS component
components.html(geolocation_html)

# Listen for the geolocation data in Streamlit
if 'latitude' in st.session_state and 'longitude' in st.session_state:
    st.write('HELLO')
    st.write(f"Latitude: {st.session_state.latitude}, Longitude: {st.session_state.longitude}")
