from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Configuration
API_KEY = "SV2r3R9pKCF8qb0RxJoz3tAah72wteriLPP4at3ZFKcL"
USE_PRIVATE_ENDPOINT = True

# Endpoints
PRIVATE_ENDPOINT = "https://private.au-syd.ml.cloud.ibm.com/ml/v4/deployments/add/predictions?version=2021-05-01"
PUBLIC_ENDPOINT = "https://au-syd.ml.cloud.ibm.com/ml/v4/deployments/add/predictions?version=2021-05-01"
DEPLOYMENT_ID = "add"
SERVING_NAME = "add"

def get_auth_token():
    """Get IBM Cloud authentication token"""
    try:
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={
            "apikey": API_KEY, 
            "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
        })
        
        if token_response.status_code == 200:
            return token_response.json()["access_token"]
        else:
            return None
    except Exception as e:
        print(f"Error getting token: {e}")
        return None

def make_prediction(input_data, token):
    """Make prediction using IBM Cloud ML"""
    try:
        endpoint_url = PRIVATE_ENDPOINT if USE_PRIVATE_ENDPOINT else PUBLIC_ENDPOINT
        
        payload_scoring = {
            "input_data": [{
                "fields": ["daily_time", "age", "areaincome", "dailyinternetuse", "adtopicline", "city", "gender", "country", "timestamp"],
                "values": [input_data]
            }]
        }
        
        headers = {'Authorization': 'Bearer ' + token}
        
        response_scoring = requests.post(endpoint_url, json=payload_scoring, headers=headers, timeout=10)
        
        if response_scoring.status_code == 200:
            return response_scoring.json()
        else:
            print(f"API Error: {response_scoring.status_code} - {response_scoring.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return None
    except Exception as e:
        print(f"Error making prediction: {e}")
        return None

def fallback_prediction(input_data):
    """Fallback prediction when API is unavailable"""
    try:
        # Simple rule-based prediction for demo purposes
        daily_time, age, areaincome, dailyinternetuse, adtopicline, city, gender, country, timestamp = input_data
        
        # Simple logic: higher daily time and internet usage increases click probability
        # Lower age and higher income also increase probability
        time_score = min(daily_time / 100, 1.0)  # Normalize to 0-1
        internet_score = min(dailyinternetuse / 300, 1.0)  # Normalize to 0-1
        age_score = max(0, (50 - age) / 50)  # Younger people more likely to click
        income_score = min(areaincome / 100000, 1.0)  # Higher income, more likely to click
        
        # Combine scores with weights
        probability = (time_score * 0.3 + internet_score * 0.3 + age_score * 0.2 + income_score * 0.2)
        probability = min(max(probability, 0.1), 0.9)  # Clamp between 0.1 and 0.9
        
        # Return mock response in same format as IBM Cloud
        return {
            'predictions': [{
                'values': [[0, [probability]]]  # Format: [class_id, [probability]]
            }]
        }
    except Exception as e:
        print(f"Fallback prediction error: {e}")
        return None

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction request"""
    try:
        # Get form data
        data = request.form
        
        # Extract input values
        daily_time = float(data.get('daily_time'))
        age = int(data.get('age'))
        areaincome = float(data.get('areaincome'))
        dailyinternetuse = float(data.get('dailyinternetuse'))
        adtopicline = data.get('adtopicline')
        city = data.get('city')
        gender = data.get('gender')
        country = data.get('country')
        timestamp = data.get('timestamp')
        
        # Prepare input data
        input_features = [daily_time, age, areaincome, dailyinternetuse, 
                         adtopicline, city, gender, country, timestamp]
        
        # Try to get authentication token and make prediction
        token = get_auth_token()
        result = None
        used_fallback = False
        
        if token:
            result = make_prediction(input_features, token)
        
        # If API prediction fails, use fallback
        if not result:
            result = fallback_prediction(input_features)
            used_fallback = True
        
        if not result:
            return jsonify({
                'success': False,
                'error': 'Prediction failed. Please try again.'
            })
        
        # Extract prediction result
        predictions = result.get('predictions', [])
        if predictions and len(predictions) > 0:
            values = predictions[0].get('values', [])
            if values and len(values) > 0:
                probability = values[0][1][0]
                
                # Determine result
                viewed_ad = probability > 0.5
                
                return jsonify({
                    'success': True,
                    'probability': round(probability * 100, 2),
                    'viewed_ad': viewed_ad,
                    'message': 'Based on the above factors, the user viewed the Advertisement' if viewed_ad else 'Based on the above factors, the user did not view the Advertisement',
                    'fallback': used_fallback
                })
        
        return jsonify({
            'success': False,
            'error': 'Unable to parse prediction result.'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
