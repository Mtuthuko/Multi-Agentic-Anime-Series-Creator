# agents/character_agents.py
from crewai import Agent
from core.resources import llm
# Note: This agent might use a visual tool in the future
# from core.resources import image_generation_tool

character_creator_agent = Agent(
    role='Expert Character Designer for Anime',
    goal='Create a new, unique, and compelling character for an ongoing anime series, including their personality, backstory, motivations, and a detailed visual description.',
    backstory=(
        'You are a world-renowned character designer, famous for creating iconic and memorable anime characters. '
        'You have a deep understanding of archetypes, character arcs, and visual storytelling. '
        'Your descriptions are so vivid that a scriptwriter can immediately understand how the character speaks and acts, '
        'and an artist knows exactly how to draw them.'
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# In the future, you could add a dedicated visual agent
# character_visuals_agent = Agent(
#     role='Anime Concept Artist',
#     goal='Generate a consistent set of visual reference images for a character based on their description.',
#     backstory='You are a master artist who can take a written description and create a definitive visual representation of a character, including turnarounds and expression sheets.',
#     tools=[image_generation_tool], # e.g., a DALL-E or Midjourney tool
#     llm=llm
# )