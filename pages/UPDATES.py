import streamlit as st
from geopy.geocoders import Nominatim

# Create a geolocator object
geolocator = Nominatim(user_agent="streamlit-location-app")

# Function to get coordinates from address
def get_coordinates(address):
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# User input for address
address = st.text_input("Enter your address:")

if address:
    lat, long = get_coordinates(address)
    if lat and long:
        st.write(f"Latitude: {lat}")
        st.write(f"Longitude: {long}")
    else:
        st.write("Address not found. Please try again.")
