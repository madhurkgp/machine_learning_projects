import datetime
import wikipedia
import webbrowser
import time
import logging
from django.conf import settings
from .models import VoiceInteraction, VoiceCommand

# Try to import speech libraries, but handle gracefully if not available
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    sr = None

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    pyttsx3 = None

logger = logging.getLogger(__name__)


class VoiceAssistantService:
    """Service class for voice assistant functionality"""
    
    def __init__(self):
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
        else:
            self.recognizer = None
        self.microphone = None
        self.engine = None
        self._initialize_tts()
        
    def _initialize_tts(self):
        """Initialize text-to-speech engine"""
        if not TTS_AVAILABLE:
            logger.warning("TTS library not available")
            self.engine = None
            return
            
        try:
            self.engine = pyttsx3.init('sapi5')
            voices = self.engine.getProperty('voices')
            # Use first available voice (usually male)
            if voices:
                self.engine.setProperty('voice', voices[0].id)
            logger.info("Text-to-speech engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            self.engine = None
    
    def speak(self, text):
        """Convert text to speech"""
        if not self.engine:
            logger.warning("TTS engine not available")
            return False
            
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            return False
    
    def listen_for_command(self, timeout=5):
        """Listen for voice command and return transcribed text"""
        if not SPEECH_RECOGNITION_AVAILABLE:
            logger.warning("Speech recognition not available")
            return None, 0.0
            
        try:
            with sr.Microphone() as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Listening...")
                
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                logger.info("Processing speech...")
                
                # Try Google Speech Recognition first
                try:
                    text = self.recognizer.recognize_google(audio, language='en-in')
                    confidence = 1.0  # Google doesn't provide confidence in basic API
                    logger.info(f"Recognized: {text}")
                    return text, confidence
                except sr.UnknownValueError:
                    logger.warning("Google Speech Recognition could not understand audio")
                    # Try Sphinx as fallback
                    try:
                        text = self.recognizer.recognize_sphinx(audio)
                        confidence = 0.7  # Lower confidence for fallback
                        logger.info(f"Sphinx recognized: {text}")
                        return text, confidence
                    except sr.UnknownValueError:
                        logger.warning("Sphinx could not understand audio")
                        return None, 0.0
                        
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return None, 0.0
        except sr.WaitTimeoutError:
            logger.info("Listening timeout")
            return None, 0.0
        except Exception as e:
            logger.error(f"Error in speech recognition: {e}")
            return None, 0.0
    
    def get_greeting_message(self):
        """Generate appropriate greeting based on time of day"""
        hour = int(datetime.datetime.now().hour)
        
        if 0 <= hour < 12:
            greeting = "Good morning! It's a fine day!"
        elif 12 <= hour < 18:
            greeting = "Good afternoon! Hope you had your brunch!"
        else:
            greeting = "Good evening! The wind is lovely!"
            
        return f"{greeting} I am your personal AI Assistant Dave! How can I be of service?"
    
    def process_command(self, command_text):
        """Process voice command and return response"""
        if not command_text:
            return {
                'command_type': 'error',
                'response': "I couldn't understand your command. Please try again.",
                'action_taken': '',
                'is_successful': False
            }
        
        command_lower = command_text.lower()
        start_time = time.time()
        
        # Wikipedia search
        if 'wikipedia' in command_lower:
            try:
                search_term = command_lower.replace('wikipedia', '').strip()
                if search_term:
                    summary = wikipedia.summary(search_term, sentences=2)
                    response = f"According to Wikipedia, {summary}"
                    return {
                        'command_type': 'wikipedia',
                        'response': response,
                        'action_taken': f"Searched Wikipedia for '{search_term}'",
                        'is_successful': True
                    }
                else:
                    return {
                        'command_type': 'wikipedia',
                        'response': "What would you like me to search on Wikipedia?",
                        'action_taken': '',
                        'is_successful': False
                    }
            except Exception as e:
                logger.error(f"Wikipedia search error: {e}")
                return {
                    'command_type': 'wikipedia',
                    'response': "Sorry, I couldn't find information on that topic.",
                    'action_taken': '',
                    'is_successful': False
                }
        
        # Website opening commands
        website_commands = {
            'open youtube': ('https://youtube.com', 'Opening YouTube'),
            'open google': ('https://google.com', 'Opening Google'),
            'open instagram': ('https://instagram.com', 'Opening Instagram'),
            'open kaggle': ('https://kaggle.com', 'Opening Kaggle'),
            'the weather': ('https://weather.com', 'Opening weather website'),
            'the score': ('https://cricbuzz.com', 'Opening cricket scores'),
        }
        
        for trigger, (url, message) in website_commands.items():
            if trigger in command_lower:
                try:
                    webbrowser.open(url)
                    return {
                        'command_type': 'web_open',
                        'response': message,
                        'action_taken': f"Opened {url}",
                        'is_successful': True
                    }
                except Exception as e:
                    logger.error(f"Browser open error: {e}")
                    return {
                        'command_type': 'web_open',
                        'response': f"Sorry, I couldn't open the website.",
                        'action_taken': '',
                        'is_successful': False
                    }
        
        # Time query
        if 'the time' in command_lower:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            return {
                'command_type': 'time_query',
                'response': f"The current time is {current_time}",
                'action_taken': '',
                'is_successful': True
            }
        
        # Music command (placeholder)
        if 'play music' in command_lower:
            return {
                'command_type': 'web_open',
                'response': "I would play music, but I need access to your music files.",
                'action_taken': 'Music playback requested',
                'is_successful': False
            }
        
        # Default response for unknown commands
        return {
            'command_type': 'unknown',
            'response': "I'm not sure how to help with that. You can ask me to search Wikipedia, open websites like YouTube or Google, or tell you the time.",
            'action_taken': '',
            'is_successful': False
        }
    
    def save_interaction(self, voice_command, transcribed_text, response_data, confidence_score, response_time):
        """Save voice interaction to database"""
        try:
            interaction = VoiceInteraction.objects.create(
                voice_command=voice_command or '',
                transcribed_text=transcribed_text or '',
                command_type=response_data['command_type'],
                response_text=response_data['response'],
                action_taken=response_data['action_taken'],
                confidence_score=confidence_score,
                response_time_ms=response_time,
                is_successful=response_data['is_successful']
            )
            logger.info(f"Saved voice interaction: {interaction.id}")
            return interaction
        except Exception as e:
            logger.error(f"Error saving interaction: {e}")
            return None
    
    def get_command_suggestions(self):
        """Get list of available voice commands"""
        return [
            "Search Wikipedia - say 'wikipedia [topic]'",
            "Open YouTube - say 'open youtube'",
            "Open Google - say 'open google'",
            "Open Instagram - say 'open instagram'",
            "Check weather - say 'the weather'",
            "Check cricket scores - say 'the score'",
            "Get current time - say 'the time'",
            "Play music - say 'play music'"
        ]
    
    def test_microphone_access(self):
        """Test if microphone is accessible"""
        if not SPEECH_RECOGNITION_AVAILABLE:
            return False, "Speech recognition library not available"
            
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                return True, "Microphone is accessible"
        except Exception as e:
            return False, f"Microphone error: {e}"
