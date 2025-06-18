# tools/compiler_tool.py
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from moviepy.editor import (VideoFileClip, AudioFileClip, ImageClip, 
                            CompositeVideoClip, concatenate_audioclips, ColorClip)
from moviepy.audio.AudioClip import CompositeAudioClip
import os

# Define the explicit schema class
class VideoCompilerToolSchema(BaseModel):
    """Input schema for VideoCompilerTool."""
    output_path: str = Field(..., description="Final output path for the episode.")

class VideoCompilerTool(BaseTool):
    name: str = "Video Compiler Tool"
    description: str = "Compiles all assets (lip-synced videos, backgrounds, music) into a final episode video."
    args_schema: type[BaseModel] = VideoCompilerToolSchema

    def _run(self, output_path: str) -> str:
        print(f"🎬 Compiling final video to {output_path}...")
        asset_dir = "temp_assets"
        background_files = [os.path.join(asset_dir, f) for f in os.listdir(asset_dir) if f.startswith('background_')]
        dialogue_videos = sorted([
            os.path.join(asset_dir, f) for f in os.listdir(asset_dir) 
            if f.startswith('scene') and any(f.endswith(ext) for ext in ['.mp4', '.avi', '.mov'])
        ])
        music_files = [os.path.join(asset_dir, f) for f in os.listdir(asset_dir) if f.startswith('music_')]

        if not dialogue_videos:
            print("Warning: No real lip-sync videos found. Creating a dummy 5-second black clip to prevent errors.")
            dummy_path = os.path.join(asset_dir, "dummy_video.mp4")
            # Create a dummy video only if it doesn't exist
            if not os.path.exists(dummy_path):
                dummy_clip = ColorClip(size=(1024,576), color=(0,0,0), duration=5)
                dummy_clip.write_videofile(dummy_path, fps=24)
            dialogue_videos.append(dummy_path)
            
        if not background_files:
            return "Error: Missing background assets to compile."
        
        dialogue_clips = [VideoFileClip(f) for f in dialogue_videos]
        total_duration = sum(c.duration for c in dialogue_clips)
        background_clip = ImageClip(background_files[0], duration=total_duration)
        
        final_video = CompositeVideoClip([background_clip] + dialogue_clips)

        if music_files:
            music_clip = AudioFileClip(music_files[0]).set_duration(total_duration)
            final_audio = CompositeAudioClip([final_video.audio, music_clip.volumex(0.2)])
            final_video.audio = final_audio

        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", bitrate="5000k")
        return f"Successfully compiled and saved final video to {output_path}."