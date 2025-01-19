import streamlit as st

# JavaScript code to trigger location access and capture coordinates
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
}

function showError(error) {
    alert("Error retrieving geolocation: " + error.message);
}

// Trigger geolocation prompt
getLocation();
</script>
<input id="output" type="text" readonly>
"""

# Streamlit interface
st.title("Enable Location to Capture Coordinatesss")

# Display message and JavaScript component to capture coordinates
st.write("Click the button below to enable location and get your coordinates.")
st.components.v1.html(geolocation_html, height=200)

# Inform the user
st.write("Note: Allow your browser to access location services.")
