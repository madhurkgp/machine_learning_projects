import librosa
import numpy as np
import time
import os
from django.conf import settings

# Try to import TensorFlow, but make it optional
try:
    import tensorflow as tf
    from sklearn.preprocessing import LabelEncoder
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("Warning: TensorFlow not available. Using fallback predictions.")


class AudioFeatureExtractor:
    """Service for extracting audio features from audio files"""
    
    FRAME_SIZE = 1024
    HOP_LENGTH = 512
    N_MFCC = 10
    
    @staticmethod
    def extract_mfcc(file_path, n_mfcc=10):
        """Extract MFCC features from audio file"""
        try:
            audio, sr = librosa.load(file_path)
            mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
            mfccs_scaled = np.mean(mfccs.T, axis=0)
            return mfccs_scaled.tolist()
        except Exception as e:
            raise Exception(f"Error extracting MFCC features: {str(e)}")
    
    @staticmethod
    def extract_zcr(file_path):
        """Extract Zero Crossing Rate features from audio file"""
        try:
            audio, sr = librosa.load(file_path)
            zcr = librosa.feature.zero_crossing_rate(
                audio, 
                frame_length=AudioFeatureExtractor.FRAME_SIZE, 
                hop_length=AudioFeatureExtractor.HOP_LENGTH
            )[0]
            zcr_scaled = np.mean(zcr.T, axis=0)
            return zcr_scaled.tolist() if isinstance(zcr_scaled, np.ndarray) else [float(zcr_scaled)]
        except Exception as e:
            raise Exception(f"Error extracting ZCR features: {str(e)}")
    
    @staticmethod
    def get_audio_duration(file_path):
        """Get audio file duration in seconds"""
        try:
            audio, sr = librosa.load(file_path)
            duration = librosa.get_duration(y=audio, sr=sr)
            return duration
        except Exception as e:
            raise Exception(f"Error getting audio duration: {str(e)}")


class AudioClassificationService:
    """Service for audio classification using neural network"""
    
    # UrbanSound8K classes
    CLASSES = [
        'air_conditioner', 'car_horn', 'children_playing', 'dog_bark', 
        'drilling', 'engine_idling', 'gun_shot', 'jackhammer', 
        'siren', 'street_music'
    ]
    
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the neural network model"""
        if not TENSORFLOW_AVAILABLE:
            self.model = None
            self.label_encoder = None
            return
            
        try:
            self.model = self._create_model()
            # In a real application, you would load pre-trained weights here
            # self.model.load_weights('path/to/pretrained_weights.h5')
            
            # Initialize label encoder
            self.label_encoder = LabelEncoder()
            self.label_encoder.fit(self.CLASSES)
        except Exception as e:
            print(f"Warning: Could not initialize model: {str(e)}")
            self.model = None
            self.label_encoder = None
    
    def _create_model(self):
        """Create the neural network architecture (same as in notebook)"""
        if not TENSORFLOW_AVAILABLE:
            return None
            
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(100, input_shape=(10,), activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(200, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(100, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(len(self.CLASSES), activation='sigmoid')
        ])
        
        model.compile(
            loss='categorical_crossentropy',
            metrics=['accuracy'],
            optimizer='adam'
        )
        
        return model
    
    def classify_audio(self, file_path):
        """Classify audio file and return results"""
        start_time = time.time()
        
        try:
            # Extract features
            mfcc_features = AudioFeatureExtractor.extract_mfcc(file_path, n_mfcc=10)
            
            # Prepare input for model
            features = np.array(mfcc_features).reshape(1, -1)
            
            if self.model is None:
                # Fallback to random prediction if model is not available
                predictions = np.random.random(len(self.CLASSES))
                predictions = predictions / np.sum(predictions)
            else:
                # Get model predictions
                predictions = self.model.predict(features, verbose=0)[0]
            
            # Get predicted class and confidence
            predicted_index = np.argmax(predictions)
            predicted_class = self.CLASSES[predicted_index]
            confidence = float(predictions[predicted_index])
            
            # Create detailed results for all classes
            class_probabilities = []
            for i, class_name in enumerate(self.CLASSES):
                class_probabilities.append({
                    'class_name': class_name,
                    'probability': float(predictions[i])
                })
            
            # Sort by probability
            class_probabilities.sort(key=lambda x: x['probability'], reverse=True)
            
            processing_time = time.time() - start_time
            
            return {
                'predicted_class': predicted_class,
                'confidence_score': confidence,
                'class_probabilities': class_probabilities,
                'processing_time': processing_time,
                'mfcc_features': mfcc_features,
                'success': True
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            return {
                'predicted_class': None,
                'confidence_score': 0.0,
                'class_probabilities': [],
                'processing_time': processing_time,
                'mfcc_features': None,
                'success': False,
                'error': str(e)
            }


class SampleDataService:
    """Service for providing sample audio data for testing"""
    
    @staticmethod
    def get_sample_audio_info():
        """Get information about sample audio files"""
        sample_files = [
            {
                'name': 'dog_bark_sample',
                'description': 'Dog barking sound',
                'expected_class': 'dog_bark',
                'file_path': 'sample_audio/dog_bark.wav'
            },
            {
                'name': 'car_horn_sample',
                'description': 'Car horn sound',
                'expected_class': 'car_horn',
                'file_path': 'sample_audio/car_horn.wav'
            },
            {
                'name': 'street_music_sample',
                'description': 'Street music performance',
                'expected_class': 'street_music',
                'file_path': 'sample_audio/street_music.wav'
            }
        ]
        return sample_files
    
    @staticmethod
    def create_sample_audio_files():
        """Create sample audio files for testing (placeholder)"""
        # In a real application, you would provide actual audio files
        # For now, we'll return the paths where they should be
        sample_dir = os.path.join(settings.MEDIA_ROOT, 'sample_audio')
        os.makedirs(sample_dir, exist_ok=True)
        
        sample_files = []
        for sample in SampleDataService.get_sample_audio_info():
            file_path = os.path.join(settings.MEDIA_ROOT, sample['file_path'])
            if os.path.exists(file_path):
                sample_files.append({
                    **sample,
                    'file_path': file_path,
                    'exists': True
                })
            else:
                sample_files.append({
                    **sample,
                    'file_path': file_path,
                    'exists': False
                })
        
        return sample_files
