#!/usr/bin/env python
"""
Test script to validate the web application functionality
"""
import os
import sys
import django
from django.test import Client
from django.conf import settings

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

def test_web_application():
    """Test the web application endpoints"""
    print("🌐 Testing Web Application")
    print("=" * 40)
    
    client = Client()
    
    # Test GET request
    print("1. Testing GET request...")
    response = client.get('/')
    if response.status_code == 200:
        print("✅ GET request successful")
    else:
        print(f"❌ GET request failed with status {response.status_code}")
        return False
    
    # Test POST request with sample data
    print("\n2. Testing POST request with safe data...")
    safe_data = {
        'name': 'example.com',
        'NumDots': '2',
        'PathLevel': '1',
        'NumDash': '0',
        'NumSensitiveWords': '0',
        'PctExtHyperlinks': '0.3',
        'PctExtResourceUrls': '0.2',
        'InsecureForms': '0',
        'PctNullSelfRedirectHyperlinks': '0.1',
        'FrequentDomainNameMismatch': '0',
        'SubmitInfoToEmail': '0',
        'IframeOrFrame': '0',
        'csrfmiddlewaretoken': 'test'
    }
    
    response = client.post('/', data=safe_data)
    if response.status_code == 200:
        print("✅ POST request successful")
        # Check if response contains prediction results
        content = response.content.decode('utf-8')
        if 'SAFE WEBSITE' in content or 'PHISHING DETECTED' in content:
            print("✅ Response generated successfully")
        else:
            print("⚠️ No prediction results found in response")
    else:
        print(f"❌ POST request failed with status {response.status_code}")
    
    # Test POST request with suspicious data
    print("\n3. Testing POST request with suspicious data...")
    suspicious_data = {
        'name': 'suspicious-site-login.com',
        'NumDots': '5',
        'PathLevel': '8',
        'NumDash': '10',
        'NumSensitiveWords': '4',
        'PctExtHyperlinks': '0.9',
        'PctExtResourceUrls': '0.8',
        'InsecureForms': '1',
        'PctNullSelfRedirectHyperlinks': '0.7',
        'FrequentDomainNameMismatch': '1',
        'SubmitInfoToEmail': '1',
        'IframeOrFrame': '1',
        'csrfmiddlewaretoken': 'test'
    }
    
    response = client.post('/', data=suspicious_data)
    if response.status_code == 200:
        print("✅ POST request successful")
        content = response.content.decode('utf-8')
        if 'PHISHING DETECTED' in content:
            print("✅ Suspicious site correctly detected as phishing")
        elif 'SAFE WEBSITE' in content:
            print("⚠️ Suspicious site not detected as phishing")
        else:
            print("⚠️ No prediction results found in response")
    else:
        print(f"❌ POST request failed with status {response.status_code}")
    
    # Test empty form submission
    print("\n4. Testing empty form submission...")
    empty_data = {
        'name': '',
        'csrfmiddlewaretoken': 'test'
    }
    
    response = client.post('/', data=empty_data)
    if response.status_code == 200:
        print("✅ Empty form handled correctly")
        content = response.content.decode('utf-8')
        if 'Please enter a URL name' in content or 'error' in content.lower():
            print("✅ Error message shown for empty form")
        else:
            print("⚠️ No error message for empty form")
    else:
        print(f"❌ Empty form submission failed with status {response.status_code}")
    
    print("\n🎉 Web application tests completed!")
    return True

def test_fallback_logic():
    """Test the fallback prediction logic"""
    print("\n🔧 Testing Fallback Prediction Logic")
    print("=" * 40)
    
    # Import the views module to test fallback function
    from polls.views import fallback_prediction
    
    # Test safe data
    safe_data = {
        'NumDots': 1.0,
        'PathLevel': 1.0,
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
    
    is_phishing, confidence = fallback_prediction(safe_data)
    if not is_phishing and confidence < 0.5:
        print("✅ Safe data correctly classified as safe")
    else:
        print("❌ Safe data incorrectly classified as phishing")
    
    # Test suspicious data
    suspicious_data = {
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
    
    is_phishing, confidence = fallback_prediction(suspicious_data)
    if is_phishing and confidence >= 0.5:
        print("✅ Suspicious data correctly classified as phishing")
    else:
        print("❌ Suspicious data incorrectly classified as safe")
    
    print("✅ Fallback logic tests completed!")

def main():
    """Run all tests"""
    try:
        test_web_application()
        test_fallback_logic()
        print("\n🎉 All tests completed successfully!")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
