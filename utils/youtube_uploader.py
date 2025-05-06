import os
import pickle
import time
import re
import random
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

UPLOAD_LOG = "upload_log.txt"

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

def load_uploaded_files(log_file=UPLOAD_LOG):
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            return set(line.strip() for line in f)
    return set()

def log_uploaded_file(filename, log_file=UPLOAD_LOG):
    with open(log_file, "a") as f:
        f.write(filename + "\n")

def clean_title(filename):
    cleaned = filename.replace("#", "")

    while True:
        cleaned_new = re.sub(r'\.(mp4|mov|avi|mkv|webm|flv|wmv)$', '', cleaned, flags=re.IGNORECASE)
        if cleaned_new == cleaned:
            break
        cleaned = cleaned_new

    cleaned = cleaned.replace("_", " ").replace("-", " ")

    return cleaned.strip()

def upload_all_videos_in_directory(directory="output", wait_minutes=60):
    uploaded_files = load_uploaded_files()

    video_files = [f for f in os.listdir(directory) if f.lower().endswith((".mp4", ".mov", ".avi", ".mkv"))]

    if not video_files:
        print("No videos found in the directory.")
        return
    
    random.shuffle(video_files)

    for filename in video_files:
        if not filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
            continue
        if filename in uploaded_files:
            print(f"Skipping already uploaded file: {filename}")
            continue

        file_path = os.path.join(directory, filename)
        title = os.path.splitext(filename)[0]
        title = clean_title(title)

        try:
            print(f"Uploading: {file_path}", title)
            upload_to_youtube(
                file_path=file_path,
                title=title,
                description="The video material has been kindly provided by HikingFex.com.\n🔗 https://www.hikingfex.com/en/videos",
                tags=["reddit", "animal", "funny", "tiktok", "cute", "shorts"],
                privacyStatus="public"
            )
            log_uploaded_file(filename)
            os.remove(file_path)
            print(f"Deleted after upload: {file_path}")

            print(f"Waiting {wait_minutes} minutes before next upload...")
            time.sleep(wait_minutes * 60)

        except Exception as e:
            print(f"Failed to upload {file_path}: {e}")

upload_all_videos_in_directory(directory="output")