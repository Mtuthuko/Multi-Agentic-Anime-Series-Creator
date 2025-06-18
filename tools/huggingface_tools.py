# tools/huggingface_tools.py
import os
import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr
from huggingface_hub.inference_api import InferenceApi
from typing import Any

class HuggingFaceImageGeneratorToolSchema(BaseModel):
    prompt: str = Field(..., description="A detailed descriptive prompt for the image.")
    output_path: str = Field(..., description="The local path to save the generated image.")
class HuggingFaceImageGeneratorTool(BaseTool):
    name: str = "Image Generator"
    description: str = "Generates a still image from a prompt using a Hugging Face model."
    args_schema: type[BaseModel] = HuggingFaceImageGeneratorToolSchema
    _inference_api: Any = PrivateAttr()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        model_id = "digiplay/AbsoluteReality_v1.8.1"
        self._inference_api = InferenceApi(repo_id=model_id, token=os.getenv("HUGGING_FACE_API_TOKEN"))
    def _run(self, prompt: str, output_path: str) -> str:
        print(f"🎨 Generating image via Hugging Face: '{prompt}'")
        try:
            image_bytes = self._inference_api.text_to_image(prompt)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f: f.write(image_bytes)
            return f"Successfully generated image and saved to {output_path}"
        except Exception as e: return f"Error during Hugging Face image generation: {e}"

class HuggingFaceVideoGeneratorToolSchema(BaseModel):
    source_image_path: str = Field(..., description="File path to the initial static image frame.")
    output_path: str = Field(..., description="Local path to save the generated video clip.")
class HuggingFaceVideoGeneratorTool(BaseTool):
    name: str = "Video Generator (from Image)"
    description: str = "Generates a short video clip from a starting image using Stable Video Diffusion on Hugging Face."
    args_schema: type[BaseModel] = HuggingFaceVideoGeneratorToolSchema
    _inference_api: Any = PrivateAttr()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        model_id = "stabilityai/stable-video-diffusion-img2vid-xt"
        self._inference_api = InferenceApi(repo_id=model_id, token=os.getenv("HUGGING_FACE_API_TOKEN"))
    def _run(self, source_image_path: str, output_path: str) -> str:
        print(f"🎬 Generating video via Hugging Face from: '{source_image_path}'")
        if not os.path.exists(source_image_path): return f"Error: Source image not found at {source_image_path}"
        try:
            with open(source_image_path, "rb") as f: video_bytes = self._inference_api.image_to_video(f.read())
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f: f.write(video_bytes)
            return f"Successfully generated video and saved to {output_path}"
        except Exception as e: return f"Error during Hugging Face video generation: {e}. The model might be loading; try again."