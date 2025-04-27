import os
from dotenv import load_dotenv
from pathlib import Path

# Загрузка переменных окружения из .env файла
load_dotenv()

class Config:
    # OpenAI API settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
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
    
    # GPT settings
    GPT_MODEL = os.getenv('GPT_MODEL', 'gpt-3.5-turbo')
    GPT_TEMPERATURE = float(os.getenv('GPT_TEMPERATURE', '0.7'))
    GPT_MAX_TOKENS = int(os.getenv('GPT_MAX_TOKENS', '1000'))
    
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
            
        if not isinstance(cls.GPT_TEMPERATURE, float) or not 0 <= cls.GPT_TEMPERATURE <= 1:
            raise ValueError("GPT_TEMPERATURE must be a float between 0 and 1")
            
        if not isinstance(cls.GPT_MAX_TOKENS, int) or cls.GPT_MAX_TOKENS <= 0:
            raise ValueError("GPT_MAX_TOKENS must be a positive integer") 