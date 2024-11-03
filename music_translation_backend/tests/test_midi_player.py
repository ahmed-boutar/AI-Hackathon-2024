import sys
from pathlib import Path
import os
import time
import fluidsynth
import mido

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

# Assuming you have a custom midi converter, otherwise this import may not work
from app.services.midi_converter import MidiConverter

DIR = os.environ.get('UPLOAD_DIR')

def play_midi_file(fs, midi_path):
    """
    Play a MIDI file using FluidSynth
    """
    try:
        print(f"Playing MIDI file: {midi_path}")
        midi_file = mido.MidiFile(midi_path)

        for msg in midi_file.play():
            if msg.type == 'note_on':
                fs.noteon(0, msg.note, msg.velocity)
            elif msg.type == 'note_off':
                fs.noteoff(0, msg.note)
            time.sleep(msg.time)

    except Exception as e:
        print(f"Error playing MIDI file: {str(e)}")

def test_midi_player():
    try:
        print("Initializing FluidSynth...")
        fs = fluidsynth.Synth()
        fs.start(driver="coreaudio")  # Use "alsa" on Linux, or "coreaudio" on MacOS

        
        # Load SoundFont
        soundfont_path = './data/sound_fonts/FluidR3_GM/FluidR3_GM.sf2'
        print(os.path.exists(soundfont_path))
        if not os.path.exists(soundfont_path):
            raise FileNotFoundError("SoundFont file not found. Please check SOUND_FONTS_PATH environment variable.")
        else:
            print(f"Found the sound font file at {soundfont_path}")

        print("Loading SoundFont from:", soundfont_path)  # Debugging line
        sfid = fs.sfload(soundfont_path)
        print(f"SFID = {sfid}")
        fs.program_select(0, sfid, 0, 0) # Bank 0, preset 0
        print('I AM HERE')
        test_midi_path = './data/20241102_211655_recording/recording_basic_pitch.mid'
        if not os.path.exists(test_midi_path):
            raise FileNotFoundError("MIDI file not found. Please check the file path.")

        
        # Test different instruments
        instruments = {
            "piano": 0,    # Grand Piano
            "guitar": 24,  # Nylon String Guitar
            "violin": 40,  # Violin
            "saxophone": 65  # Alto Sax
        }

        for instrument_name, program_num in instruments.items():
            print(f"\nTesting {instrument_name}...")
            fs.program_change(0, program_num)
            play_midi_file(fs, test_midi_path)
            time.sleep(1)

        print("\nTest completed successfully!")

    except Exception as e:
        print(f"Error during test: {str(e)}")
    finally:
        if 'fs' in locals():
            fs.delete()
            print("\nCleaned up FluidSynth resources")

if __name__ == "__main__":
    test_midi_player()
