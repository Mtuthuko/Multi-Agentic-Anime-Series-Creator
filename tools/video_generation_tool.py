# tools/google_veo_tool.py
import os
import time
import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import ClassVar

# Import Google GenAI SDK (for client and types)
# import google.generativeai as genai
from google import genai
# from google import types as genai_types
from google.generativeai import types as genai_types
from google.genai.types import GenerateVideosConfig

# Import Google Cloud Storage for downloading from GCS
from google.cloud import storage 

# We no longer need aiplatform_v1 directly as genai.Client handles Vertex AI
# from google.cloud import aiplatform_v1 
# from google.protobuf import json_format # Not needed for this genai.Client approach
# from google.api_core.exceptions import GoogleAPIError # Handled by genai.Client's exception catching


import sys
import time
import urllib

from IPython.display import Video, display
from PIL import Image as PIL_Image
from google import genai
from google.oauth2 import service_account
from google.genai import types
import matplotlib.pyplot as plt

if "google.colab" in sys.modules:
    from google.colab import auth

    auth.authenticate_user()

import os

PROJECT_ID = "multi-agentic-animme"  # @param {type: "string", placeholder: "[your-project-id]", isTemplate: true}
if not PROJECT_ID or PROJECT_ID == "[your-project-id]":
    PROJECT_ID = str(os.environ.get("GOOGLE_CLOUD_PROJECT"))

LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/mtuthukomngomezulu/Documents/SaaS Multi-Agentic Anime Series Creator/Multi-Agentic-Anime-Series-Creator/multi-agentic-animme-c2cd2e511178.json'
scopes = [
    "https://www.googleapis.com/auth/generative-language",
    "https://www.googleapis.com/auth/cloud-platform",
]
credentials = service_account.Credentials.from_service_account_file(os.getenv('GOOGLE_APPLICATION_CREDENTIALS','/Users/mtuthukomngomezulu/Documents/SaaS Multi-Agentic Anime Series Creator/Multi-Agentic-Anime-Series-Creator/multi-agentic-animme-c2cd2e511178.json'), scopes=scopes)

client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION, credentials=credentials)
output_gcs = "gs://animation_creator_bucket"  # @param {type: 'string'}
enhance_prompt = True  # @param {type: 'boolean'}
generate_audio = True  # @param {type: 'boolean'}

# def show_video(gcs_uri):
#     file_name = gcs_uri.split("/")[-1]
#     !gsutil cp {gcs_uri} {file_name}
#     display(Video(file_name, embed=True, width=600))


# def display_images(image) -> None:
#     fig, axis = plt.subplots(1, 1, figsize=(12, 6))
#     axis.imshow(image)
#     axis.set_title("Starting Image")
#     axis.axis("off")
#     plt.show()




class GoogleVeoVideoGeneratorTool(BaseTool): 
    name: str = "Google Veo Video Generator"
    description: str = "Generates a video from a text prompt using Google's Veo 2 model via the Gemini API configured for Vertex AI."
    
    class Input(BaseModel):
        prompt: str = Field(..., description="The text prompt to generate the video.")
        file_path: str = Field(..., description="The local path to save the generated video file (e.g., 'temp_assets/scene_01_video.mp4').")
        aspect_ratio: str = Field("16:9", description="Aspect ratio of the video ('16:9' or '9:16').")
        person_generation: str = Field("DONT_ALLOW", description="Control person generation ('DONT_ALLOW', 'ALLOW_ADULT', 'ALLOW_ALL').")
        duration_seconds: int = Field(5, description="Desired video duration in seconds (5-8 seconds usually).")
        enhance_prompt: bool = Field(True, description="Whether to automatically enhance the prompt for better video quality.")

    # Class-level client instance and project/location info
    _client: genai.Client = None 
    _project_id: ClassVar[str] = None
    _location: ClassVar[str] = None
    _gcs_temp_bucket: ClassVar[str] = output_gcs # New: for the GCS output bucket

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if GoogleVeoVideoGeneratorTool._client is None:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
            location = os.getenv("GOOGLE_CLOUD_LOCATION")
            gcs_temp_bucket = output_gcs

            # client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
            # output_gcs = "gs://animation_creator_bucket"  # @param {type: 'string'}
            # enhance_prompt = True  # @param {type: 'boolean'}
            # generate_audio = True  # @param {type: 'boolean'}

            if not project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
            if not location:
                raise ValueError("GOOGLE_CLOUD_LOCATION environment variable not set.")
            if not gcs_temp_bucket:
                raise ValueError("GCS_TEMP_BUCKET environment variable not set. Please specify a GCS bucket for Veo output.")
            
            GoogleVeoVideoGeneratorTool._project_id = project_id
            GoogleVeoVideoGeneratorTool._location = location
            GoogleVeoVideoGeneratorTool._gcs_temp_bucket = gcs_temp_bucket

            try:
                # Configure genai client for Vertex AI
                print(f"DEBUG: Attempting to configure genai client for Vertex AI: Project={project_id}, Location={location}")
                genai.configure(vertexai=True, project=project_id, location=location)
                
                # Explicitly initialize the client AFTER configuration
                GoogleVeoVideoGeneratorTool._client = genai.Client(vertexai=True, project=project_id, location=location)
                print(f"DEBUG: Google Veo client initialized successfully for Vertex AI.")

            except Exception as e:
                # Catch any initialization errors here
                print(f"ERROR: Failed to initialize Google Veo client for Vertex AI: {e}")
                # Do NOT re-raise if you want the tool to fail gracefully with a message.
                # If you re-raise, the whole script might crash at startup.
                GoogleVeoVideoGeneratorTool._client = None # Ensure it's None if it fails
                raise RuntimeError(f"Google Veo client initialization FAILED: {e}. Check your service account (GOOGLE_APPLICATION_CREDENTIALS), project ID, and location.")
    

    def _run(self, prompt: str, file_path: str, aspect_ratio: str = "16:9",
             person_generation: str = "DONT_ALLOW", duration_seconds: int = 5,
             enhance_prompt: bool = True) -> str:

        print(f"🎬 Generating video via Google Veo 2 (Vertex AI) for prompt: '{prompt}'")
        GoogleVeoVideoGeneratorTool._gcs_temp_bucket = os.getenv("GCS_TEMP_BUCKET", "gs://animation_creator_bucket") # Ensure we have a bucket name

        unique_filename = f"temp_videos/{os.path.basename(file_path).replace('.mp4', '')}_{int(time.time())}.mp4"
        output_gcs_uri = f"{GoogleVeoVideoGeneratorTool._gcs_temp_bucket}/{unique_filename}"
        try:
            # THIS IS THE BLOCK THAT NEEDS ROBUST ERROR CATCHING
            # Try the core Veo generation first
            try:
                video_model = "veo-2.0-generate-001"
                # operation = self._client.models.generate_videos(
                #     model=video_model,
                #     prompt=prompt,
                #     config=genai_types.GenerateVideosConfig(
                #         aspect_ratio=aspect_ratio,
                #         output_gcs_uri=output_gcs_uri,
                #         number_of_videos=1,
                #         duration_seconds=min(max(duration_seconds, 5), 8),
                #         person_generation=person_generation,
                #         enhance_prompt=enhance_prompt
                #     ),
                # )
                # video_model = "veo-3.0-generate-preview"
                operation = client.models.generate_videos(
                model=video_model,
                prompt=prompt,
                # config=genai_types.GenerateVideosConfig(
                #     aspect_ratio="16:9",
                #     output_gcs_uri=output_gcs,
                #     number_of_videos=1,
                #     duration_seconds=8,
                #     person_generation="allow_adult",
                #     enhance_prompt=enhance_prompt,
                #     generate_audio=generate_audio,
                #     ),
                    )

                print("Polling Google Veo operation status...", end="", flush=True)
                while not operation.done:
                    time.sleep(15)
                    operation = client.operations.get(operation)
                    print(operation)
                    print(".", end="", flush=True)

                result = operation.result()
                print("\n")

                if result.error:
                    return f"Google Veo API error: {result.error.message} (Code: {result.error.code})"

                if not result.video_info or not result.video_info.uri:
                    return f"Error: Google Veo did not return a video URI. Result: {result}"

                video_uri = result.video_info.uri

            except Exception as e: # Catch any and all exceptions from the generation API call
                return f"Google Veo generation failed at API call/polling stage: {e}. Check GOOGLE_APPLICATION_CREDENTIALS, project permissions, and Veo API quotas."

            # If generation was successful, proceed to download from GCS
            print(f"Video generated at GCS URI: {video_uri}")

            try:
                storage_client = storage.Client(project=GoogleVeoVideoGeneratorTool._project_id)
                uri_parts = video_uri.split("//")[1].split("/", 1)
                bucket_name = uri_parts[0]
                blob_name = uri_parts[1]

                bucket = storage_client.get_bucket(bucket_name)
                blob = bucket.blob(blob_name)

                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                blob.download_to_filename(file_path)

                return f"Successfully generated video and saved locally to {file_path} from GCS."

            except Exception as e: # Catch any and all exceptions from the download stage
                return f"Google Veo video download from GCS failed: {e}. Check GCS bucket permissions or if the file was truly saved."

        except Exception as e: # Outer general catch-all for any other unexpected errors
            return f"An unexpected critical error occurred during Google Veo tool execution: {e}"