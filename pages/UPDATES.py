import streamlit as st
import streamlit.components.v1 as components

# Create a button for the user to get their location
if st.button('Get My Location'):
    # Embed JavaScript to get location when the button is clicked
    components.html("""
        <script>
            function getLocation() {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        function(position) {
                            const latitude = position.coords.latitude;
                            const longitude = position.coords.longitude;
                            // Store the coordinates in the window's session storage
                            window.sessionStorage.setItem("lat", latitude);
                            window.sessionStorage.setItem("long", longitude);

                            // Send the coordinates back to Streamlit using postMessage
                            window.parent.postMessage({latitude: latitude, longitude: longitude}, "*");
                        },
                        function(error) {
                            alert("Error: " + error.message);
                        }
                    );
                } else {
                    alert("Geolocation is not supported by this browser.");
                }
            }
            getLocation();
        </script>
    """, height=0)
    
    # Wait for the location data
    st.write("Fetching location...")

else:
    st.write("Click the button to get your location.")

# To get the location data, retrieve from session state
if 'lat' in st.session_state and 'long' in st.session_state:
    lat = st.session_state['lat']
    long = st.session_state['long']
    st.write(f"Latitude: {lat}")
    st.write(f"Longitude: {long}")
else:
    st.write("Waiting for location data...")
