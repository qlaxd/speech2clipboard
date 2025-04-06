#!/usr/bin/env python3

import os
import sys
import time
import numpy as np

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from audio_recorder import AudioRecorder

def test_recorder():
    """Simple test for the audio recorder"""
    recorder = AudioRecorder(sample_rate=16000, channels=1)
    
    print("Starting recording (3 seconds)...")
    recorder.start_recording()
    
    # Record for 3 seconds
    time.sleep(3)
    
    print("Stopping recording...")
    audio_data = recorder.stop_recording()
    
    # Check if we got any audio data
    if len(audio_data) > 0:
        print(f"Recording successful! Got {len(audio_data)} samples.")
        
        # Save the recorded audio to a file
        test_file = "test_recording.wav"
        success = recorder.save_to_file(test_file, audio_data)
        
        if success:
            print(f"Saved audio to {test_file}")
        else:
            print("Failed to save audio")
    else:
        print("No audio data recorded.")
        
if __name__ == "__main__":
    test_recorder() 