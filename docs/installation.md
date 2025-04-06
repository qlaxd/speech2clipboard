# Installation Guide

This document provides instructions for installing and running Hungarian Speech to Clipboard on different platforms.

## System Requirements

- Python 3.8 or higher
- CUDA-compatible GPU (recommended for faster transcription)
- Microphone for audio input
- Internet connection for initial model download

## Installation Methods

### Option 1: Install with pipx (Recommended)

[pipx](https://pypa.github.io/pipx/) installs the application in an isolated environment while making it available system-wide. This is the recommended approach, especially on Linux systems with externally managed Python environments.

1. Install pipx if you don't have it already:

   ```bash
   # On Arch Linux
   sudo pacman -S python-pipx

   # On Ubuntu/Debian
   sudo apt install python3-pipx

   # On macOS
   brew install pipx
   pipx ensurepath
   ```

2. Install speech2clipboard:

   ```bash
   # Navigate to the project directory
   cd speech2clipboard
   
   # Install using pipx
   pipx install .
   ```

3. The `speech2clipboard` command will now be available in your PATH.

### Option 2: Install in a Virtual Environment

This method is recommended for development or if you prefer more control over the environment.

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/speech2clipboard.git
   cd speech2clipboard
   ```

2. Create and activate a virtual environment:

   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate on Linux/macOS
   source .venv/bin/activate
   
   # Activate on Windows
   .venv\Scripts\activate
   ```

3. Install the package in development mode:

   ```bash
   pip install -e .
   ```

4. Run the application:

   ```bash
   # Using the entry point
   speech2clipboard
   
   # Or directly
   python src/main.py
   ```

### Option 3: Install from PyPI

*Note: This package is not yet available on PyPI.*

## Running the Application

After installation, you can run the application in one of these ways:

- If installed with pipx or as a system package:
  ```bash
  speech2clipboard
  ```

- If using a virtual environment (make sure it's activated):
  ```bash
  speech2clipboard
  # or
  python src/main.py
  ```

## Troubleshooting

### Missing Dependencies

If you encounter errors about missing packages, particularly with the speech recognition model, ensure you have all required dependencies:

```bash
pip install transformers torch sounddevice numpy pyperclip PyQt5 librosa python-dotenv scipy accelerate
```

### CUDA Support

For GPU acceleration:

1. Ensure you have installed PyTorch with CUDA support.
2. Verify CUDA is working:
   ```bash
   python -c "import torch; print(torch.cuda.is_available())"
   ```
   This should print `True` if CUDA is properly configured.

### Clipboard Issues

If the application can't access the clipboard:

- On Linux/Wayland: Install `wl-clipboard` package
- On Linux/X11: Install `xclip` or `xsel` packages

### Model Download Issues

The first time you run the application, it will download the Hungarian speech recognition model. This requires internet access and may take some time depending on your connection speed.

If the download fails:
- Check your internet connection
- Ensure you have sufficient disk space (the model is approximately 1GB)
- Try again later as the Hugging Face model servers might be temporarily unavailable

## Uninstalling

To uninstall:

```bash
# If installed with pipx
pipx uninstall speech2clipboard

# If installed in a virtual environment
# Simply delete the virtual environment directory
rm -rf .venv  # on Linux/macOS
``` 