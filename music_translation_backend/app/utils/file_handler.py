import os
from werkzeug.utils import secure_filename
from datetime import datetime

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

# def save_audio_file(file):
        
#     # Generate unique filename using timestamp
#     timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#     original_filename = secure_filename(file.filename)
#     filename = f"{timestamp}_{original_filename}"
    
#     filepath = os.path.join(UPLOAD_FOLDER, filename)
#     file.save(filepath)
    
#     return filepath
