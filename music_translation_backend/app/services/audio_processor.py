import os
import uuid
from pathlib import Path
import numpy as np
import librosa
import pretty_midi
from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH
import os

import sys 
# backend_dir = Path(__file__).resolve().parent.parent  # This points to 'backend'
# sys.path.append(str(backend_dir))


class AudioProcessor:
    def __init__(self):
        self.sample_rate = 22050  # Standard sample rate for librosa
        self.upload_dir = os.environ.get("UPLOAD_DIR")

    async def save_upload_file(self, file) -> Path:
        """Save uploaded file to temporary directory"""
        print("Trying to upload file")
        temp_file = self.upload_dir / f"{uuid.uuid4()}.wav"
        with temp_file.open("wb") as buffer:
            content = await file.read()
            buffer.write(content)
        return temp_file
    
    def transcribe_to_midi(self, input_audio_path, output_midi_path):
        '''
        Use the basic-pitch model by spotify to convert audio to midi
        '''
        predict_and_save(
            [input_audio_path],
            output_directory=output_midi_path,
            save_midi=True,
            save_model_outputs=True,
            sonify_midi=True, 
            save_notes=True,
            model_or_model_path=ICASSP_2022_MODEL_PATH,
        )
        print(f"Saved MIDI file to {output_midi_path}")
    
    def cleanup_files(self, *files: Path):
        """Clean up temporary files"""
        for file in files:
            try:
                if file.exists():
                    file.unlink()
            except Exception as e:
                print(f"Error deleting file {file}: {e}")