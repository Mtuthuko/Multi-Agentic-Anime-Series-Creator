# test_tools.py
import os
from dotenv import load_dotenv
load_dotenv() # Load your .env variables

# Test Google Veo
try:
    from tools.video_generation_tool import GoogleVeoVideoGeneratorTool
    veo_tool = GoogleVeoVideoGeneratorTool()
    # Call the _run method directly (you'd typically do this via agent, but for isolated test)
    # This might require providing args in a dict if _run expects a dict.
    # For simplicity, let's just test instantiation here.
    print(f"Google Veo tool initialized: {veo_tool.name}")
    # You could try a simple call here, e.g. veo_tool._run(prompt="a dog", file_path="test_veo.mp4")
except Exception as e:
    print(f"ERROR: Google Veo Tool failed initialization: {e}")

print("-" * 30)

# Test MusicGen
try:
    from tools.music_generator_tool import MusicGeneratorTool
    music_tool = MusicGeneratorTool()
    print(f"MusicGen tool initialized: {music_tool.name}")
    # Try a simple call: music_tool._run(prompt="a short melody", file_path="test_music.wav")
except Exception as e:
    print(f"ERROR: MusicGen Tool failed initialization: {e}")

print("-" * 30)

# Test YouTube Uploader
try:
    from tools.youtube_tool import YouTubeUploaderTool
    yt_tool = YouTubeUploaderTool()
    print(f"YouTube Uploader tool initialized: {yt_tool.name}")
except Exception as e:
    print(f"ERROR: YouTube Uploader Tool failed initialization: {e}")

print("-" * 30)

# Test Compiler
try:
    from tools.compiler_tool import VideoCompilerTool
    compiler_tool_instance = VideoCompilerTool()
    print(f"Video Compiler tool initialized: {compiler_tool_instance.name}")
except Exception as e:
    print(f"ERROR: Video Compiler Tool failed initialization: {e}")

# ... and so on for other tools.