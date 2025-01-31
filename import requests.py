import requests
import json
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Set up OAuth 2.0 authentication
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.appendonly']
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

def upload_photo(photo_path):
    """Uploads a photo and creates a media item in Google Photos."""
    with open(photo_path, "rb") as photo:
        headers = {
            "Authorization": f"Bearer {creds.token}",
            "Content-Type": "application/octet-stream",
            "X-Goog-Upload-File-Name": photo_path.split("/")[-1],
            "X-Goog-Upload-Protocol": "raw"
        }
        
        # Upload the photo to Google Photos (returns an upload token)
        response = requests.post(
            "https://photoslibrary.googleapis.com/v1/uploads",
            headers=headers,
            data=photo
        )
    
    if response.status_code == 200:
        upload_token = response.text  # Get the upload token
        print(f"Upload successful! Token: {upload_token}")
        
        # Now create the media item in Google Photos
        create_media_item(upload_token, photo_path)
    else:
        print(f"Upload failed: {response.text}")

def create_media_item(upload_token, file_name):
    """Creates a media item using the upload token so the photo appears in Google Photos."""
    create_item_url = "https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate"

    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }

    data = {
        "newMediaItems": [
            {
                "description": file_name,
                "simpleMediaItem": {
                    "uploadToken": upload_token
                }
            }
        ]
    }

    response = requests.post(create_item_url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"Successfully added {file_name} to Google Photos!")
    else:
        print(f"Error adding {file_name}: {response.text}")

# Upload all JPEGs in a folder
folder_path = "Pictures/"
for file in os.listdir(folder_path):
    if file.endswith(".jpg") or file.endswith(".jpeg"):
        upload_photo(os.path.join(folder_path, file))
