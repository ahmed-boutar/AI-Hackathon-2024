from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
# from services.audio_processor import AudioProcessor
# from services.midi_converter import MidiConverter
from app.utils.file_handler import save_audio_file
from werkzeug.utils import secure_filename
from app.services.audio_processor import AudioProcessor
import os

audio_bp = Blueprint('audio', __name__)
audio_processor = AudioProcessor()
# midi_converter = MidiConverter()

@audio_bp.route('/api/process-audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
        
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = save_audio_file(audio_file)
    # DATA_DIRECTORY = './data/'
    # input_file = os.path.join(DATA_DIRECTORY, 'test-humming-01-1102.m4a')
    # # Process audio to MIDI
    # midi_data = audio_processor.transcribe_to_midi(input_file, DATA_DIRECTORY)
    
    # # Convert to selected instrument
    # instrument = request.form.get('instrument', 'piano')
    # converted_audio = midi_converter.convert_instrument(midi_data, instrument)
    
    # Return the processed audio path or base64 encoded audio
    return jsonify({
        'status': 'success',
        # 'input_file': input_file
        # 'data': {
        #     # 'converted_audio': converted_audio,
        #     'midi_data': midi_data,
        #     # 'instrument': instrument,
        # }
    })

@audio_bp.route('/api/instruments', methods=['GET'])
def get_instruments():
    print('Hello today')
    instruments = ['piano', 'guitar', 'saxophone', 'violin']
    return jsonify({'instruments': instruments})