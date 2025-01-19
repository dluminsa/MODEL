import streamlit as st
import streamlit.components.v1 as components
import json

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
        
        # Store the geolocation in session state (you could also write it to a file if needed)
        st.session_state['geolocation'] = {"latitude": lat, "longitude": lon}
        st.success(f"Latitude: {lat}, Longitude: {lon}")
        
        # Optionally, save to a JSON file
        with open('geolocation_data.json', 'w') as json_file:
            json.dump({"latitude": lat, "longitude": lon}, json_file)

# Initialize session state if not already present
if 'geolocation' not in st.session_state:
    st.session_state['geolocation'] = {}

# Render the HTML/JS component in Streamlit
components.html(geolocation_html)

# Display stored geolocation data if it exists
if 'geolocation' in st.session_state and st.session_state['geolocation']:
    geolocation = st.session_state['geolocation']
    st.write(f"Stored Latitude: {geolocation['latitude']}, Longitude: {geolocation['longitude']}")
