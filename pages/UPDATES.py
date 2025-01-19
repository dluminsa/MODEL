import streamlit as st
import streamlit.components.v1 as components
import gspread
from google.oauth2.service_account import Credentials

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

    // Send the location back to Streamlit using postMessage
    window.parent.postMessage({ lat: lat, lon: lon }, "*");
}

function showError(error) {
    alert("Error retrieving geolocation: " + error.message);
}

getLocation();
</script>
"""

# Streamlit app
st.title("Precise Geolocation App")

# Display geolocation component
components.html(geolocation_html, height=100)

# Initialize session state for location
if "location" not in st.session_state:
    st.session_state.location = None

# JavaScript Listener for geolocation
geo_listener = """
<script>
window.addEventListener('message', (event) => {
    // Check if the message contains geolocation data
    if (event.data.lat && event.data.lon) {
        const location = { lat: event.data.lat, lon: event.data.lon };

        // Send the location data back to Streamlit via a form
        const streamlitForm = document.createElement("form");
        streamlitForm.method = "post";
        streamlitForm.action = "";

        const latInput = document.createElement("input");
        latInput.type = "hidden";
        latInput.name = "lat";
        latInput.value = location.lat;

        const lonInput = document.createElement("input");
        lonInput.type = "hidden";
        lonInput.name = "lon";
        lonInput.value = location.lon;

        streamlitForm.appendChild(latInput);
        streamlitForm.appendChild(lonInput);

        document.body.appendChild(streamlitForm);
        streamlitForm.submit();
    }
});
</script>
"""

components.html(geo_listener, height=0)

# Capture location from form data
query_params = st.query_params
if "lat" in query_params and "lon" in query_params:
    lat = query_params["lat"][0]
    lon = query_params["lon"][0]
    st.session_state.location = (lat, lon)

# Display the location
if st.session_state.location:
    st.write(f"Location: Latitude = {st.session_state.location[0]}, Longitude = {st.session_state.location[1]}")

# Add a button to use the location
if st.button("Use Location"):
    if st.session_state.location:
        st.success("Using the captured location for further processing.")
    else:
        st.warning("No location captured yet. Please allow geolocation access.")
