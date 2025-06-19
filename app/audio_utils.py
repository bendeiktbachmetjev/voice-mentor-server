import subprocess
import tempfile
import os
import logging

logger = logging.getLogger(__name__)

def convert_to_wav_16k_mono(input_path):
    """
    Converts any audio file to WAV format, 16kHz, mono using ffmpeg.
    Returns the path to the converted file (temporary file).
    Raises exception if conversion fails.
    """
    output_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    output_path = output_file.name
    output_file.close()
    command = [
        'ffmpeg',
        '-y',  # Overwrite output file if exists
        '-i', input_path,
        '-ac', '1',  # mono
        '-ar', '16000',  # 16kHz
        '-sample_fmt', 's16',  # 16-bit PCM
        output_path
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"Audio converted to WAV 16kHz mono: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"ffmpeg conversion failed: {e.stderr.decode()}")
        os.remove(output_path)
        raise Exception(f"ffmpeg conversion failed: {e.stderr.decode()}") 