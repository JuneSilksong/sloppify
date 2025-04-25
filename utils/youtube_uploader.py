import os
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_youtube(file_path, title, description, tags=[], categoryId="22", privacyStatus="public"):

    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file("client_secrets.json", scopes)
    
    credentials = flow.run_local_server(port=8080)

    youtube = build("youtube", "v3", credentials=credentials)

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

"""upload_to_youtube(
    file_path="output/test.mp4",
    title="test_title",
    description="test_description",
    tags=["reddit","tifu","tts","tiktok"],
    privacyStatus="private"
)"""