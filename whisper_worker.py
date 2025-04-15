import requests
import os

def transcribe_audio(file_path):
    with open(file_path, "rb") as f:
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
            },
            files={
                "file": (file_path, f, "audio/wav")
            },
            data={
                "model": "whisper-1"
            }
        )
    return response.json()["text"]
