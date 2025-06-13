# tools/video_tool.py
import json
import os
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip

# --- ADD THIS CONFIGURATION BLOCK IF YOU NEED IT ---
# from moviepy.config import change_config
# For Windows, if auto-detect fails, uncomment and update the path below.
# Make sure to use double backslashes in the path.
# change_config({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})
# --- END OF CONFIGURATION BLOCK ---

# 1. Define the input schema for the tool
class VideoGeneratorToolSchema(BaseModel):
    """Input schema for VideoGeneratorTool."""
    scene_number: int = Field(..., description="The sequential number of the scene in the episode.")
    description: str = Field(..., description="A detailed visual description of the scene to be generated.")
    duration: int = Field(..., description="The duration of the scene in seconds.")

class VideoGeneratorTool(BaseTool):
    name: str = "Video Scene Generator"
    description: str = "Generates a video clip for a single scene based on a detailed description, scene number, and duration."
    args_schema: type[BaseModel] = VideoGeneratorToolSchema # 2. Assign the schema to the tool

    # 3. Update the _run method to accept named arguments
    def _run(self, scene_number: int, description: str, duration: int) -> str:
        """
        SIMULATED VIDEO GENERATION:
        This tool creates a simple text overlay on a black background to represent the scene.
        In a real-world scenario, this would call a text-to-video API.
        """
        print(f"🎬 Generating video for Scene {scene_number}: '{description}' (Duration: {duration}s)")

        # Create a placeholder clip
        size = (1920, 1080)
        try:
            bg_clip = ColorClip(size=size, color=(0, 0, 0), duration=duration)
            text_clip = TextClip(
                description,
                fontsize=50,
                color='white',
                size=(size[0] - 100, size[1]), # Add some padding
                method='caption'
            ).set_duration(duration)

            video = CompositeVideoClip([bg_clip, text_clip.set_position('center')])
            
            # Save the clip to a temporary file, ensuring the folder exists
            output_dir = "temp_assets"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"scene_{scene_number}.mp4")
            
            # Use logger=None to prevent verbose console output from moviepy
            video.write_videofile(output_path, codec="libx264", fps=24, logger=None)
            
            return f"Successfully created video clip for scene {scene_number} at {output_path}"
        except Exception as e:
            return f"Error generating video clip for scene {scene_number}: {e}"