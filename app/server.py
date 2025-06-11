from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from werkzeug.utils import secure_filename
from app.config import Config
from app.whisper_worker import transcribe_audio

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
        
        # Transcribe audio
        logger.info("Starting audio transcription")
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