# main.py
import os
import schedule
import time
from dotenv import load_dotenv
from crewai import Agent, Crew, Process

# Load environment variables first
load_dotenv()

from agents.story_agents import storyline_agent, script_writer_agent
from agents.production_crew_agents import (
    production_planner, video_director, audio_engineer, editor, video_director
)
from tasks.episode_tasks import create_crew_tasks
from utils.file_handler import setup_episode_directory
from core.resources import youtube_tool, memory_writer_tool, llm

# --- State Management ---
STATE_FILE = "series_state.txt"
def get_current_episode_id():
    if not os.path.exists(STATE_FILE): return 1
    with open(STATE_FILE, "r") as f:
        try: return int(f.read().strip())
        except: return 1

def save_next_episode_id(episode_id):
    with open(STATE_FILE, "w") as f: f.write(str(episode_id + 1))

# --- Main Production Function ---
def run_episode_creation_job():
    print("🚀 Starting Local Visuals episode creation job...")
    
    episode_id = get_current_episode_id()
    print(f"🎬 --- Creating Episode {episode_id} ---")
    
    episode_path = setup_episode_directory(episode_id)
    os.makedirs("temp_assets", exist_ok=True)

    # Define YouTube Agent here for clarity
    youtube_agent = Agent(
        role='Digital Distribution Manager',
        goal='Upload the final anime episode to YouTube and update the series memory.',
        backstory='You handle the final step of bringing the series to the world and ensuring the system remembers its creation.',
        tools=[youtube_tool, memory_writer_tool],
        llm=llm,
        verbose=True
    )

    tasks = create_crew_tasks(episode_id, episode_path, youtube_agent)
    
    anime_crew = Crew(
        agents=[
            storyline_agent, script_writer_agent, production_planner,
             audio_engineer, video_director, editor, youtube_agent
        ],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    result = anime_crew.kickoff()
    
    print("\n\n✅ --- Episode Creation Job Finished ---")
    print(f"Episode {episode_id} final result: {result}")
    
    save_next_episode_id(episode_id)
    print(f"📈 System state updated. Ready for next episode: {episode_id + 1}")

if __name__ == "__main__":
    print("🌟 AI Anime Studio (Local Visuals) system is now RUNNING. 🌟")
    print("The first run will download several GB of models. Please be patient.")
    run_episode_creation_job()