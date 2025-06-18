# core/resources.py
import os
from langchain_google_vertexai import ChatVertexAI

# --- IMPORTS FOR THE KEN BURNS ARCHITECTURE ---
# core/resources.py
from tools.memory_tool import MemoryReaderTool, MemoryWriterTool
# CORRECTED IMPORTS: We are importing the two separate tools, not the LTX tool.
from tools.huggingface_tools import HuggingFaceImageGeneratorTool, HuggingFaceVideoGeneratorTool
# CORRECTED IMPORTS: We are importing the new HF music tool.
from tools.audio_tools import VoiceGeneratorTool, SfxGeneratorTool, HuggingFaceMusicGeneratorTool
from tools.compiler_tool import VideoCompilerTool
from tools.youtube_tool import YouTubeUploaderTool
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
memory_reader_tool = MemoryReaderTool(memory_manager=memory_manager)
memory_writer_tool = MemoryWriterTool(memory_manager=memory_manager)

# CORRECTED INSTANTIATION
hf_image_tool = HuggingFaceImageGeneratorTool()
hf_video_tool = HuggingFaceVideoGeneratorTool()
voice_tool = VoiceGeneratorTool()
sfx_tool = SfxGeneratorTool()
hf_music_tool = HuggingFaceMusicGeneratorTool() # Using the new HF music tool
compiler_tool = VideoCompilerTool()
youtube_tool = YouTubeUploaderTool()
print("All tools initialized.")

