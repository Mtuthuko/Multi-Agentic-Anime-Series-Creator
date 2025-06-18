# agents/production_crew_agents.py
from crewai import Agent
from pydantic import BaseModel, Field
from core.resources import (llm, local_image_tool, voice_tool, sfx_tool, music_tool, 
                             local_lip_sync_tool, FaceAnimationTool, compiler_tool)

production_planner = Agent(
    role='Producer and Production Planner',
    goal='Break down a script into a detailed, machine-readable JSON plan for all asset creation and editing.',
    backstory='You are a meticulous producer, the bridge between writers and the technical crew. Your job is to create a perfect JSON blueprint so every other agent knows exactly what to do.',
    llm=llm,
    verbose=True
)

image_artist = Agent(
    role='Local AI Concept Artist',
    goal='Generate all visual assets (character portraits, backgrounds) using a local Text-to-Image model, based on the production plan.',
    backstory='You are a master of local AI image generation. You take prompts from a production plan and bring the world to life on this machine.',
    tools=[local_image_tool],
    llm=llm,
    verbose=True
)

audio_engineer = Agent(
    role='Chief Audio Engineer',
    goal='Generate all audio assets (dialogue, music, SFX) using cloud APIs, based on the production plan.',
    backstory='You have a golden ear and are an expert in AI audio generation. You create the entire auditory experience for the episode.',
    tools=[voice_tool, sfx_tool, music_tool],
    llm=llm,
    verbose=True
)



face_animator = Agent( # Renamed from lip_sync_animator
    role='Face Animation Specialist',
    goal='Create "talking" video clips by animating between a character\'s neutral and open-mouth portraits, timed to their dialogue audio.',
    backstory='You bring characters to life. Using simple but effective animation techniques, you create the illusion of speech, ready for the final edit.',
    tools=[FaceAnimationTool()], # <-- Give it the new, real tool
    llm=llm,
    verbose=True
)

editor = Agent(
    role='Final Editor and Compositor',
    goal='Assemble the final episode by combining all assets (backgrounds, lip-synced videos, music, SFX) according to the production plan.',
    backstory='You are the final gatekeeper of quality. As a master editor, you take all the raw components and stitch them together into a seamless video.',
    tools=[compiler_tool], # Subtitles are part of the compiler tool now
    llm=llm,
    verbose=True
)