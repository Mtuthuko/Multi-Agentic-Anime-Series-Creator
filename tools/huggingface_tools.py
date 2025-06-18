# tools/huggingface_tools.py
import os
import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from huggingface_hub import HfApi, snapshot_download
from huggingface_hub.inference_api import InferenceApi

class HuggingFaceImageGeneratorToolSchema(BaseModel):
    prompt: str = Field(..., description="A detailed, descriptive prompt for the image.")
    output_path: str = Field(..., description="The local path to save the generated image.")

class HuggingFaceImageGeneratorTool(BaseTool):
    name: str = "Hugging Face Image Generator"
    description: str = "Generates a still image using an open-source model via the Hugging Face Inference API."
    args_schema: type[BaseModel] = HuggingFaceImageGeneratorToolSchema

    def _run(self, prompt: str, output_path: str) -> str:
        print(f"🎨 Generating image via Hugging Face with prompt: '{prompt}'")
        try:
            inference = InferenceApi(token=os.getenv("HUGGING_FACE_API_TOKEN"))
            # A popular Stable Diffusion model
            model_id = "digiplay/AbsoluteReality_v1.8.1" 
            
            image_bytes = inference.text_to_image(prompt, model=model_id)

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(image_bytes)

            return f"Successfully generated and saved image to {output_path}"
        except Exception as e:
            return f"Error during Hugging Face image generation: {e}"


class HuggingFaceVideoGeneratorToolSchema(BaseModel):
    source_image_path: str = Field(..., description="The file path to the initial static image frame.")
    output_path: str = Field(..., description="The local path to save the generated video clip.")

class HuggingFaceVideoGeneratorTool(BaseTool):
    name: str = "Hugging Face Video Generator (SVD)"
    description: str = "Generates a short video clip from a starting image using the Stable Video Diffusion model via the Hugging Face Inference API."
    args_schema: type[BaseModel] = HuggingFaceVideoGeneratorToolSchema

    def _run(self, source_image_path: str, output_path: str) -> str:
        print(f"🎬 Generating video via Hugging Face from image: '{source_image_path}'")
        try:
            if not os.path.exists(source_image_path):
                return f"Error: Source image not found at {source_image_path}"

            inference = InferenceApi(token=os.getenv("HUGGING_FACE_API_TOKEN"))
            model_id = "stabilityai/stable-video-diffusion-img2vid-xt"

            with open(source_image_path, "rb") as f:
                video_bytes = inference.image_to_video(f.read(), model=model_id)

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(video_bytes)

            return f"Successfully generated video and saved to {output_path}"
        except Exception as e:
            # The free tier often has models loading, which can cause timeouts.
            return f"Error during Hugging Face video generation: {e}. The model might be loading on the free tier; try again in a few minutes."