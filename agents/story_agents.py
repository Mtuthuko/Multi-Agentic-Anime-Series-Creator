# agents/story_agents.py
from crewai import Agent
from core.resources import llm, memory_reader_tool
from config import SERIES_TITLE
from pydantic import BaseModel, Field

storyline_agent = Agent(
    role='Chief Storyline Officer',
    goal=f'Develop a compelling and continuous storyline for each new episode of the anime series "{SERIES_TITLE}".',
    backstory='You are a master storyteller, responsible for crafting the next chapter in the series, focusing on emotional depth and character growth. You always check past episodes for continuity.',
    tools=[memory_reader_tool],
    llm=llm,
    verbose=True
)

script_writer_agent = Agent(
    role='Lead Script Writer',
    goal='Write a detailed, 5-minute anime script based on the provided episode plot, including scenes, dialogue, and actions.',
    backstory='You are a professional scriptwriter known for bringing characters to life. You translate a high-level plot into a vivid script for the production team.',
    llm=llm,
    verbose=True
)