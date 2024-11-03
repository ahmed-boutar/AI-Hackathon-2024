from flask import Blueprint, request, jsonify, send_file
from flask_cors import cross_origin
# from services.audio_processor import AudioProcessor
# from services.midi_converter import MidiConverter
from app.utils.file_handler import save_audio_file
from werkzeug.utils import secure_filename
from app.services.audio_processor import AudioProcessor
import os
from pathlib import Path

audio_bp = Blueprint('audio', __name__)
audio_processor = AudioProcessor()
DATA_DIR = os.environ.get('UPLOAD_DIR')
# midi_converter = MidiConverter()

@audio_bp.route('/api/process-audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
        
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    recording_name = request.form.get('name', 'recording')
    try:
        result = audio_processor.process_audio(audio_file, recording_name)
        
        return jsonify({
            'status': 'success',
            'data': {
                'folder_path': result['folder_path'],
                'audio_path': result['audio_path']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    # filename = save_audio_file(audio_file)
    # DATA_DIRECTORY = './data/'
    # input_file = os.path.join(DATA_DIRECTORY, 'test-humming-01-1102.m4a')
    # # Process audio to MIDI
    # midi_data = audio_processor.transcribe_to_midi(input_file, DATA_DIRECTORY)
    
    # # Convert to selected instrument
    # instrument = request.form.get('instrument', 'piano')
    # converted_audio = midi_converter.convert_instrument(midi_data, instrument)
    
   

@audio_bp.route('/api/instruments', methods=['GET'])
def get_instruments():
    print('Hello today')
    instruments = ['piano', 'guitar', 'saxophone', 'violin']
    return jsonify({'instruments': instruments})

@audio_bp.route('/api/latest-recordings', methods=['GET'])
def get_latest_recordings():
    try:
        # Get the most recent recording folder
        data_dir = Path(DATA_DIR)
        folders = [f for f in data_dir.iterdir() if f.is_dir() and f.name[0].isdigit()]
        latest_folder = max(folders, key=lambda x: x.name)

        # Get all audio files in the folder
        audio_files = {}
        tracks = []
        
        for file in latest_folder.glob('*.wav'):
            # Parse filename to get track ID and instrument
            name_parts = file.stem.split('_')
            track_id = name_parts[0]
            instrument = name_parts[-1]
            
            # Create URL for the audio file
            audio_files[f"{track_id}_{instrument}"] = f"/data/{latest_folder.name}/{file.name}"
            
            # Add track info if not already added
            if track_id not in [t['id'] for t in tracks]:
                tracks.append({
                    'id': track_id,
                    'fileName': f"{track_id}.mid"
                })

        return jsonify({
            'audio_files': audio_files,
            'tracks': tracks
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# @audio_bp.route('/api/audio/<path:filename>')
# def serve_audio(filename):
#     try:
#         # Construct the full path to the audio file
#         audio_path = filename
#         print(audio_path)
#         if not os.path.exists(audio_path):
#             return jsonify({'error': 'Audio file not found'}), 404
            
#         return send_file(
#             audio_path,
#             mimetype='audio/wav',
#             as_attachment=False,
#             conditional=True  # Enable partial content support
#         )
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

@audio_bp.route('/api/audio/<path:filename>')
def serve_audio(filename):
    try:
        # Construct the full path to the audio file
        audio_path = filename
        
        if not os.path.exists(audio_path):
            return jsonify({'error': 'Audio file not found'}), 404
            
        return send_file(
            audio_path,
            mimetype='audio/wav',
            conditional=True,
            as_attachment=False,
            download_name=os.path.basename(audio_path)
        )
    except Exception as e:
        print(f"Error serving audio: {str(e)}")
        return jsonify({'error': str(e)}), 500
