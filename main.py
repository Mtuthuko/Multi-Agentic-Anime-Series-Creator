# main.py
import os
import schedule
import time
from dotenv import load_dotenv
from crewai import Crew, Process

# Load environment variables
load_dotenv()

# Import ALL agents
from agents.story_agents import storyline_agent, script_writer_agent
from agents.production_crew_agents import (
    audio_engineer, editor_agent # Change 'production_planner' to 'director_agent'
)
from agents.production_crew_agents import (
    production_planner, scene_compositor_agent, editor_agent
)
from agents.post_production_agents import youtube_agent
from tasks.episode_tasks import create_crew_tasks
from tasks.episode_tasks import create_crew_tasks
# Import the task creation function
from tasks.episode_tasks import create_crew_tasks
from utils.file_handler import setup_episode_directory

# --- State Management (Unchanged) ---
STATE_FILE = "series_state.txt"
# ... (get_current_episode_id and save_next_episode_id functions remain the same) ...
def get_current_episode_id():
    if not os.path.exists(STATE_FILE): return 1
    with open(STATE_FILE, "r") as f:
        try: return int(f.read().strip())
        except: return 1

def save_next_episode_id(episode_id):
    with open(STATE_FILE, "w") as f: f.write(str(episode_id + 1))


# --- Main Production Function ---
def run_episode_creation_job():
    print("🚀 Starting new episode creation job with full production crew...")
    
    episode_id = get_current_episode_id()
    print(f"🎬 --- Creating Episode {episode_id} ---")
    
    episode_path = setup_episode_directory(episode_id)
    os.makedirs("temp_assets", exist_ok=True) # Ensure temp asset dir exists

    tasks = create_crew_tasks(episode_id, episode_path)
    
    # ASSEMBLE THE NEW CREW
    anime_crew = Crew(
        agents=[
            storyline_agent, 
            script_writer_agent,
            production_planner, # Now it exists
            scene_compositor_agent,
            # audio_engineer,
            editor_agent,
            youtube_agent
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

# --- Scheduler (Unchanged) ---
if __name__ == "__main__":
    print("🌟 AI Anime Studio system is now RUNNING. 🌟")
    run_episode_creation_job()