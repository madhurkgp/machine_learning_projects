#!/usr/bin/env python
"""
Test script for Medical Cost Prediction ML Model
This script tests the ML model functionality independently.
"""

import pandas as pd
import pickle
import os
import sys

def test_model_loading():
    """Test if the model can be loaded successfully."""
    print("🔄 Testing model loading...")
    
    model_path = 'polls/Medical.pickle'
    
    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        return False
    
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print("✅ Model loaded successfully")
        return model
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return False

def test_prediction(model):
    """Test model prediction with sample data."""
    print("\n🔄 Testing model prediction...")
    
    # Sample test cases
    test_cases = [
        {
            'name': 'Young Non-Smoker',
            'data': {'age': 25, 'sex': 1, 'bmi': 22.5, 'children': 0, 'smoker': 0, 'region': 2}
        },
        {
            'name': 'Middle-aged Smoker',
            'data': {'age': 45, 'sex': 0, 'bmi': 30.2, 'children': 2, 'smoker': 1, 'region': 1}
        },
        {
            'name': 'Senior Non-Smoker',
            'data': {'age': 65, 'sex': 1, 'bmi': 28.8, 'children': 3, 'smoker': 0, 'region': 0}
        }
    ]
    
    try:
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📊 Test Case {i}: {test_case['name']}")
            
            # Create DataFrame
            df = pd.DataFrame([test_case['data']])
            print(f"Input: {test_case['data']}")
            
            # Make prediction
            prediction = model.predict(df)[0]
            print(f"Predicted Cost: ${prediction:,.2f}")
            
        print("\n✅ All predictions completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error during prediction: {str(e)}")
        return False

def test_edge_cases(model):
    """Test edge cases and boundary conditions."""
    print("\n🔄 Testing edge cases...")
    
    edge_cases = [
        {'name': 'Minimum Age', 'data': {'age': 18, 'sex': 0, 'bmi': 15.0, 'children': 0, 'smoker': 0, 'region': 0}},
        {'name': 'Maximum Age', 'data': {'age': 100, 'sex': 1, 'bmi': 50.0, 'children': 10, 'smoker': 1, 'region': 3}},
        {'name': 'Low BMI', 'data': {'age': 30, 'sex': 0, 'bmi': 10.0, 'children': 0, 'smoker': 0, 'region': 1}},
        {'name': 'High BMI', 'data': {'age': 40, 'sex': 1, 'bmi': 50.0, 'children': 5, 'smoker': 0, 'region': 2}},
    ]
    
    try:
        for test_case in edge_cases:
            print(f"\n📊 Testing {test_case['name']}")
            df = pd.DataFrame([test_case['data']])
            prediction = model.predict(df)[0]
            print(f"Input: {test_case['data']}")
            print(f"Predicted Cost: ${prediction:,.2f}")
            
        print("\n✅ Edge cases tested successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error during edge case testing: {str(e)}")
        return False

def main():
    """Main test function."""
    print("🧪 Medical Cost Prediction Model Test Suite")
    print("="*50)
    
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mysite_dir = os.path.join(script_dir, 'mysite')
    
    if os.path.exists(mysite_dir):
        os.chdir(mysite_dir)
        print(f"📁 Changed to directory: {mysite_dir}")
    else:
        print(f"❌ Directory not found: {mysite_dir}")
        return False
    
    # Run tests
    tests = [
        ("Model Loading", test_model_loading),
        ("Prediction", test_prediction),
        ("Edge Cases", test_edge_cases),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"🧪 Running {test_name} Tests")
        print('='*50)
        
        if test_name == "Model Loading":
            model = test_func()
            results.append((test_name, model is not False))
        else:
            if 'model' in locals() and model is not False:
                results.append((test_name, test_func(model)))
            else:
                print(f"❌ Skipping {test_name} - model not loaded")
                results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📋 Test Results Summary")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The model is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
