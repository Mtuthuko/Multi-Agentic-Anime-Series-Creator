# tasks/episode_tasks.py
import os
from crewai import Task
from config import SERIES_TITLE, CHARACTERS 
from textwrap import dedent

# Import all agents
# Import the NEW lean crew
from agents.story_agents import storyline_agent, script_writer_agent
from agents.production_crew_agents import production_planner, audio_engineer, editor_agent # Change 'production_planner' to 'director_agent'
from agents.post_production_agents import youtube_agent
from agents.production_crew_agents import scene_compositor_agent, audio_engineer, editor_agent
from core.resources import llm, image_tool, ken_burns_tool, voice_tool, music_tool, sfx_tool, compiler_tool


def create_crew_tasks(episode_id: int, episode_path: str):
    """Creates and returns a list of all tasks for the new, complex episode creation process."""

    # Define a shared temporary asset directory
    asset_dir = "temp_assets"
    
    # 1. Pre-Production Tasks
    task_storyline = Task(
        description=f"""Develop the plot for Episode {episode_id} of '{SERIES_TITLE}'.
        You MUST adhere strictly to the established backstory of Mtuthuko, his family, and their struggles in the KwaThema township.
        DO NOT introduce fantasy or sci-fi elements like 'Neo-Khaya' or 'Guardians'. The story is a realistic drama about overcoming adversity.
        Use the memory tool to check the summary of the previous episode and continue the story from there.
        For Episode 1, start the story from the moment Mtuthuko and his family are forced to move into the shack.
        """,
        expected_output=f"A detailed, realistic plot summary for Episode {episode_id} that continues Mtuthuko's real-life story.",
        agent=storyline_agent
    )

    task_script = Task(
        description="Based on the plot, write a complete 5-minute anime script with clear scene descriptions, dialogue, and action notes.",
        expected_output="A full script as a single block of text.",
        context=[task_storyline],
        agent=script_writer_agent
    )

    

    # 2. Audio Design Task
    task_production_plan = Task(
        description=dedent(f"""\
            Read the script and create a JSON plan that breaks the episode into scenes.
            The plan should be a list of "scene" objects. Each object needs:
            1.  'scene_number': The sequence number.
            2.  'background_prompt': A detailed prompt for the scene's background image.
            3.  'dialogue': The line of dialogue spoken in this scene.
            4.  'file_paths': An object containing the names for the files to be created:
                - 'background_image': e.g., '{asset_dir}/scene_01_bg.png'
                - 'dialogue_audio': e.g., '{asset_dir}/scene_01_audio.mp3'
                - 'final_clip': e.g., '{asset_dir}/scene_01_clip.mp4'

            Example scene object:
            {{
                "scene_number": 1,
                "background_prompt": "A cramped corrugated iron shack. Sunlight streams through cracks...",
                "dialogue": "Another day...",
                "file_paths": {{
                    "background_image": "temp_assets/scene_01_bg.png",
                    "dialogue_audio": "temp_assets/scene_01_audio.mp3",
                    "final_clip": "temp_assets/scene_01_clip.mp4"
                }}
            }}
            """),
        agent=production_planner, # The planner agent is back, but simpler
        context=[task_script],
        expected_output="A valid JSON object which is a list of scene plans."
    )
    
    # 3. Scene Composition Task
    task_compose_scenes = Task(
    description="""
    Take the JSON plan of scenes. For each scene in the plan, execute the following steps:
    1. Use the 'Still Scene Image Generator' with the 'background_prompt' to create the background image.
    2. **If the 'dialogue' field is not empty or null**, use the 'Character Voice Generator' with the 'dialogue' to create the audio file.
    3. **If the 'dialogue' field is not empty or null**, use the 'Ken Burns Effect Video Creator' with the paths to the image and audio you just created to produce the final video clip.
    4. **If the 'dialogue' field IS empty or null**, just create a 3-second silent video clip from the background image using the Ken Burns tool (you can pass a dummy audio path, the tool should handle it, or we can improve the tool).

    Ensure every scene from the plan is converted into a final video clip, whether it has dialogue or not.
    """,
    agent=scene_compositor_agent,
    context=[task_production_plan],
    expected_output="Confirmation that all scenes have been processed and their final video clips have been created."
    )
    
    # 4. Final Edit (Now simpler: just stitch clips and add music)
    task_final_edit = Task(
        description=f"""
        Take all the generated scene clips from '{asset_dir}' (scene_01_clip.mp4, etc.) and compile them.
        Generate a main music track and layer it over the final video.
            Save the final episode to '{os.path.join(episode_path, f'episode_{episode_id}.mp4')}'.
            """,
            agent=editor_agent,
            tools=[compiler_tool, music_tool], # The editor can also make music now
            context=[task_compose_scenes],
            expected_output="The full path to the final compiled video file."
        )
     
    


    # 5. Distribution Task
    task_upload = Task(
        description=f"Upload the final video file to YouTube with title '{SERIES_TITLE} - Episode {episode_id}'. Also, save a summary of the episode's plot (from the first task) to the long-term memory.",
        expected_output="Confirmation of YouTube upload and memory update.",
        context=[task_final_edit, task_storyline],
        agent=youtube_agent
    )

    return [
        task_storyline, 
        task_script, 
        task_production_plan,
        task_compose_scenes,
        task_final_edit,
        task_upload
    ]