import requests
from config import Config

def transcribe_audio(file_path):
    api_key = Config.OPENAI_API_KEY
    if not api_key:
        raise ValueError('OPENAI_API_KEY not set in environment')
    with open(file_path, "rb") as f:
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={
                "Authorization": f"Bearer {api_key}"
            },
            files={
                "file": (os.path.basename(file_path), f, "audio/wav")
            },
            data={
                "model": "whisper-1"
            }
        )
    if response.status_code != 200:
        raise Exception(f'Whisper API error: {response.text}')
    return response.json().get("text", "")
