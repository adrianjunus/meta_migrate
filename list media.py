import requests
import json
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Set up OAuth 2.0 authentication
SCOPES = [
    'https://www.googleapis.com/auth/photoslibrary',
]

creds = None
creds_file = "credentials.json"

flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
creds = flow.run_local_server(port=8080)

# Set API headers
headers = {
    "Authorization": f"Bearer {creds.token}",
    "Content-type": "application/octet-stream",
    "X-Goog-Upload-File-Name": "photo.jpg",
    "X-Goog-Upload-Protocol": "raw"
}

def list_media_items():
    headers = {
        "Authorization": f"Bearer {creds.token}"
    }
    
    response = requests.get(
        "https://photoslibrary.googleapis.com/v1/mediaItems?pageSize=10",
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        for item in data.get("mediaItems", []):
            print(f"Filename: {item['filename']}, URL: {item['baseUrl']}")
    else:
        print(f"Error: {response.text}")

list_media_items()
