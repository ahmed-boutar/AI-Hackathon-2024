# import sys
# from pathlib import Path
# import os
# import time
# import fluidsynth
# import mido
# import numpy as np
# import soundfile as sf
# import subprocess

# # Add the backend directory to Python path
# backend_dir = Path(__file__).resolve().parent.parent
# sys.path.append(str(backend_dir))

# # Assuming you have a custom midi converter, otherwise this import may not work
# from app.services.midi_converter import MidiConverter

# DIR = os.environ.get('UPLOAD_DIR')

# def play_midi_file(fs, midi_path):
#     """
#     Play a MIDI file using FluidSynth
#     """
#     try:
#         print(f"Playing MIDI file: {midi_path}")
#         midi_file = mido.MidiFile(midi_path)

#         for msg in midi_file.play():
#             if msg.type == 'note_on':
#                 fs.noteon(0, msg.note, msg.velocity)
#             elif msg.type == 'note_off':
#                 fs.noteoff(0, msg.note)
#             time.sleep(msg.time)

#     except Exception as e:
#         print(f"Error playing MIDI file: {str(e)}")



# def convert_midi_to_audio(midi_path, instrument_name, program_num, soundfont_path):
#     """
#     Convert MIDI file to audio using FluidSynth CLI for a specific instrument
#     """
#     try:
#         midi_dir = os.path.dirname(midi_path)
#         midi_filename = os.path.splitext(os.path.basename(midi_path))[0]
#         output_path = os.path.join(midi_dir, f"{midi_filename}_{instrument_name}.wav")
        
#         print(f"Converting MIDI to audio for {instrument_name} (program {program_num})...")
#         print(f"Output path: {output_path}")

#         # Construct FluidSynth command with initial program number
#         command = [
#             'fluidsynth',
#             '-ni',                    # Non-interactive mode
#             '-g', '0.2',             # Set gain (default = 0.2)
#             '-r', '44100',           # Sample rate
#             '-F', output_path,        # Fast render to file
#             '-a', 'file',            # Use file audio driver
#             '-q',                     # Quiet mode
#             # Set initial program (instrument) number for channel 0
#             '-o', f'synth.midi-channel.0.program={program_num}',
#             soundfont_path,           # SoundFont file
#             midi_path                 # MIDI file path
#         ]

#         print(f"Executing command: {' '.join(command)}")
#         result = subprocess.run(
#             command,
#             capture_output=True,
#             text=True
#         )
        
#         if result.returncode == 0:
#             print(f"Created audio file: {output_path}")
#             return output_path
#         else:
#             print(f"Command failed with error: {result.stderr}")
#             print(f"Command output: {result.stdout}")
#             return None

#     except Exception as e:
#         print(f"Error converting MIDI to audio: {str(e)}")
#         return None

# def test_midi_player():
#     try:
#         print("Initializing FluidSynth...")
#         fs = fluidsynth.Synth()
#         fs.start(driver="coreaudio")  # Use "alsa" on Linux, or "coreaudio" on MacOS

        
#         # Load SoundFont
#         soundfont_path = './data/sound_fonts/FluidR3_GM/FluidR3_GM.sf2'
#         print(os.path.exists(soundfont_path))
#         if not os.path.exists(soundfont_path):
#             raise FileNotFoundError("SoundFont file not found. Please check SOUND_FONTS_PATH environment variable.")
#         else:
#             print(f"Found the sound font file at {soundfont_path}")

#         print("Loading SoundFont from:", soundfont_path)  # Debugging line
#         sfid = fs.sfload(soundfont_path)
#         print(f"SFID = {sfid}")
#         fs.program_select(0, sfid, 0, 0) # Bank 0, preset 0
#         print('I AM HERE')
#         test_midi_path = './data/20241102_211655_recording/recording_basic_pitch.mid'
#         if not os.path.exists(test_midi_path):
#             raise FileNotFoundError("MIDI file not found. Please check the file path.")
        
        
#         # Test different instruments
#         instruments = {
#             "piano": 0,    # Grand Piano
#             "guitar": 24,  # Nylon String Guitar
#             "violin": 40,  # Violin
#             "saxophone": 65  # Alto Sax
#         }

#         # for instrument_name, program_num in instruments.items():
#         #     print(f"\nTesting {instrument_name}...")
#         #     fs.program_change(0, program_num)
#         #     play_midi_file(fs, test_midi_path)
#         #     time.sleep(1)

#         generated_files = []
#         for instrument_name, program_num in instruments.items():
#             print(f"\nProcessing {instrument_name}...")
#             output_path = convert_midi_to_audio(
#                 test_midi_path,
#                 instrument_name,
#                 program_num,
#                 soundfont_path
#             )
#             if output_path:
#                 generated_files.append(output_path)

#         print("\nGenerated audio files:")
#         for file_path in generated_files:
#             print(f"- {file_path}")
        
#         print("\nTest completed successfully!")

#     except Exception as e:
#         print(f"Error during test: {str(e)}")
#     finally:
#         if 'fs' in locals():
#             fs.delete()
#             print("\nCleaned up FluidSynth resources")

# if __name__ == "__main__":
#     test_midi_player()

import sys
from pathlib import Path
import os
import fluidsynth
import mido
import soundfile as sf
import numpy as np

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

DIR = os.environ.get('UPLOAD_DIR')

def play_midi_file(fs, midi_path, sample_rate=48000):
    """
    Play a MIDI file using FluidSynth and capture the audio output, adjusting for MIDI timing.
    """
    audio_data = []
    try:
        print(f"Playing MIDI file: {midi_path}")
        midi_file = mido.MidiFile(midi_path)
        
        for msg in midi_file:
            if msg.type == 'note_on':
                fs.noteon(0, msg.note, msg.velocity)
            elif msg.type == 'note_off':
                fs.noteoff(0, msg.note)
            
            # Wait for the specified time before moving to the next event
            time_to_wait = int(msg.time * sample_rate)
            if time_to_wait > 0:
                audio_data.append(fs.get_samples(time_to_wait))

    except Exception as e:
        print(f"Error playing MIDI file: {str(e)}")

    # Concatenate all the audio data chunks into a single array
    audio_data = np.concatenate(audio_data)
    return audio_data

def save_audio(audio_data, output_path, sample_rate=48000):
    """
    Save the audio data to a .wav file with the specified sample rate.
    """
    sf.write(output_path, audio_data, sample_rate)
    print(f"Created audio file: {output_path}")

def test_midi_player():
    #TODO: Try to make the output wavs less distorted 
    try:
        print("Initializing FluidSynth...")
        fs = fluidsynth.Synth(gain=0.5)  # Set gain (adjustable)
        fs.start(driver="coreaudio")  # Set sample rate to 44100 Hz for better quality

        # Load SoundFont
        soundfont_path = './data/sound_fonts/FluidR3_GM/FluidR3_GM.sf2'
        if not os.path.exists(soundfont_path):
            raise FileNotFoundError("SoundFont file not found. Please check SOUND_FONTS_PATH environment variable.")
        
        sfid = fs.sfload(soundfont_path)
        
        test_midi_path = './data/20241102_211655_recording/recording_basic_pitch.mid'
        if not os.path.exists(test_midi_path):
            raise FileNotFoundError("MIDI file not found. Please check the file path.")
        
        # Instrument program numbers
        instruments = {
            "piano": 0,    # Grand Piano
            "guitar": 24,  # Nylon String Guitar
            "violin": 40,  # Violin
            "saxophone": 65  # Alto Sax
        }

        generated_files = []
        for instrument_name, program_num in instruments.items():
            print(f"\nProcessing {instrument_name}...")
            fs.program_select(0, sfid, 0, program_num)  # Select instrument program
            
            # Play and capture audio data with correct timing
            audio_data = play_midi_file(fs, test_midi_path, sample_rate=48000)
            
            # Save audio data to .wav file
            output_path = os.path.join(os.path.dirname(test_midi_path), f"{Path(test_midi_path).stem}_{instrument_name}.wav")
            save_audio(audio_data, output_path, sample_rate=48000)
            generated_files.append(output_path)

        print("\nGenerated audio files:")
        for file_path in generated_files:
            print(f"- {file_path}")
        
        print("\nTest completed successfully!")

    except Exception as e:
        print(f"Error during test: {str(e)}")
    finally:
        if 'fs' in locals():
            fs.delete()
            print("\nCleaned up FluidSynth resources")

if __name__ == "__main__":
    test_midi_player()



