# tools/compiler_tool.py
from crewai.tools import BaseTool
from moviepy.editor import (VideoFileClip, AudioFileClip, ImageClip, 
                            CompositeVideoClip, concatenate_videoclips, TextClip)
import os
# Import BaseModel and Field from pydantic
from pydantic import BaseModel, Field 

# --- CORRECT SCHEMA DEFINITION FOR VideoCompilerTool ---
class VideoCompilerToolSchema(BaseModel):
    """Input schema for VideoCompilerTool."""
    output_path: str = Field(..., description="The final output path for the episode video, e.g., 'episodes/episode_1/episode_1.mp4'.")

class VideoCompilerTool(BaseTool):
    name: str = "Video Compiler Tool"
    description: str = "Compiles all generated scene video clips and a music track into a final episode video."
    args_schema: type[BaseModel] = VideoCompilerToolSchema # Assign the correct schema

    def _run(self, output_path: str) -> str:
        print(f"🎬 Compiling final video from scene clips to {output_path}...")
        
        asset_dir = "temp_assets"
        if not os.path.exists(asset_dir):
            return "Error: The 'temp_assets' directory does not exist. No clips were generated."
            
        # Find all files named 'scene_XX_clip.mp4' and sort them numerically
        scene_clips_files = sorted(
            [os.path.join(asset_dir, f) for f in os.listdir(asset_dir) if f.startswith('scene_') and f.endswith('_clip.mp4')],
            key=lambda x: int(os.path.basename(x).split('_')[1])
        )

        if not scene_clips_files:
            return "Error: Missing critical assets. No scene clips (scene_XX_clip.mp4) found to compile."

        try:
            video_clips = [VideoFileClip(f) for f in scene_clips_files]
            final_video = concatenate_videoclips(video_clips, method="compose")
            
            # Find a music file to layer over
            music_files = [os.path.join(asset_dir, f) for f in os.listdir(asset_dir) if f.startswith('music_')]
            if music_files:
                music_clip = AudioFileClip(music_files[0]).set_duration(final_video.duration)
                final_video = final_video.set_audio(music_clip)

            final_video.write_videofile(
                output_path, 
                codec="libx264", 
                audio_codec="aac",
                logger=None
            )
            
            return f"Successfully compiled and saved final video to {output_path}."
        except Exception as e:
            return f"An error occurred during video compilation: {e}"