# agents/production_crew_agents.py
from crewai import Agent
from core.resources import llm, image_tool, ken_burns_tool, voice_tool, music_tool, sfx_tool, compiler_tool #, first_frame_tool, animate_tool

production_planner = Agent(
    role='Producer and Production Planner',
    goal='Break down a script into a detailed, machine-readable JSON plan. This plan will define every scene, the required visual prompt, the dialogue, and the file paths for all assets.',
    backstory='You are a meticulous producer. You are the bridge between the creative writers and the technical production crew. Your job is to create a perfect blueprint so that every other agent knows exactly what to create and how it all fits together. You do not generate any assets yourself, you ONLY create the plan.',
    llm=llm,
    verbose=True,
    allow_delegation=False, # This agent should not delegate its core planning task
)

scene_compositor_agent = Agent(
    role='Scene Compositor',
    goal='Execute the JSON production plan by generating the necessary visual and audio assets for each scene and combining them into a final video clip.',
    backstory='You are a master of efficient filmmaking. You take a scene-by-scene plan and use your tools to generate the background image, create the voice-over, and then combine them into a compelling video clip with a subtle zoom effect.',
    tools=[image_tool, voice_tool, ken_burns_tool],
    llm=llm,
    verbose=True
)

# Audio Engineer is now simpler
audio_engineer = Agent(
    role='Sound Designer & Composer',
    goal='Create the overall soundscape: background music and ambient sound effects.',
    backstory='You set the mood. Your job is to generate a background music track and key sound effects that will be layered over the final video edit.',
    tools=[music_tool, sfx_tool],
    llm=llm,
    verbose=True
)

editor_agent = Agent(
    role='Final Video Editor',
    goal='Assemble all the final scene video clips and the main music track into a single, cohesive final episode.',
    backstory='You are the master of post-production. You take the finished scene clips and a music track and edit them together into a polished, professional final product, ready for distribution.',
    tools=[compiler_tool, music_tool], # The editor can also create the main theme
    llm=llm,
    verbose=True
)