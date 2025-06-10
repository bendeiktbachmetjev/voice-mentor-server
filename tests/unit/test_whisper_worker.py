import pytest
import os
from unittest.mock import patch, mock_open, MagicMock
from app.whisper_worker import transcribe_audio

@pytest.fixture
def mock_audio_file():
    return "test_audio.mp3"

@pytest.fixture
def mock_transcript():
    transcript = MagicMock()
    transcript.text = "Это тестовая транскрипция"
    return transcript

def test_transcribe_audio_file_not_found():
    with patch('os.path.exists', return_value=False):
        with pytest.raises(FileNotFoundError):
            transcribe_audio("non_existent_file.mp3")

def test_transcribe_audio_empty_file(tmp_path):
    # Создаем пустой файл
    empty_file = tmp_path / "empty.mp3"
    empty_file.touch()
    
    with pytest.raises(ValueError, match="Audio file is empty"):
        transcribe_audio(str(empty_file))

@patch('app.whisper_worker.client.audio.transcriptions.create')
def test_transcribe_audio_success(mock_transcribe):
    # Настраиваем мок
    mock_transcribe.return_value = MagicMock(text="Тестовая транскрипция")
    
    # Создаем временный файл для теста
    with patch('os.path.exists', return_value=True), \
         patch('os.path.getsize', return_value=1024), \
         patch('builtins.open', mock_open(read_data=b'test audio data')):
        result = transcribe_audio('test_audio.mp3')
        
        assert result == "Тестовая транскрипция"
        mock_transcribe.assert_called_once()

@patch('app.whisper_worker.client.audio.transcriptions.create')
def test_transcribe_audio_api_error(mock_transcribe):
    # Настраиваем мок для вызова исключения
    mock_transcribe.side_effect = Exception("Test API Error")

    with patch('os.path.exists', return_value=True), \
         patch('os.path.getsize', return_value=1024), \
         patch('builtins.open', mock_open(read_data=b'test audio data')):
        with pytest.raises(ValueError) as exc_info:
            transcribe_audio('test_audio.mp3')
        assert str(exc_info.value) == "API Error: Test API Error" 