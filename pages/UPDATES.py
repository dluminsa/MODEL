import streamlit as st
import streamlit.components.v1 as components
components.html("""
    <script src="https://apis.google.com/js/api.js"></script>
    <script>
        // Function to authenticate with Google Sheets API
        function authenticate() {
            return new Promise(function(resolve, reject) {
                gapi.auth2.getAuthInstance().signIn().then(function() {
                    resolve();
                }, function(error) {
                    reject(error);
                });
            });
        }

        // Function to initialize the Google API client
        function initClient() {
            gapi.client.init({
                apiKey: 'AIzaSyAO5vJ44e5AYp7N6wxl6r9tmJj_3pS7q0k',  // Your API Key
                clientId: '115904525169801082180',  // Your Client ID
                scope: 'https://www.googleapis.com/auth/spreadsheets',
                discoveryDocs: ['https://sheets.googleapis.com/$discovery/rest?version=v4']
            });
        }

        // Function to capture and send coordinates to Google Sheets
        function sendLocationToSheet(latitude, longitude) {
            const spreadsheetId = '1qGCvtnYZ9SOva5YqztSX7wjh8JLF0QRw-zbX9djQBWo';  // Your Spreadsheet ID
            const range = 'LOCATION!A1:B1';  // Range to write data
            const values = [
                [latitude, longitude]
            ];

            const body = {
                values: values
            };

            console.log('Sending location:', latitude, longitude);  // Debugging line

            gapi.client.sheets.spreadsheets.values.update({
                spreadsheetId: spreadsheetId,
                range: range,
                valueInputOption: 'RAW',
                resource: body
            }).then((response) => {
                console.log('Location written to Google Sheets:', response);
            }, function(error) {
                console.log('Error writing to Google Sheets:', error);
            });
        }

        // Capture the user's location and send it to Google Sheets
        window.onload = function() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;

                    authenticate().then(function() {
                        initClient().then(function() {
                            sendLocationToSheet(latitude, longitude);
                        });
                    });
                }, function(error) {
                    alert('Error getting location: ' + error.message);
                });
            } else {
                alert('Geolocation is not supported by this browser.');
            }
        };
    </script>
""", height=0)
