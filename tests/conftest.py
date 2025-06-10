import os
import sys
import pytest
import tempfile
from app.server import app

# Add the project root directory to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def app_with_temp_folder():
    # Create a temporary folder for file uploads
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
        # Delete the file after use
        try:
            os.unlink(f.name)
        except OSError:
            pass 