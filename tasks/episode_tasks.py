# tasks/episode_tasks.py
import os
from crewai import Task
from textwrap import dedent
from config import SERIES_TITLE, CHARACTERS
from agents.story_agents import storyline_agent, script_writer_agent
from agents.production_crew_agents import (production_planner, video_director, audio_engineer, editor)

def create_crew_tasks(episode_id: int, episode_path: str, youtube_agent):
    asset_dir = "temp_assets"
    
    task_storyline = Task(description=f"Develop a plot for Episode {episode_id}.", expected_output="A detailed plot summary.", agent=storyline_agent)
    task_script = Task(description="Write a script based on the plot.", expected_output="A full script as a single block of text.", context=[task_storyline], agent=script_writer_agent)

    task_production_plan = Task(
        description=dedent(f"""\
            Read the script and create a detailed JSON production plan.
            This plan MUST ONLY use the asset types that the crew can create: visuals via image-then-video, and audio.
            The JSON MUST have two keys: 'video_plan' and 'audio_plan'.

            1. 'video_plan': A list of scene clips. Each clip object MUST have:
               - 'clip_id': A unique ID (e.g., 'clip_01').
               - 'image_prompt': A detailed text prompt for the 'Image Generator' tool. This prompt MUST be in a cinematic, anime style and include detailed character descriptions from this list: {CHARACTERS}.
               - 'image_path': The file path for this initial frame (e.g., '{asset_dir}/frame_01.png').
               - 'video_path': The file path for the final video clip (e.g., '{asset_dir}/clip_01.mp4').
            
            2. 'audio_plan': A list of all audio assets. Each asset object MUST have:
               - 'audio_id': A unique ID (e.g., 'dialogue_01').
               - 'type': 'dialogue', 'sfx', or 'music'.
               - 'text_or_prompt': The dialogue text for 'dialogue' or a descriptive prompt for 'sfx' and 'music'.
               - 'output_path': The file path (e.g., '{asset_dir}/dialogue_01.mp3').
            """),
        expected_output="A single, valid JSON object with 'video_plan' and 'audio_plan'.",
        context=[task_script],
        agent=production_planner
    )

    task_generate_videos = Task(
        description=dedent("""\
            Execute the 'video_plan' from the JSON production plan.
            For EACH item in the list, you must perform a two-step process:
            1. Use the 'Image Generator' tool with the 'image_prompt' to create the starting frame at 'image_path'.
            2. Once the image is created, use the 'Video Generator (from Image)' tool. The input is the 'image_path', and the output is 'video_path'.
            """),
        expected_output="Confirmation that all frames and video clips have been generated successfully.",
        context=[task_production_plan],
        agent=video_director
    )

    task_generate_audio = Task(
        description=f"Execute the 'audio_plan' from the JSON plan. Use 'Voice Generator' for dialogue, 'SFX Generator' for sfx, and 'Music Generator' for music.",
        expected_output="Confirmation that all audio assets have been generated successfully.",
        context=[task_production_plan],
        agent=audio_engineer
    )

    task_final_edit = Task(
        description=dedent(f"""\
            Assemble the final episode using the 'Video Compiler' tool.
            - Get all 'video_path' values from the 'video_plan' for the 'video_paths' argument.
            - Get all 'output_path' values from the 'audio_plan' for the 'audio_paths' argument.
            - Find the music file for the 'music_path' argument.
            - The final output path is '{os.path.join(episode_path, f"episode_{episode_id}.mp4")}'.
            """),
        expected_output="The full path to the final compiled episode video.",
        context=[task_generate_videos, task_generate_audio, task_production_plan],
        agent=editor
    )

    task_upload = Task(
        description=dedent(f"""\
            The final episode has been created at the path from the previous task. Your job is twofold:
            1. Upload the video file to YouTube. Title it '{SERIES_TITLE} - Episode {episode_id}'. Create a description based on the episode's plot summary.
            2. After uploading, use the 'Series Memory Writer' tool to save the plot summary for episode {episode_id}.
            """),
        expected_output="Confirmation of YouTube upload and memory update.",
        context=[task_final_edit, task_storyline],
        agent=youtube_agent
    )

    return [
        task_storyline, task_script, task_production_plan,
        task_generate_videos, task_generate_audio,
        task_final_edit, task_upload
    ]