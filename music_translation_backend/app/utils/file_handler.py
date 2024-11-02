import os
from werkzeug.utils import secure_filename
from datetime import datetime

UPLOAD_FOLDER = os.environ.get("UPLOAD_DIR")
ALLOWED_EXTENSIONS = {'wav', 'mp3'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_audio_file(file):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        
    # Generate unique filename using timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    original_filename = secure_filename(file.filename)
    filename = f"{timestamp}_{original_filename}"
    
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    return filepath