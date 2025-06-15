# tools/post_production_tools.py
import os
import replicate
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import requests

# Define the schema using a standard class
class LipSyncToolSchema(BaseModel):
    """Input schema for LipSyncTool."""
    character_image_path: str = Field(..., description="The file path to the character's static portrait image.")
    dialogue_audio_path: str = Field(..., description="The file path to the dialogue audio file.")
    output_video_path: str = Field(..., description="The path where the final lip-synced video will be saved.")

class LipSyncTool(BaseTool):
    name: str = "Lip Sync Generator"
    description: str = "Creates a lip-synced video from a character image and a dialogue audio file."
    args_schema: type[BaseModel] = LipSyncToolSchema # Assign the correct schema class

    def _run(self, character_image_path: str, dialogue_audio_path: str, output_video_path: str) -> str:
        print(f"👄 Generating Lip Sync for {os.path.basename(character_image_path)}...")
        try:
            with open(character_image_path, "rb") as image_file, open(dialogue_audio_path, "rb") as audio_file:
                output_url = replicate.run(
                    "devx/wav2lip:5e35bdc353c42873f1d2b8b99c0d9a6c95353c8427b375bda871578d85d9d7b0",
                    input={
                        "face": image_file,
                        "audio": audio_file
                    }
                )

            response = requests.get(output_url)
            response.raise_for_status()
            
            with open(output_video_path, 'wb') as f:
                f.write(response.content)

            return f"Successfully generated lip-synced video at {output_video_path}"
        except Exception as e:
            return f"Error during lip-sync generation: {e}"


# Define the schema using a standard class
class SubtitleGeneratorToolSchema(BaseModel):
    """Input schema for SubtitleGeneratorTool."""
    audio_path: str = Field(..., description="The file path to the audio file that needs to be transcribed.")

class SubtitleGeneratorTool(BaseTool):
    name: str = "Subtitle Generator (Transcription)"
    description: str = "Transcribes an audio file to generate subtitles using the Whisper model."
    args_schema: type[BaseModel] = SubtitleGeneratorToolSchema # Assign the correct schema class

    def _run(self, audio_path: str) -> str:
        print(f"✍️ Generating Subtitles for {os.path.basename(audio_path)}...")
        try:
            with open(audio_path, "rb") as audio_file:
                output = replicate.run(
                    "openai/whisper:4d50797290df275329f202e48c76360b3f22b08d28c196cbc54600319435f815",
                    input={"audio": audio_file}
                )
            
            transcript = output.get('text', '')
            return transcript if transcript else "Transcription failed or audio was empty."
        except Exception as e:
            return f"Error during transcription: {e}"