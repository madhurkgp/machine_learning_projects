import pandas as pd
import numpy as np
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

# Load the dataset
print("Loading dataset...")
dataset_path = '../Dataset/MusicDataset.csv'
df = pd.read_csv(dataset_path)
print(f"Dataset loaded with shape: {df.shape}")

# Data preprocessing
print("Preprocessing data...")
drop_list = ['artist_location', 'artist_latitude', 'artist_longitude','artist_name', 'release', 'title']
train = df.drop(drop_list, axis=1)

# Fill null values
train["song_hotttnesss"] = train["song_hotttnesss"].fillna(train["song_hotttnesss"].mean())
train["artist_familiarity"] = train["artist_familiarity"].fillna(train["artist_familiarity"].median())

# Prepare features
train1 = train.drop(['artist_id', 'bbhot'], axis = 1)
train2 = train1.drop(['end_of_fade_in', 'key', 'key_confidence', 'mode', 'mode_confidence', 'year'], axis = 1)

print(f"Features prepared: {list(train2.columns)}")

# Prepare target
Y = train['bbhot'].copy(deep=True)

# Split data
X_train, X_test, y_train, y_test = train_test_split(train2, Y, test_size=0.3, random_state=0)

# Train model
print("Training model...")
clf1 = MLPClassifier(hidden_layer_sizes=(200,150,50), max_iter=200,activation = 'relu',solver='adam',random_state=1)
clf1.fit(X_train, y_train)

train_score = clf1.score(X_train, y_train)
test_score = clf1.score(X_test, y_test)

print(f"Training accuracy: {train_score}")
print(f"Test accuracy: {test_score}")

# Save model
model_path = 'mysite/polls/music-popularity-model.pkl'
pickle.dump(clf1, open(model_path, 'wb'))
print(f"Model saved to {model_path}")
