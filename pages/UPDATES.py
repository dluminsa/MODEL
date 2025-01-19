import streamlit as st
import streamlit.components.v1 as components
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Function to authenticate and access Google Sheets
def authenticate_google_sheets():
    credentials = Credentials.from_service_account_file(
        'path/to/your/credentials.json', 
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service.spreadsheets()

# Function to update Google Sheet with Client ID and geolocation
def update_google_sheet(client_id, lat, lon):
    spreadsheet_id = 'YOUR_SPREADSHEET_ID'  # Replace with your Google Sheets ID
    range_ = 'Sheet1!A1'  # Adjust as needed
    
    values = [
        [client_id, lat, lon]
    ]
    
    body = {
        'values': values
    }
    
    service = authenticate_google_sheets()
    service.values().append(
        spreadsheetId=spreadsheet_id, range=range_,
        valueInputOption="RAW", body=body
    ).execute()

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
    // Send the location back to the parent window (Streamlit)
    window.parent.postMessage({ lat: lat, lon: lon }, "*");
}

function showError(error) {
    alert("Error retrieving geolocation.");
}

getLocation();
</script>
<input id="output" type="text" readonly>
"""

# Streamlit App
st.title("Precise Geolocation App")

# Client ID input
client_id = st.number_input("Enter Client ID", min_value=1)

# Display geolocation component
components.v1.html(geolocation_html, height=100)

# Inform users about the accuracy
st.write("Note: Using browser geolocation provides more precise results compared to IP-based services.")

# Use session_state to capture coordinates after user grants permission
if "location" not in st.session_state:
    st.session_state.location = None

# Message listener for geolocation data
def js_listener():
    if "location" in st.session_state and st.session_state.location:
        lat, lon = st.session_state.location
        st.write(f"Geolocation: Latitude: {lat}, Longitude: {lon}")
        
        # Update Google Sheets with Client ID and geolocation
        update_google_sheet(client_id, lat, lon)
        st.success("Location data successfully sent to Google Sheets.")
    else:
        st.write("Waiting for geolocation data...")

# Function to receive the coordinates from JavaScript
def receive_coordinates(event):
    if event.data:
        st.session_state.location = (event.data["lat"], event.data["lon"])
        js_listener()

# Listen for messages from the JavaScript component
st.components.v1.html("""
    <script>
        window.addEventListener('message', (event) => {
            // Check if we have geolocation data
            if (event.data.lat && event.data.lon) {
                window.parent.postMessage({ lat: event.data.lat, lon: event.data.lon }, "*");
            }
        });
    </script>
""", height=0)

# Run the listener to handle geolocation
st.query_params
