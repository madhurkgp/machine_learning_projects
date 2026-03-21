from django.shortcuts import render, redirect
import pandas as pd
import pickle
import os
from django.conf import settings

# Create your views here.
def index_func(request):
    res = 0
    error_message = ""
    
    if request.method == 'POST':
        try:
            name = request.POST.get('Name', '').strip()
            age = request.POST.get('age', '').strip()
            years_marr = request.POST.get('years_marr', '').strip()
            child = request.POST.get('child', '').strip()
            education = request.POST.get('education', '').strip()
            occu_level = request.POST.get('occu_level', '').strip()
            rate_marr = request.POST.get('rate_marr', '').strip()
            religion_type = request.POST.get('religion_type', '').strip()
            occu_hus_level = request.POST.get('occu_hus_level', '').strip()

            # Validation
            if not name:
                error_message = "Please enter your name"
            elif not age or not age.isdigit() or int(age) < 17 or int(age) > 50:
                error_message = "Please enter a valid age (17-50)"
            elif not years_marr or not years_marr.replace('.', '').isdigit() or float(years_marr) < 0 or float(years_marr) > 30:
                error_message = "Please enter valid years married (0-30)"
            elif not child or not child.replace('.', '').isdigit() or float(child) < 0 or float(child) > 6:
                error_message = "Please enter valid number of children (0-6)"
            elif not education or not education.isdigit() or int(education) < 9 or int(education) > 20:
                error_message = "Please select education level"
            elif not occu_level or not occu_level.isdigit() or int(occu_level) < 1 or int(occu_level) > 6:
                error_message = "Please enter valid occupation level (1-6)"
            elif not rate_marr or not rate_marr.isdigit() or int(rate_marr) < 1 or int(rate_marr) > 5:
                error_message = "Please select marriage rating"
            elif not religion_type or not religion_type.isdigit() or int(religion_type) < 1 or int(religion_type) > 4:
                error_message = "Please select religion type"
            elif not occu_hus_level or not occu_hus_level.isdigit() or int(occu_hus_level) < 1 or int(occu_hus_level) > 6:
                error_message = "Please select husband's occupation level"
            
            if error_message:
                return render(request, "index.html", {'response': res, 'error': error_message})

            # Create DataFrame with proper feature columns
            df = pd.DataFrame(columns=['age', 'yrs_married', 'children', 'educ', 'occupation',
                                       'rate_1.0', 'rate_2.0', 'rate_3.0', 'rate_4.0', 'rate_5.0',
                                       'religion_1.0', 'religion_2.0', 'religion_3.0', 'religion_4.0',
                                       'husb_occ_1.0', 'husb_occ_2.0', 'husb_occ_3.0', 'husb_occ_4.0',
                                       'husb_occ_5.0', 'husb_occ_6.0'])

            rate = helperRate(int(rate_marr))
            rel = helperReligion(int(religion_type))
            hus = helperOccupationHusband(int(occu_hus_level))

            df2 = {'age': float(age), 'yrs_married': float(years_marr), 'children': float(child),
                   'educ': float(education), 'occupation': float(occu_level), 'rate_1.0': rate[0],
                   'rate_2.0': rate[1], 'rate_3.0': rate[2], 'rate_4.0': rate[3], 'rate_5.0': rate[4],
                    'religion_1.0': rel[0], 'religion_2.0': rel[1], 'religion_3.0': rel[2],
                   'religion_4.0': rel[3], 'husb_occ_1.0': hus[0], 'husb_occ_2.0': hus[1],
                   'husb_occ_3.0': hus[2], 'husb_occ_4.0': hus[3], 'husb_occ_5.0': hus[4],
                   'husb_occ_6.0': hus[5]}

            df = pd.concat([df, pd.DataFrame([df2])], ignore_index=True)
            
            # Load models
            model_path = os.path.join(settings.BASE_DIR, 'polls')
            pca_path = os.path.join(model_path, 'AffairsPCA.pickle')
            model_path_full = os.path.join(model_path, 'Affairs.pickle')
            
            with open(pca_path, 'rb') as f:
                pca = pickle.load(f)
            
            with open(model_path_full, 'rb') as f:
                loaded_model = pickle.load(f)

            data = pca.transform(df)
            res = loaded_model.predict(data)
            res = int(res[0]) if hasattr(res, '__iter__') else int(res)

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return render(request, "index.html", {'response': res, 'error': error_message})

    return render(request, "index.html", {'response': res, 'error': error_message})




def helperRate(x):
    if x == 1:
        return [1, 0, 0, 0, 0]
    elif x == 2:
        return [0, 1, 0, 0, 0]
    elif x == 3:
        return [0, 0, 1, 0, 0]
    elif x == 4:
        return [0, 0, 0, 1, 0]
    else:
        return [0, 0, 0, 0, 1]


def helperReligion(x):
    if x == 1:
        return [1, 0, 0, 0]
    elif x == 2:
        return [0, 1, 0, 0]
    elif x == 3:
        return [0, 0, 1, 0]
    else:
        return [0, 0, 0, 1]


def helperOccupationHusband(x):
    if x == 1:
        return [1, 0, 0, 0, 0, 0]
    elif x == 2:
        return [0, 1, 0, 0, 0, 0]
    elif x == 3:
        return [0, 0, 1, 0, 0, 0]
    elif x == 4:
        return [0, 0, 0, 1, 0, 0]
    elif x == 5:
        return [0, 0, 0, 0, 1, 0]
    else:
        return [0, 0, 0, 0, 0, 1]