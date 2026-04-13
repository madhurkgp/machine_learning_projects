from django.shortcuts import render, redirect
import pandas as pd
import pickle
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def index_func(request):
    res = 0
    error_message = ""
    
    if request.method == 'POST':
        if request.POST.get('pred_button'):
            try:
                # Get form data
                name = request.POST.get('Name', '').strip()
                yor = request.POST.get('yor', '').strip()
                NA = request.POST.get('NA', '').strip()
                EU = request.POST.get('EU', '').strip()
                JP = request.POST.get('JP', '').strip()
                score = request.POST.get('score', '').strip()
                critic_count = request.POST.get('critic_count', '').strip()
                user_count = request.POST.get('user_count', '').strip()
                console = request.POST.get('console', '').strip()
                dev = request.POST.get('dev', '').strip()
                rate = request.POST.get('rate', '').strip()
                pub = request.POST.get('pub', '').strip()

                # Validate required fields
                if not all([name, yor, NA, EU, JP, score, critic_count, user_count, console, dev, rate, pub]):
                    error_message = "All fields are required!"
                    return render(request, 'index.html', {'result': res, 'error': error_message})

                # Validate numeric inputs
                try:
                    yor = int(yor)
                    NA = float(NA)
                    EU = float(EU)
                    JP = float(JP)
                    score = float(score)
                    critic_count = float(critic_count)
                    user_count = int(user_count)
                except ValueError:
                    error_message = "Please enter valid numeric values!"
                    return render(request, 'index.html', {'result': res, 'error': error_message})

                # Validate ranges
                if not (1980 <= yor <= 2024):
                    error_message = "Year must be between 1980 and 2024!"
                    return render(request, 'index.html', {'result': res, 'error': error_message})
                
                if not (0 <= NA <= 42):
                    error_message = "NA Sales must be between 0 and 42!"
                    return render(request, 'index.html', {'result': res, 'error': error_message})
                
                if not (0 <= EU <= 30):
                    error_message = "EU Sales must be between 0 and 30!"
                    return render(request, 'index.html', {'result': res, 'error': error_message})
                
                if not (0 <= JP <= 10):
                    error_message = "JP Sales must be between 0 and 10!"
                    return render(request, 'index.html', {'result': res, 'error': error_message})
                
                if not (0 <= score <= 100):
                    error_message = "Critic Score must be between 0 and 100!"
                    return render(request, 'index.html', {'result': res, 'error': error_message})
                
                if not (0 <= critic_count <= 100):
                    error_message = "Critic Count must be between 0 and 100!"
                    return render(request, 'index.html', {'result': res, 'error': error_message})
                
                if not (100 <= user_count <= 10000):
                    error_message = "User Count must be between 100 and 10000!"
                    return render(request, 'index.html', {'result': res, 'error': error_message})

                # Create DataFrame with correct column order
                df = pd.DataFrame(columns=['Year_of_Release', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Critic_Score',
                                    'Critic_Count', 'User_Count', 'PC', 'PS2', 'PS3', 'X360',
                                    'other_console', 'Capcom', 'EA', 'Komani', 'Ubisoft', 'other_dev', 'E',
                                    'E10+', 'M', 'T', 'other_rating', 'Activision', 'Electronic Arts',
                                    'Konami Digital Entertainment', 'Nintendo',
                                    'Sony Computer Entertainment', 'Ubisoft', 'other_publisher'])

                # Process categorical features
                console_encoded = console_func(console)
                dev_encoded = dev_func(dev)
                pg_rate_encoded = rate_func(rate)
                pub_encoded = pub_func(pub)

                # Create data row
                df2 = {'Year_of_Release': yor, 'NA_Sales': NA, 'EU_Sales': EU,
                       'JP_Sales': JP, 'Critic_Score': score, 'Critic_Count': critic_count,
                       'User_Count': user_count, 'PC': console_encoded[0], 'PS2': console_encoded[1], 
                       'PS3': console_encoded[2], 'X360': console_encoded[3], 'other_console': console_encoded[4], 
                       'Capcom': dev_encoded[0], 'EA': dev_encoded[1], 'Komani': dev_encoded[2], 
                       'Ubisoft': dev_encoded[3], 'other_dev': dev_encoded[4], 'E': pg_rate_encoded[0],
                       'E10+': pg_rate_encoded[1], 'M': pg_rate_encoded[2], 'T': pg_rate_encoded[3], 
                       'other_rating': pg_rate_encoded[4], 'Activision': pub_encoded[0], 
                       'Electronic Arts': pub_encoded[1], 'Konami Digital Entertainment': pub_encoded[2],
                       'Nintendo': pub_encoded[3], 'Sony Computer Entertainment': pub_encoded[4],
                       'Ubisoft': pub_encoded[5], 'other_publisher': pub_encoded[6]}

                df = pd.concat([df, pd.DataFrame([df2])], ignore_index=True)
                
                # Load and use model
                model_path = 'polls/VideoGamesModel.pickle'
                if os.path.exists(model_path):
                    try:
                        loaded_model = pickle.load(open(model_path, 'rb'))
                        prediction = loaded_model.predict(df)
                        res = float(abs(prediction[0]))
                        logger.info(f"Prediction successful: {res}")
                    except Exception as e:
                        logger.error(f"Model prediction error: {str(e)}")
                        error_message = "Error making prediction. Please try again."
                else:
                    logger.error("Model file not found!")
                    error_message = "Model file not found. Please contact administrator."
                    
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                error_message = "An unexpected error occurred. Please try again."
                
        else:
            return redirect('homepage')
    
    return render(request, 'index.html', {'result': res, 'error': error_message})


def console_func(x):
    # PC	PS2	PS3	X360	other_console
    if x == 'PC':
        return [1, 0, 0, 0, 0]
    elif x == 'PS2':
        return [0, 1, 0, 0, 0]
    if x == 'PS3':
        return [0, 0, 1, 0, 0]
    if x == 'X360':
        return [0, 0, 0, 1, 0]
    else:
        return [0, 0, 0, 0, 1]


def dev_func(x):
    # Capcom	EA	Komani	Ubisoft	other_dev
    if x == 'Capcom':
        return [1, 0, 0, 0, 0]
    elif x == 'EA':
        return [0, 1, 0, 0, 0]
    if x == 'Komani':
        return [0, 0, 1, 0, 0]
    if x == 'Ubisoft':
        return [0, 0, 0, 1, 0]
    else:
        return [0, 0, 0, 0, 1]


def rate_func(x):
    # E	E10+	M	T	other_rating
    if x == 'E':
        return [1, 0, 0, 0, 0]
    elif x == 'E10+':
        return [0, 1, 0, 0, 0]
    elif x == 'M':
        return [0, 0, 1, 0, 0]
    elif x == 'T':
        return [0, 0, 0, 1, 0]
    else:
        return [0, 0, 0, 0, 1]


def pub_func(x):
    # Activision, Electronic Arts, Konami Digital Entertainment, Nintendo,
    # Sony Computer Entertainment, Ubisoft, other_publisher
    if x == 'Activision':
        return [1, 0, 0, 0, 0, 0, 0]
    elif x == 'Electronic Arts':
        return [0, 1, 0, 0, 0, 0, 0]
    if x == 'Konami Digital Entertainment':
        return [0, 0, 1, 0, 0, 0, 0]
    if x == 'Nintendo':
        return [0, 0, 0, 1, 0, 0, 0]
    elif x == 'Sony Computer Entertainment':
        return [0, 0, 0, 0, 1, 0, 0]
    elif x == 'Ubisoft':
        return [0, 0, 0, 0, 0, 1, 0]
    else:
        return [0, 0, 0, 0, 0, 0, 1]
