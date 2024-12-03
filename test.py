import streamlit as st

# Define the question and options
st.write("What are your favorite colors? (You can select multiple options)")

options = ["Red", "Blue", "Green", "Yellow", "Purple"]

# Store selected options
selected_options = []

# Create checkboxes for each option
for option in options:
    if st.checkbox(option):
        selected_options.append(option)

# Display the selected options
st.write("You selected:", selected_options)