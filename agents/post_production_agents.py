# agents/post_production_agents.py
from crewai import Agent
from core.resources import llm, compiler_tool, youtube_tool, memory_tool

compiler_agent = Agent(
    role='Post-Production Editor',
    goal='Compile all the generated video and audio assets into a single, cohesive 5-minute video file.',
    backstory=(
        'You are a meticulous editor. Your job is to take all the raw pieces from the production team '
        'and stitch them together into a final, polished episode, ready for distribution.'
    ),
    tools=[compiler_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

youtube_agent = Agent(
    role='Digital Distribution Manager',
    goal='Upload the final anime episode to the YouTube channel and update the series memory with a summary of the new episode.',
    backstory=(
        'You are in charge of bringing the series to the world. You handle the technical details of uploading the content '
        'and, crucially, you ensure the system remembers what it created by logging a summary of the episode '
        'for future continuity.'
    ),
    tools=[youtube_tool, memory_tool],
    llm=llm,
    verbose=True
)