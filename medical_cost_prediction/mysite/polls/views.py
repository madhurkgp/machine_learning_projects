from django.shortcuts import render, redirect
import pandas as pd
import pickle
import logging

# Configure logging
logger = logging.getLogger(__name__)

def index_func(request):
    res = 0
    error_message = ""
    
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            age = request.POST.get('age', '').strip()
            gender = request.POST.get('sex', '').strip()
            bmi = request.POST.get('bmi', '').strip()
            child = request.POST.get('child', '').strip()
            smoker = request.POST.get('smoker', '').strip()
            region = request.POST.get('region', '').strip()

            # Validation
            if not name:
                error_message = "Please enter your name"
            elif not age or not age.isdigit() or int(age) < 18 or int(age) > 100:
                error_message = "Please enter a valid age (18-100)"
            elif not bmi or not (bmi.replace('.', '', 1).isdigit()) or float(bmi) < 10 or float(bmi) > 50:
                error_message = "Please enter a valid BMI (10-50)"
            elif not child or not child.isdigit() or int(child) < 0 or int(child) > 10:
                error_message = "Please enter a valid number of children (0-10)"
            elif not gender or not smoker or not region:
                error_message = "Please select all dropdown options"
            
            if error_message:
                return render(request, "index.html", {'response': res, 'error_message': error_message})

            # Create DataFrame with proper method
            df = pd.DataFrame(columns=['age', 'sex', 'bmi', 'children', 'smoker', 'region'])
            df2 = {'age': float(age), 'sex': int(gender), 'bmi': float(bmi), 'children': int(child),
                   'smoker': int(smoker), 'region': int(region)}
            
            df = pd.concat([df, pd.DataFrame([df2])], ignore_index=True)
            
            # Load the model from disk
            filename1 = 'polls/Medical.pickle'
            try:
                loaded_model = pickle.load(open(filename1, 'rb'))
                res = loaded_model.predict(df)[0]
                logger.info(f"Prediction successful for {name}: ${res:.2f}")
            except FileNotFoundError:
                error_message = "Model file not found. Please ensure the ML model is properly deployed."
                logger.error("Model file not found")
            except Exception as e:
                # Fallback prediction if model fails
                error_message = "Model prediction failed. Using fallback calculation."
                logger.error(f"Model prediction error: {str(e)}")
                
                # Simple fallback calculation based on insurance industry heuristics
                base_cost = 2000
                age_factor = (float(age) - 25) * 50
                bmi_factor = (float(bmi) - 22) * 100 if float(bmi) > 22 else 0
                smoker_factor = 15000 if int(smoker) == 1 else 0
                children_factor = int(child) * 500
                region_factor = 500 if int(region) in [0, 1] else 0  # Northeast/Northwest more expensive
                
                res = base_cost + age_factor + bmi_factor + smoker_factor + children_factor + region_factor
                res = max(res, 1000)  # Minimum cost
                logger.warning(f"Used fallback prediction for {name}: ${res:.2f}")

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            logger.error(f"Unexpected error: {str(e)}")

    return render(request, "index.html", {'response': res, 'error_message': error_message})
