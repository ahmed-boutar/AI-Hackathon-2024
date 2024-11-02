// components/AudioRecorder.js
import React, { useState, useEffect } from 'react';
import { View, StyleSheet, Text, Pressable } from 'react-native';
import { Audio } from 'expo-av';
import * as FileSystem from 'expo-file-system';

export default function AudioRecorder() {
  const [recording, setRecording] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [permissionResponse, requestPermission] = Audio.usePermissions();

  useEffect(() => {
    // Cleanup recording on unmount
    return () => {
      if (recording) {
        recording.unloadAsync();
      }
    };
  }, [recording]);

  async function startRecording() {
    try {
      // Request permissions if not already granted
      if (!permissionResponse?.granted) {
        await requestPermission();
      }

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

  // components/AudioRecorder.js - Modified stopRecording function
  async function stopRecording() {
    try {
      if (!recording) return;
  
      setIsRecording(false);
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      
      // Upload to backend and get MIDI file
      const midiUri = await audioService.uploadRecording(uri);
      
      // Clean up recording file
      await FileSystem.deleteAsync(uri);
      setRecording(null);
  
      // Handle the MIDI file (e.g., play it, save it, etc.)
      console.log('MIDI file saved at:', midiUri);
  
    } catch (err) {
      console.error('Failed to stop recording:', err);
    }
  }

  return (
    <View style={styles.container}>
      <Pressable
        style={[styles.button, isRecording && styles.recordingButton]}
        onPress={isRecording ? stopRecording : startRecording}
      >
        <Text style={styles.buttonText}>
          {isRecording ? 'Stop Recording' : 'Start Recording'}
        </Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  button: {
    backgroundColor: '#007AFF',
    padding: 20,
    borderRadius: 50,
    width: 200,
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