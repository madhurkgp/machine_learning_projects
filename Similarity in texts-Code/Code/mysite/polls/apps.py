from django.apps import AppConfig
import pickle
import os
import logging

logger = logging.getLogger(__name__)

word_embed = None

def startup():
    """Load word embeddings model"""
    global word_embed
    try:
        # This file has the information on every common word and its embeddings.
        model_path = os.path.join(os.path.dirname(__file__), 'word_embeddings_smaller.pickle')
        with open(model_path, 'rb') as save_data:
            word_embed = pickle.load(save_data)
        
        # If it's a Word2Vec model, get the vocabulary
        if hasattr(word_embed, 'wv'):
            logger.info("Word2Vec model loaded successfully")
        else:
            logger.info("Word embeddings loaded successfully")
    except Exception as e:
        logger.error(f"Error loading word embeddings: {e}")
        word_embed = None


class PollsConfig(AppConfig):
    name = 'polls'
    verbose_name = "Text Similarity Application"

    def ready(self):
        # Only load model when running the server, not during migrations
        if os.environ.get('RUN_MAIN') or os.environ.get('DJANGO_SETTINGS_MODULE'):
            startup()
