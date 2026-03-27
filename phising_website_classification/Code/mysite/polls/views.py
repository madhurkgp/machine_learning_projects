from django.shortcuts import render, redirect
import pandas as pd
import pickle
import os
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

def fallback_prediction(form_data):
    """
    Fallback prediction logic when ML model fails to load
    Uses rule-based approach as backup
    """
    risk_score = 0
    
    # URL structure risks
    if form_data['NumDots'] > 3:
        risk_score += 15
    if form_data['NumDash'] > 5:
        risk_score += 10
    if form_data['PathLevel'] > 5:
        risk_score += 10
    if form_data['NumSensitiveWords'] > 2:
        risk_score += 20
    
    # Security risks
    if form_data['InsecureForms'] == 1:
        risk_score += 25
    if form_data['FrequentDomainNameMismatch'] == 1:
        risk_score += 20
    if form_data['SubmitInfoToEmail'] == 1:
        risk_score += 15
    if form_data['IframeOrFrame'] == 1:
        risk_score += 10
    
    # Content risks
    if form_data['PctExtHyperlinks'] > 0.7:
        risk_score += 15
    if form_data['PctExtResourceUrls'] > 0.6:
        risk_score += 10
    if form_data['PctNullSelfRedirectHyperlinks'] > 0.5:
        risk_score += 10
    
    # Normalize to 0-1 confidence
    confidence = min(risk_score / 100, 0.95)
    is_phishing = risk_score >= 50  # Threshold for phishing
    
    return is_phishing, confidence

def index_func(request):
    res = None
    error_message = None
    model_loaded = False
    
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            if not name:
                error_message = "Please enter a URL name"
                return render(request, "index.html", {
                    'response': res, 
                    'error': error_message,
                    'model_loaded': model_loaded
                })

            # Get form values with defaults
            form_data = {
                'NumDots': float(request.POST.get('NumDots', 0)),
                'PathLevel': float(request.POST.get('PathLevel', 0)),
                'NumDash': float(request.POST.get('NumDash', 0)),
                'NumSensitiveWords': float(request.POST.get('NumSensitiveWords', 0)),
                'PctExtHyperlinks': float(request.POST.get('PctExtHyperlinks', 0)),
                'PctExtResourceUrls': float(request.POST.get('PctExtResourceUrls', 0)),
                'InsecureForms': float(request.POST.get('InsecureForms', 0)),
                'PctNullSelfRedirectHyperlinks': float(request.POST.get('PctNullSelfRedirectHyperlinks', 0)),
                'FrequentDomainNameMismatch': float(request.POST.get('FrequentDomainNameMismatch', 0)),
                'SubmitInfoToEmail': float(request.POST.get('SubmitInfoToEmail', 0)),
                'IframeOrFrame': float(request.POST.get('IframeOrFrame', 0))
            }

            # Create DataFrame with proper column order
            columns = ['NumDots','PathLevel','NumDash','NumSensitiveWords',
                      'PctExtHyperlinks','PctExtResourceUrls','InsecureForms',
                      'PctNullSelfRedirectHyperlinks','FrequentDomainNameMismatch',
                      'SubmitInfoToEmail','IframeOrFrame']
            
            df = pd.DataFrame([form_data], columns=columns)

            # Try to load and use the ML model
            try:
                model_path = os.path.join('polls', 'Phishing.pickle')
                if os.path.exists(model_path):
                    loaded_model = pickle.load(open(model_path, 'rb'))
                    prediction = loaded_model.predict(df)
                    probability = loaded_model.predict_proba(df) if hasattr(loaded_model, 'predict_proba') else None
                    
                    is_phishing = bool(prediction[0])
                    confidence = float(probability[0][1]) if probability is not None else 0.8
                    model_loaded = True
                    
                    logger.info(f"ML model prediction: {is_phishing} with confidence {confidence}")
                else:
                    raise FileNotFoundError("Model file not found")
                    
            except Exception as model_error:
                logger.warning(f"ML model failed, using fallback: {model_error}")
                is_phishing, confidence = fallback_prediction(form_data)
                model_loaded = False
            
            res = {
                'is_phishing': is_phishing,
                'confidence': confidence,
                'url_name': name,
                'model_loaded': model_loaded
            }

        except ValueError as e:
            error_message = f"Invalid input values: {str(e)}"
            logger.error(f"Value error: {e}")
        except Exception as e:
            error_message = f"An error occurred during prediction: {str(e)}"
            logger.error(f"Prediction error: {e}")

    return render(request, "index.html", {
        'response': res, 
        'error': error_message,
        'model_loaded': getattr(res, 'model_loaded', False) if res else False
    })