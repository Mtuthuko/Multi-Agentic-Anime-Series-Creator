# tools/audio_tools.py
from crewai.tools import BaseTool
import os
import json
from google.cloud import texttospeech

class VoiceGeneratorTool(BaseTool):
    name: str = "Character Voice Generator"
    description: str = "Generates a real audio file for a character's dialogue using a Text-to-Speech API. Input must be a JSON object with 'character', 'dialogue', 'emotion', and 'file_path'."
    tts_client: texttospeech.TextToSpeechClient = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tts_client = texttospeech.TextToSpeechClient()

    def _run(self, voice_data_json: str) -> str:
        """Generates a real audio file using Google Cloud TTS."""
        try:
            voice_data = json.loads(voice_data_json)
            character = voice_data['character']
            dialogue = voice_data['dialogue']
            # The 'emotion' field isn't directly used by standard TTS but is good practice for more advanced services.
            # We can use it to select different voices or pitches in the future.
            file_path = voice_data['file_path']
        except (json.JSONDecodeError, KeyError) as e:
            return f"Error: Invalid JSON input for VoiceGeneratorTool. {e}"

        print(f"🔊 Generating REAL voice for {character}: '{dialogue}'")

        try:
            synthesis_input = texttospeech.SynthesisInput(text=dialogue)

            # TODO: In the future, you can create a mapping of characters to specific voices.
            # For now, we'll use a standard high-quality voice.
            # Find more voices here: https://cloud.google.com/text-to-speech/docs/voices
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US", 
                name="en-US-Wavenet-F", # A good quality female voice
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )

            # We'll use MP3 format as it's efficient.
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            response = self.tts_client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )

            # The response's audio_content is binary. We must write it in 'wb' mode.
            with open(file_path, "wb") as out:
                out.write(response.audio_content)
                
            return f"Successfully created real audio voice file at {file_path}"

        except Exception as e:
            return f"An error occurred during Text-to-Speech generation: {e}"


class SoundTool(BaseTool):
    name: str = "Sound Effect and Music Tool"
    description: str = "Generates or finds a sound effect or music track. Input must be a JSON object with 'type' ('music' or 'sfx'), 'description', and 'file_path'."

    def _run(self, sound_data_json: str) -> str:
        """
        THIS IS STILL A PLACEHOLDER.
        A real implementation would use an AI music/sfx generator (e.g., Suno, AudioCraft)
        or search a licensed sound library API (e.g., Epidemic Sound).
        """
        try:
            sound_data = json.loads(sound_data_json)
            sound_type = sound_data['type']
            description = sound_data['description']
            file_path = sound_data['file_path']
        except (json.JSONDecodeError, KeyError) as e:
            return f"Error: Invalid JSON input for SoundTool. {e}"
        
        print(f"🎵 Generating DUMMY {sound_type}: {description}")
        with open(file_path, "w") as f:
            f.write(f"Placeholder for {sound_type}: {description}")
        return f"Successfully created dummy {sound_type} file at {file_path}"