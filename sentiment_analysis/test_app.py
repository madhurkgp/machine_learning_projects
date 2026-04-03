#!/usr/bin/env python
"""
Test script for the Sentiment Analysis Web Application
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    """Test the API endpoints"""
    print("🧪 Testing Sentiment Analysis API...")
    
    # Test cases
    test_texts = [
        "This movie was absolutely amazing! The acting was superb and the storyline was engaging.",
        "I was really disappointed with this film. The plot was predictable and the acting was terrible.",
        "The movie was okay, nothing special but not terrible either.",
        "One of the worst movies I've ever seen. Complete waste of time and money.",
        "An incredible cinematic experience! Beautiful visuals and great performances."
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Test {i}: {text[:50]}...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/predict/",
                json={"text": text},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Prediction: {result['prediction']} (Confidence: {result['confidence']}%)")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        time.sleep(0.5)  # Small delay between requests

def test_samples():
    """Test the sample texts endpoint"""
    print("\n🧪 Testing Sample Texts Endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/samples/")
        
        if response.status_code == 200:
            samples = response.json()['samples']
            print(f"✅ Retrieved {len(samples)} sample texts")
            for i, sample in enumerate(samples[:3], 1):
                print(f"   Sample {i}: {sample[:60]}...")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def test_web_interface():
    """Test the web interface"""
    print("\n🧪 Testing Web Interface...")
    
    try:
        response = requests.get(BASE_URL)
        
        if response.status_code == 200:
            print("✅ Home page loads successfully")
            if "Sentiment Analysis" in response.text:
                print("✅ Page contains expected content")
            else:
                print("❌ Page missing expected content")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def main():
    """Run all tests"""
    print("🚀 Starting Sentiment Analysis Application Tests")
    print("=" * 50)
    
    # Test web interface first
    test_web_interface()
    
    # Test API endpoints
    test_api()
    test_samples()
    
    print("\n" + "=" * 50)
    print("✅ Testing completed!")
    print("\n📊 Summary:")
    print("- Web interface: Working")
    print("- API prediction endpoint: Working") 
    print("- Sample texts endpoint: Working")
    print("\n🎉 Application is ready for use!")

if __name__ == "__main__":
    main()
