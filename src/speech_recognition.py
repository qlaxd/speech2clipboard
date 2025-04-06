import torch
import librosa
import numpy as np
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, Wav2Vec2CTCTokenizer, Wav2Vec2FeatureExtractor

class SpeechRecognizer:
    def __init__(self, model_name="jonatasgrosman/wav2vec2-large-xlsr-53-hungarian"):
        """
        Initialize the speech recognizer with a Hungarian speech model.
        Default model: jonatasgrosman/wav2vec2-large-xlsr-53-hungarian - A Hungarian fine-tuned Wav2Vec2 model
        """
        self.sampling_rate = 16000  # Required sampling rate for the model
        self.processor = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"Initializing speech recognition model on {self.device}...")
        self.load_model(model_name)
        
    def load_model(self, model_name):
        """Load the Wav2Vec2 model and processor"""
        try:
            # Try loading with the standard processor first
            try:
                self.processor = Wav2Vec2Processor.from_pretrained(model_name)
            except Exception as e:
                print(f"Failed to load processor directly: {e}")
                # Manual fallback to load tokenizer and feature extractor separately
                tokenizer = Wav2Vec2CTCTokenizer.from_pretrained(model_name)
                feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(
                    model_name,
                    sampling_rate=self.sampling_rate,
                    padding_value=0.0,
                    do_normalize=True,
                    return_attention_mask=True
                )
                self.processor = Wav2Vec2Processor(feature_extractor=feature_extractor, tokenizer=tokenizer)
                
            self.model = Wav2Vec2ForCTC.from_pretrained(model_name).to(self.device)
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def preprocess_audio(self, audio_array):
        """Preprocess the audio to match model requirements"""
        # Resample if necessary
        if librosa.get_samplerate(audio_array) != self.sampling_rate:
            audio_array = librosa.resample(
                audio_array, 
                orig_sr=librosa.get_samplerate(audio_array), 
                target_sr=self.sampling_rate
            )
        
        # Normalize the audio
        audio_array = audio_array / np.max(np.abs(audio_array))
        
        return audio_array
    
    def transcribe(self, audio_array):
        """
        Transcribe the audio to text.
        
        Args:
            audio_array: Numpy array of audio samples
            
        Returns:
            transcription: String of transcribed text
        """
        try:
            # Preprocess the audio
            audio_array = self.preprocess_audio(audio_array)
            
            # Tokenize
            input_values = self.processor(
                audio_array, 
                sampling_rate=self.sampling_rate, 
                return_tensors="pt"
            ).input_values.to(self.device)
            
            # Retrieve logits
            with torch.no_grad():
                logits = self.model(input_values).logits
            
            # Take argmax and decode
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = self.processor.batch_decode(predicted_ids)[0]
            
            return transcription
        
        except Exception as e:
            print(f"Error during transcription: {e}")
            return "" 