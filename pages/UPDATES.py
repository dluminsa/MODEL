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
    // Use a more reliable method to communicate with the parent window
    const event = new Event('coordinates_received'); 
    event.detail = { latitude: lat, longitude: lon };
    window.dispatchEvent(event);
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

def receive_coordinates(event):
    global lat, lon
    if event.detail:
        lat = event.detail["latitude"]
        lon = event.detail["longitude"]

st.session_state.receive_coordinates = receive_coordinates

st.write("Note: Using browser geolocation provides more precise results compared to IP-based services.")

# Register the event listener
st.components.v1.html("""
<script>
window.addEventListener('coordinates_received', st.session_state.receive_coordinates);
</script>
""", height=0) 

# Display coordinates in Python
if lat and lon:
    st.write(f"Latitude: {lat}")
    st.write(f"Longitude: {lon}") 
