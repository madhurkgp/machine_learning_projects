#!/usr/bin/env python
"""
Test script for Parkinson's Disease Prediction App
"""

import os
import sys
import django
import joblib
import numpy as np

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parkinson_app.settings')
django.setup()

from predictor.forms import ParkinsonPredictionForm

def test_model_loading():
    """Test if ML model loads correctly"""
    print("🧪 Testing model loading...")
    try:
        model = joblib.load('parkinson_model.joblib')
        feature_names = joblib.load('feature_names.joblib')
        print("✅ Model and feature names loaded successfully")
        print(f"   Model type: {type(model).__name__}")
        print(f"   Number of features: {len(feature_names)}")
        return True
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False

def test_form_validation():
    """Test Django form validation"""
    print("\n🧪 Testing form validation...")
    
    # Test valid data
    valid_data = {
        'mdvp_fo': 174.188,
        'mdvp_fhi': 230.978,
        'mdvp_flo': 94.261,
        'mdvp_jitter': 0.00459,
        'mdvp_jitter_abs': 0.00003,
        'mdvp_rap': 0.00263,
        'mdvp_ppq': 0.00259,
        'jitter_ddp': 0.00790,
        'mdvp_shimmer': 0.04087,
        'mdvp_shimmer_db': 0.327,
        'shimmer_apq3': 0.01717,
        'shimmer_apq5': 0.02183,
        'mdvp_apq': 0.02453,
        'shimmer_dda': 0.07008,
        'nhr': 0.02764,
        'hnr': 19.517,
        'rpde': 0.448439,
        'dfa': 0.657899,
        'spread1': -6.538586,
        'spread2': 0.121952,
        'd2': 2.657476,
        'ppe': 0.133050
    }
    
    form = ParkinsonPredictionForm(data=valid_data)
    if form.is_valid():
        print("✅ Valid form data passes validation")
        features = form.get_features_array()
        print(f"   Features array shape: {features.shape}")
        return True
    else:
        print("❌ Valid form data failed validation")
        print(f"   Errors: {form.errors}")
        return False

def test_invalid_data():
    """Test form validation with invalid data"""
    print("\n🧪 Testing invalid data validation...")
    
    # Test invalid data (out of range)
    invalid_data = {
        'mdvp_fo': 1000,  # Too high (should be 50-300)
        'mdvp_fhi': 230.978,
        'mdvp_flo': 94.261,
        'mdvp_jitter': 0.00459,
        'mdvp_jitter_abs': 0.00003,
        'mdvp_rap': 0.00263,
        'mdvp_ppq': 0.00259,
        'jitter_ddp': 0.00790,
        'mdvp_shimmer': 0.04087,
        'mdvp_shimmer_db': 0.327,
        'shimmer_apq3': 0.01717,
        'shimmer_apq5': 0.02183,
        'mdvp_apq': 0.02453,
        'shimmer_dda': 0.07008,
        'nhr': 0.02764,
        'hnr': 19.517,
        'rpde': 0.448439,
        'dfa': 0.657899,
        'spread1': -6.538586,
        'spread2': 0.121952,
        'd2': 2.657476,
        'ppe': 0.133050
    }
    
    form = ParkinsonPredictionForm(data=invalid_data)
    if not form.is_valid():
        print("✅ Invalid form data correctly rejected")
        if 'mdvp_fo' in form.errors:
            print(f"   Correctly caught error in mdvp_fo: {form.errors['mdvp_fo']}")
        return True
    else:
        print("❌ Invalid form data was incorrectly accepted")
        return False

def test_model_predictions():
    """Test model predictions with sample data"""
    print("\n🧪 Testing model predictions...")
    
    try:
        model = joblib.load('parkinson_model.joblib')
        
        # Test healthy sample
        healthy_data = np.array([[
            174.188, 230.978, 94.261, 0.00459, 0.00003, 0.00263, 0.00259, 0.00790,
            0.04087, 0.327, 0.01717, 0.02183, 0.02453, 0.07008, 0.02764, 19.517,
            0.448439, 0.657899, -6.538586, 0.121952, 2.657476, 0.133050
        ]])
        
        prediction = model.predict(healthy_data)[0]
        proba = model.predict_proba(healthy_data)[0]
        
        print(f"✅ Healthy sample prediction: {prediction} (0=Healthy, 1=Parkinson's)")
        print(f"   Confidence: {max(proba)*100:.1f}%")
        
        # Test Parkinson's sample
        parkinsons_data = np.array([[
            119.992, 157.302, 74.997, 0.00784, 0.00007, 0.00370, 0.00554, 0.01109,
            0.04374, 0.426, 0.02182, 0.03130, 0.02971, 0.06545, 0.02211, 21.033,
            0.414783, 0.815285, -4.813031, 0.266482, 2.301442, 0.284654
        ]])
        
        prediction2 = model.predict(parkinsons_data)[0]
        proba2 = model.predict_proba(parkinsons_data)[0]
        
        print(f"✅ Parkinson's sample prediction: {prediction2} (0=Healthy, 1=Parkinson's)")
        print(f"   Confidence: {max(proba2)*100:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Model prediction failed: {e}")
        return False

def test_feature_order():
    """Test that form features are in the correct order for the model"""
    print("\n🧪 Testing feature order consistency...")
    
    try:
        # Load expected feature names
        expected_features = joblib.load('feature_names.joblib')
        
        # Get form field names in order
        form = ParkinsonPredictionForm()
        form_fields = list(form.fields.keys())
        
        print(f"   Expected features: {len(expected_features)}")
        print(f"   Form fields: {len(form_fields)}")
        
        if len(expected_features) == len(form_fields):
            print("✅ Feature count matches")
            return True
        else:
            print("❌ Feature count mismatch")
            return False
            
    except Exception as e:
        print(f"❌ Feature order test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Running Parkinson's Disease Prediction App Tests\n")
    
    tests = [
        test_model_loading,
        test_form_validation,
        test_invalid_data,
        test_model_predictions,
        test_feature_order
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready for use.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
