import os
from flask import Flask, request, jsonify
from whisper_worker import transcribe_audio
from gpt_worker import generate_response
from config import Config

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_audio():
    if 'audio_file' not in request.files:
        return jsonify({"error": "No audio_file part"}), 400

    audio = request.files['audio_file']
    temp_path = "temp_audio.wav"
    audio.save(temp_path)
    try:
        text = transcribe_audio(temp_path)
        gpt_reply = generate_response(text)
        return jsonify({
            "transcription": text,
            "coach_reply": gpt_reply
        })
        return jsonify({'transcript': transcript, 'advice': advice})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
