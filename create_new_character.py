# create_new_character.py
from crewai import Task, Crew
from agents.character_agents import character_creator_agent
from dotenv import load_dotenv
import textwrap

# Load environment variables
load_dotenv()

def run_character_creation():
    """A utility script to generate a new character for the series."""
    print("--- Character Creation Utility ---")
    
    # Get input from the user (the "showrunner")
    character_concept = input(textwrap.dedent("""
        Enter a brief concept for the new character. 
        For example: 'A cynical but brilliant senior Data Scientist at FNB who becomes Mtuthuko's rival.'
        > """))
    
    # Create the character creation task
    task_create_character = Task(
        description=(
            f"Based on the concept: '{character_concept}', create a full character sheet. "
            "The sheet must include:\n"
            "1.  **Name:** (A suitable South African name)\n"
            "2.  **Age:**\n"
            "3.  **Personality:** (At least 3-4 key traits)\n"
            "4.  **Backstory:** (How they got to where they are)\n"
            "5.  **Motivation:** (What drives them?)\n"
            "6.  **Relationship to Mtuthuko:** (e.g., mentor, rival, friend, antagonist)\n"
            "7.  **Visual Description:** (Detailed description of their appearance, style of dress, and typical expression)."
        ),
        expected_output="A complete, well-formatted character sheet as a block of text.",
        agent=character_creator_agent
    )
    
    # Create and run a temporary crew for this one-off task
    character_crew = Crew(
        agents=[character_creator_agent],
        tasks=[task_create_character],
        verbose=2
    )
    
    print("\nGenerating character... please wait.\n")
    character_sheet = character_crew.kickoff()
    
    print("\n--- ✨ New Character Sheet Generated! ---")
    print(character_sheet)
    print("\n-------------------------------------------")
    print("\nACTION REQUIRED: Please copy the character's details and add them to the CHARACTERS dictionary in `config.py` to make them a permanent part of the series.")

if __name__ == "__main__":
    run_character_creation()