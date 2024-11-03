import { View, StyleSheet, Text, Pressable, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Picker } from '@react-native-picker/picker';
import { Ionicons } from '@expo/vector-icons';
import { useState } from 'react';
import { router } from 'expo-router';
import { Audio } from 'expo-av';
import { useEffect } from 'react';

interface AudioFile {
  uri: string;
}

interface AudioFiles {
  [key: string]: string; // The key will be in the format "trackId_instrument"
}

interface Track {
  id: string;
  fileName: string;
  instrument: string;
}
const API_BASE_URL = 'http://10.197.92.154:5001';

// export default function CustomizeScreen() {
//   const [selectedInstrument, setSelectedInstrument] = useState('piano');
//   const [isPlaying, setIsPlaying] = useState(false);

//   // State to track which row's instrument is being edited
//   const [editingInstrumentId, setEditingInstrumentId] = useState(null);

//   const [sound, setSound] = useState<Audio.Sound | null>(null);
//   const [currentTrack, setCurrentTrack] = useState<string | null>(null);
//   const [audioFiles, setAudioFiles] = useState<AudioFiles>({});
//   const [tracks, setTracks] = useState<Track[]>([
//     { id: '1', fileName: 'melody_001.mid', instrument: 'Piano' },
//     { id: '2', fileName: 'melody_002.mid', instrument: 'Piano' },
//   ]);

//   const API_BASE_URL = 'http://10.197.92.154:5001';

//   // Fetch audio files when component mounts
//   useEffect(() => {
//     fetchAudioFiles();
//     return () => {
//       // Cleanup sound when component unmounts
//       if (sound) {
//         sound.unloadAsync();
//       }
//     };
//   }, []);

//   // const handleInstrumentChange = (trackId: any, instrument: string) => {
//   //   // Update the instrument for the specific track
//   //   setTracks((prevTracks) =>
//   //     prevTracks.map((track) =>
//   //       track.id === trackId ? { ...track, instrument } : track
//   //     )
//   //   );
//   //   setEditingInstrumentId(null); // Close the picker after selection
//   //   console.log(tracks)
//   // };
//   const handleInstrumentChange = async (trackId: string, instrument: string) => {
//     setTracks((prevTracks) =>
//       prevTracks.map((track) =>
//         track.id === trackId ? { ...track, instrument } : track
//       )
//     );
//     setEditingInstrumentId(null);
  
//     // If this track is currently playing, switch to the new instrument
//     if (isPlaying && currentTrack === trackId) {
//       await playAudio(trackId, instrument);
//     }
//   };

//   const fetchAudioFiles = async () => {
//     try {
//       const response = await fetch(`${API_BASE_URL}/api/latest-recordings`);
//       const data = await response.json();
      
//       // Type assertion for the response data
//       const audioFiles: AudioFiles = data.audio_files;
//       const fetchedTracks: Track[] = data.tracks.map((track: any) => ({
//         id: track.id,
//         fileName: track.fileName,
//         instrument: 'Piano' // default instrument
//       }));
  
//       setAudioFiles(audioFiles);
//       setTracks(fetchedTracks);
//     } catch (error) {
//       console.error('Error fetching audio files:', error);
//     }
//   };

//   const playAudio = async (trackId: string, instrument: string) => {
//     try {
//       // Unload previous sound if exists
//       if (sound) {
//         await sound.unloadAsync();
//       }
  
//       // Create the key in a type-safe way
//       const audioKey = `${trackId}_${instrument.toLowerCase()}` as keyof AudioFiles;
//       const audioUrl = audioFiles[audioKey];
      
//       if (!audioUrl) {
//         console.error('Audio file not found');
//         return;
//       }
  
//       // Load and play the sound
//       const { sound: newSound } = await Audio.Sound.createAsync(
//         { uri: audioUrl },
//         { shouldPlay: true }
//       );
      
//       setSound(newSound);
//       setIsPlaying(true);
//       setCurrentTrack(trackId);
  
//       // Handle playback status updates
//       newSound.setOnPlaybackStatusUpdate((status) => {
//         if ("didJustFinish" in status && status.didJustFinish) {
//           setIsPlaying(false);
//         }
//       });
//     } catch (error) {
//       console.error('Error playing audio:', error);
//     }
//   };

//   const handlePlayPause = async (trackId: string) => {
//     if (isPlaying) {
//       await sound?.pauseAsync();
//       setIsPlaying(false);
//     } else {
//       const track = tracks.find(t => t.id === trackId);
//       if (track) {
//         await playAudio(trackId, track.instrument);
//       }
//     }
//   };

//   const handleStop = async () => {
//     if (sound) {
//       await sound.stopAsync();
//       await sound.setPositionAsync(0);
//       setIsPlaying(false);
//     }
//   };

//   return (
//     <SafeAreaView style={styles.container}>
//       {/* Header */}
//       <View style={styles.header}>
//         <Pressable onPress={() => router.back()} style={styles.backButton}>
//           <Ionicons name="chevron-back" size={24} color="#007AFF" />
//           <Text style={styles.backText}>Back</Text>
//         </Pressable>
//         <Text style={styles.title}>Customize Melody</Text>
//         <Pressable style={styles.exportButton} onPress={() => console.log('Export')}>
//           <Text style={styles.exportText}>Export</Text>
//         </Pressable>
//       </View>

//       {/* Table */}
//       <View style={styles.tableContainer}>
//         <View style={styles.tableHeader}>
//           <Text style={[styles.tableHeaderText, { flex: 2 }]}>Instrument</Text>
//           <Text style={[styles.tableHeaderText, { flex: 2 }]}>File Name</Text>
//           <Text style={[styles.tableHeaderText, { flex: 1 }]}>Actions</Text>
//         </View>

//         {tracks.map((track) => (
//           <View key={track.id} style={styles.tableRow}>
//             <View style={{ flex: 2 }}>
//               {editingInstrumentId === track.id ? (
//                 <Picker
//                   selectedValue={track.instrument}
//                   style={styles.picker}
//                   onValueChange={(value) => handleInstrumentChange(track.id, value)}
//                 >
//                   <Picker.Item label="Piano" value="Piano" />
//                   <Picker.Item label="Guitar" value="Guitar" />
//                   <Picker.Item label="Violin" value="Violin" />
//                   <Picker.Item label="Saxophone" value="Saxophone" />
//                 </Picker>
//               ) : (
//                 <Pressable onPress={() => setEditingInstrumentId(track.id)}>
//                   <Text style={styles.instrumentText}>{track.instrument}</Text>
//                 </Pressable>
//               )}
//             </View>
//             <Text style={[styles.tableCell, { flex: 2 }]}>{track.fileName}</Text>
//             <Pressable 
//               style={[styles.editButton, { flex: 1 }]}
//               onPress={() => router.push('/edit-midi')}
//             >
//               <Text style={styles.editButtonText}>Edit MIDI</Text>
//             </Pressable>
//           </View>
//         ))}
//       </View>

//       {/* Playback Controls */}
//       <View style={styles.playbackControls}>
//         <View style={styles.playbackButtons}>
//           <Pressable
//             style={styles.playbackButton}
//             onPress={() => currentTrack && handlePlayPause(currentTrack)}
//           >
//             <Ionicons 
//               name={isPlaying ? "pause" : "play"} 
//               size={28} 
//               color="white" 
//             />
//           </Pressable>
//           <Pressable 
//             style={styles.playbackButton}
//             onPress={handleStop}
//           >
//             <Ionicons name="stop" size={28} color="white" />
//           </Pressable>
//         </View>
//     </SafeAreaView>
//   );
// }
export default function CustomizeScreen() {
  const [tracks, setTracks] = useState<Track[]>([]);
  const [audioFiles, setAudioFiles] = useState<AudioFiles>({});
  const [sound, setSound] = useState<Audio.Sound | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTrack, setCurrentTrack] = useState<string | null>(null);
  const [editingInstrumentId, setEditingInstrumentId] = useState<string | null>(null);

  // Fetch data when component mounts
  useEffect(() => {
    fetchLatestRecordings();
    return () => {
      // Cleanup sound when component unmounts
      if (sound) {
        sound.unloadAsync();
      }
    };
  }, []);

  const fetchLatestRecordings = async () => {
    try {
      console.log('Fetching from:', `${API_BASE_URL}/api/latest-recordings`);
      const response = await fetch(`${API_BASE_URL}/api/latest-recordings`);
      const data = await response.json();
      
      if (data.error) {
        console.error('API Error:', data.error);
        return;
      }

      console.log('Received data:', data);
      
      if (data.tracks && Array.isArray(data.tracks)) {
        setTracks(data.tracks.map((track: any) => ({
          id: track.id,
          fileName: track.fileName,
          instrument: track.instrument || 'Piano'
        })));
      }

      if (data.audio_files) {
        setAudioFiles(data.audio_files);
      }
    } catch (error) {
      console.error('Error fetching audio files:', error);
    }
  };

  const playAudio = async (trackId: string, instrument: string) => {
    try {
      // Stop current playback
      if (sound) {
        await sound.unloadAsync();
      }

      const fileName = tracks.find(t => t.id === trackId)?.fileName;
      if (!fileName) return;

      const audioKey = `${fileName.replace('.mid', '')}_${instrument.toLowerCase()}`;
      let audioUrl = audioFiles[audioKey];

      if (!audioUrl) {
        console.error('Audio file not found');
        return;
      }

      // Construct full URL
      audioUrl = `${API_BASE_URL}${audioUrl}`;
      console.log('Playing audio from:', audioUrl); // Debug log

      // Load and play the sound
      const { sound: newSound } = await Audio.Sound.createAsync(
        { 
          uri: audioUrl,
          headers: {
            'Accept': 'audio/wav',
            'Range': 'bytes=0-' // Add range header for iOS
          }
        },
        { 
          shouldPlay: true,
          volume: 1.0,
          progressUpdateIntervalMillis: 1000,
        },
        (status) => {
          console.log('Playback status:', status); // Debug log
        }
      );

      setSound(newSound);
      setIsPlaying(true);
      setCurrentTrack(trackId);

      // Handle playback status updates
      newSound.setOnPlaybackStatusUpdate((status: any) => {
        if (status.isLoaded) {
          if (status.didJustFinish) {
            setIsPlaying(false);
            setCurrentTrack(null);
          }
        } else if (status.error) {
          console.error('Playback error:', status.error);
          setIsPlaying(false);
          setCurrentTrack(null);
        }
      });

    } catch (error) {
      console.error('Error playing audio:', error);
      setIsPlaying(false);
      setCurrentTrack(null);
      
      Alert.alert(
        'Playback Error',
        'Unable to play the audio file. Please try again.'
      );
    }
};

const handlePlayPause = async () => {
  try {
    if (!currentTrack) {
      // If no track is selected, play the first one
      const firstTrack = tracks[0];
      if (firstTrack) {
        await playAudio(firstTrack.id, firstTrack.instrument);
      }
      return;
    }

    if (isPlaying && sound) {
      await sound.pauseAsync();
      setIsPlaying(false);
    } else {
      const track = tracks.find(t => t.id === currentTrack);
      if (track) {
        await playAudio(track.id, track.instrument);
      }
    }
  } catch (error) {
    console.error('Error handling play/pause:', error);
    Alert.alert(
      'Playback Error',
      'An error occurred while playing the audio.'
    );
  }
};

  const handleStop = async () => {
    if (sound) {
      await sound.stopAsync();
      await sound.setPositionAsync(0);
      setIsPlaying(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* Your existing header */}
      <View style={styles.header}>
        <Pressable onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="chevron-back" size={24} color="#007AFF" />
          <Text style={styles.backText}>Back</Text>
        </Pressable>
        <Text style={styles.title}>Customize Melody</Text>
        <Pressable style={styles.exportButton}>
          <Ionicons name="share-outline" size={24} color="white" />
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
          <Pressable 
            key={track.id} 
            style={[
              styles.tableRow,
              currentTrack === track.id && styles.selectedRow
            ]}
            onPress={() => setCurrentTrack(track.id)}
          >
            <View style={{ flex: 2 }}>
              {editingInstrumentId === track.id ? (
                <Picker
                  selectedValue={track.instrument}
                  style={styles.picker}
                  onValueChange={(value) => {
                    setTracks(tracks.map(t => 
                      t.id === track.id ? {...t, instrument: value} : t
                    ));
                    setEditingInstrumentId(null);
                  }}
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
          </Pressable>
        ))}
      </View>

      {/* Playback Controls */}
      <View style={styles.playbackControls}>
        <View style={styles.playbackButtons}>
          <Pressable
            style={styles.playbackButton}
            onPress={handlePlayPause}
          >
            <Ionicons 
              name={isPlaying ? "pause" : "play"} 
              size={28} 
              color="white" 
            />
          </Pressable>
          <Pressable 
            style={styles.playbackButton}
            onPress={handleStop}
          >
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
  selectedRow: {
    backgroundColor: '#f0f0f0',
  },
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
