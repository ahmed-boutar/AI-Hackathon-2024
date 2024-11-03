import os
from werkzeug.utils import secure_filename
from datetime import datetime
from pathlib import Path

UPLOAD_FOLDER = os.environ.get("UPLOAD_DIR")
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}

def create_recording_folder(recording_name):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    folder_name = f"{timestamp}_{recording_name}"
    folder_path = os.path.join(UPLOAD_FOLDER, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_audio_file(file, folder_path):
    filename = secure_filename(file.filename)
    file_path = os.path.join(folder_path, filename)
    file.save(file_path)
    return file_path

def get_midi_path(folder_path):
    # Specify the directory path
    directory_path = Path(folder_path)  # Replace with your directory path

    # Find all files in the directory that end with .mid
    midi_files = list(directory_path.glob("*.mid"))

    # Check if any .mid files were found
    if midi_files:
        # Get the first .mid file found
        midi_file_path = midi_files[0]
        print(f"Found MIDI file: {midi_file_path}")
        return midi_file_path
        
    else:
        print("No .mid files found in the directory.")
        return ""
        

# def save_audio_file(file):
        
#     # Generate unique filename using timestamp
#     timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#     original_filename = secure_filename(file.filename)
#     filename = f"{timestamp}_{original_filename}"
    
#     filepath = os.path.join(UPLOAD_FOLDER, filename)
#     file.save(filepath)
    
#     return filepath
