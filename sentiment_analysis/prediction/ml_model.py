import re
import string
import pickle
import joblib
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import nltk
import os

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

# Contraction mapping
CONTRACTION_MAP = {
    "ain't": "is not", "aren't": "are not", "can't": "cannot", "can't've": "cannot have",
    "'cause": "because", "could've": "could have", "couldn't": "could not",
    "couldn't've": "could not have", "didn't": "did not", "doesn't": "does not",
    "don't": "do not", "hadn't": "had not", "hadn't've": "had not have",
    "hasn't": "has not", "haven't": "have not", "he'd": "he would",
    "he'd've": "he would have", "he'll": "he will", "he'll've": "he he will have",
    "he's": "he is", "how'd": "how did", "how'd'y": "how do you", "how'll": "how will",
    "how's": "how is", "I'd": "I would", "I'd've": "I would have", "I'll": "I will",
    "I'll've": "I will have", "I'm": "I am", "I've": "I have", "i'd": "i would",
    "i'd've": "i would have", "i'll": "i will", "i'll've": "i will have", "i'm": "i am",
    "i've": "i have", "isn't": "is not", "it'd": "it would", "it'd've": "it would have",
    "it'll": "it will", "it'll've": "it will have", "it's": "it is", "let's": "let us",
    "ma'am": "madam", "mayn't": "may not", "might've": "might have", "mightn't": "might not",
    "mightn't've": "might not have", "must've": "must have", "mustn't": "must not",
    "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have",
    "o'clock": "of the clock", "oughtn't": "ought not", "oughtn't've": "ought not have",
    "shan't": "shall not", "sha'n't": "shall not", "shan't've": "shall not have",
    "she'd": "she would", "she'd've": "she would have", "she'll": "she will",
    "she'll've": "she will have", "she's": "she is", "should've": "should have",
    "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have",
    "so's": "so as", "that'd": "that would", "that'd've": "that would have",
    "that's": "that is", "there'd": "there would", "there'd've": "there would have",
    "there's": "there is", "they'd": "they would", "they'd've": "they would have",
    "they'll": "they will", "they'll've": "they will have", "they're": "they are",
    "they've": "they have", "to've": "to have", "wasn't": "was not", "we'd": "we would",
    "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have",
    "we're": "we are", "we've": "we have", "weren't": "were not", "what'll": "what will",
    "what'll've": "what will have", "what're": "what are", "what's": "what is",
    "what've": "what have", "when's": "when is", "when've": "when have",
    "where'd": "where did", "where's": "where is", "where've": "where have",
    "who'll": "who will", "who'll've": "who will have", "who's": "who is",
    "who've": "who have", "why's": "why is", "why've": "why have", "will've": "will have",
    "won't": "will not", "won't've": "will not have", "would've": "would have",
    "wouldn't": "would not", "wouldn't've": "would not have", "y'all": "you all",
    "y'all'd": "you all would", "y'all'd've": "you all would have", "y'all're": "you all are",
    "y'all've": "you all have", "you'd": "you would", "you'd've": "you would have",
    "you'll": "you will", "you'll've": "you will have", "you're": "you are",
    "you've": "you have"
}

class SentimentAnalyzer:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.model_path = os.path.join(os.path.dirname(__file__), '..', 'models')
        self.load_or_train_model()

    def contraction_remove(self, text):
        for key, value in CONTRACTION_MAP.items():
            text = re.sub(r"{}".format(re.escape(key)), value, text, flags=re.IGNORECASE)
        return text

    def w_tokenization(self, text):
        text = text.lower()
        text = self.contraction_remove(text)
        tokens = word_tokenize(text)
        without_special = []
        for word in tokens:
            if word not in string.punctuation:
                without_special.append(word)
        return without_special

    def lemmatization_sentence(self, tokens):
        from nltk import pos_tag
        tag_list = pos_tag(tokens, tagset=None)
        lema_sent = []
        for token, pos_token in tag_list:
            if pos_token.startswith('V'):
                pos_val = 'v'
            elif pos_token.startswith('J'):
                pos_val = 'a'
            elif pos_token.startswith('R'):
                pos_val = 'r'
            else:
                pos_val = 'n'
            lema_token = self.lemmatizer.lemmatize(token, pos_val)
            lema_sent.append(lema_token)
        return " ".join(lema_sent)

    def preprocess_text(self, text):
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove non-alphabetic characters
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Tokenize and process
        tokens = self.w_tokenization(text)
        # Remove stopwords and lemmatize
        tokens = [token for token in tokens if token not in self.stop_words]
        processed_text = self.lemmatization_sentence(tokens)
        return processed_text

    def load_or_train_model(self):
        # Try to load existing model
        model_file = os.path.join(self.model_path, 'sentiment_model.pkl')
        vectorizer_file = os.path.join(self.model_path, 'vectorizer.pkl')
        
        os.makedirs(self.model_path, exist_ok=True)
        
        if os.path.exists(model_file) and os.path.exists(vectorizer_file):
            try:
                self.model = joblib.load(model_file)
                self.vectorizer = joblib.load(vectorizer_file)
                return
            except Exception as e:
                print(f"Error loading model: {e}")
        
        # Train new model if loading fails
        self.train_model()

    def train_model(self):
        # Load training data
        data_file = os.path.join(os.path.dirname(__file__), '..', 'Notebook', 'TextAnalytics.txt')
        
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"Training data not found at {data_file}")
        
        # Read and parse data
        data = []
        with open(data_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    # Extract the sentiment label from the beginning of the line
                    # Format: 0,"text..." or 1,"text..."
                    match = re.match(r'^(\d+),"(.*)"$', line.strip())
                    if match:
                        try:
                            label = int(match.group(1))
                            text = match.group(2)
                            if text and len(text.strip()) > 10:  # Ensure meaningful text
                                data.append((text, label))
                        except ValueError:
                            print(f"Skipping line {line_num}: Invalid label format")
                    else:
                        print(f"Skipping line {line_num}: Invalid format")
        
        if not data:
            raise ValueError("No valid training data found")
        
        print(f"Loaded {len(data)} training samples")
        
        # Create DataFrame
        df = pd.DataFrame(data, columns=['text', 'label'])
        
        # Check label distribution
        print(f"Label distribution: {df['label'].value_counts().to_dict()}")
        
        # Preprocess texts
        print("Preprocessing texts...")
        df['processed_text'] = df['text'].apply(self.preprocess_text)
        
        # Remove empty processed texts
        df = df[df['processed_text'].str.len() > 0]
        
        if df.empty:
            raise ValueError("No valid processed text data")
        
        print(f"Valid samples after preprocessing: {len(df)}")
        
        # Create TF-IDF features
        print("Creating TF-IDF features...")
        self.vectorizer = TfidfVectorizer(max_features=5000, min_df=1, max_df=0.9)
        X = self.vectorizer.fit_transform(df['processed_text'])
        y = df['label']
        
        print(f"Feature matrix shape: {X.shape}")
        
        # Train model
        print("Training model...")
        self.model = LogisticRegression(random_state=42, max_iter=1000)
        self.model.fit(X, y)
        
        # Save model and vectorizer
        joblib.dump(self.model, os.path.join(self.model_path, 'sentiment_model.pkl'))
        joblib.dump(self.vectorizer, os.path.join(self.model_path, 'vectorizer.pkl'))
        
        print("Model training completed successfully!")

    def predict_sentiment(self, text):
        if self.model is None or self.vectorizer is None:
            raise ValueError("Model not loaded")
        
        # Preprocess input text
        processed_text = self.preprocess_text(text)
        
        if not processed_text.strip():
            return {
                'prediction': 'Neutral',
                'confidence': 0.5,
                'processed_text': processed_text
            }
        
        # Vectorize and predict
        X = self.vectorizer.transform([processed_text])
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]
        
        # Get confidence
        confidence = max(probabilities)
        
        # Convert prediction to label (0-2: Negative, 3-4: Neutral, 5+: Positive)
        if prediction <= 2:
            prediction_label = 'Negative'
        elif prediction <= 4:
            prediction_label = 'Neutral'
        else:
            prediction_label = 'Positive'
        
        return {
            'prediction': prediction_label,
            'confidence': round(confidence * 100, 2),
            'processed_text': processed_text
        }

# Global instance
sentiment_analyzer = SentimentAnalyzer()
