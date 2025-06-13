# agents/story_agents.py
from crewai import Agent
from core.resources import llm, memory_tool
from config import SERIES_TITLE

storyline_agent = Agent(
    role='Chief Storyline Officer',
    goal=f'Develop a compelling and continuous storyline for each new episode of the anime series "{SERIES_TITLE}", ensuring it logically follows from previous episodes.',
    backstory=(
        f'You are a master storyteller for the anime series "{SERIES_TITLE}". '
        'Your job is to remember everything that has happened and craft the next chapter in Mtuthuko\'s life, '
        'focusing on his struggles, growth, and emotions. You use the series memory to maintain continuity.'
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