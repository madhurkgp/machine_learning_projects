from django.shortcuts import render, redirect
import pandas as pd
import pickle
import numpy as np
from django.contrib import messages

def index_func(request):
    res = 0
    if request.method == 'POST':
        try:
            attrite = request.POST.get('attrite')
            name = request.POST.get('name', '').strip()
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            children = request.POST.get('children')
            edu = request.POST.get('edu')
            marital = request.POST.get('marital')
            income = request.POST.get('income')
            monthOnBooks = request.POST.get('monthOnBooks')
            totalRelationshipCount = request.POST.get('totalRelationshipCount')
            monthsInactive12mon = request.POST.get('monthsInactive12mon')
            contactsCount12mon = request.POST.get('contactsCount12mon')
            creditLimit = request.POST.get('creditLimit')
            totalRevolvingBal = request.POST.get('totalRevolvingBal')
            avgOpenToBuy = request.POST.get('avgOpenToBuy')
            totalAmtChngQ4Q1 = request.POST.get('totalAmtChngQ4Q1')
            totalTransAmt = request.POST.get('totalTransAmt')
            totalTransCt = request.POST.get('totalTransCt')
            totalCtChngQ4Q1 = request.POST.get('totalCtChngQ4Q1')
            avgUtilizationRatio = request.POST.get('avgUtilizationRatio')

            if not name:
                messages.error(request, 'Please enter your name')
                return render(request, "index.html", {'response': res})

            # Validate required fields
            required_fields = [age, gender, children, edu, marital, income, monthOnBooks, 
                             totalRelationshipCount, monthsInactive12mon, contactsCount12mon,
                             creditLimit, totalRevolvingBal, avgOpenToBuy, totalAmtChngQ4Q1,
                             totalTransAmt, totalTransCt, totalCtChngQ4Q1, avgUtilizationRatio]
            
            if any(field in ['', None] for field in required_fields):
                messages.error(request, 'Please fill in all required fields')
                return render(request, "index.html", {'response': res})

            # Create DataFrame with proper data types
            df = pd.DataFrame([{
                'Attrition_Flag': int(attrite),
                'Customer_Age': float(age),
                'Gender': int(gender),
                'Dependent_count': float(children),
                'Education_Level': int(edu),
                'Marital_Status': int(marital),
                'Income_Category': int(income),
                'Months_on_book': int(monthOnBooks),
                'Total_Relationship_Count': int(totalRelationshipCount),
                'Months_Inactive_12_mon': int(monthsInactive12mon),
                'Contacts_Count_12_mon': int(contactsCount12mon),
                'Credit_Limit': float(creditLimit),
                'Total_Revolving_Bal': float(totalRevolvingBal),
                'Avg_Open_To_Buy': float(avgOpenToBuy),
                'Total_Amt_Chng_Q4_Q1': float(totalAmtChngQ4Q1),
                'Total_Trans_Amt': float(totalTransAmt),
                'Total_Trans_Ct': float(totalTransCt),
                'Total_Ct_Chng_Q4_Q1': float(totalCtChngQ4Q1),
                'Avg_Utilization_Ratio': float(avgUtilizationRatio)
            }])

            # Load the model from disk
            try:
                filename = 'polls/BankCardsPCA.pickle'
                pca = pickle.load(open(filename, 'rb'))
                data = pca.transform(df)
                filename1 = 'polls/BankCards.pickle'
                loaded_model = pickle.load(open(filename1, 'rb'))
                res = loaded_model.predict(data)[0]
                
                # Map prediction to card category names
                card_categories = {0: 'Blue', 1: 'Gold', 2: 'Silver', 3: 'Platinum'}
                res = card_categories.get(res, 'Unknown')
                messages.success(request, f'Prediction completed successfully!')
                
            except FileNotFoundError as e:
                messages.error(request, 'Model files not found. Please ensure ML models are properly deployed.')
                res = 'Error'
            except Exception as e:
                messages.error(request, f'Error during prediction: {str(e)}')
                res = 'Error'

        except ValueError as e:
            messages.error(request, 'Invalid input format. Please check your values.')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')

    return render(request, "index.html", {'response': res})
