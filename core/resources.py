# core/resources.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.memory_tool import MemoryTool
from tools.video_tool import VideoGeneratorTool
from tools.audio_tools import VoiceGeneratorTool, SoundTool
from tools.compiler_tool import VideoCompilerTool
from tools.youtube_tool import YouTubeUploaderTool
from utils.memory_manager import MemoryManager
from langchain_google_vertexai import ChatVertexAI

llm = ChatVertexAI(
    model_name="gemini-2.0-flash-001", # Vertex AI uses slightly different model names
    project="multi-agentic-animme" # You need to specify your project ID
)

# --- Initialize Tools ---
memory_manager = MemoryManager(collection_name="mtuthuko_series_memory")
memory_tool = MemoryTool(memory_manager=memory_manager)
video_tool = VideoGeneratorTool()
voice_tool = VoiceGeneratorTool()
sound_tool = SoundTool()
compiler_tool = VideoCompilerTool()
youtube_tool = YouTubeUploaderTool()