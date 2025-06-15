# tools/video_tool.py
import os
import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from moviepy.editor import ImageClip, AudioFileClip
from moviepy.video.fx.all import crop, resize
from gradio_client import Client

# --- CORRECT SCHEMA DEFINITION FOR StillImageGeneratorTool ---
class StillImageGeneratorToolSchema(BaseModel):
    """Input schema for StillImageGeneratorTool."""
    prompt: str = Field(..., description="A detailed visual prompt for the image.")
    file_path: str = Field(..., description="The path to save the generated image.")

class StillImageGeneratorTool(BaseTool):
    name: str = "Still Scene Image Generator"
    description: str = "Generates a single, high-quality still image for a scene using a Hugging Face Space."
    args_schema: type[BaseModel] = StillImageGeneratorToolSchema

    def _run(self, prompt: str, file_path: str) -> str:
        print(f"🎨 Generating Still Image via Gradio Client: '{prompt}'")
        try:
            client = Client("KBlueLeaf/Kohaku-v2.1")
            result = client.predict(
                prompt=f"masterpiece, best quality, cinematic anime art, {prompt}",
                negative_prompt="lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry",
                steps=25,
                width=1024,
                height=576,
                api_name="/generate_image_1"
            )
            generated_image_path = result
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(generated_image_path, 'rb') as f_in, open(file_path, 'wb') as f_out:
                f_out.write(f_in.read())
            return f"Successfully generated still image at {file_path}"
        except Exception as e:
            return f"An unexpected error occurred during image generation: {e}"

# --- CORRECT SCHEMA DEFINITION FOR KenBurnsVideoTool ---
class KenBurnsVideoToolSchema(BaseModel):
    """Input schema for KenBurnsVideoTool."""
    image_path: str = Field(..., description="The path to the still image to animate.")
    audio_path: str = Field(..., description="The path to the dialogue audio file to layer over the video. This can be a path to a non-existent file for silent scenes.")
    output_path: str = Field(..., description="The path to save the final video clip.")

class KenBurnsVideoTool(BaseTool):
    name: str = "Ken Burns Effect Video Creator"
    description: str = "Creates a short video clip from a still image by adding a slow zoom/pan effect and layering dialogue audio over it."
    args_schema: type[BaseModel] = KenBurnsVideoToolSchema

    def _run(self, image_path: str, audio_path: str, output_path: str) -> str:
        print(f"📹 Creating Ken Burns video for {os.path.basename(image_path)}")
        has_audio = os.path.exists(audio_path)
        if not os.path.exists(image_path):
            return f"Error: Missing input image file: {image_path}"
        if not has_audio:
            print("...Detected silent scene. Creating video without dialogue.")
        try:
            duration = 3.0
            if has_audio:
                with AudioFileClip(audio_path) as audio_clip_handle:
                    duration = audio_clip_handle.duration + 0.5
            image_clip = ImageClip(image_path).set_duration(duration)
            (w, h) = image_clip.size
            zoomed_clip = image_clip.fx(resize.Resize, lambda t: 1 + 0.05 * (t / duration)).set_position(('center', 'center'))
            final_clip = crop(zoomed_clip, width=w, height=h, x_center=zoomed_clip.w/2, y_center=zoomed_clip.h/2)
            if has_audio:
                audio_clip_to_set = AudioFileClip(audio_path)
                final_clip = final_clip.set_audio(audio_clip_to_set)
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
            return f"Successfully created video clip at {output_path}"
        except Exception as e:
            return f"Error creating Ken Burns video: {e}"