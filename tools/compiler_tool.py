# tools/compiler_tool.py
from crewai.tools import BaseTool
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
import os

class VideoCompilerTool(BaseTool):
    name: str = "Video Compiler Tool"
    description: str = "Compiles video clips, voiceovers, music, and sound effects into a final video file. The input should be the final output path for the video."

    def _run(self, output_path: str) -> str:
        """
        This tool finds all generated asset files (temp_*.mp4, temp_*.wav)
        and compiles them. This is a simplified compilation. A more robust
        version would take a structured list of assets and timings.
        """
        print(f"Compiling final video to {output_path}...")
        
        # Find all scene clips and sort them
        video_files = sorted([f for f in os.listdir('.') if f.startswith('temp_scene_') and f.endswith('.mp4')])
        if not video_files:
            return "Error: No video scene files found to compile."
            
        clips = [VideoFileClip(f) for f in video_files]
        final_video = concatenate_videoclips(clips)

        # In a real implementation, you would layer audio here
        # For now, we'll just use the concatenated video
        # final_audio = AudioFileClip("path/to/music.wav")
        # final_video = final_video.set_audio(final_audio)

        final_video.write_videofile(output_path, codec="libx264", fps=24, logger=None)

        # Clean up temporary files
        for f in video_files:
            os.remove(f)
        # Add cleanup for audio files as well
        # for f in audio_files: os.remove(f)
        
        return f"Successfully compiled and saved final video to {output_path}."