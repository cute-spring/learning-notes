# Voice Input and Replay

This simple project allows users to:

- **Record their voice** via a button click.
- **Convert voice input to text** using the Web Speech API (`webkitSpeechRecognition`).
- **Replay the recorded audio** using the `<audio>` element in HTML.

## How it works:
1. **Recording**: When the user clicks "Start Recording", their voice is captured using the `MediaRecorder` API.
2. **Speech Recognition**: The recorded voice is processed using the Web Speech API for real-time transcription.
3. **Replay**: After stopping the recording, the user can replay the audio using the "Replay Audio" button.

## Technologies used:
- **MediaRecorder API**: For recording audio from the user's microphone.
- **Web Speech API**: For converting speech to text.
- **HTML5 Audio**: For replaying the recorded voice.

## Demo:
- Try recording your voice and see how it's transcribed in real-time. You can also replay the audio for confirmation.

## Notes:
- The Web Speech API (SpeechRecognition) is supported in **Google Chrome** and **Chromium-based browsers**. Make sure your browser allows microphone access.