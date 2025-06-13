# utils/file_handler.py
import os
from datetime import datetime

def setup_episode_directory(episode_id: int):
    """Creates a directory for the current episode's assets."""
    today = datetime.now().strftime("%Y-%m-%d")
    path = f"episodes/episode_{episode_id}_{today}"
    os.makedirs(path, exist_ok=True)
    return path