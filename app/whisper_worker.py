from openai import OpenAI
import os
from typing import Optional
from app.config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribe audio file using OpenAI Whisper API
    
    Args:
        audio_file_path (str): Path to the audio file
        
    Returns:
        str: Transcribed text
        
    Raises:
        FileNotFoundError: If audio file doesn't exist
        ValueError: If file is empty, API key is not set, or API error occurs
    """
    # Check if file exists
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
    
    # Check if file is not empty
    if os.path.getsize(audio_file_path) == 0:
        raise ValueError("Audio file is empty")
    
    # Check if API key is set
    if not Config.OPENAI_API_KEY:
        raise ValueError("OpenAI API key is not set in environment variables")
    
    try:
        with open(audio_file_path, 'rb') as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            if not transcription.text:
                raise ValueError("Transcription returned empty text")
            return transcription.text
    except Exception as e:
        raise ValueError(f"API Error: {str(e)}") 