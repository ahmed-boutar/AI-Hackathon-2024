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
backend_dir = Path(__file__).resolve().parent.parent  # This points to 'backend'
sys.path.append(str(backend_dir))

# from core.config import get_settings

# settings = get_settings()

class AudioService:
    def __init__(self):
        # self.upload_dir = Path(settings.UPLOAD_DIR)
        # self.upload_dir.mkdir(exist_ok=True)
        self.sample_rate = 22050  # Standard sample rate for librosa

    async def save_upload_file(self, file) -> Path:
        """Save uploaded file to temporary directory"""
        temp_file = self.upload_dir / f"{uuid.uuid4()}.wav"
        with temp_file.open("wb") as buffer:
            content = await file.read()
            buffer.write(content)
        return temp_file
    
    def transcribe_to_midi(self, input_audio_path, output_midi_path):
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

    # def transcribe_to_midi(self, audio_path: Path) -> Path:
    #     """Convert audio file to MIDI using librosa pitch detection"""
    #     try:
    #         # Load the audio file
    #         y, sr = librosa.load(str(audio_path), sr=self.sample_rate, mono=True)
            
    #         # Extract pitch using librosa's pitch detection
    #         pitches, magnitudes = librosa.piptrack(
    #             y=y,
    #             sr=sr,
    #             fmin=librosa.note_to_hz('C2'),
    #             fmax=librosa.note_to_hz('C7')
    #         )

    #         # Create a MIDI file
    #         pm = pretty_midi.PrettyMIDI()
    #         piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    #         piano = pretty_midi.Instrument(program=piano_program)

    #         # Process the pitch data
    #         onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    #         onset_times = librosa.frames_to_time(onset_frames, sr=sr)
            
    #         # Parameters for note detection
    #         min_note_length = 0.1  # minimum note length in seconds
    #         current_note = None
    #         note_start_time = None
            
    #         # Convert frames to time
    #         times = librosa.frames_to_time(np.arange(pitches.shape[1]), sr=sr)
            
    #         for frame_idx in range(pitches.shape[1]):
    #             # Find the highest magnitude pitch in this frame
    #             pitch_idx = magnitudes[:, frame_idx].argmax()
    #             pitch = pitches[pitch_idx, frame_idx]
    #             magnitude = magnitudes[pitch_idx, frame_idx]
                
    #             # Only consider frames with significant magnitude
    #             if magnitude > np.mean(magnitudes) * 1.5:
    #                 midi_note = int(round(librosa.hz_to_midi(pitch)))
                    
    #                 if current_note is None:
    #                     # Start a new note
    #                     current_note = midi_note
    #                     note_start_time = times[frame_idx]
    #                 elif midi_note != current_note:
    #                     # Note changed, add the previous note if it was long enough
    #                     if times[frame_idx] - note_start_time >= min_note_length:
    #                         note = pretty_midi.Note(
    #                             velocity=int(min(100, magnitude * 100)),
    #                             pitch=current_note,
    #                             start=note_start_time,
    #                             end=times[frame_idx]
    #                         )
    #                         piano.notes.append(note)
                        
    #                     # Start a new note
    #                     current_note = midi_note
    #                     note_start_time = times[frame_idx]
    #             elif current_note is not None:
    #                 # End the current note if magnitude drops
    #                 if times[frame_idx] - note_start_time >= min_note_length:
    #                     note = pretty_midi.Note(
    #                         velocity=100,
    #                         pitch=current_note,
    #                         start=note_start_time,
    #                         end=times[frame_idx]
    #                     )
    #                     piano.notes.append(note)
    #                 current_note = None
            
    #         # Add the instrument to the MIDI file
    #         pm.instruments.append(piano)
            
    #         # Save MIDI file
    #         output_path = audio_path.with_suffix('.mid')
    #         pm.write(str(output_path))
            
    #         return output_path
            
    #     except Exception as e:
    #         raise Exception(f"Failed to transcribe audio: {str(e)}")
    
    def cleanup_files(self, *files: Path):
        """Clean up temporary files"""
        for file in files:
            try:
                if file.exists():
                    file.unlink()
            except Exception as e:
                print(f"Error deleting file {file}: {e}")