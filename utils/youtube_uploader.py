import os
import pickle
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

def get_authenticated_service():
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    credentials = None
    
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file("client_secrets.json", scopes)
            credentials = flow.run_local_server(port=8080)
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)
    
    return build("youtube", "v3", credentials=credentials)

def upload_to_youtube(file_path, title, description, tags=[], categoryId="22", privacyStatus="public"):

    youtube = get_authenticated_service()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": categoryId
            },
            "status": {
                "privacyStatus": privacyStatus
            }
        },
        media_body=MediaFileUpload(file_path)
    )

    response = request.execute()
    print("Video uploaded:", response["id"])


upload_to_youtube(
    file_path="output/test.mp4",
    title="test_title",
    description="test_description",
    tags=["reddit","tifu","animal","funny","tts","tiktok"],
    privacyStatus="private"
)
