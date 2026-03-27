#!/usr/bin/env python
"""
Test script to validate ML model integration
"""
import os
import sys
import pandas as pd
import pickle

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_model_loading():
    """Test if the ML model can be loaded successfully"""
    try:
        model_path = os.path.join('polls', 'Phishing.pickle')
        if not os.path.exists(model_path):
            print("❌ Model file not found at:", model_path)
            return False
            
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        print("✅ Model loaded successfully")
        print(f"📊 Model type: {type(model).__name__}")
        return True, model
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False, None

def test_prediction(model):
    """Test model prediction with sample data"""
    try:
        # Sample data for testing
        sample_data = {
            'NumDots': 2.0,
            'PathLevel': 1.0,
            'NumDash': 0.0,
            'NumSensitiveWords': 0.0,
            'PctExtHyperlinks': 0.5,
            'PctExtResourceUrls': 0.3,
            'InsecureForms': 0.0,
            'PctNullSelfRedirectHyperlinks': 0.1,
            'FrequentDomainNameMismatch': 0.0,
            'SubmitInfoToEmail': 0.0,
            'IframeOrFrame': 0.0
        }
        
        # Create DataFrame with correct column order
        columns = ['NumDots','PathLevel','NumDash','NumSensitiveWords',
                  'PctExtHyperlinks','PctExtResourceUrls','InsecureForms',
                  'PctNullSelfRedirectHyperlinks','FrequentDomainNameMismatch',
                  'SubmitInfoToEmail','IframeOrFrame']
        
        df = pd.DataFrame([sample_data], columns=columns)
        
        # Make prediction
        prediction = model.predict(df)
        probability = model.predict_proba(df) if hasattr(model, 'predict_proba') else None
        
        print("✅ Prediction successful")
        print(f"🎯 Prediction result: {prediction[0]}")
        if probability is not None:
            print(f"📈 Confidence scores: {probability[0]}")
        
        return True
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return False

def test_edge_cases(model):
    """Test model with edge cases"""
    test_cases = [
        {
            'name': 'Suspicious site',
            'data': {
                'NumDots': 5.0,
                'PathLevel': 8.0,
                'NumDash': 10.0,
                'NumSensitiveWords': 4.0,
                'PctExtHyperlinks': 0.9,
                'PctExtResourceUrls': 0.8,
                'InsecureForms': 1.0,
                'PctNullSelfRedirectHyperlinks': 0.7,
                'FrequentDomainNameMismatch': 1.0,
                'SubmitInfoToEmail': 1.0,
                'IframeOrFrame': 1.0
            }
        },
        {
            'name': 'Legitimate site',
            'data': {
                'NumDots': 1.0,
                'PathLevel': 2.0,
                'NumDash': 0.0,
                'NumSensitiveWords': 0.0,
                'PctExtHyperlinks': 0.2,
                'PctExtResourceUrls': 0.1,
                'InsecureForms': 0.0,
                'PctNullSelfRedirectHyperlinks': 0.0,
                'FrequentDomainNameMismatch': 0.0,
                'SubmitInfoToEmail': 0.0,
                'IframeOrFrame': 0.0
            }
        }
    ]
    
    columns = ['NumDots','PathLevel','NumDash','NumSensitiveWords',
              'PctExtHyperlinks','PctExtResourceUrls','InsecureForms',
              'PctNullSelfRedirectHyperlinks','FrequentDomainNameMismatch',
              'SubmitInfoToEmail','IframeOrFrame']
    
    for test_case in test_cases:
        try:
            df = pd.DataFrame([test_case['data']], columns=columns)
            prediction = model.predict(df)
            probability = model.predict_proba(df) if hasattr(model, 'predict_proba') else None
            
            result = "PHISHING" if prediction[0] == 1 else "SAFE"
            confidence = f" ({probability[0][1]:.2f})" if probability is not None else ""
            
            print(f"✅ {test_case['name']}: {result}{confidence}")
        except Exception as e:
            print(f"❌ Error testing {test_case['name']}: {e}")

def main():
    """Run all tests"""
    print("🧪 Testing ML Model Integration")
    print("=" * 50)
    
    # Test model loading
    success, model = test_model_loading()
    if not success:
        print("❌ Cannot proceed with prediction tests")
        return
    
    print()
    
    # Test basic prediction
    if test_prediction(model):
        print()
        
        # Test edge cases
        print("🔍 Testing edge cases:")
        test_edge_cases(model)
        
        print()
        print("🎉 All tests completed successfully!")
    else:
        print("❌ Prediction tests failed")

if __name__ == "__main__":
    main()
