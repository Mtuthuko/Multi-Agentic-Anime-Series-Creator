# tools/audio_tools.py
import os
import requests
from elevenlabs.client import ElevenLabs
from google.cloud import texttospeech
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr
from typing import Any
from huggingface_hub.inference_api import InferenceApi


class VoiceGeneratorToolSchema(BaseModel):
    dialogue: str = Field(..., description="The dialogue text to be converted to speech.")
    file_path: str = Field(..., description="The local path to save the generated audio file.")
class VoiceGeneratorTool(BaseTool):
    name: str = "Voice Generator"
    description: str = "Generates a real audio file for dialogue using Google Cloud TTS."
    args_schema: type[BaseModel] = VoiceGeneratorToolSchema
    _tts_client: Any = PrivateAttr()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # This tool uses the Google client, NOT ElevenLabs
        self._tts_client = texttospeech.TextToSpeechClient()
    def _run(self, dialogue: str, file_path: str) -> str:
        print(f"🔊 Generating voice for: '{dialogue}'")
        try:
            synthesis_input = texttospeech.SynthesisInput(text=dialogue)
            voice = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Wavenet-D")
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
            # Use the CORRECT client
            response = self._tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as out: out.write(response.audio_content)
            return f"Successfully created voice file at {file_path}"
        except Exception as e: return f"Error generating voice: {e}"


class SfxGeneratorToolSchema(BaseModel):
    prompt: str = Field(..., description="A description of the sound effect.")
    file_path: str = Field(..., description="The local path to save the SFX file.")
class SfxGeneratorTool(BaseTool):
    name: str = "SFX Generator"
    description: str = "Generates a sound effect from a text description via ElevenLabs."
    args_schema: type[BaseModel] = SfxGeneratorToolSchema
    _eleven_client: Any = PrivateAttr()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._eleven_client = ElevenLabs(api_key=os.getenv("ELEVEN_LABS_API_KEY"))
    def _run(self, prompt: str, file_path: str) -> str:
        print(f"🔊 Generating SFX: '{prompt}'")
        try:
            # CORRECTED METHOD CALL
            audio_iterator = self._eleven_client.sound_effects.create(text=prompt)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                for chunk in audio_iterator:
                    f.write(chunk)
            return f"Successfully generated SFX to {file_path}"
        except Exception as e: return f"Error generating SFX: {e}"


class HuggingFaceMusicGeneratorToolSchema(BaseModel):
    prompt: str = Field(..., description="A prompt describing the music's mood.")
    file_path: str = Field(..., description="The local path to save the music file.")
class HuggingFaceMusicGeneratorTool(BaseTool):
    name: str = "Music Generator"
    description: str = "Generates background music from a prompt via Hugging Face."
    args_schema: type[BaseModel] = HuggingFaceMusicGeneratorToolSchema
    _inference_api: Any = PrivateAttr()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        model_id = "facebook/musicgen-small"
        self._inference_api = InferenceApi(repo_id=model_id, token=os.getenv("HUGGING_FACE_API_TOKEN"))
    def _run(self, prompt: str, file_path: str) -> str:
        print(f"🎵 Generating Music via Hugging Face: '{prompt}'")
        try:
            audio_bytes = self._inference_api.text_to_audio(prompt)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f: f.write(audio_bytes)
            return f"Successfully generated music to {file_path}"
        except Exception as e: return f"Error during music generation: {e}"