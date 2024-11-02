import { useState, useEffect } from 'react';
import { View, StyleSheet, Text, Pressable } from 'react-native';
import { Audio } from 'expo-av';
import { router } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function RecordScreen() {
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [isRecording, setIsRecording] = useState(false);

  useEffect(() => {
    // Request permission when component mounts
    Audio.requestPermissionsAsync();
  }, []);

  async function startRecording() {
    try {
      // Configure audio mode
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      // Start recording
      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      setRecording(recording);
      setIsRecording(true);
    } catch (err) {
      console.error('Failed to start recording', err);
    }
  }

  async function stopRecording() {
    if (!recording) return;

    try {
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      setIsRecording(false);
      const { sound, status } = await recording.createNewLoadedSoundAsync();
      router.push({
        pathname: '/ViewRecordings/viewRecordings',
        params: { recordingUri: uri }
      });
      
    //   // Send recording to backend
    //   await sendAudioToBackend(uri);
      
      // Navigate to results screen
    //   router.push('/Results/results');
    } catch (err) {
      console.error('Failed to stop recording', err);
    }
  }

  async function sendAudioToBackend(audioUri: string) {
    const formData = new FormData();
    formData.append('audio', {
      uri: audioUri,
      type: 'audio/wav',
      name: 'recording.wav',
    } as any);

    try {
      const response = await fetch('http://your-backend-url/api/process-audio', {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const result = await response.json();
      console.log('Processing result:', result);
      
      // Store the result for the results screen
      // You might want to use global state management here
      
    } catch (error) {
      console.error('Error sending audio:', error);
    }
  }

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Record Your Melody</Text>
      <View style={styles.buttonContainer}>
        <Pressable
          style={[styles.button, isRecording && styles.recordingButton]}
          onPress={isRecording ? stopRecording : startRecording}
        >
          <Text style={styles.buttonText}>
            {isRecording ? 'Stop Recording' : 'Start Recording'}
          </Text>
        </Pressable>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginVertical: 20,
  },
  buttonContainer: {
    flex: 1,
    justifyContent: 'center',
  },
  button: {
    backgroundColor: '#007AFF',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  recordingButton: {
    backgroundColor: '#FF3B30',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
});