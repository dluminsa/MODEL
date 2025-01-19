import streamlit as st
import streamlit.components.v1 as components

# Button to trigger location retrieval
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
                            // Display the coordinates in the Streamlit app
                            alert("Latitude: " + latitude + "\nLongitude: " + longitude);
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
else:
    st.write("Click the button to get your location.")
