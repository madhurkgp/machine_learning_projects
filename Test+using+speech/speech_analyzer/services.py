import speech_recognition as sr
import pandas as pd
import numpy as np
from pydub import AudioSegment
from collections import Counter
import os


class SpeechAnalyzerService:
    """Service class for speech recognition and text analysis"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def analyze_audio_file(self, audio_file_path):
        """
        Analyze audio file and return comprehensive results
        """
        try:
            # Get audio duration
            audio_duration = self._get_audio_duration(audio_file_path)
            
            # Perform speech recognition
            transcribed_text = self._transcribe_audio(audio_file_path)
            
            if not transcribed_text:
                return {
                    'success': False,
                    'error': 'Could not transcribe audio'
                }
            
            # Perform text analysis
            text_analysis = self._analyze_text(transcribed_text, audio_duration)
            
            return {
                'success': True,
                'transcribed_text': transcribed_text,
                'audio_duration': audio_duration,
                **text_analysis
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_audio_duration(self, audio_file_path):
        """Get audio file duration in minutes"""
        try:
            audio = AudioSegment.from_file(audio_file_path)
            duration_seconds = len(audio) / 1000.0
            return duration_seconds / 60.0  # Convert to minutes
        except Exception:
            return 0.0
    
    def _transcribe_audio(self, audio_file_path):
        """Transcribe audio file to text using Google Speech Recognition"""
        try:
            with sr.AudioFile(audio_file_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Record the audio
                audio_data = self.recognizer.record(source)
                
                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(audio_data)
                return text
                
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            raise Exception(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            raise Exception(f"Error processing audio file: {e}")
    
    def _analyze_text(self, text, audio_duration):
        """Analyze transcribed text for various metrics"""
        # Split text into words
        words = text.split(' ')
        words = [word.strip() for word in words if word.strip()]
        
        # Basic metrics
        word_count = len(words)
        unique_words = len(set(words))
        
        # Calculate words per minute
        if audio_duration > 0:
            words_per_minute = word_count / audio_duration
        else:
            words_per_minute = 0
        
        # Word frequency analysis
        word_counter = Counter(words)
        word_frequencies = dict(word_counter.most_common())
        
        # Generate insights
        insights = self._generate_insights(words, word_count, unique_words, words_per_minute)
        
        return {
            'word_count': word_count,
            'unique_words': unique_words,
            'words_per_minute': round(words_per_minute, 2),
            'word_frequencies': word_frequencies,
            'insights': insights
        }
    
    def _generate_insights(self, words, word_count, unique_words, words_per_minute):
        """Generate insights based on text analysis"""
        insights = []
        
        # Speaking speed analysis
        if words_per_minute > 150:
            insights.append("Fast speaking speed detected (over 150 WPM)")
        elif words_per_minute < 100:
            insights.append("Slow speaking speed detected (under 100 WPM)")
        else:
            insights.append("Normal speaking speed (100-150 WPM)")
        
        # Vocabulary diversity
        if word_count > 0:
            diversity_ratio = unique_words / word_count
            if diversity_ratio > 0.7:
                insights.append("High vocabulary diversity detected")
            elif diversity_ratio < 0.4:
                insights.append("Low vocabulary diversity - consider using more varied vocabulary")
            else:
                insights.append("Moderate vocabulary diversity")
        
        # Content length
        if word_count < 20:
            insights.append("Short content - very brief speech")
        elif word_count > 200:
            insights.append("Long content - detailed speech")
        else:
            insights.append("Medium length content")
        
        return insights
