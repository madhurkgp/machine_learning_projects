import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the dataset
df = pd.read_csv('parkinsons.data')

# Remove the name column as it's not a feature
df = df.drop('name', axis=1)

# Split features and target
X = df.drop('status', axis=1)
y = df['status']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Decision Tree model (best performer from analysis)
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Print accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.4f}")
print(f"Classification Report:\n{classification_report(y_test, y_pred)}")

# Save the model
joblib.dump(model, 'parkinson_model.joblib')

# Save feature names for later use
feature_names = X.columns.tolist()
joblib.dump(feature_names, 'feature_names.joblib')

print("Model saved successfully!")
print(f"Features: {feature_names}")
