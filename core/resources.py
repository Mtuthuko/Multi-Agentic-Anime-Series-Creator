# core/resources.py
import os
from langchain_google_vertexai import ChatVertexAI

# --- IMPORTS FOR THE KEN BURNS ARCHITECTURE ---
# core/resources.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Import all tools
from tools.memory_tool import MemoryTool
from tools.local_image_tool import LocalImageGeneratorTool
from tools.audio_tools import VoiceGeneratorTool, SfxGeneratorTool, MusicGeneratorTool
from tools.post_production_tools import FaceAnimationTool
from tools.compiler_tool import VideoCompilerTool
from tools.youtube_tool import YouTubeUploaderTool # Assuming you still have youtube_tool.py from previous steps
from utils.memory_manager import MemoryManager

# --- Initialize the LLM ---
llm = ChatVertexAI(
    model_name="gemini-2.0-flash-001", # Vertex AI uses slightly different model names
    project="multi-agentic-animme" # You need to specify your project ID
)

# --- Initialize ALL Tools ---
# Note: LocalImageGeneratorTool will download models on first run.
print("Initializing tools...")
memory_manager = MemoryManager(collection_name="mtuthuko_series_memory")
memory_tool = MemoryTool(memory_manager=memory_manager)
local_image_tool = LocalImageGeneratorTool()
voice_tool = VoiceGeneratorTool()
sfx_tool = SfxGeneratorTool()
music_tool = MusicGeneratorTool()
local_lip_sync_tool = FaceAnimationTool()
compiler_tool = VideoCompilerTool()
youtube_tool = YouTubeUploaderTool()
print("All tools initialized.")

