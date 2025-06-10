import pytest
import os
import tempfile
import json
from unittest.mock import patch, MagicMock
from app.server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def temp_audio_file():
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        f.write(b"fake audio data")
        f.flush()  # Убедимся, что данные записаны на диск
        yield f.name
        os.unlink(f.name)

def test_process_audio_no_file(client):
    response = client.post('/process-audio')
    assert response.status_code == 400
    assert b"No audio file provided" in response.data

def test_process_audio_empty_file(client):
    with tempfile.NamedTemporaryFile(suffix='.mp3') as f:
        response = client.post('/process-audio', data={'audio': (f, 'test.mp3')})
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['error'] == "Audio file is empty"

def test_process_audio_invalid_file_type(client):
    with tempfile.NamedTemporaryFile(suffix='.txt') as f:
        f.write(b"not an audio file")
        f.seek(0)
        response = client.post('/process-audio', data={'audio': (f, 'test.txt')})
        assert response.status_code == 400
        assert b"Invalid file type" in response.data

@patch('app.whisper_worker.client.audio.transcriptions.create')
def test_process_audio_success(mock_transcribe, client, temp_audio_file):
    # Настраиваем мок
    mock_transcribe.return_value.text = "Test transcription"

    # Создаем тестовый аудио файл и записываем данные
    with open(temp_audio_file, 'wb') as f:
        f.write(b'test audio data')
        f.flush()

    # Отправляем запрос
    with open(temp_audio_file, 'rb') as f:
        data = {}
        data['audio'] = (f, 'test.mp3', 'audio/mpeg')
        response = client.post(
            '/process-audio',
            data=data,
            content_type='multipart/form-data'
        )

    # Проверяем ответ
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['transcript'] == "Test transcription"

    # Проверяем вызов мока
    mock_transcribe.assert_called_once()

@patch('app.whisper_worker.client.audio.transcriptions.create')
def test_process_audio_api_error(mock_transcribe, client, temp_audio_file):
    # Настраиваем мок для симуляции ошибки API
    mock_transcribe.side_effect = Exception("Test API Error")

    # Создаем тестовый аудио файл и записываем данные
    with open(temp_audio_file, 'wb') as f:
        f.write(b'test audio data')
        f.flush()

    # Отправляем запрос
    with open(temp_audio_file, 'rb') as f:
        data = {}
        data['audio'] = (f, 'test.mp3', 'audio/mpeg')
        response = client.post(
            '/process-audio',
            data=data,
            content_type='multipart/form-data'
        )

    # Проверяем ответ
    assert response.status_code == 500
    response_data = response.get_json()
    assert response_data['error'] == "Test API Error" 