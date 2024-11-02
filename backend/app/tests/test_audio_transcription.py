import sys
from pathlib import Path
import asyncio

backend_dir = Path(__file__).resolve().parent.parent 
sys.path.append(str(backend_dir))

from services.audio_service import AudioService

# from basic_pitch import ICASSP_2022_MODEL_PATH, inference
# from basic_pitch.inference import predict_and_save
# from basic_pitch.inference import predict





# async def test_transcription(audio_file_path: str, output_file: str):
#     print(f"Processing file: {audio_file_path}")
    
#     # audio_service = AudioService()
    
#     try:
#         # Convert the audio file to MIDI
#         # Initialize the model
#         # model = inference.Model(ICASSP_2022_MODEL_PATH)

#         # Transcribe the audio file and save it as a MIDI file
#         # predict_and_save([audio_file_path], output_file, model_or)

#         model_output, midi_data, note_events = predict(audio_file_path)
#         inference.predict_and_save(
#             [audio_file_path],
#             "../../data/",
#             True,
#             True,
#             True,
#             True,
#             model_or_model_path=ICASSP_2022_MODEL_PATH,
#         )
        
#         print(f"Successfully created MIDI file: {output_file}")
        
#     except Exception as e:
#         print(f"Error during transcription: {str(e)}")

# if __name__ == "__main__":
#     if len(sys.argv) < 3:
#         print("Usage: python test_audio_transcription.py <path_to_audio_file> <path_to_output_file>")
#         sys.exit(1)
    
#     audio_file = sys.argv[1]
#     output_file = sys.argv[2]
#     asyncio.run(test_transcription(audio_file, output_file))


from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH

async def test_transcription(audio_file_path: str, output_midi_path: str):
    print(f"Processing file: {audio_file_path}")

    audio_service = AudioService()
    
    try:

        audio_service.transcribe_to_midi(audio_file_path, output_midi_path)
        
        print(f"Successfully created MIDI file: {output_midi_path}")
        
    except Exception as e:
        print(f"Error during transcription: {str(e)}")


audio_file_path = "../../data/test-humming-01-1102.m4a"  # Replace with your actual audio file path
output_midi_path = "../../data/"  # Output path for the MIDI file
asyncio.run(test_transcription(audio_file_path, output_midi_path))
