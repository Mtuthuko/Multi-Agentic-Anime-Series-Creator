# tools/music_generator_tool.py
import os
import soundfile as sf
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import ClassVar
import torch
print(f"torch.backends.mps.is_available(): {torch.backends.mps.is_available()}")
print(f"torch.backends.mps.is_built(): {torch.backends.mps.is_built()}")
import sys

from transformers import pipeline

import base64

from IPython.display import Audio
import google.auth
import google.auth.transport.requests
import requests

PROJECT_ID = "multi-agentic-animme"  # @param {type:"string"}
music_model = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/us-central1/publishers/google/models/lyria-002:predict"

class MusicGeneratorToolSchema(BaseModel):
    """Input schema for MusicGeneratorTool."""
    prompt: str = Field(..., description="A detailed text prompt describing the desired music, e.g., 'calm piano melody, 30 seconds long, hopeful mood'.")
    file_path: str = Field(..., description="The local path to save the generated music file (e.g., 'temp_assets/episode_1_music.wav').")
    duration_seconds: int = Field(10, description="Desired duration of the generated music in seconds (max depends on model).")

class MusicGeneratorTool(BaseTool):
    name: ClassVar[str] = "Background Music Generator"
    # --- FIX IS HERE: Remove ClassVar from description ---
    description: str = "Generates a music track from a text description using the local MusicGen model."
    # --- END FIX ---
    args_schema: type[BaseModel] = MusicGeneratorToolSchema

    _music_pipeline: pipeline = None # Class-level pipeline instance

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if MusicGeneratorTool._music_pipeline is None:
            # --- DEBUG PRINTS ---
            print("\nDEBUG (MusicGen Tool Init): Attempting to load MusicGen pipeline...")
            print(f"DEBUG (MusicGen Tool Init): PyTorch version: {torch.__version__}")
            print(f"DEBUG (MusicGen Tool Init): Is CUDA available? {torch.cuda.is_available()}")
            print(f"DEBUG (MusicGen Tool Init): Is MPS (Apple Silicon) available? {torch.backends.mps.is_available()}")
            if torch.backends.mps.is_available():
                print("DEBUG (MusicGen Tool Init): Using MPS backend.")
                device = "mps"
            elif torch.cuda.is_available():
                print("DEBUG (MusicGen Tool Init): Using CUDA backend.")
                device = "cuda"
            else:
                print("DEBUG (MusicGen Tool Init): Using CPU backend. This will be very slow and might fail for large models.")
                device = "cpu"
            # --- END DEBUG PRINTS ---

            try:
                # Pass device argument to pipeline
                # MusicGeneratorTool._music_pipeline = pipeline("text-to-audio", model="facebook/musicgen-melody", device=device)
                MusicGeneratorTool._music_pipeline = pipeline("text-to-audio", model="facebook/musicgen-small")
                print("MusicGen pipeline (facebook/musicgen-melody) initialized.")
            except Exception as e:
                print(f"ERROR (MusicGen Tool Init): Failed to initialize MusicGen pipeline: {e}")
                print(f"ERROR (MusicGen Tool Init): This often means:")
                print(f"  1. Missing or incorrect GPU drivers (CUDA for NVIDIA, specific PyTorch build for Apple Silicon).")
                print(f"  2. Insufficient VRAM for 'facebook/musicgen-melody' (it's large).")
                print(f"  3. Try 'facebook/musicgen-small' model first for testing if VRAM is an issue.")
                print(f"  4. Check your internet connection for model download.")
                # Raise error to stop execution if pipeline fails to init
                raise RuntimeError(f"MusicGen pipeline initialization failed: {e}")
            


    def send_request_to_google_api(self,api_endpoint, data=None):
        """
        Sends an HTTP request to a Google API endpoint.

        Args:
            api_endpoint: The URL of the Google API endpoint.
            data: (Optional) Dictionary of data to send in the request body (for POST, PUT, etc.).

        Returns:
            The response from the Google API.
        """

        # Get access token calling API
        creds, project = google.auth.default()
        auth_req = google.auth.transport.requests.Request()
        creds.refresh(auth_req)
        access_token = creds.token

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(api_endpoint, headers=headers, json=data)
        response.raise_for_status()
        return response.json()


    def generate_music(self,request: dict):
        req = {"instances": [request], "parameters": {}}
        print(req)
        resp = self.send_request_to_google_api(music_model, req)
        return resp["predictions"]


    # def play_audio(self,preds):
    #     for pred in preds:
    #         bytes_b64 = dict(pred)["bytesBase64Encoded"]
    #         decoded_audio_data = base64.b64decode(bytes_b64)

    #         audio = Audio(decoded_audio_data, rate=48000, autoplay=False)
    #         display(audio)

    def _run(self, prompt: str, file_path: str, duration_seconds: int = 10) -> str:
        print(f"🎵 Generating music with MusicGen: '{prompt}' for {duration_seconds} seconds.")
        
        try:



           
            negative_prompt = ""  # @param {type:"string"}
            seed = 111  # @param {type:"number"}


            # music = self.generate_music(
            #     {"prompt": prompt, "negative_prompt": negative_prompt, "sample_count": sample_count}
            # )


            audio_output =  self.generate_music(
                {"prompt": prompt, "negative_prompt": negative_prompt, "seed": seed}
            )
            
            if not audio_output or not audio_output[0].get('audio'):
                return "Error: MusicGen pipeline did not return audio data."

            audio_array = audio_output[0]['audio']
            sampling_rate = audio_output[0]['sampling_rate']

            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            if not file_path.lower().endswith(".wav"):
                file_path_wav = os.path.splitext(file_path)[0] + ".wav"
                print(f"Warning: Music file saved as .wav due to format, original request was {os.path.splitext(file_path)[1]}.")
            else:
                file_path_wav = file_path

            sf.write(file_path_wav, audio_array, sampling_rate)

            return f"Successfully generated music and saved to {file_path_wav}"

        except Exception as e:
            return f"An unexpected error occurred during MusicGen generation: {e}. Check GPU availability and VRAM."