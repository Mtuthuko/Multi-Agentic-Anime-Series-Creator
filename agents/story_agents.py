# agents/story_agents.py
from crewai import Agent
from core.resources import llm, memory_tool
from config import SERIES_TITLE, INITIAL_STORY_PROMPT

storyline_agent = Agent(
    role='Chief Storyline Officer',
    goal=f'Develop a compelling and continuous storyline for each new episode of the anime series "{SERIES_TITLE}", ensuring it logically follows from previous episodes AND the core premise.',
    backstory=(
        f'You are a master storyteller for the anime series "{SERIES_TITLE}". '
        'Your SOLE FOCUS is the story of Mtuthuko as described in the initial premise. '
        'You MUST NOT deviate from this core story of a boy from a township overcoming hardship through education. '
        f'The initial premise is: {INITIAL_STORY_PROMPT}. '
        'Your job is to write the NEXT chapter of THIS specific story.'
    ),
    tools=[memory_tool],
    llm=llm,
    verbose=True
)

script_writer_agent = Agent(
    role='Lead Script Writer',
    goal='Write a detailed, 5-minute anime script based on the provided episode plot. The script must include scene descriptions, character dialogues, actions, and emotional cues.',
    backstory=(
        'You are a professional scriptwriter known for bringing characters to life. '
        'You translate a high-level plot into a vivid, moment-by-moment script that the production team can follow precisely. '
        'You have a deep understanding of all the characters and their personalities.'
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)