# Importing necessary libraries

from nltk.corpus import stopwords
import re
import numpy as np


def Cleaning(text):
  def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


  def replaceUrls(data):
      #Removing URLs with a regular expression
      url_pattern = re.compile(r'https?://\S+|www\.\S+')
      data = url_pattern.sub(r'', data)
      return data

  def removeEmail(data):
      # Remove Emails
      data = re.sub('\S*@\S*\s?', '', data)
      return data

  def misc(data):
      # Remove new line characters
      data = re.sub(r'\.+', ".", data)
      data = re.sub('\s+', ' ', data)
      # Remove distracting single quotes
      data = re.sub("\'", "", data)
      return data

  sentence = cleanhtml(text)
  sentence = replaceUrls(sentence)
  sentence = removeEmail(sentence)
  sentence = misc(sentence)
  sentence = re.sub(r'[^a-zA-Z]', ' ', sentence)
  sentence = re.sub(' +', ' ', sentence)
  sentence = sentence.lower()

  return sentence


# nltk.download('stopwords')


stopwords_list = stopwords.words('english')
def removeStopwords(sentence):
  words = sentence.split(" ")
  filtered_sentence = [word for word in words if not word in stopwords_list]
  ans = ' '.join([i for i in filtered_sentence if len(i) >= 2])

  return ans


# We will go for cosine_similarity
def cosine_similarity(A, B):
    """
    Calculate cosine similarity between two vectors.
    
    Input:
        A: a numpy array which corresponds to a word vector
        B: A numpy array which corresponds to a word vector
    Output:
        cos: numerical number representing the cosine similarity between A and B.
    """
    try:
        dot_product = np.dot(A, B)
        norm_a = np.sqrt(np.dot(A, A))
        norm_b = np.sqrt(np.dot(B, B))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        cos_sim = dot_product / (norm_a * norm_b)
        # Ensure result is between 0 and 1
        cos_sim = max(0.0, min(1.0, cos_sim))
        return round(cos_sim, 4)
    except Exception as e:
        logging.getLogger(__name__).error(f"Error calculating cosine similarity: {e}")
        return 0.0