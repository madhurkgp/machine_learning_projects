from django.shortcuts import render, redirect
import pandas as pd
import pickle
import numpy as np
import os
from django.contrib import messages

def index_func(request):
    res = 0
    error = None
    
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            size = request.POST.get('size', '').strip()
            cup = request.POST.get('cup', '').strip()
            bra = request.POST.get('bra', '').strip()
            category = request.POST.get('category', '').strip()
            length = request.POST.get('length', '').strip()
            fit = request.POST.get('fit', '').strip()
            shoeSize = request.POST.get('shoeSize', '').strip()
            shoeWidth = request.POST.get('shoeWidth', '').strip()
            height = request.POST.get('height', '').strip()

            # Validate inputs
            if not name:
                error = "Please enter your name"
            elif not all([size, cup, bra, category, length, fit, shoeSize, shoeWidth, height]):
                error = "Please fill in all required fields"
            else:
                # Convert to floats with validation
                try:
                    size = float(size)
                    cup = float(cup)
                    bra = float(bra)
                    category = float(category)
                    length = float(length)
                    fit = float(fit)
                    shoeSize = float(shoeSize)
                    shoeWidth = float(shoeWidth)
                    height = float(height)
                    
                    # Validate ranges
                    if not (0 <= size <= 50):
                        error = "Size must be between 0 and 50"
                    elif not (28 <= bra <= 44):
                        error = "Bra size must be between 28 and 44"
                    elif not (48 <= height <= 84):
                        error = "Height must be between 48 and 84 inches"
                    elif not (4 <= shoeSize <= 15):
                        error = "Shoe size must be between 4 and 15"
                    elif not (0 <= cup <= 11):
                        error = "Invalid cup size selected"
                    elif not (0 <= category <= 6):
                        error = "Invalid category selected"
                    elif not (0 <= length <= 5):
                        error = "Invalid length selected"
                    elif not (0 <= fit <= 2):
                        error = "Invalid fit selected"
                    elif not (0 <= shoeWidth <= 2):
                        error = "Invalid shoe width selected"
                    else:
                        # Create DataFrame for prediction
                        df = pd.DataFrame(columns=['size', 'cup size', 'bra size', 'category',
                                                   'length', 'fit', 'shoe size', 'shoe width',
                                                   'height_inches'])

                        df2 = {'size': size, 'cup size': cup, 'bra size': bra, 'category':
                               category, 'length': length, 'fit': fit, 'shoe size':
                               shoeSize, 'shoe width': shoeWidth, 'height_inches': height}

                        df = pd.concat([df, pd.DataFrame([df2])], ignore_index=True)
                        
                        # Load the model with error handling
                        model_path = 'polls/Clothes.pickle'
                        if os.path.exists(model_path):
                            try:
                                loaded_model = pickle.load(open(model_path, 'rb'))
                                res = loaded_model.predict(df)
                                
                                # Ensure result is a valid quality score (1-5)
                                if len(res) > 0:
                                    res = np.clip(res[0], 1, 5)
                                else:
                                    error = "Model prediction failed"
                                    
                            except Exception as model_error:
                                print(f"Model loading/prediction error: {model_error}")
                                error = "ML model error. Please try again later."
                        else:
                            error = "ML model not found. Please contact administrator."
                            
                except ValueError as ve:
                    error = "Invalid input values. Please enter valid numbers."
                    print(f"Value error: {ve}")

        except Exception as e:
            error = "An unexpected error occurred. Please try again."
            print(f"Unexpected error: {e}")

        if error:
            messages.error(request, error)
            return render(request, "index.html", {'response': None, 'error': error})

    return render(request, "index.html", {'response': res, 'error': None})
