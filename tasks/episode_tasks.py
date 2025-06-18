# tasks/episode_tasks.py
import os
from crewai import Task
from textwrap import dedent
from config import SERIES_TITLE 

from agents.story_agents import storyline_agent, script_writer_agent
from agents.production_crew_agents import (
    production_planner, video_director, audio_engineer, face_animator, editor
)
from core.resources import youtube_tool # Assuming youtube_tool is in core resources now

def create_crew_tasks(episode_id: int, episode_path: str, youtube_agent):
    asset_dir = "temp_assets"
    
    task_storyline = Task(
        description=f"Develop the plot for Episode {episode_id}.",
        expected_output="A detailed plot summary.",
        agent=storyline_agent
    )
    task_script = Task(
        description="Write a complete 5-minute anime script based on the plot.",
        expected_output="A full script as text.",
        context=[task_storyline],
        agent=script_writer_agent
    )
    task_production_plan = Task(
        description=dedent(f"""Read the script and create a detailed JSON production plan with 'asset_list' and 'timeline' keys. Ensure all file paths use '{asset_dir}/' and are unique."""),
        expected_output="A single, valid JSON object containing the full production plan.",
        context=[task_script],
        agent=production_planner
    )
    task_generate_images = Task(
        description=f"Read the 'asset_list' in the JSON plan. Use the Local Image Generator tool to create every image asset.",
        expected_output="Confirmation that all image assets have been generated.",
        context=[task_production_plan],
        agent=video_director
    )
    task_generate_audio = Task(
        description=f"Read the 'asset_list' in the JSON plan. Use audio tools to create all dialogue, SFX, and music assets.",
        expected_output="Confirmation that all audio assets have been generated.",
        context=[task_production_plan],
        agent=audio_engineer
    )
    task_animate_faces = Task(
        description=f"Read the 'timeline' in the JSON production plan. For every entry in each scene's 'dialogue_sequence', use the Face Animation Generator tool. Use the 'neutral_character_image', 'talking_character_image', and 'dialogue_audio' file paths as inputs, and save the result to the 'animated_video' file path.",
        expected_output="Confirmation that all animated 'talking' videos have been generated for every line of dialogue.",
        context=[task_generate_images, task_generate_audio],
        agent=video_director # Use the new agent name
    )
    task_final_edit = Task(
        description=f"Assemble the final episode using the Video Compiler tool, saving to '{os.path.join(episode_path, f'episode_{episode_id}.mp4')}'.",
        expected_output="The full path to the final compiled video.",
        context=[task_animate_faces],
        agent=editor
    )
    task_upload = Task(
        description=dedent(f"""\
            The final episode has been created. Your job is twofold:
            1. Upload the final video file to YouTube. The file is located at the path provided from the previous task. The title should be '{SERIES_TITLE} - Episode {episode_id}'. Create an engaging description based on the episode's plot summary.
            2. After a successful upload, use the Series Memory Writer Tool to save the plot summary for this episode. You will need to provide the 'episode_id' ({episode_id}) and the 'summary' text from the first task.
            """),
        expected_output="A confirmation of both the successful YouTube upload (with Video ID) and the successful memory update.",
        context=[task_final_edit, task_storyline],
        agent=youtube_agent
    )

    return [
        task_storyline, task_script, task_production_plan,
        task_generate_images, task_generate_audio,
        task_animate_faces, task_final_edit, task_upload
    ]