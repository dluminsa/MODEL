import pandas as pd 
import streamlit as st 

from datetime import datetime 

st.set_page_config(
    page_title = 'NS TRACKER',
    page_icon =":bar_chart"
    )
import json
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
}

function showError(error) {
    alert("Error retrieving geolocation.");
}

getLocation();
</script>
<input id="output" type="text" readonly>
"""

st.title("Precise Geolocation App")
st.components.v1.html(geolocation_html, height=100)

# Inform users about the accuracy
st.write("Note: Using browser geolocation provides more precise results compared to IP-based services.")
