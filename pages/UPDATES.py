import streamlit as st
import streamlit.components.v1 as components

st.title("Get User's Location")

# Embed JavaScript to get location
components.html("""
    <script>
        // Function to get the user's location
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const latitude = position.coords.latitude;
                        const longitude = position.coords.longitude;

                        // Pass the data back to Streamlit
                        const data = {latitude: latitude, longitude: longitude};
                        window.parent.postMessage(JSON.stringify(data), "*");
                    },
                    (error) => {
                        console.error(error);
                    }
                );
            } else {
                console.log("Geolocation is not supported by this browser.");
            }
        }
        getLocation();
    </script>
""", height=0)

# Get location data from query params
location_data = st.query_params.get("location")
if location_data:
    # Assuming location_data is a JSON string that contains the coordinates
    location = eval(location_data[0])  # Convert string to dictionary
    st.write("Latitude:", location["latitude"])
    st.write("Longitude:", location["longitude"])
else:
    st.write("Waiting for location data...")
