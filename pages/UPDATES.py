import streamlit as st
import streamlit.components.v1 as components

# Initialize session state for geolocation
if "geolocation" not in st.session_state:
    st.session_state.geolocation = "Waiting for geolocation data..."

# Function to update the geolocation state
def update_geolocation(data):
    st.session_state.geolocation = data

# HTML/JavaScript to get geolocation
geolocation_html = """
<script>
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        window.parent.postMessage("Geolocation is not supported by this browser.", "*");
    }
}

function showPosition(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    const location = `${lat},${lon}`;
    window.parent.postMessage(location, "*");
}

function showError(error) {
    let message;
    switch (error.code) {
        case error.PERMISSION_DENIED:
            message = "User denied the request for Geolocation.";
            break;
        case error.POSITION_UNAVAILABLE:
            message = "Location information is unavailable.";
            break;
        case error.TIMEOUT:
            message = "The request to get user location timed out.";
            break;
        case error.UNKNOWN_ERROR:
            message = "An unknown error occurred.";
            break;
    }
    window.parent.postMessage(message, "*");
}

getLocation();
</script>
"""

# Inject the HTML/JavaScript into the Streamlit app
components.html(geolocation_html, height=200)

# Add a listener for the JavaScript postMessage
st.components.v1.html("""
<script>
window.addEventListener('message', function(event) {
    if (event.origin !== window.location.origin) {
        return; // Ignore the message if it's from an untrusted source
    }
    const geolocationData = event.data;
    // Send geolocation data back to Streamlit
    Streamlit.setComponentValue(geolocationData);
});
</script>
""", height=0)

# Get the geolocation data from the JS side and update Streamlit session state
if "geolocation" in st.session_state:
    st.write(f"Location: {st.session_state.geolocation}")
else:
    st.write("Waiting for geolocation data...")

st.write("Ensure your browser allows location access for this app.")
