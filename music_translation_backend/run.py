from flask import Flask, request
from app.routes.audio_routes import audio_bp
from flask_cors import CORS
from dotenv import load_dotenv
from config import Config

load_dotenv() 

def create_app(config_class=Config):
    app = Flask("Music Transcription API")
    # Simplified CORS setup that should work with React Native
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Accept"],
            "expose_headers": ["Content-Type"],
            "supports_credentials": False  # Changed to False for mobile apps
        }
    })
    
    # Add some debug logging
    @app.before_request
    def log_request_info():
        app.logger.debug('Headers: %s', request.headers)
        app.logger.debug('Body: %s', request.get_data())

    app.config.from_object(config_class)
    app.register_blueprint(audio_bp)
    return app
    # ... other app configurations
    return app

app = create_app(Config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)