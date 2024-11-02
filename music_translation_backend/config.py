import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    UPLOAD_FOLDER = os.environ.get("UPLOAD_DIR")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}
    CORS_HEADERS = 'Content-Type'