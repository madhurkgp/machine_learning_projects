#!/usr/bin/env python
"""
Test script for Indian Air Quality Prediction Application
Tests both web interface and API endpoints
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_api_endpoint():
    """Test the API prediction endpoint"""
    print("Testing API Endpoint...")
    
    test_cases = [
        {"so2": 15.2, "no2": 25.8, "rspm": 45.3, "spm": 78.5},
        {"so2": 8.5, "no2": 18.2, "rspm": 32.1, "spm": 55.7},
        {"so2": 45.8, "no2": 67.3, "rspm": 89.4, "spm": 123.6},
        {"so2": 3.2, "no2": 12.5, "rspm": 28.9, "spm": 41.2},
        {"so2": 78.9, "no2": 89.4, "rspm": 156.7, "spm": 234.8}
    ]
    
    for i, test_data in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_data}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/predict/",
                data=test_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"  AQI Value: {result['aqi_value']}")
                    print(f"  AQI Category: {result['aqi_category']}")
                    print(f"  Color: {result['aqi_color']}")
                    print("  Pollutant Indices:")
                    for key, value in result['pollutant_indices'].items():
                        print(f"    {key}: {value}")
                    print("  Status: PASSED")
                else:
                    print(f"  Status: FAILED - {result.get('error', 'Unknown error')}")
            else:
                print(f"  Status: FAILED - HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"  Status: FAILED - Connection error: {e}")
        
        time.sleep(0.5)  # Small delay between requests

def test_web_interface():
    """Test the web interface accessibility"""
    print("\nTesting Web Interface...")
    
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("  Home page: PASSED")
            if "Air Quality Prediction" in response.text:
                print("  Content validation: PASSED")
            else:
                print("  Content validation: FAILED - Missing expected content")
        else:
            print(f"  Home page: FAILED - HTTP {response.status_code}")
            
        # Test sample data page
        response = requests.get(f"{BASE_URL}/sample-data/")
        if response.status_code == 200:
            print("  Sample data page: PASSED")
        else:
            print(f"  Sample data page: FAILED - HTTP {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"  Web interface: FAILED - Connection error: {e}")

def validate_aqi_categories():
    """Validate AQI categories are within expected ranges"""
    print("\nValidating AQI Categories...")
    
    categories = {
        "Good": (0, 50),
        "Moderate": (51, 100),
        "Poor": (101, 200),
        "Unhealthy": (201, 300),
        "Very unhealthy": (301, 400),
        "Hazardous": (401, float('inf'))
    }
    
    test_data = {"so2": 15.2, "no2": 25.8, "rspm": 45.3, "spm": 78.5}
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/predict/",
            data=test_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                aqi_value = result['aqi_value']
                aqi_category = result['aqi_category']
                
                if aqi_category in categories:
                    min_val, max_val = categories[aqi_category]
                    if min_val <= aqi_value <= max_val:
                        print(f"  Category validation: PASSED")
                        print(f"    {aqi_category}: {aqi_value} (expected range: {min_val}-{max_val if max_val != float('inf') else 'inf'})")
                    else:
                        print(f"  Category validation: FAILED")
                        print(f"    {aqi_category}: {aqi_value} (expected range: {min_val}-{max_val if max_val != float('inf') else 'inf'})")
                else:
                    print(f"  Category validation: FAILED - Unknown category: {aqi_category}")
            else:
                print(f"  Category validation: FAILED - {result.get('error', 'Unknown error')}")
        else:
            print(f"  Category validation: FAILED - HTTP {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"  Category validation: FAILED - Connection error: {e}")

def main():
    """Run all tests"""
    print("=" * 60)
    print("Indian Air Quality Prediction Application Tests")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code != 200:
            print("Server is not responding correctly. Please ensure the Django server is running.")
            return
    except requests.exceptions.RequestException:
        print("Cannot connect to server. Please ensure the Django server is running on http://127.0.0.1:8000")
        return
    
    # Run tests
    test_web_interface()
    test_api_endpoint()
    validate_aqi_categories()
    
    print("\n" + "=" * 60)
    print("Testing completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
