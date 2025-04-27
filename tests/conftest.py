import os
import sys
import pytest
import tempfile
from app.server import app

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def app_with_temp_folder():
    # Создаем временную папку для загрузки файлов
    with tempfile.TemporaryDirectory() as temp_dir:
        app.config['UPLOAD_FOLDER'] = temp_dir
        app.config['TESTING'] = True
        yield app

@pytest.fixture
def client(app_with_temp_folder):
    return app_with_temp_folder.test_client()

@pytest.fixture
def temp_audio_file():
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        yield f.name
        # Удаляем файл после использования
        try:
            os.unlink(f.name)
        except OSError:
            pass 