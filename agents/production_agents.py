# agents/production_agents.py
from crewai import Agent
# from core.resources import llm, video_tool, voice_tool, sound_tool # Old import for general production_agent
from core.resources import llm, voice_tool, sfx_tool, music_tool, video_tool # Use the newly defined video_tool

production_agent = Agent(
    role='Multimedia Production Specialist',
    goal='Create all the visual and audio assets for the episode based on the script. This includes generating video scenes, character voiceovers, background music, and sound effects.',
    backstory=(
        'You are a one-person production house, a master of AI-powered generation tools. '
        'You take a script and meticulously create every asset required to build the episode, '
        'ensuring each element matches the script\'s tone and description.'
    ),
    # Now, `video_tool` will be your Hugging Face video generator
    # You'll use `voice_tool` for dialogue, `sfx_tool` for sound effects, `music_tool` for background music
    tools=[video_tool, voice_tool, sfx_tool, music_tool], 
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# Might still use the scene_compositor_agent if it's more about combining pre-generated elements.
# If the HuggingFaceVideoGeneratorTool produces full scenes, then the scene_compositor_agent might become redundant
# or its role would shift to just handling the assembly if "video_tool" produces full scenes.
# Given your existing tasks, `scene_compositor_agent` uses `image_tool` and `ken_burns_tool`,
# which suggests it's for animating still images.
# You need to decide if you want to generate full video scenes directly (Hugging Face text-to-video)
# OR if you want to generate still images and then apply Ken Burns.
# If you want full video scenes, then `HuggingFaceVideoGeneratorTool` is your primary.