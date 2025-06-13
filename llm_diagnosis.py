# main.py
import os
import schedule
import time
from dotenv import load_dotenv

# --- NEW DIAGNOSTIC CODE ---
# We will add this block to test the API key directly.
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

def run_api_diagnostic():
    """A simple function to test the Google API key and model access."""
    print("--- 🩺 Running Google API Diagnostic Test ---")
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ ERROR: GOOGLE_API_KEY environment variable not found.")
            print("   Please ensure your .env file is in the root directory and correctly formatted.")
            return False

        print(f"🔑 Found API Key starting with: {api_key[:4]}...{api_key[-4:]}")
        
        genai.configure(api_key=api_key)
        
        print("✅ API Key configured successfully.")
        print("🧠 Attempting to list available models...")
        
        # This is a simple, free API call that should work if the key is valid.
        models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        model_names = [m.name for m in models]
        print(f"✅ Successfully listed {len(model_names)} models.")

        # Check for the specific model we want to use
        target_model = "models/gemini-1.5-flash-latest"
        if target_model in model_names:
            print(f"✅ Target model '{target_model}' is available!")
        else:
            print(f"⚠️ WARNING: Target model '{target_model}' not found in the list of available models.")
            print("   Available models for content generation:")
            for m in sorted(model_names):
                print(f"     - {m}")
            print("   The script might fail if the model is not available to your account.")

        print("--- ✅ Diagnostic Test Passed ---")
        return True

    except Exception as e:
        print(f"--- ❌ DIAGNOSTIC TEST FAILED ---")
        print(f"An error occurred during the API diagnostic test: {e}")
        print("This indicates a fundamental problem with your API key, billing, or enabled APIs in Google Cloud.")
        return False

# --- END OF NEW DIAGNOSTIC CODE ---


# Import agents from their respective files
from agents.story_agents import storyline_agent, script_writer_agent
# ... (rest of your imports)

# ... (rest of your existing code: get_current_episode_id, save_next_episode_id, etc.)

# --- Main Production Function ---
def run_episode_creation_job():
    """Defines and runs the full episode creation crew."""
    # ... (the existing code for this function)

# --- Scheduler ---
if __name__ == "__main__":
    print("🌟 Multi-Agentic Anime Series Creator system is now RUNNING. 🌟")
    
    # Run the diagnostic test before starting the crew
    if run_api_diagnostic():
        # For testing purposes, run the job once immediately upon starting the script.
        run_episode_creation_job() 
    else:
        print("\nHalting execution due to failed API diagnostic. Please resolve the issues above.")

    # --- UNCOMMENT FOR DAILY PRODUCTION ---
    # ... (rest of the scheduler code)