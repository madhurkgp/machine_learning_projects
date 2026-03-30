#!/usr/bin/env python
"""
Test script for Black Friday Sale Prediction application
"""

import requests
import json
import sys

BASE_URL = 'http://127.0.0.1:8000'

def test_sample_data():
    """Test sample data endpoint"""
    print("Testing sample data endpoint...")
    try:
        response = requests.get(f'{BASE_URL}/sample-data/')
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Sample data retrieved successfully")
            return data
        else:
            print(f"✗ Sample data failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None

def test_prediction(data, description):
    """Test prediction endpoint with given data"""
    print(f"Testing prediction: {description}...")
    try:
        response = requests.post(
            f'{BASE_URL}/api/predict/',
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✓ Prediction successful: {result['formatted_prediction']}")
                return True
            else:
                print(f"✗ Prediction failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"✗ HTTP error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_form_validation():
    """Test form validation with invalid data"""
    print("Testing form validation...")
    
    invalid_cases = [
        ({'user_id': -1}, "Invalid user ID"),
        ({'product_id': ''}, "Empty product ID"),
        ({'age': 'invalid'}, "Invalid age"),
        ({'occupation': 25}, "Invalid occupation"),
    ]
    
    passed = 0
    for data, description in invalid_cases:
        # Add required fields
        test_data = {
            'user_id': 1000001,
            'product_id': 'P00069042',
            'gender': 'M',
            'age': '26-35',
            'occupation': 10,
            'city_category': 'A',
            'stay_years': '2',
            'marital_status': 0,
            'product_category_1': 3,
            'product_category_2': 6.0
        }
        test_data.update(data)
        
        try:
            response = requests.post(
                f'{BASE_URL}/api/predict/',
                json=test_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code in [400, 422]:
                print(f"✓ Validation caught: {description}")
                passed += 1
            else:
                print(f"✗ Validation missed: {description}")
        except Exception as e:
            print(f"✗ Error testing {description}: {str(e)}")
    
    return passed == len(invalid_cases)

def test_edge_cases():
    """Test edge cases"""
    print("Testing edge cases...")
    
    edge_cases = [
        ({'user_id': 1000001, 'gender': 'F', 'age': '0-17'}, "Young female customer"),
        ({'user_id': 1006040, 'gender': 'M', 'age': '55+'}, "Senior male customer"),
        ({'occupation': 0, 'marital_status': 1}, "Entry-level married"),
        ({'occupation': 20, 'marital_status': 0}, "Senior occupation single"),
        ({'city_category': 'C', 'stay_years': '0'}, "New rural resident"),
        ({'city_category': 'A', 'stay_years': '4'}, "Long-term urban resident"),
    ]
    
    passed = 0
    for data, description in edge_cases:
        # Create complete test data
        test_data = {
            'user_id': 1000001,
            'product_id': 'P00069042',
            'gender': 'M',
            'age': '26-35',
            'occupation': 10,
            'city_category': 'A',
            'stay_years': '2',
            'marital_status': 0,
            'product_category_1': 3,
            'product_category_2': 6.0
        }
        test_data.update(data)
        
        if test_prediction(test_data, description):
            passed += 1
    
    return passed == len(edge_cases)

def main():
    """Run all tests"""
    print("=" * 50)
    print("Black Friday Sale Prediction App Tests")
    print("=" * 50)
    
    # Test basic functionality
    sample_data = test_sample_data()
    if not sample_data:
        print("❌ Cannot proceed without sample data")
        sys.exit(1)
    
    # Test with sample data
    sample_success = test_prediction(sample_data, "Sample data")
    
    # Test edge cases
    edge_cases_passed = test_edge_cases()
    
    # Test validation
    validation_passed = test_form_validation()
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"✓ Sample data test: {'PASS' if sample_success else 'FAIL'}")
    print(f"✓ Edge cases test: {'PASS' if edge_cases_passed else 'FAIL'}")
    print(f"✓ Validation test: {'PASS' if validation_passed else 'FAIL'}")
    
    all_passed = sample_success and edge_cases_passed and validation_passed
    print(f"\n🎯 Overall Result: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print("=" * 50)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
