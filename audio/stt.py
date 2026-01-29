import os
from deepgram import DeepgramClient, PrerecordedOptions
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

def transcribe(audio_path: str) -> str:
    """
    Speech to text using Deepgram.
    Works perfectly with Streamlit.
    """

    if not DEEPGRAM_API_KEY:
        return "Deepgram API key not found"

    try:
        dg_client = DeepgramClient(DEEPGRAM_API_KEY)

        with open(audio_path, "rb") as audio:
            payload = {"buffer": audio, "mimetype": "audio/wav"}

            options = PrerecordedOptions(
                model="nova-2",
                language="en",
                smart_format=True,
                punctuate=True
            )

            response = dg_client.listen.prerecorded.v("1").transcribe_file(
                payload, options
            )

            transcript = (
                response["results"]["channels"][0]
                ["alternatives"][0]["transcript"]
            )

            return transcript.strip()

    except Exception as e:
        return f"STT error: {str(e)}"
