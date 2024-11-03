import sys
from pathlib import Path
import requests
import json

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

def test_latest_recordings_api():
    """Test the /api/latest-recordings endpoint"""
    try:
        # Make request to your API endpoint
        response = requests.get('http://10.197.92.154:5001/api/latest-recordings')
        
        # Print status code
        print(f"Status Code: {response.status_code}")
        
        # Pretty print the response JSON
        data = response.json()
        print("\nResponse Data:")
        print(json.dumps(data, indent=2))
        
        # Validate response structure
        if 'audio_files' in data and 'tracks' in data:
            print("\nValidation:")
            print(f"Number of tracks: {len(data['tracks'])}")
            print(f"Number of audio files: {len(data['audio_files'])}")
            
            # Print each track and its associated audio files
            print("\nTracks and Associated Audio Files:")
            for track in data['tracks']:
                print(f"\nTrack ID: {track['id']}")
                print(f"File Name: {track['fileName']}")
                
                # Find associated audio files
                track_audio_files = {
                    k: v for k, v in data['audio_files'].items() 
                    if k.startswith(track['id'])
                }
                print("Associated Audio Files:")
                for audio_key, audio_url in track_audio_files.items():
                    print(f"- {audio_key}: {audio_url}")
        
    except Exception as e:
        print(f"Error testing API: {str(e)}")

if __name__ == "__main__":
    test_latest_recordings_api()