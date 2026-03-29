from django.shortcuts import render
import numpy as np
import logging
from .apps import word_embed
from .utils import Cleaning, removeStopwords, cosine_similarity

logger = logging.getLogger(__name__)

def index_func(request):
    similarity = 0
    error_message = None
    processed_texts = {'text1_processed': '', 'text2_processed': ''}
    
    if request.method == 'POST':
        text1 = request.POST.get('text1', '').strip()
        text2 = request.POST.get('text2', '').strip()
        
        # Validate inputs
        if not text1 or not text2:
            error_message = "Please enter text in both fields to calculate similarity."
        elif word_embed is None:
            error_message = "Model is not available. Please try again later."
        else:
            try:
                # Process first text
                pre_final1 = Cleaning(text1)
                pre_final1 = removeStopwords(pre_final1)
                processed_texts['text1_processed'] = pre_final1
                logger.info(f"Processed text 1: {pre_final1[:100]}...")

                # Process second text
                pre_final2 = Cleaning(text2)
                pre_final2 = removeStopwords(pre_final2)
                processed_texts['text2_processed'] = pre_final2
                logger.info(f"Processed text 2: {pre_final2[:100]}...")

                # Create embeddings for text 1
                count1 = 0
                document_embeddings1 = np.zeros(50, dtype=float)
                
                # Handle both dictionary and Word2Vec model formats
                model = word_embed.wv if hasattr(word_embed, 'wv') else word_embed
                
                for word in pre_final1.split(" "):
                    try:
                        if word in model:
                            array = np.asarray(model[word], dtype=float)
                            document_embeddings1 = np.add(document_embeddings1, array, out=document_embeddings1, casting="unsafe")
                        else:
                            count1 += 1
                    except Exception as e:
                        logger.warning(f"Error processing word '{word}': {e}")
                        count1 += 1

                logger.info(f"Text 1: {len(pre_final1.split(' '))} words, {count1} unrecognized")

                # Create embeddings for text 2
                count2 = 0
                document_embeddings2 = np.zeros(50, dtype=float)
                for word in pre_final2.split(" "):
                    try:
                        if word in model:
                            array = np.asarray(model[word], dtype=float)
                            document_embeddings2 = np.add(document_embeddings2, array, out=document_embeddings2, casting="unsafe")
                        else:
                            count2 += 1
                    except Exception as e:
                        logger.warning(f"Error processing word '{word}': {e}")
                        count2 += 1

                logger.info(f"Text 2: {len(pre_final2.split(' '))} words, {count2} unrecognized")

                # Calculate similarity
                if np.linalg.norm(document_embeddings1) > 0 and np.linalg.norm(document_embeddings2) > 0:
                    similarity = cosine_similarity(document_embeddings1, document_embeddings2)
                    logger.info(f"Similarity calculated: {similarity}")
                else:
                    similarity = 0.0
                    error_message = "Could not calculate similarity due to insufficient recognizable words."
                    
            except Exception as e:
                logger.error(f"Error processing texts: {e}")
                error_message = f"An error occurred while processing the texts: {str(e)}"
                similarity = 0.0

    context = {
        'response': similarity,
        'error_message': error_message,
        'processed_texts': processed_texts,
        'text1_input': request.POST.get('text1', ''),
        'text2_input': request.POST.get('text2', ''),
    }
    
    return render(request, 'index.html', context)


# Links to look at, for startup code implementation:
# https://stackoverflow.com/questions/2781383/where-to-put-django-startup-code


