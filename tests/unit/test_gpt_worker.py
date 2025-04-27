import pytest
from unittest.mock import patch, MagicMock
from app.gpt_worker import generate_response

@pytest.fixture
def mock_gpt_response():
    response = MagicMock()
    response.choices = [MagicMock()]
    response.choices[0].message = MagicMock()
    response.choices[0].message.content = "Это тестовый ответ от GPT"
    return response

def test_generate_response_empty_text():
    with pytest.raises(ValueError, match="Input text cannot be empty"):
        generate_response("")

def test_generate_response_invalid_temperature():
    with pytest.raises(ValueError, match="Temperature must be between 0 and 1"):
        generate_response("test", temperature=1.5)

def test_generate_response_invalid_max_tokens():
    with pytest.raises(ValueError, match="Max tokens must be greater than 0"):
        generate_response("test", max_tokens=0)

@patch('app.gpt_worker.client.chat.completions.create')
def test_generate_response_success(mock_completion):
    # Настраиваем мок
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Тестовый ответ"))]
    mock_completion.return_value = mock_response
    
    result = generate_response("Тестовый запрос")
    
    assert result == "Тестовый ответ"
    mock_completion.assert_called_once()

@patch('app.gpt_worker.client.chat.completions.create')
def test_generate_response_api_error(mock_completion):
    # Настраиваем мок для вызова исключения
    mock_completion.side_effect = Exception("API Error")
    
    result = generate_response("Тестовый запрос")
    
    assert result is None
    mock_completion.assert_called_once() 