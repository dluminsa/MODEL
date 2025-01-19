import streamlit as st
import streamlit.components.v1 as components
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate and access the Google Sheets API
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client

# Save coordinates to Google Sheets
def save_to_google_sheets(latitude, longitude):
    # Authenticate and get the Google Sheets client
    client = authenticate_google_sheets()

    # Open the Google Sheet by name or ID (replace with your own Google Sheet name or URL)
    sheet = client.open("GeolocationData").sheet1  # Ensure this is the name of your sheet
    
    # Append new coordinates to the sheet
    sheet.append_row([latitude, longitude])

# HTML/JavaScript component for getting browser geolocation and sending it to Python via postMessage
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

    // Create a JSON object to store lat and lon
    const geolocationData = {
        "latitude": lat,
        "longitude": lon
    };

    // Send the geolocation data to Streamlit (Python backend)
    window.parent.postMessage({ type: 'geolocation', data: geolocationData }, '*');
}

function showError(error) {
    alert("Error retrieving geolocation.");
}

getLocation();
</script>
"""

# Function to handle message from JavaScript in the Streamlit app
def handle_message(event):
    if event['type'] == 'geolocation':
        # Get latitude and longitude
        lat = event['data']['latitude']
        lon = event['data']['longitude']
        
        # Store the geolocation in session state
        st.session_state['geolocation'] = {"latitude": lat, "longitude": lon}
        st.success(f"Latitude: {lat}, Longitude: {lon}")

        # Save to Google Sheets
        save_to_google_sheets(lat, lon)

# Initialize session state if not already present
if 'geolocation' not in st.session_state:
    st.session_state['geolocation'] = {}

# Render the HTML/JS component in Streamlit
components.html(geolocation_html)
