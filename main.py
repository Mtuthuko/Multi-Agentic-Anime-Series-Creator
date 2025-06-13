# main.py
import os
import schedule
import time
from dotenv import load_dotenv
from crewai import Crew, Process

# Load environment variables from .env file
load_dotenv()

# Import agents from their respective files
from agents.story_agents import storyline_agent, script_writer_agent
from agents.production_agents import production_agent
from agents.post_production_agents import compiler_agent, youtube_agent

# Import the task creation function
from tasks.episode_tasks import create_crew_tasks

from utils.file_handler import setup_episode_directory

# --- State Management ---
# In a real production system, you'd use a database or a remote file store.
STATE_FILE = "series_state.txt"

def get_current_episode_id():
    """Reads the current episode number from the state file."""
    if not os.path.exists(STATE_FILE):
        return 1
    with open(STATE_FILE, "r") as f:
        try:
            return int(f.read().strip())
        except (ValueError, IndexError):
            return 1

def save_next_episode_id(episode_id):
    """Saves the next episode number to the state file."""
    with open(STATE_FILE, "w") as f:
        f.write(str(episode_id + 1))

# --- Main Production Function ---
def run_episode_creation_job():
    """Defines and runs the full episode creation crew."""
    print("🚀 Starting new episode creation job...")
    
    episode_id = get_current_episode_id()
    print(f"🎬 --- Creating Episode {episode_id} ---")
    
    # Setup directory for the episode's assets
    episode_path = setup_episode_directory(episode_id)

    # 1. Create the tasks for the current episode
    tasks = create_crew_tasks(episode_id, episode_path)
    
    # 2. Define the Crew
    anime_crew = Crew(
        agents=[storyline_agent, script_writer_agent, production_agent, compiler_agent, youtube_agent],
        tasks=tasks,
        process=Process.sequential,  # Tasks will run one after another
        verbose=True
    )
    
    # 3. Kick off the job
    result = anime_crew.kickoff()
    
    print("\n\n✅ --- Episode Creation Job Finished ---")
    print(f"Episode {episode_id} final result: {result}")
    
    # 4. Update state for the next run
    save_next_episode_id(episode_id)
    print(f"📈 System state updated. Ready for next episode: {episode_id + 1}")


# --- Scheduler ---
if __name__ == "__main__":
    print("🌟 Multi-Agentic Anime Series Creator system is now RUNNING. 🌟")
    
    # For testing purposes, run the job once immediately upon starting the script.
    # For a real daily deployment, you might comment this line out.
    run_episode_creation_job() 
    
    # --- UNCOMMENT FOR DAILY PRODUCTION ---
    # print("\n🕒 Scheduling job for daily execution at 01:00 AM.")
    # schedule.every().day.at("01:00").do(run_episode_creation_job)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(60) # check every minute