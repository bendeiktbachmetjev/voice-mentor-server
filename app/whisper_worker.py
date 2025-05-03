from openai import OpenAI
from app.config import Config
import logging

logger = logging.getLogger(__name__)

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def transcribe_audio(file_path: str) -> str:
    """
    Transcribe audio file using OpenAI Whisper API
    
    Args:
        file_path (str): Path to audio file
        
    Returns:
        str: Transcribed text
        
    Raises:
        ValueError: If API key is not set or file doesn't exist
        Exception: For other API errors
    """
    if not Config.OPENAI_API_KEY:
        raise ValueError("OpenAI API key is not set in environment variables")
        
    try:
        with open(file_path, 'rb') as audio_file:
            logger.info(f"Starting transcription for file: {file_path}")
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=Config.WHISPER_LANGUAGE
            )
            logger.info("Transcription completed successfully")
            return response.text
            
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        raise Exception(f"Error during transcription: {str(e)}") 