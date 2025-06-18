# tools/youtube_tool.py
from crewai.tools import BaseTool
import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from pydantic import BaseModel, Field


class YouTubeUploaderToolSchema(BaseModel):
    """Input schema for YouTubeUploaderTool."""
    file_path: str = Field(..., description="The path to the final video file to be uploaded.")
    title: str = Field(..., description="The title of the YouTube video.")
    description: str = Field(..., description="The description for the YouTube video.")


class YouTubeUploaderTool(BaseTool):
    name: str = "YouTube Uploader Tool"
    description: str = "Uploads a video file to YouTube with a title and description."
    args_schema: type[BaseModel] = YouTubeUploaderToolSchema # 2. 
    
    def _get_credentials(self):
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/youtube.upload"])
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", ["https://www.googleapis.com/auth/youtube.upload"])
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds

    def _run(self, file_path: str, title: str, description: str) -> str:
        if not os.path.exists(file_path):
            return f"Error: Video file not found at {file_path}"
        
        try:
            credentials = self._get_credentials()
            youtube = build("youtube", "v3", credentials=credentials)
            request_body = { "snippet": { "title": title, "description": description, "tags": ["AI", "Anime", "CrewAI"], "categoryId": "1" }, "status": { "privacyStatus": "public" } }
            media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
            print("Uploading to YouTube...")
            request = youtube.videos().insert(part=",".join(request_body.keys()), body=request_body, media_body=media)
            response = request.execute()
            return f"Successfully uploaded video. Video ID: {response.get('id')}"
        except Exception as e:
            return f"An error occurred during YouTube upload: {e}"