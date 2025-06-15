# core/resources.py
import os
from langchain_google_vertexai import ChatVertexAI

# --- IMPORTS FOR THE KEN BURNS ARCHITECTURE ---
from tools.memory_tool import MemoryTool
from tools.video_tool import StillImageGeneratorTool, KenBurnsVideoTool
from tools.audio_tools import VoiceGeneratorTool, MusicGeneratorTool, SfxGeneratorTool
from tools.compiler_tool import VideoCompilerTool
from tools.youtube_tool import YouTubeUploaderTool
from utils.memory_manager import MemoryManager

# --- Initialize the LLM ---


# --- Initialize the LLM with adjusted safety settings ---
# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash-latest",
#     google_api_key=os.getenv("GOOGLE_API_KEY"),
#     # ADD THIS BLOCK TO RELAX SAFETY FILTERS
#     safety_settings={
#         HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
#     },
# )

llm = ChatVertexAI(
    model_name="gemini-2.0-flash-001", # Vertex AI uses slightly different model names
    project="multi-agentic-animme" # You need to specify your project ID
)

# --- Initialize the NEW, LEANER Toolset ---

memory_manager = MemoryManager(collection_name="mtuthuko_series_memory")
memory_tool = MemoryTool(memory_manager=memory_manager)
image_tool = StillImageGeneratorTool()
ken_burns_tool = KenBurnsVideoTool()
voice_tool = VoiceGeneratorTool()
music_tool = MusicGeneratorTool()
sfx_tool = SfxGeneratorTool()
compiler_tool = VideoCompilerTool()
youtube_tool = YouTubeUploaderTool()