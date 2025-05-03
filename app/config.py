import os
from dotenv import load_dotenv
from pathlib import Path

# Загрузка переменных окружения из .env файла
load_dotenv()

class Config:
    # OpenAI API settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(Path(__file__).parent.parent, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'm4a'}
    
    # Whisper settings
    WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'whisper-1')
    WHISPER_LANGUAGE = os.getenv('WHISPER_LANGUAGE', 'en')
    
    # Ensure upload folder exists
    @classmethod
    def init_app(cls, app):
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
        
    # Validate configuration
    @classmethod
    def validate_config(cls):
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")
        
        if not os.path.exists(cls.UPLOAD_FOLDER):
            os.makedirs(cls.UPLOAD_FOLDER) 