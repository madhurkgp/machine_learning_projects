#!/usr/bin/env python
"""
Debug script for model training
"""

import os
import sys
import pandas as pd

# Add the project directory to Python path
sys.path.append(os.path.dirname(__file__))

from prediction.ml_model import SentimentAnalyzer

def debug_training():
    """Debug the model training process"""
    print("🔍 Debugging Model Training...")
    
    try:
        # Create analyzer instance
        analyzer = SentimentAnalyzer()
        
        # Test with a simple prediction
        test_text = "This is a great movie!"
        print(f"\n📝 Testing with: '{test_text}'")
        
        result = analyzer.predict_sentiment(test_text)
        print(f"✅ Result: {result}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

def debug_data():
    """Debug the training data"""
    print("\n🔍 Debugging Training Data...")
    
    data_file = os.path.join(os.path.dirname(__file__), 'Notebook', 'TextAnalytics.txt')
    print(f"Data file: {data_file}")
    print(f"File exists: {os.path.exists(data_file)}")
    
    if os.path.exists(data_file):
        data = []
        with open(data_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if line_num <= 10:  # Show first 10 lines
                    print(f"Line {line_num}: {line.strip()[:100]}...")
                
                if line.strip():
                    parts = line.strip().split(',', 1)
                    if len(parts) == 2:
                        try:
                            label = int(parts[0])
                            text = parts[1].strip('"')
                            if text and len(text.strip()) > 10:
                                data.append((text, label))
                        except ValueError:
                            print(f"❌ Line {line_num}: Invalid label format")
        
        print(f"\n📊 Total valid samples: {len(data)}")
        
        if data:
            df = pd.DataFrame(data, columns=['text', 'label'])
            print(f"📈 Label distribution:")
            print(df['label'].value_counts())
            
            print(f"\n📝 Sample texts:")
            for i, (text, label) in enumerate(data[:3], 1):
                print(f"{i}. [{label}] {text[:100]}...")

if __name__ == "__main__":
    debug_data()
    debug_training()
