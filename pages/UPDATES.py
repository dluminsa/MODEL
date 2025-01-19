import streamlit as st
import requests

# Function to get geolocation based on IP address
def get_geolocation():
    try:
        # Make a request to the IP geolocation API
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        location = data.get('loc', '0.0, 0.0').split(',')
        lat, lon = location[0], location[1]
        return lat, lon
    except Exception as e:
        st.error(f"Error fetching geolocation: {e}")
        return None, None

# Initialize session state for geolocation
if "geolocation" not in st.session_state:
    st.session_state.geolocation = "Fetching geolocation..."

# Title for the app
st.title("Automatic Geolocation App (IP-based)")

# Get geolocation on app load
lat, lon = get_geolocation()

if lat and lon:
    # Update session state with the retrieved geolocation
    st.session_state.geolocation = f"{lat}, {lon}"
    st.write(f"Location: {st.session_state.geolocation}")
else:
    st.write("Unable to fetch geolocation automatically.")

st.write("Your geolocation is determined based on your IP address.")
