# Voice Mentor API

Backend API for iOS application Voice Mentor, providing speech transcription.

## API Endpoints

### POST /process-audio

Processes an audio file and returns the transcription.

**Request Parameters:**
- `audio`: Audio file (supported formats: mp3, wav)
- Content-Type: multipart/form-data

**Example of successful response:**
```json
{
    "transcript": "Text from audio"
}
```

**Example of usage in Swift:**
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

**Error Codes:**
- 400: Invalid file format or file not provided
- 500: Internal server error

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with environment variables:
```
OPENAI_API_KEY=your_api_key
SECRET_KEY=your_secret_key
FLASK_ENV=development
FLASK_DEBUG=1
```

3. Start the server:
```bash
python -m flask run
```

## Testing

```bash
export OPENAI_API_KEY=test_key && python -m pytest tests/ -v
```

## Новое: Voice Activity Detection (VAD)

Если вы отправляете .wav-файл (16kHz, моно), сервер сначала выделяет только участки с речью (VAD), а потом уже распознаёт их. Это помогает убрать тишину и шумы.

## Зависимости

Вам нужен пакет webrtcvad:
```bash
pip install -r requirements.txt
```
