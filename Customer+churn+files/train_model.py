import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# Load and prepare the data
print("Loading and preparing data...")
df = pd.read_csv("Notebook/Churn Modeling.csv")

# Drop unnecessary columns
df = df.drop(['RowNumber', 'CustomerId', 'Surname'], axis=1)

# Label encoding for categorical variables
cat_cols = ['Geography', 'Gender']
le = LabelEncoder()
for col in cat_cols:
    df[col] = le.fit_transform(df[col])

# Split features and target
X = df.drop(['Exited'], axis=1)
y = df['Exited']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=40)

# Train Random Forest model (best performing)
print("Training Random Forest model...")
rf_model = RandomForestClassifier(
    n_estimators=100,
    min_samples_split=2,
    min_samples_leaf=1,
    max_features='sqrt',
    random_state=42
)

rf_model.fit(X_train, y_train)

# Evaluate the model
train_preds = rf_model.predict(X_train)
test_preds = rf_model.predict(X_test)

print(f"Train Accuracy: {accuracy_score(y_train, train_preds):.4f}")
print(f"Test Accuracy: {accuracy_score(y_test, test_preds):.4f}")
print(f"ROC AUC Score: {roc_auc_score(y_test, test_preds):.4f}")

# Save the model and encoders
joblib.dump(rf_model, 'models/random_forest_model.pkl')
joblib.dump(le, 'models/label_encoder.pkl')

# Save feature names for later use
feature_names = X.columns.tolist()
joblib.dump(feature_names, 'models/feature_names.pkl')

print("Model and artifacts saved successfully!")
print(f"Features used: {feature_names}")
