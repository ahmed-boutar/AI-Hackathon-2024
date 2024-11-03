import os
import uuid
from pathlib import Path
import numpy as np
import librosa
import pretty_midi
from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH
from app.utils.file_handler import create_recording_folder, save_audio_file, get_midi_path
from app.services.midi_converter import MidiConverter
import os

import sys 
# backend_dir = Path(__file__).resolve().parent.parent  # This points to 'backend'
# sys.path.append(str(backend_dir))


class AudioProcessor:
    def __init__(self):
        self.sample_rate = 22050  # Standard sample rate for librosa
        self.upload_dir = os.environ.get("UPLOAD_DIR")
        self.midi_converter = MidiConverter()
    
    def process_audio(self, audio_file, recording_name):
        # Create a folder for this recording
        folder_path = create_recording_folder(recording_name)
        
        # Save the audio file
        audio_path = save_audio_file(audio_file, folder_path)
        
        # Transcribe to MIDI
        midi_data = self.transcribe_to_midi(audio_path, folder_path)
        midi_file_path = get_midi_path(folder_path)

        instrument_files = self.midi_converter.generate_instrument_audio(midi_file_path)
        
        
        # # Save the MIDI file
        # midi_path = save_midi_file(midi_data, folder_path)
        
        return {
            'folder_path': folder_path,
            'audio_path': audio_path,
            # 'midi_path': midi_path
        }
    
    def transcribe_to_midi(self, input_audio_path, output_dir):
        '''
        Use the basic-pitch model by spotify to convert audio to midi
        '''
        predict_and_save(
            [input_audio_path],
            output_directory=output_dir,
            save_midi=True,
            save_model_outputs=True,
            sonify_midi=True, 
            save_notes=True,
            model_or_model_path=ICASSP_2022_MODEL_PATH,
        )
        print(f"Saved MIDI file to {output_dir}")
    
    def cleanup_files(self, *files: Path):
        """Clean up temporary files"""
        for file in files:
            try:
                if file.exists():
                    file.unlink()
            except Exception as e:
                print(f"Error deleting file {file}: {e}")
