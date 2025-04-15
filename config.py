import os

class Config:
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    # Можно добавить другие переменные окружения по мере необходимости
