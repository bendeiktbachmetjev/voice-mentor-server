import openai
import os
from app.config import Config

def transcribe_audio(audio_file_path):
    """
    Transcribe audio file using OpenAI Whisper API
    
    Args:
        audio_file_path (str): Path to the audio file
        
    Returns:
        str: Transcribed text
        
    Raises:
        FileNotFoundError: If audio file doesn't exist
        ValueError: If API key is not set
        Exception: For other errors during transcription
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
        # Open and read the audio file
        with open(audio_file_path, "rb") as audio_file:
            # Call Whisper API
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                api_key=Config.OPENAI_API_KEY,
                language="en"  # Optional: specify language for better results
            )
            
        # Return the transcribed text
        return transcript["text"]
        
    except openai.error.AuthenticationError:
        raise Exception("Invalid OpenAI API key")
    except openai.error.RateLimitError:
        raise Exception("Rate limit exceeded. Please try again later")
    except openai.error.APIError as e:
        raise Exception(f"OpenAI API error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error in transcription: {str(e)}") 