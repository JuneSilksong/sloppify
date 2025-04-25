import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from elevenlabs import VoiceSettings

from utils.text_preprocessor import preprocess_text

load_dotenv('eleven_labs.env')


API_KEY = os.getenv("ELEVEN_LABS_API_KEY")


client = ElevenLabs(api_key=API_KEY)

voice_id = "pNInz6obpgDQGcFmaJgB"
output_format = "mp3_44100_128"
model_id = "eleven_flash_v2" 

def tts_output(text, voice_id, filename="tts_output.mp3"):

    try:
        # documentation: https://docs.elevenlabs.io/api/text-to-speech/convert
        response = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format=output_format,
            text=text,
            model_id=model_id,
            voice_settings=VoiceSettings(
                stability=0.25,
                similarity_boost=.3,
                style=0.2,
                speed=1.12,
        
            )
        )

        if isinstance(response, bytes):
            with open(filename, "wb") as f:
                f.write(response)
            print(f"Audio saved as {filename}")
        else:
            audio_data = b''.join(response)
            with open(filename, "wb") as f:
                f.write(audio_data)
            print(f"Audio saved as {filename}")
            
    except Exception as e:
        print(f"Error processing audio data: {e}")
        print(f"Response content: {response}")

