import streamlit as st
import streamlit.components.v1 as components

# Initialize session state for geolocation
if "geolocation" not in st.session_state:
    st.session_state.geolocation = "Waiting for geolocation data..."

# Function to update the geolocation state
def update_geolocation(data):
    st.session_state.geolocation = data

# HTML/JavaScript to get geolocation and update a hidden input field
geolocation_html = """
<script>
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        document.getElementById("geolocationData").value = "Geolocation is not supported by this browser.";
        Streamlit.setComponentValue(document.getElementById("geolocationData").value);
    }
}

function showPosition(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    const location = `${lat},${lon}`;
    document.getElementById("geolocationData").value = location;
    Streamlit.setComponentValue(document.getElementById("geolocationData").value);
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
    document.getElementById("geolocationData").value = message;
    Streamlit.setComponentValue(document.getElementById("geolocationData").value);
}

getLocation();
</script>
<input type="hidden" id="geolocationData" value="">
"""

# Inject the HTML/JavaScript into the Streamlit app
components.html(geolocation_html, height=200)

# Get the geolocation data from the hidden input field
geolocation = st.text_input("Geolocation Data", "", key="geolocation_data")

# Update session state if geolocation data is available
if geolocation:
    st.session_state.geolocation = geolocation

# Display the geolocation result
st.write(f"Location: {st.session_state.geolocation}")

st.write("Ensure your browser allows location access for this app.")
