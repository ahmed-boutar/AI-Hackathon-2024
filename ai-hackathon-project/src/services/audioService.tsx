import axios from 'axios';
import * as FileSystem from 'expo-file-system';

const API_URL = 'http://your-backend-ip:8000/api/v1';

export const audioService = {
  async uploadRecording(uri: any) {
    try {
      // Create form data
      const formData = new FormData();
      formData.append('file', {
        uri: uri,
        type: 'audio/wav',
        name: 'recording.wav'
      });

      // Upload to backend
      const response = await axios.post(`${API_URL}/audio/transcribe`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        responseType: 'blob',
      });

      // Save MIDI file
      const midiUri = `${FileSystem.documentDirectory}transcribed.mid`;
      await FileSystem.writeAsStringAsync(midiUri, response.data, {
        encoding: FileSystem.EncodingType.Base64,
      });

      return midiUri;
    } catch (error) {
      console.error('Error uploading recording:', error);
      throw error;
    }
  }
};

