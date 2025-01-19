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
    const iframe = window.parent.document.getElementsByTagName('iframe')[0];
    iframe.contentWindow.postMessage(location, "*");
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
    const iframe = window.parent.document.getElementsByTagName('iframe')[0];
    iframe.contentWindow.postMessage(message, "*");
}

getLocation();
</script>
"""

# Streamlit app logic
st.title("Precise Geolocation App")

# Initialize session state for geolocation
if "geolocation" not in st.session_state:
    st.session_state.geolocation = "Waiting for geolocation data..."

# JavaScript communication listener
def handle_message(msg):
    if msg.data:
        st.session_state.geolocation = msg.data

# Embed the HTML/JavaScript and enable message listening
components.html(
    f"""
    <script>
    {geolocation_html}
    window.addEventListener('message', (event) => {{
        const iframe = window.parent.document.getElementsByTagName('iframe')[0];
        iframe.contentWindow.postMessage(event.data, "*");
    }});
    </script>
    """,
    height=200,
)

# Display the result
st.write(st.session_state.geolocation)

st.write("Ensure your browser allows location access for this app.")
