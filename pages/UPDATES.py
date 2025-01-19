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
    document.getElementById("output").value = `${lat},${lon}`;
    // Send the location back to the parent window (Streamlit)
    window.parent.postMessage({ lat: lat, lon: lon }, "*");
}

function showError(error) {
    alert("Error retrieving geolocation.");
}

getLocation();
</script>
<input id="output" type="text" readonly>
"""

# Streamlit App
st.title("Precise Geolocation App")

# Get Client ID input
client_id = st.number_input("Enter Client ID", min_value=1)

# Display geolocation component
components.html(geolocation_html, height=100)

# Inform users about the accuracy
st.write("Note: Using browser geolocation provides more precise results compared to IP-based services.")

# Use session state to capture coordinates after user grants permission
if "location" not in st.session_state:
    st.session_state.location = None

# Credentials setup from secrets
secrets = st.secrets["connections"]["gsheets"]

# Prepare the credentials dictionary
credentials_info = {
    "type": secrets["type"],
    "project_id": secrets["project_id"],
    "private_key_id": secrets["private_key_id"],
    "private_key": secrets["private_key"],
    "client_email": secrets["client_email"],
    "client_id": secrets["client_id"],
    "auth_uri": secrets["auth_uri"],
    "token_uri": secrets["token_uri"],
    "auth_provider_x509_cert_url": secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": secrets["client_x509_cert_url"],
}

# Function to update Google Sheet with Client ID and geolocation
def update_google_sheet(client_id, lat, lon):
    try:
        # Define the scopes needed for your application
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        # Authenticate with Google Sheets API
        credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
        client = gspread.authorize(credentials)

        # Open the Google Sheet by URL
        spreadsheet_url = "https://docs.google.com/spreadsheets/d/1qGCvtnYZ9SOva5YqztSX7wjh8JLF0QRw-zbX9djQBWo"
        spreadsheet = client.open_by_url(spreadsheet_url)
        sheet = spreadsheet.worksheet("LOCATION")

        # Append data to the Google Sheet
        sheet.append_row([client_id, lat, lon])
        st.success("Location data successfully sent to Google Sheets.")
    except Exception as e:
        st.error(f"Error updating Google Sheet: {e}")

# Function to handle JavaScript listener
def js_listener():
    if "location" in st.session_state and st.session_state.location:
        lat, lon = st.session_state.location
        st.write(f"Geolocation: Latitude: {lat}, Longitude: {lon}")

        # Update Google Sheets with Client ID and geolocation
        update_google_sheet(client_id, lat, lon)
    else:
        st.write("Waiting for geolocation data...")

# Listen for messages from JavaScript component
st.components.v1.html(
    """
    <script>
        window.addEventListener('message', (event) => {
            // Check if we have geolocation data
            if (event.data.lat && event.data.lon) {
                const location = { lat: event.data.lat, lon: event.data.lon };
                window.parent.postMessage(location, "*");
            }
        });
    </script>
    """,
    height=0,
)

# Run the listener to handle geolocation
st.query_params
