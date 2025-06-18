# tools/post_production_tools.py
import os
import cv2
import numpy as np
from PIL import Image
from moviepy.editor import ImageSequenceClip
from crewai.tools import BaseTool
from pydantic import BaseModel, Field





class FaceAnimationToolSchema(BaseModel):
    """Input schema for FaceAnimationTool."""
    base_character_image_path: str = Field(..., description="Path to the character's neutral expression portrait.")
    open_mouth_image_path: str = Field(..., description="Path to the character's 'talking' (open mouth) portrait.")
    dialogue_audio_path: str = Field(..., description="Path to the dialogue audio file to match the video duration.")
    output_video_path: str = Field(..., description="Path to save the output animated video.")

class FaceAnimationTool(BaseTool):
    name: str = "Face Animation Generator"
    description: str = "Creates a simple, real 'talking' animation video from a character's neutral and open-mouth images, timed to an audio file."
    args_schema: type[BaseModel] = FaceAnimationToolSchema

    def _run(self, base_character_image_path: str, open_mouth_image_path: str, dialogue_audio_path: str, output_video_path: str) -> str:
        print(f"👄 Generating REAL animation for {os.path.basename(base_character_image_path)}...")
        
        try:
            # Get the duration from the audio file to sync the video length
            audio_clip = AudioFileClip(dialogue_audio_path)
            duration = audio_clip.duration
            fps = 24

            # Load images using PIL and convert to numpy arrays for OpenCV/moviepy
            base_img = np.array(Image.open(base_character_image_path).convert("RGB"))
            open_mouth_img = np.array(Image.open(open_mouth_image_path).convert("RGB"))

            frames = []
            num_frames = int(duration * fps)

            # Create a sequence of frames alternating between open and closed mouth
            # This creates a simple but effective talking illusion
            for i in range(num_frames):
                if (i // 4) % 2 == 0:  # Switch image every 4 frames
                    frames.append(base_img)
                else:
                    frames.append(open_mouth_img)
            
            # Create a video clip from the image sequence
            animation_clip = ImageSequenceClip(frames, fps=fps)
            
            # Set the audio of the animation clip to the dialogue
            final_clip = animation_clip.set_audio(audio_clip)

            # Write the final video file
            final_clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac", logger=None)
            
            return f"Successfully generated real animated video at {output_video_path}"
        except Exception as e:
            return f"Error during face animation generation: {e}"
# Define the explicit schema class
class LocalLipSyncToolSchema(BaseModel):
    """Input schema for LocalLipSyncTool."""
    character_image_path: str = Field(..., description="Path to the character's portrait image.")
    dialogue_audio_path: str = Field(..., description="Path to the dialogue audio file.")
    output_video_path: str = Field(..., description="Path to save the output lip-synced video.")

class LocalLipSyncTool(BaseTool):
    name: str = "Local Lip Sync Generator (SadTalker)"
    description: str = "Creates a lip-synced video from an image and audio file using a local model."
    args_schema: type[BaseModel] = LocalLipSyncToolSchema

    def _run(self, character_image_path: str, dialogue_audio_path: str, output_video_path: str) -> str:
        print(f"👄 SIMULATING Local Lip Sync for {os.path.basename(character_image_path)}...")
        command_to_run = f"python /path/to/SadTalker/inference.py --driven_audio {dialogue_audio_path} --source_image {character_image_path} --result_dir {os.path.dirname(output_video_path)}"
        print(f"   Placeholder for command: {command_to_run}")
        
        with open(output_video_path, 'w') as f:
            f.write(f"Dummy lip sync video for {character_image_path}")
        
        return f"Successfully simulated local lip-sync video at {output_video_path}. NOTE: This is a placeholder."