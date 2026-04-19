import librosa
import numpy as np
import json
from django.core.files.storage import default_storage
from .models import AudioFile, AudioAnalysis

class AudioProcessor:
    def __init__(self):
        self.frame_size = 1024
        self.hop_length = 512
    
    def process_audio_file(self, audio_file_instance):
        """Process uploaded audio file and extract features"""
        try:
            # Load audio file
            file_path = audio_file_instance.audio_file.path
            y, sr = librosa.load(file_path, sr=None)
            
            # Update audio file metadata
            audio_file_instance.duration = len(y) / sr
            audio_file_instance.sample_rate = sr
            audio_file_instance.save()
            
            # Extract features
            features = self.extract_features(y, sr)
            
            # Create analysis record
            analysis = AudioAnalysis.objects.create(
                audio_file=audio_file_instance,
                amplitude_envelope_avg=features['amplitude_envelope_avg'],
                zero_crossing_rate_avg=features['zero_crossing_rate_avg'],
                rms_energy_avg=features['rms_energy_avg'],
                spectral_centroid_avg=features['spectral_centroid_avg'],
                spectral_bandwidth_avg=features['spectral_bandwidth_avg'],
                spectral_rolloff_avg=features['spectral_rolloff_avg'],
                mfcc_features=features['mfcc_features'],
                frame_size=self.frame_size,
                hop_length=self.hop_length
            )
            
            return analysis
            
        except Exception as e:
            raise Exception(f"Error processing audio file: {str(e)}")
    
    def extract_features(self, y, sr):
        """Extract all audio features"""
        features = {}
        
        # Time domain features
        features['amplitude_envelope_avg'] = self.calculate_amplitude_envelope(y)
        features['zero_crossing_rate_avg'] = self.calculate_zero_crossing_rate(y)
        features['rms_energy_avg'] = self.calculate_rms_energy(y)
        
        # Frequency domain features
        features['spectral_centroid_avg'] = self.calculate_spectral_centroid(y, sr)
        features['spectral_bandwidth_avg'] = self.calculate_spectral_bandwidth(y, sr)
        features['spectral_rolloff_avg'] = self.calculate_spectral_rolloff(y, sr)
        
        # MFCC features
        features['mfcc_features'] = self.calculate_mfcc_features(y, sr)
        
        return features
    
    def calculate_amplitude_envelope(self, signal):
        """Calculate amplitude envelope"""
        amplitude_envelope = []
        
        for i in range(0, len(signal), self.hop_length):
            amplitude_envelope_current_frame = max(signal[i:i+self.frame_size])
            amplitude_envelope.append(amplitude_envelope_current_frame)
        
        return np.mean(amplitude_envelope)
    
    def calculate_zero_crossing_rate(self, signal):
        """Calculate zero crossing rate"""
        zcr = librosa.feature.zero_crossing_rate(
            signal, 
            frame_length=self.frame_size, 
            hop_length=self.hop_length
        )[0]
        return np.mean(zcr)
    
    def calculate_rms_energy(self, signal):
        """Calculate RMS energy"""
        rms = librosa.feature.rms(
            signal, 
            frame_length=self.frame_size, 
            hop_length=self.hop_length
        )[0]
        return np.mean(rms)
    
    def calculate_spectral_centroid(self, signal, sr):
        """Calculate spectral centroid"""
        spectral_centroids = librosa.feature.spectral_centroid(
            y=signal, 
            sr=sr, 
            hop_length=self.hop_length
        )[0]
        return np.mean(spectral_centroids)
    
    def calculate_spectral_bandwidth(self, signal, sr):
        """Calculate spectral bandwidth"""
        spectral_bandwidth = librosa.feature.spectral_bandwidth(
            y=signal, 
            sr=sr, 
            hop_length=self.hop_length
        )[0]
        return np.mean(spectral_bandwidth)
    
    def calculate_spectral_rolloff(self, signal, sr):
        """Calculate spectral rolloff"""
        spectral_rolloff = librosa.feature.spectral_rolloff(
            y=signal, 
            sr=sr, 
            hop_length=self.hop_length
        )[0]
        return np.mean(spectral_rolloff)
    
    def calculate_mfcc_features(self, signal, sr):
        """Calculate MFCC features"""
        mfccs = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=13)
        
        # Calculate statistics for each MFCC coefficient
        mfcc_stats = {}
        for i in range(mfccs.shape[0]):
            mfcc_stats[f'mfcc_{i+1}_mean'] = float(np.mean(mfccs[i]))
            mfcc_stats[f'mfcc_{i+1}_std'] = float(np.std(mfccs[i]))
            mfcc_stats[f'mfcc_{i+1}_min'] = float(np.min(mfccs[i]))
            mfcc_stats[f'mfcc_{i+1}_max'] = float(np.max(mfccs[i]))
        
        return mfcc_stats
    
    def get_audio_insights(self, analysis):
        """Generate insights based on audio features"""
        insights = []
        
        # Analyze zero crossing rate
        if analysis.zero_crossing_rate_avg:
            if analysis.zero_crossing_rate_avg > 0.1:
                insights.append("High zero crossing rate suggests percussive or noisy content")
            else:
                insights.append("Low zero crossing rate suggests tonal or harmonic content")
        
        # Analyze RMS energy
        if analysis.rms_energy_avg:
            if analysis.rms_energy_avg > 0.2:
                insights.append("High RMS energy indicates loud audio content")
            else:
                insights.append("Low RMS energy indicates quiet audio content")
        
        # Analyze spectral centroid
        if analysis.spectral_centroid_avg:
            if analysis.spectral_centroid_avg > 2000:
                insights.append("High spectral centroid suggests bright, treble-heavy content")
            else:
                insights.append("Low spectral centroid suggests dark, bass-heavy content")
        
        return insights
