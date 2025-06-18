# tools/audio_tools.py
import os
import json
import replicate
import requests
from elevenlabs.client import ElevenLabs
from google.cloud import texttospeech
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr
from typing import Any

# --- VOICE GENERATOR (CORRECTED) ---
class VoiceGeneratorToolSchema(BaseModel):
    """Input schema for VoiceGeneratorTool."""
    dialogue: str = Field(..., description="The dialogue text to be converted to speech.")
    file_path: str = Field(..., description="The local path to save the generated audio file.")

class VoiceGeneratorTool(BaseTool):
    name: str = "Character Voice Generator"
    description: str = "Generates a real audio file for dialogue using Google Cloud TTS."
    args_schema: type[BaseModel] = VoiceGeneratorToolSchema # 2. Assign the new schema
    _tts_client: Any = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tts_client = texttospeech.TextToSpeechClient()

    # 3. Update _run to accept named arguments, not a JSON string
    def _run(self, dialogue: str, file_path: str) -> str:
        print(f"🔊 Generating voice for: '{dialogue}'")
        try:
            synthesis_input = texttospeech.SynthesisInput(text=dialogue)
            voice = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Wavenet-F")
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
            response = self._tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
            with open(file_path, "wb") as out: out.write(response.audio_content)
            return f"Successfully created voice file at {file_path}"
        except Exception as e:
            return f"Error generating voice: {e}"
# --- SFX GENERATOR (CORRECTED) ---
class SfxGeneratorToolSchema(BaseModel):
    prompt: str = Field(..., description="A description of the sound effect.")
    file_path: str = Field(..., description="The local path to save the SFX file.")

class SfxGeneratorTool(BaseTool):
    name: str = "Sound Effect (SFX) Generator"
    description: str = "Generates a sound effect from a text description via ElevenLabs."
    args_schema: type[BaseModel] = SfxGeneratorToolSchema
    _eleven_client: Any = PrivateAttr() # Define as private attribute

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._eleven_client = ElevenLabs(api_key=os.getenv("ELEVEN_LABS_API_KEY"))

    def _run(self, prompt: str, file_path: str) -> str:
        print(f"🔊 Generating SFX: '{prompt}'")
        try:
            audio = self._eleven_client.text_to_sound_effects.create(text=prompt)
            with open(file_path, "wb") as f: f.write(audio)
            return f"Successfully generated SFX to {file_path}"
        except Exception as e: return f"Error generating SFX: {e}"

# --- MUSIC GENERATOR (No changes needed as it had no internal state) ---
class MusicGeneratorToolSchema(BaseModel):
    prompt: str = Field(..., description="A prompt describing the music's mood.")
    file_path: str = Field(..., description="The local path to save the music file.")

class MusicGeneratorTool(BaseTool):
    name: str = "Background Music Generator"
    description: str = "Generates background music from a prompt via Replicate."
    args_schema: type[BaseModel] = MusicGeneratorToolSchema
    
    def _run(self, prompt: str, file_path: str) -> str:
        print(f"🎵 Generating Music: '{prompt}'")
        try:
            output_url = replicate.run("riffusion/riffusion:8cf61ea6c56afd61d8f5b9ffd14d7c216c0a93844ce2d82ac1c9ecc9c7f24e05", input={"prompt_a": prompt})
            response = requests.get(output_url['audio'])
            response.raise_for_status()
            with open(file_path, 'wb') as f: f.write(response.content)
            return f"Successfully generated music to {file_path}"
        except Exception as e: return f"Error during music generation: {e}"