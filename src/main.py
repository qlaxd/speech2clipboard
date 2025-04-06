#!/usr/bin/env python3

import sys
import os
import threading
import numpy as np
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt, QObject

# Import custom modules
from src.speech_recognition import SpeechRecognizer
from src.audio_recorder import AudioRecorder
from src.clipboard_manager import ClipboardManager
from src.ui.main_window import MainWindow

class SpeechProcessThread(QThread):
    """Thread for processing speech in the background"""
    
    # Signal to send transcription back to the main thread
    transcription_ready = pyqtSignal(str)
    
    def __init__(self, audio_data, recognizer):
        """
        Initialize the speech processing thread.
        
        Args:
            audio_data: Audio data as numpy array
            recognizer: SpeechRecognizer instance
        """
        super().__init__()
        self.audio_data = audio_data
        self.recognizer = recognizer
    
    def run(self):
        """Process the audio data and emit the result"""
        try:
            # Transcribe the audio
            transcription = self.recognizer.transcribe(self.audio_data)
            
            # Emit the transcription signal
            self.transcription_ready.emit(transcription)
        except Exception as e:
            print(f"Error in speech processing thread: {e}")
            self.transcription_ready.emit("")


class SpeechToClipboardApp(QObject):
    """Main application class"""
    
    def __init__(self):
        """Initialize the application"""
        super().__init__() # Call QObject initializer
        # Create Qt application
        self.app = QApplication(sys.argv)
        
        # Initialize components
        self.setup_components()
        
        # Connect signals
        self.connect_signals()
        
        # Show the main window
        self.window.show()
    
    def setup_components(self):
        """Initialize the application components"""
        # Create the speech recognizer
        self.recognizer = SpeechRecognizer()
        
        # Create the audio recorder
        self.recorder = AudioRecorder(sample_rate=16000, channels=1)
        
        # Create the clipboard manager
        self.clipboard = ClipboardManager()
        
        # Create the main window
        self.window = MainWindow()
    
    def connect_signals(self):
        """Connect the signals between components"""
        # Connect recording signals
        self.window.start_recording_signal.connect(self.start_recording)
        self.window.stop_recording_signal.connect(self.stop_recording)
        
        # Connect clipboard button
        self.window.clipboard_btn.clicked.connect(self.copy_to_clipboard)
    
    @pyqtSlot()
    def start_recording(self):
        """Start recording audio"""
        self.recorder.start_recording()
    
    @pyqtSlot()
    def stop_recording(self):
        """Stop recording and process the audio"""
        # Stop the recording
        audio_data = self.recorder.stop_recording()
        
        if len(audio_data) > 0:
            # Create and start a thread for processing
            self.process_thread = SpeechProcessThread(audio_data, self.recognizer)
            self.process_thread.transcription_ready.connect(self.handle_transcription)
            self.process_thread.start()
        else:
            self.window.status_bar.showMessage("No audio recorded", 3000)
            self.window.recording_status.setText("Ready")
    
    @pyqtSlot(str)
    def handle_transcription(self, text):
        """Handle the transcription result"""
        # Update the UI
        self.window.set_transcription(text)
        
        # Automatically copy to clipboard if there's text
        if text:
            self.copy_to_clipboard()
    
    def copy_to_clipboard(self):
        """Copy the transcription to clipboard"""
        text = self.window.get_transcription()
        if text:
            success = self.clipboard.copy_to_clipboard(text)
            if success:
                self.window.status_bar.showMessage("Copied to clipboard!", 3000)
            else:
                self.window.status_bar.showMessage("Failed to copy to clipboard", 3000)
    
    def run(self):
        """Run the application"""
        # Exit when the application is closed
        return self.app.exec_()


if __name__ == "__main__":
    # Create and run the application
    app = SpeechToClipboardApp()
    sys.exit(app.run())

def main():
    """Entry point for the application"""
    app = SpeechToClipboardApp()
    return app.run() 