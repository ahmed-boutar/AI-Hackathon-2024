import { View, StyleSheet, Text } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Link } from 'expo-router';

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
});