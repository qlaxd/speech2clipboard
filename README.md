# Hungarian Speech to Clipboard

A Python application that transcribes Hungarian speech to text and automatically copies it to the clipboard.

## Features

- Record Hungarian speech through your microphone
- Transcribe speech to text using Wav2Vec2 model optimized for Hungarian language
- Automatically copy transcription to clipboard
- Simple and intuitive user interface

## Setup

1. Clone this repository
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python src/main.py
   ```

## Requirements

- Python 3.8 or higher
- Microphone for audio input
- Internet connection for initial model download

## Usage

1. Click the "Record" button or press the keyboard shortcut to start recording
2. Speak in Hungarian
3. Click "Stop" or release the key to end recording
4. The transcribed text will automatically be copied to your clipboard
5. Paste the text in any application

## License

MIT 