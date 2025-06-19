from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from werkzeug.utils import secure_filename
from app.config import Config
from app.whisper_worker import transcribe_audio
from app.vad import read_wave, frame_generator, vad_collector, save_wave
import webrtcvad
import tempfile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config.from_object(Config)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'Voice Mentor API is running'
    })

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/process-audio', methods=['POST'])
def process_audio():
    logger.info("Received audio processing request")
    
    if 'audio' not in request.files:
        logger.warning("No audio file provided in request")
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    if file.filename == '':
        logger.warning("Empty filename in request")
        return jsonify({'error': 'No selected file'}), 400
    
    if not file or not allowed_file(file.filename):
        logger.warning(f"Invalid file type: {file.filename}")
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        logger.info(f"Saving file to: {filepath}")
        file.save(filepath)
        
        # VAD: если файл wav, 16kHz, моно, прогоняем через VAD
        if filename.lower().endswith('.wav'):
            try:
                audio, sample_rate = read_wave(filepath)
                vad = webrtcvad.Vad(2)
                frames = frame_generator(30, audio, sample_rate)
                segments = list(vad_collector(sample_rate, 30, 300, vad, frames))
                if segments:
                    speech_audio = b''.join(segments)
                    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as vad_out:
                        save_wave(vad_out.name, speech_audio, sample_rate)
                        vad_filepath = vad_out.name
                    logger.info(f"VAD applied, new file: {vad_filepath}")
                    transcript = transcribe_audio(vad_filepath)
                    os.remove(vad_filepath)
                else:
                    logger.warning("No speech detected by VAD")
                    return jsonify({'error': 'No speech detected'}), 400
            except Exception as vad_e:
                logger.error(f"VAD error: {vad_e}")
                return jsonify({'error': f'VAD error: {vad_e}'}), 500
        else:
            # Для других форматов — как раньше
            transcript = transcribe_audio(filepath)
        logger.info("Transcription completed successfully")
        
        # Clean up
        logger.info(f"Cleaning up file: {filepath}")
        os.remove(filepath)
        
        return transcript
        
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True) 