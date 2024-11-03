import { useState, useEffect } from 'react';
import { View, StyleSheet, Text, Pressable } from 'react-native';
import { Audio } from 'expo-av';
import { router, useLocalSearchParams } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';

const API_BASE_URL = 'http://10.197.92.154:5001';

export default function ViewRecordingScreen() {
  const { recordingUri } = useLocalSearchParams();
  const [sound, setSound] = useState<Audio.Sound | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Load the sound when component mounts
  useEffect(() => {
    loadSound();
    return () => {
      // Cleanup sound when component unmounts
      if (sound) {
        sound.unloadAsync();
      }
    };
  }, [recordingUri]);

  async function loadSound() {
    try {
      const { sound: newSound } = await Audio.Sound.createAsync(
        { uri: recordingUri as string },
        { shouldPlay: false }
      );
      setSound(newSound);

      // Handle playback status updates
      newSound.setOnPlaybackStatusUpdate((status) => {
        if (status.isLoaded) {
          setIsPlaying(status.isPlaying);
          if (status.didJustFinish) {
            setIsPlaying(false);
          }
        }
      });
    } catch (error) {
      console.error('Error loading sound:', error);
    }
  }

  async function handlePlayPause() {
    if (!sound) return;

    if (isPlaying) {
      await sound.pauseAsync();
    } else {
      await sound.playAsync();
    }
  }

  async function handleCreateMidi() {
    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('audio', {
        uri: recordingUri,
        type: 'audio/wav',
        name: 'recording.wav',
      } as any);

      console.log('Sending request to:', `${API_BASE_URL}/api/process-audio`);

      const response = await fetch(`${API_BASE_URL}/api/process-audio`, {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
          Accept: 'application/json',
        },
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);

      }

      const result = await response.json();
      
      // Navigate to results page with the MIDI data
      router.push({
        pathname: '/Results/results',
        params: { midiData: JSON.stringify(result.data) }
      });
    } catch (error) {
      console.error('Error processing audio:', error);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Review Recording</Text>
      
      <View style={styles.buttonContainer}>
        <Pressable
          style={[styles.button, styles.playButton]}
          onPress={handlePlayPause}
        >
          <Text style={styles.buttonText}>
            {isPlaying ? 'Pause' : 'Play Recording'}
          </Text>
        </Pressable>

        <Pressable
          style={[styles.button, styles.createButton]}
          onPress={handleCreateMidi}
          disabled={isLoading}
        >
          <Text style={styles.buttonText}>
            {isLoading ? 'Processing...' : 'Create MIDI'}
          </Text>
        </Pressable>

        <Pressable
          style={[styles.button, styles.recordAgainButton]}
          onPress={() => router.back()}
        >
          <Text style={styles.buttonText}>Record Again</Text>
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
    gap: 20,
  },
  button: {
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  playButton: {
    backgroundColor: '#34C759',
  },
  createButton: {
    backgroundColor: '#007AFF',
  },
  recordAgainButton: {
    backgroundColor: '#FF3B30',
  },
  customizeButton: {
    backgroundColor: '#FF3B30',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
});