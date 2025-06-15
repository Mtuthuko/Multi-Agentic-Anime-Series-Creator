# tools/audio_tools.py
import os
import requests
from elevenlabs.client import ElevenLabs
from google.cloud import texttospeech
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from gradio_client import Client

# --- SCHEMA AND TOOL FOR VOICE GENERATOR ---
class VoiceGeneratorToolSchema(BaseModel):
    """Input schema for VoiceGeneratorTool."""
    dialogue: str = Field(..., description="The exact line of dialogue to be converted to speech.")
    file_path: str = Field(..., description="The local path to save the generated audio file.")

class VoiceGeneratorTool(BaseTool):
    name: str = "Character Voice Generator"
    description: str = "Generates a real audio file for a character's dialogue using a Text-to-Speech API."
    args_schema: type[BaseModel] = VoiceGeneratorToolSchema
    tts_client: texttospeech.TextToSpeechClient = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tts_client = texttospeech.TextToSpeechClient()

    def _run(self, dialogue: str, file_path: str) -> str:
        print(f"🔊 Generating REAL voice for dialogue: '{dialogue}'")
        try:
            synthesis_input = texttospeech.SynthesisInput(text=dialogue)
            voice = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Wavenet-F")
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
            response = self.tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as out:
                out.write(response.audio_content)
            return f"Successfully created real audio voice file at {file_path}"
        except Exception as e:
            return f"An error occurred during Text-to-Speech generation: {e}"


# --- SCHEMA AND TOOL FOR SFX GENERATOR ---
class SfxGeneratorToolSchema(BaseModel):
    """Input schema for SfxGeneratorTool."""
    prompt: str = Field(..., description="A description of the sound effect, e.g., 'a door creaking open'.")
    file_path: str = Field(..., description="The local path to save the generated SFX audio file.")

class SfxGeneratorTool(BaseTool):
    name: str = "Sound Effect (SFX) Generator"
    description: str = "Generates a sound effect based on a text description using the ElevenLabs API."
    args_schema: type[BaseModel] = SfxGeneratorToolSchema
    eleven_client: ElevenLabs = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        api_key = os.getenv("ELEVEN_LABS_API_KEY")
        if not api_key:
            raise ValueError("ELEVEN_LABS_API_KEY not found in environment variables.")
        self.eleven_client = ElevenLabs(api_key=api_key)

    def _run(self, prompt: str, file_path: str) -> str:
        print(f"🔊 Generating SFX with prompt: '{prompt}'")
        try:
            audio_bytes_iterator = self.eleven_client.sounds.generate_from_text(text=prompt)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                for chunk in audio_bytes_iterator:
                    f.write(chunk)
            return f"Successfully generated SFX and saved to {file_path}"
        except Exception as e:
            return f"Error generating SFX: {e}"


# --- SCHEMA AND TOOL FOR MUSIC GENERATOR ---
class MusicGeneratorToolSchema(BaseModel):
    """Input schema for MusicGeneratorTool."""
    prompt: str = Field(..., description="A prompt describing the music's mood, e.g., 'sad, melancholic, lofi hip hop'.")
    file_path: str = Field(..., description="The local path to save the generated music file.")

class MusicGeneratorTool(BaseTool):
    name: str = "Background Music Generator"
    description: str = "Generates a short background music track based on a descriptive prompt using a Hugging Face Space."
    args_schema: type[BaseModel] = MusicGeneratorToolSchema
    
    def _run(self, prompt: str, file_path: str) -> str:
        print(f"🎵 Generating Music via Gradio Client: '{prompt}'")
        try:
            client = Client("fffiloni/riffusion-app")
            result = client.predict(
                prompt_a=prompt,
                api_name="/predict"
            )
            generated_audio_path = result['audio']
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(generated_audio_path, 'rb') as f_in, open(file_path, 'wb') as f_out:
                f_out.write(f_in.read())
            return f"Successfully generated music and saved to {file_path}"
        except Exception as e:
            return f"An unexpected error occurred during music generation: {e}"