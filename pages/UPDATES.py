import streamlit as st
import streamlit.components.v1 as components

# Embed JavaScript to automatically get the user's location when the app loads
components.html("""
    <script>
        window.onload = function() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        // Capture latitude and longitude
                        const latitude = position.coords.latitude;
                        const longitude = position.coords.longitude;

                        // Store coordinates in session storage for later use
                        window.sessionStorage.setItem("latitude", latitude);
                        window.sessionStorage.setItem("longitude", longitude);

                        // Send coordinates back to Streamlit using postMessage
                        const locationData = {latitude: latitude, longitude: longitude};
                        window.parent.postMessage(locationData, "*");
                    },
                    function(error) {
                        alert("Error: " + error.message);
                    }
                );
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        };
    </script>
""", height=0)

# Retrieve coordinates from session state after getting them from JavaScript
if "latitude" in st.session_state and "longitude" in st.session_state:
    lat = st.session_state["latitude"]
    long = st.session_state["longitude"]
    st.write(f"Latitude: {lat}")
    st.write(f"Longitude: {long}")
else:
    st.write("Waiting for location data...")
