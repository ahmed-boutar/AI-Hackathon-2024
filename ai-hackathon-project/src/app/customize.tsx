import { View, StyleSheet, Text, Pressable } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Picker } from '@react-native-picker/picker';
import { Ionicons } from '@expo/vector-icons';
import { useState } from 'react';
import { router } from 'expo-router';

export default function CustomizeScreen() {
  const [selectedInstrument, setSelectedInstrument] = useState('piano');
  const [isPlaying, setIsPlaying] = useState(false);
  const [tracks, setTracks] = useState([
    { id: '1', fileName: 'melody_001.mid', instrument: 'Piano' },
    { id: '2', fileName: 'melody_002.mid', instrument: 'Piano' },
  ]);

  // State to track which row's instrument is being edited
  const [editingInstrumentId, setEditingInstrumentId] = useState(null);

  const handleInstrumentChange = (trackId: any, instrument: string) => {
    // Update the instrument for the specific track
    setTracks((prevTracks) =>
      prevTracks.map((track) =>
        track.id === trackId ? { ...track, instrument } : track
      )
    );
    setEditingInstrumentId(null); // Close the picker after selection
    console.log(tracks)
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Pressable onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="chevron-back" size={24} color="#007AFF" />
          <Text style={styles.backText}>Back</Text>
        </Pressable>
        <Text style={styles.title}>Customize Melody</Text>
        <Pressable style={styles.exportButton} onPress={() => console.log('Export')}>
          <Text style={styles.exportText}>Export</Text>
        </Pressable>
      </View>

      {/* Table */}
      <View style={styles.tableContainer}>
        <View style={styles.tableHeader}>
          <Text style={[styles.tableHeaderText, { flex: 2 }]}>Instrument</Text>
          <Text style={[styles.tableHeaderText, { flex: 2 }]}>File Name</Text>
          <Text style={[styles.tableHeaderText, { flex: 1 }]}>Actions</Text>
        </View>

        {tracks.map((track) => (
          <View key={track.id} style={styles.tableRow}>
            <View style={{ flex: 2 }}>
              {editingInstrumentId === track.id ? (
                <Picker
                  selectedValue={track.instrument}
                  style={styles.picker}
                  onValueChange={(value) => handleInstrumentChange(track.id, value)}
                >
                  <Picker.Item label="Piano" value="Piano" />
                  <Picker.Item label="Guitar" value="Guitar" />
                  <Picker.Item label="Violin" value="Violin" />
                  <Picker.Item label="Saxophone" value="Saxophone" />
                </Picker>
              ) : (
                <Pressable onPress={() => setEditingInstrumentId(track.id)}>
                  <Text style={styles.instrumentText}>{track.instrument}</Text>
                </Pressable>
              )}
            </View>
            <Text style={[styles.tableCell, { flex: 2 }]}>{track.fileName}</Text>
            <Pressable 
              style={[styles.editButton, { flex: 1 }]}
              onPress={() => router.push('/edit-midi')}
            >
              <Text style={styles.editButtonText}>Edit MIDI</Text>
            </Pressable>
          </View>
        ))}
      </View>

      {/* Playback Controls */}
      <View style={styles.playbackControls}>
        <View style={styles.playbackButtons}>
          <Pressable
            style={styles.playbackButton}
            onPress={() => setIsPlaying(!isPlaying)}
          >
            <Ionicons 
              name={isPlaying ? "pause" : "play"} 
              size={28} 
              color="white" 
            />
          </Pressable>
          <Pressable style={styles.playbackButton}>
            <Ionicons name="stop" size={28} color="white" />
          </Pressable>
        </View>

        <Pressable style={styles.generateButton}>
          <Text style={styles.generateText}>Generate</Text>
        </Pressable>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5E5',
  },
  backButton: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  backText: {
    color: '#007AFF',
    fontSize: 17,
  },
  title: {
    fontSize: 17,
    fontWeight: '600',
  },
  exportButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
  },
  exportText: {
    color: 'white',
    fontWeight: '600',
  },
  tableContainer: {
    flex: 1,
    margin: 16,
    backgroundColor: '#fff',
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  tableHeader: {
    flexDirection: 'row',
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5E5',
    backgroundColor: '#F8F8F8',
    borderTopLeftRadius: 10,
    borderTopRightRadius: 10,
  },
  tableHeaderText: {
    fontWeight: '600',
    color: '#666',
  },
  tableRow: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5E5',
  },
  tableCell: {
    fontSize: 15,
  },
  instrumentText: {
    fontSize: 15,
    color: '#007AFF',
  },
  picker: {
    height: 40,
    marginTop: -8,
  },
  editButton: {
    backgroundColor: '#007AFF',
    padding: 6,
    borderRadius: 6,
    alignItems: 'center',
    marginHorizontal: 8,
  },
  editButtonText: {
    color: 'white',
    fontSize: 13,
    fontWeight: '500',
  },
  playbackControls: {
    padding: 16,
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#E5E5E5',
  },
  playbackButtons: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 16,
    marginBottom: 16,
  },
  playbackButton: {
    backgroundColor: '#007AFF',
    width: 56,
    height: 56,
    borderRadius: 28,
    justifyContent: 'center',
    alignItems: 'center',
  },
  generateButton: {
    backgroundColor: '#34C759',
    padding: 16,
    borderRadius: 10,
    alignItems: 'center',
  },
  generateText: {
    color: 'white',
    fontSize: 17,
    fontWeight: '600',
  },
});
