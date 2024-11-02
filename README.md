# AI Music Translator Hackathon Project

An AI-driven app that translates hummed melodies into instrumental music.

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)
- Expo Go app installed on your mobile device

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd ai-hackathon-project
```

2. Install dependencies:
```bash
npm install
```
```bash
npx expo install expo-av
```

3. Start the development server:
```bash
npx expo start
```

## Running on Physical Device

1. Install Expo Go on your mobile device
2. Connect your device to the same WiFi network as your computer
3. Scan the QR code with:
   - iOS: Use the Camera app
   - Android: Use the Expo Go app

## Development Setup

To run the app in development mode on a connected device:

```bash
# For iOS
npx expo run:ios

# For Android
npx expo run:android
```

## Environment Setup

1. Create a `.env` file in the root directory:
```env
API_URL=your_backend_url
```

## Available Scripts

- `npm start` - Start the Expo development server
- `npm run android` - Start the app on Android
- `npm run ios` - Start the app on iOS
- `npm run test` - Run tests
- `npm run lint` - Run ESLint

## Troubleshooting

If you encounter any issues:

1. Clear npm cache:
```bash
npm cache clean --force
```

2. Delete node_modules and reinstall:
```bash
rm -rf node_modules
npm install
```

3. Reset Expo cache:
```bash
npx expo start -c
```