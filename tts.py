import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

load_dotenv('eleven_labs.env')


API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
client = ElevenLabs(api_key=API_KEY)

voice_id = "pNInz6obpgDQGcFmaJgB"
output_format = "mp3_44100_128"
model_id = "eleven_multilingual_v2" 

def tts_output(text, voice_id, filename="tts_output.mp3"):

    try:
        # documentation: https://docs.elevenlabs.io/api/text-to-speech/convert
        response = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format=output_format,
            text=text,
            model_id=model_id
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

if __name__ == "__main__":
    text = "If you shit in the sink at exactly 4:20 am and yell “amogus” 69 times,a shadowy figured called mom will come to beat you up and you will wake up in a place called the orphanage "
    tts_output(text, voice_id, "elevenlabs_output.mp3")
