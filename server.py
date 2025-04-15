from flask import Flask, request, jsonify
from whisper_worker import transcribe_audio
from gpt_worker import generate_response

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_audio():
    try:
        if 'audio_file' not in request.files:
            return jsonify({"error": "No audio_file part"}), 400

        audio = request.files['audio_file']
        audio.save("temp_audio.wav")

        # Вызов функции транскрипции
        text = transcribe_audio("temp_audio.wav")

        # Вызов генерации ответа AI
        gpt_reply = generate_response(text)

        return jsonify({
            "transcription": text,
            "coach_reply": gpt_reply
        })
    except Exception as e:
        # Логирование ошибки для диагностики
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
