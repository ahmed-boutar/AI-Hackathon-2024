import os
from pathlib import Path
import fluidsynth

class MidiConverter:
    def __init__(self):
        # Path to soundfont file - you'll need to download this
        self.soundfont_path = "path/to/your/soundfont.sf2"
        
        # Instrument mapping
        self.instrument_map = {
            "piano": 0,  # Grand Piano
            "guitar": 24,  # Nylon String Guitar
            "violin": 40,  # Violin
            "saxophone": 65,  # Alto Sax
        }
        
        # Initialize FluidSynth
        self.fs = fluidsynth.Synth()
        self.fs.start()
        
        # Load soundfont
        self.sfid = self.fs.sfload(self.soundfont_path)
        self.fs.sfont_select(0, self.sfid)

    def convert_midi_to_audio(self, midi_path: str, instrument: str, output_dir: str) -> str:
        """
        Convert MIDI file to audio using specified instrument
        
        Args:
            midi_path: Path to the MIDI file
            instrument: Name of the instrument (piano, guitar, violin, saxophone)
            output_dir: Directory to save the output audio file
        
        Returns:
            Path to the generated audio file
        """
        try:
            # # Create output directory if it doesn't exist
            # os.makedirs(output_dir, exist_ok=True)
            
            # Get instrument program number
            program = self.instrument_map.get(instrument.lower(), 0)
            
            # Set instrument
            self.fs.program_change(0, program)
            
            # Generate output path
            midi_filename = Path(midi_path).stem
            output_path = os.path.join(output_dir, f"{midi_filename}_{instrument}.wav")
            
            # Convert MIDI to audio
            self.fs.midi_to_audio(midi_path, output_path)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error converting MIDI to audio: {str(e)}")

    def cleanup(self):
        """Cleanup FluidSynth resources"""
        self.fs.delete()
