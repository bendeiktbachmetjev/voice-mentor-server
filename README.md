# Voice Mentor API

Backend API для iOS-приложения Voice Mentor, предоставляющего транскрипцию речи.

## API Endpoints

### POST /process-audio

Обрабатывает аудиофайл и возвращает транскрипцию.

**Параметры запроса:**
- `audio`: Аудиофайл (поддерживаемые форматы: mp3, wav)
- Content-Type: multipart/form-data

**Пример успешного ответа:**
```json
{
    "transcript": "Текст из аудио"
}
```

**Пример использования в Swift:**
```swift
func processAudio(audioData: Data) async throws -> String {
    let url = URL(string: "https://voice-mentor-server.onrender.com/process-audio")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    
    let boundary = UUID().uuidString
    request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
    
    var body = Data()
    body.append("--\(boundary)\r\n".data(using: .utf8)!)
    body.append("Content-Disposition: form-data; name=\"audio\"; filename=\"audio.mp3\"\r\n".data(using: .utf8)!)
    body.append("Content-Type: audio/mpeg\r\n\r\n".data(using: .utf8)!)
    body.append(audioData)
    body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
    
    request.httpBody = body
    
    let (data, response) = try await URLSession.shared.data(for: request)
    
    guard let httpResponse = response as? HTTPURLResponse else {
        throw APIError.invalidResponse
    }
    
    switch httpResponse.statusCode {
    case 200:
        let result = try JSONDecoder().decode(AudioProcessingResult.self, from: data)
        return result.transcript
    case 400:
        throw APIError.invalidRequest
    case 500:
        throw APIError.serverError
    default:
        throw APIError.unknown
    }
}
```

**Коды ошибок:**
- 400: Неверный формат файла или файл не предоставлен
- 500: Внутренняя ошибка сервера

## Локальная разработка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Создайте файл `.env` с переменными окружения:
```
OPENAI_API_KEY=your_api_key
SECRET_KEY=your_secret_key
FLASK_ENV=development
FLASK_DEBUG=1
```

3. Запустите сервер:
```bash
python -m flask run
```

## Тестирование

```bash
export OPENAI_API_KEY=test_key && python -m pytest tests/ -v
```
