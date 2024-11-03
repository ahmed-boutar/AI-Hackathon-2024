import { View, StyleSheet, Text, Pressable } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Link, router } from 'expo-router';

export default function ResultsScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Processing Complete</Text>
      <View style={styles.resultContainer}>
        <Text>Your melody has been processed!</Text>
        {/* Add more UI elements to display the processed MIDI data */}
      </View>
      <Link href="/record" style={styles.link}>
        Record Another
      </Link>
      <Pressable
        style={[styles.button, styles.customizeButton]}
        onPress={() => router.push('/customize')}
      >
        <Text style={styles.buttonText}>Customize File</Text>
      </Pressable>
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
  resultContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  link: {
    color: '#007AFF',
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 20,
  },
  button: {
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
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