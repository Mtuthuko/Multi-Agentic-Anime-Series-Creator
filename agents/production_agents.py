# agents/production_agents.py
from crewai import Agent
from core.resources import llm, video_tool, voice_tool, sound_tool

production_agent = Agent(
    role='Multimedia Production Specialist',
    goal='Create all the visual and audio assets for the episode based on the script. This includes generating video scenes, character voiceovers, background music, and sound effects.',
    backstory=(
        'You are a one-person production house, a master of AI-powered generation tools. '
        'You take a script and meticulously create every asset required to build the episode, '
        'ensuring each element matches the script\'s tone and description.'
    ),
    tools=[video_tool, voice_tool, sound_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False,
)