import streamlit as st
import streamlit.components.v1 as components

# HTML/JavaScript component for getting browser geolocation
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

# Streamlit app logic
st.title("Precise Geolocation App")

# Create an empty container to display the location or errors
geolocation_container = st.empty()

# Inject the JavaScript into the app
components.html(geolocation_html, height=200)

# Use Streamlit's session state to capture location data
if "geolocation" not in st.session_state:
    st.session_state.geolocation = None

# JavaScript-to-Python communication listener
def js_listener():
    from streamlit.runtime.scriptrunner import RerunException, StopException
    import streamlit.runtime.runtime_util as util
    try:
        data = util.get_query_string_params().get('message')
        if data:
            st.session_state.geolocation = data
            raise RerunException()
    except StopException:
        pass

# Call the listener
js_listener()

# Add a callback to handle the geolocation data
if st.session_state.geolocation:
    geolocation_container.write(f"Location: {st.session_state.geolocation}")
else:
    geolocation_container.write("Waiting for geolocation data...")

st.write("Ensure your browser allows location access for this app.")
