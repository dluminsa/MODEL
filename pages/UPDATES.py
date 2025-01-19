import streamlit as st

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
    // Send coordinates to Python using JavaScript's postMessage API
    window.parent.postMessage({ latitude: lat, longitude: lon }, '*'); 
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

# Receive coordinates from JavaScript
lat = None
lon = None

def receive_coordinates(message):
    global lat, lon
    if "latitude" in message.data:
        lat = message.data["latitude"]
        lon = message.data["longitude"]

st.session_state.receive_coordinates = receive_coordinates

st.write("Note: Using browser geolocation provides more precise results compared to IP-based services.")

# Display coordinates in Python
if lat and lon:
    st.write(f"Latitude: {lat}")
    st.write(f"Longitude: {lon}") 
