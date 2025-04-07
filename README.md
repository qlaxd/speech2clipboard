# Hungarian Speech to Clipboard

A Python application that transcribes Hungarian speech to text and automatically copies it to the clipboard.

## Features
- Privacy focused: it uses your own GPU for speech recognition - data doesn't leave your hardware
- Record Hungarian speech through your microphone
- Transcribe speech to text using Wav2Vec2 model optimized for Hungarian language
- Automatically copy transcription to clipboard
- Simple and intuitive user interface

## Setup

For detailed installation instructions, please see the [Installation Guide](docs/installation.md).

Quick installation:

```bash
# For system-wide installation (recommended)
pipx install .

# For development in a virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -e .
```

## Requirements

- Python 3.13.2 or higher
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
