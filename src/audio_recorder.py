import sounddevice as sd
import numpy as np
import threading
import time
from scipy.io import wavfile

class AudioRecorder:
    def __init__(self, sample_rate=16000, channels=1):
        """
        Initialize the audio recorder.
        
        Args:
            sample_rate: Sampling rate in Hz (default 16000)
            channels: Number of channels (1 for mono, 2 for stereo)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.audio_data = []
        self.record_thread = None
        
    def start_recording(self):
        """Start recording audio from the microphone"""
        if self.recording:
            return
        
        self.recording = True
        self.audio_data = []
        
        # Start recording in a separate thread
        self.record_thread = threading.Thread(target=self._record)
        self.record_thread.daemon = True
        self.record_thread.start()
        
    def stop_recording(self):
        """Stop recording audio and return the recorded data"""
        if not self.recording:
            return np.array([])
        
        self.recording = False
        
        # Wait for the recording thread to finish
        if self.record_thread:
            self.record_thread.join()
            
        # Combine all audio chunks
        if len(self.audio_data) > 0:
            return np.concatenate(self.audio_data)
        else:
            return np.array([])
    
    def is_recording(self):
        """Check if recording is in progress"""
        return self.recording
    
    def _record(self):
        """Internal method to record audio"""
        def callback(indata, frames, time, status):
            if status:
                print(f"Status: {status}")
            # Add the audio data to our list
            self.audio_data.append(indata.copy())
        
        # Start the recording stream
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=callback
        ):
            # Keep the stream open until recording is stopped
            while self.recording:
                time.sleep(0.1)
    
    def save_to_file(self, filename, audio_data=None):
        """
        Save the recorded audio to a WAV file.
        
        Args:
            filename: Name of the file to save to
            audio_data: Audio data to save (if None, use the last recorded data)
        """
        if audio_data is None:
            if len(self.audio_data) == 0:
                print("No audio data to save")
                return False
            
            audio_data = np.concatenate(self.audio_data)
        
        try:
            # Ensure audio data is the right shape
            if audio_data.ndim > 1 and self.channels == 1:
                audio_data = audio_data.flatten()
            
            # Scale to int16 range
            audio_data = (audio_data * 32767).astype(np.int16)
            
            # Save as WAV
            wavfile.write(filename, self.sample_rate, audio_data)
            return True
        except Exception as e:
            print(f"Error saving audio: {e}")
            return False 