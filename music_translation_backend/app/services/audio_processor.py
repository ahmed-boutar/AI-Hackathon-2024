import os
import uuid
from pathlib import Path
import pretty_midi
import logging
from werkzeug.utils import secure_filename
from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH
from app.utils.file_handler import create_recording_folder, save_audio_file

class AudioProcessor:
    def __init__(self):
        self.sample_rate = 22050  # Standard sample rate for librosa
        print(os.environ.get("UPLOAD_DIR"))
        self.upload_dir = Path(os.environ.get("UPLOAD_DIR"))  # Ensure this is a Path object

    def process_audio(self, audio_file, recording_name):
        try:
            # Create a folder for this recording
            folder_path = Path(create_recording_folder(recording_name))
            logging.debug(f"Created folder: {folder_path}")
            
            # Save the audio file
            audio_path = Path(save_audio_file(audio_file, folder_path))
            logging.debug(f"Saved audio file: {audio_path}")
            
            # Transcribe audio file to MIDI
            self.transcribe_to_midi(audio_path, folder_path)
            logging.debug(f"Transcribed audio to MIDI in folder: {folder_path}")

            # Post-process MIDI file
            midi_files = list(folder_path.glob("*.mid"))
            if not midi_files:
                raise FileNotFoundError("No MIDI file found in the output directory after transcription.")
            
            # Assume there is only one MIDI file generated, process it
            midi_path = midi_files[0]
            final_midi_path = self.postprocess_midi(midi_path)
            logging.debug(f"Post-processed MIDI file: {final_midi_path}")

            # Cleanup temporary files, including the original audio
            self.cleanup_files(audio_path)
            logging.debug(f"Cleaned up temporary files")

            # Move the final MIDI file to the output directory (ensuring it is the only file)
            final_output_path = folder_path / "final_basic_pitch.mid"
            final_midi_path.rename(final_output_path)
            logging.debug(f"Moved final MIDI file to: {final_output_path}")
            
            return {
                'folder_path': str(folder_path),
                'audio_path': str(audio_path),
                'midi_path': str(final_output_path)
            }
        except Exception as e:
            logging.error(f"Error processing audio: {e}")
            raise
    
    def transcribe_to_midi(self, input_audio_path, output_dir):
        '''
        Use the basic-pitch model by spotify to convert audio to midi
        '''
        try:
            logging.debug(f"Starting transcription for audio file: {input_audio_path}")
            predict_and_save(
                [input_audio_path],
                output_directory=output_dir,
                save_midi=True,
                save_model_outputs=True,
                sonify_midi=True, 
                save_notes=True,
                model_or_model_path=ICASSP_2022_MODEL_PATH,
            )
            logging.debug(f"Saved MIDI file to {output_dir}")
        except Exception as e:
            logging.error(f"Error transcribing audio to MIDI: {e}")
            raise
    
    def postprocess_midi(self, midi_path):
        '''
        Post-process the midi file
        '''
        try:
            logging.debug(f"Starting post-processing for MIDI file: {midi_path}")
            
            # Load the MIDI file using pretty_midi
            midi_data = pretty_midi.PrettyMIDI(str(midi_path))
            
            # Remove all pitch bend messages from each instrument
            for instrument in midi_data.instruments:
                instrument.pitch_bends = []
            
            # Save the modified MIDI file
            modified_midi_path = midi_path.with_name(f"{midi_path.stem}.mid")
            midi_data.write(str(modified_midi_path))
            
            logging.debug(f"Post-processed MIDI file saved to {modified_midi_path}")
            return modified_midi_path
        except Exception as e:
            logging.error(f"Error post-processing MIDI: {e}")
            raise

    def cleanup_files(self, *files: Path):
        """Clean up temporary files"""
        for file in files:
            try:
                file_path = Path(file)  # Ensure file is a Path object
                if file_path.exists():
                    file_path.unlink()
            except Exception as e:
                logging.error(f"Error deleting file {file}: {e}")
