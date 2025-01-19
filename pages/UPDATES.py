import streamlit as st

# JavaScript code to capture coordinates and store them in session state
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
    // Send the coordinates back to Streamlit via the session state
    const event = new CustomEvent('coordinates_event', {
        detail: {latitude: lat, longitude: lon}
    });
    window.dispatchEvent(event);
}

function showError(error) {
    alert("Error retrieving geolocation: " + error.message);
}

// Trigger geolocation prompt when the page loads
getLocation();
</script>
"""

# Streamlit interface
st.title("Enable Location to Save Coordinates")

# Display a message for the user
st.write("We will capture and save your coordinates when you allow location access.")

# Store coordinates in session state if not already set
if "coordinates" not in st.session_state:
    st.session_state.coordinates = None

# Listen for coordinates event from JavaScript
def save_coordinates(event):
    # Save the coordinates in session state when the event is triggered
    st.session_state.coordinates = event.detail
    st.write(f"Coordinates saved: {st.session_state.coordinates}")

# Add an event listener in JavaScript to trigger the Python function
st.components.v1.html(geolocation_html, height=200)

# Output saved coordinates
if st.session_state.coordinates:
    st.write(f"Saved coordinates: Latitude = {st.session_state.coordinates['latitude']}, Longitude = {st.session_state.coordinates['longitude']}")
else:
    st.write("Waiting for coordinates...")
