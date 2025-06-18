# agents/production_crew_agents.py
from crewai import Agent
from core.resources import (llm, hf_image_tool, hf_video_tool, 
                             voice_tool, sfx_tool, hf_music_tool, compiler_tool)

production_planner = Agent(
    role='Producer and Scene Planner',
    goal='Break down a script into a detailed, machine-readable JSON plan for asset generation using the available tools.',
    backstory='You are a meticulous producer. You create a perfect JSON blueprint so every other agent knows exactly what to create and how it all fits together.',
    llm=llm,
    verbose=True
)

video_director = Agent(
    role='AI Video Director',
    goal='Create all visual video clips using Hugging Face APIs. This is a two-step process: first generate a starting image, then generate a video from that image.',
    backstory='You are a master of remote AI APIs. You direct the visual creation process, ensuring each scene starts with a perfect frame and is then brought to life.',
    tools=[hf_image_tool, hf_video_tool],
    llm=llm,
    verbose=True
)

audio_engineer = Agent(
    role='Chief Audio Engineer',
    goal='Generate all audio assets: dialogue, music, and sound effects, based on the production plan.',
    backstory='You have a golden ear and are an expert in AI audio generation. You create the entire auditory experience for the episode.',
    tools=[voice_tool, sfx_tool, hf_music_tool],
    llm=llm,
    verbose=True
)

editor = Agent(
    role='Final Editor',
    goal='Assemble the final episode by stitching together all generated video clips and layering the complete audio track.',
    backstory='You are the master editor. You take the raw video clips and audio tracks and combine them into a single, cohesive final product.',
    tools=[compiler_tool],
    llm=llm,
    verbose=True
)