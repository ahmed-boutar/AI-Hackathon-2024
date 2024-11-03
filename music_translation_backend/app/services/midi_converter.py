import os
from pathlib import Path
import fluidsynth
import mido
import soundfile as sf
import numpy as np

class MidiConverter:
    def __init__(self):
        self.sample_rate = 48000
        self.instruments = {
            "piano": 0,    # Grand Piano
            "guitar": 24,  # Nylon String Guitar
            "violin": 40,  # Violin
            "saxophone": 65  # Alto Sax
        }
        self.soundfont_path = './data/sound_fonts/FluidR3_GM/FluidR3_GM.sf2'
        self.fs = None

    def initialize_synth(self):
        """Initialize FluidSynth with settings"""
        if self.fs is None:
            self.fs = fluidsynth.Synth(gain=0.5)
            self.fs.start(driver="coreaudio")
            
            if not os.path.exists(self.soundfont_path):
                raise FileNotFoundError("SoundFont file not found")
            
            self.sfid = self.fs.sfload(self.soundfont_path)

    def cleanup(self):
        """Cleanup FluidSynth resources"""
        if self.fs:
            self.fs.delete()
            self.fs = None

    def _play_midi_file(self, midi_path):
        """
        Convert MIDI file to audio data using FluidSynth
        """
        audio_data = []
        try:
            midi_file = mido.MidiFile(midi_path)
            
            for msg in midi_file:
                if msg.type == 'note_on':
                    self.fs.noteon(0, msg.note, msg.velocity)
                elif msg.type == 'note_off':
                    self.fs.noteoff(0, msg.note)
                
                time_to_wait = int(msg.time * self.sample_rate)
                if time_to_wait > 0:
                    audio_data.append(self.fs.get_samples(time_to_wait))

        except Exception as e:
            raise Exception(f"Error processing MIDI file: {str(e)}")

        return np.concatenate(audio_data)

    def _save_audio(self, audio_data, output_path):
        """Save audio data to WAV file"""
        sf.write(output_path, audio_data, self.sample_rate)

    def generate_instrument_audio(self, midi_path):
        """
        Generate audio files for all instruments from a MIDI file
        Returns a dictionary mapping instrument names to their audio file paths
        """
        try:
            self.initialize_synth()
            
            if not os.path.exists(midi_path):
                raise FileNotFoundError(f"MIDI file not found: {midi_path}")

            output_dir = os.path.dirname(midi_path)
            midi_stem = Path(midi_path).stem
            generated_files = {}

            for instrument_name, program_num in self.instruments.items():
                print(f"Processing {instrument_name}...")
                self.fs.program_select(0, self.sfid, 0, program_num)
                
                # Generate and save audio
                audio_data = self._play_midi_file(midi_path)
                output_path = os.path.join(output_dir, f"{midi_stem}_{instrument_name}.wav")
                self._save_audio(audio_data, output_path)
                
                generated_files[instrument_name] = output_path

            return generated_files

        except Exception as e:
            raise Exception(f"Error generating instrument audio: {str(e)}")
        finally:
            self.cleanup()
