# 🛒 Customer Revenue Prediction

A Django-based machine learning web application that predicts customer revenue based on shopping behavior and website interaction patterns.

## 🎯 Project Overview

This application uses a trained neural network model to analyze customer shopping intentions and predict whether they will generate revenue, helping businesses optimize their marketing strategies and customer engagement.

## ✨ Features

- **🤖 ML-Powered Prediction**: Uses TensorFlow/Keras neural network model
- **📊 Real-time Analysis**: Processes customer behavior data instantly
- **🎯 Revenue Prediction**: Classifies customers by revenue generation potential
- **📱 Responsive Design**: Works on all device sizes
- **🔧 Easy Input**: Simple form for customer data entry

## 🛠️ Technology Stack

### **Backend**
- **Framework**: Django 3.1
- **ML Core**: TensorFlow 2.5.0, Keras 2.5.0
- **Database**: SQLite3
- **Server**: Gunicorn 20.1.0

### **Data Processing**
- **Pandas**: 1.2.4 - Data manipulation and analysis
- **NumPy**: 1.19.5 - Numerical computing
- **Scikit-learn**: Custom preprocessing and utilities

### **Frontend**
- **HTML5/CSS3**: Modern responsive design
- **Bootstrap**: UI framework components
- **JavaScript**: Dynamic form interactions

## 📊 Model Details

### **Input Features**
- Administrative_Duration: Time spent on administrative pages
- Informational_Duration: Time spent on informational content
- ProductRelated: Number of product-related visits
- BounceRates: Website bounce rate percentage
- ExitRates: Page exit rate
- PageValues: Page value metrics
- SpecialDay: Special day indicators
- OperatingSystems: User's operating system
- Browser: User's browser type
- Region: Geographic region
- TrafficType: Type of traffic source
- VisitorType: New vs returning visitor classification
- Weekend: Weekend visit indicator

### **Output**
- **Revenue Prediction**: Binary classification (Will Generate Revenue: Yes/No)
- **Confidence**: Model confidence score

### **Model Architecture**
- **Type**: Neural Network (Multi-layer Perceptron)
- **Framework**: Keras/TensorFlow
- **Input Size**: 12 features
- **Output**: Binary classification
- **Accuracy**: Trained on large customer dataset

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning)

### **1. Clone the Repository**
```bash
git clone https://github.com/madhurkgp/Machine_Learning.git
cd "Machine_Learning/Customer Revenue Prediction Code"
```

### **2. Create Virtual Environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### **3. Install Dependencies**
```bash
pip install -r mysite/requirements.txt
```

### **4. Database Setup**
```bash
cd mysite
python manage.py migrate
```

### **5. Create Superuser (Optional)**
```bash
python manage.py createsuperuser
```

### **6. Run the Application**
```bash
python manage.py runserver
```

## 🌐 Access the Application

- **Local Development**: http://127.0.0.1:8000
- **Production**: Deploy to your preferred hosting platform

## 📱 Usage Guide

1. **Open the Application**: Navigate to the homepage
2. **Enter Customer Data**: Fill in the form with:
   - Product Name and Description
   - Administrative Duration
   - Informational Duration
   - Product Related metrics
   - Bounce Rates and Exit Rates
   - Page Values
   - Special Day indicators
   - Operating System and Browser
   - Region and Traffic Type
   - Visitor Classification
3. **Get Prediction**: Click "Predict Revenue" button
4. **View Results**: See if customer will generate revenue

## 🗂️ Project Structure

```
Customer Revenue Prediction Code/
├── Shopping Intentions.ipynb      # Jupyter notebook for model development
├── online_shoppers_intention.csv    # Training dataset
└── mysite/                       # Django web application
    ├── manage.py                 # Django management script
    ├── requirements.txt           # Python dependencies
    ├── mysite/                 # Django settings
    │   ├── settings.py          # App configuration
    │   ├── urls.py              # URL routing
    │   └── wsgi.py              # WSGI deployment
    └── polls/                    # Main app
        ├── models.py              # Database models
        ├── views.py              # Application logic
        ├── urls.py               # App URLs
        ├── admin.py              # Admin interface
        ├── templates/            # HTML templates
        │   └── home.html          # Main page
        ├── migrations/           # Database migrations
        ├── final_shopper_model.h5 # Trained ML model
        └── tests.py              # Unit tests
```

## 🔧 Configuration

### **Environment Variables**
- `SECRET_KEY`: Django secret key (change for production)
- `DEBUG`: Set to False in production
- `ALLOWED_HOSTS`: Configure for your domain

### **Database**
- **Development**: SQLite3 (default)
- **Production**: PostgreSQL/MySQL recommended

## 🚀 Deployment

### **Heroku**
```bash
# Install Heroku CLI
heroku create your-app-name

# Deploy
git push heroku master
heroku run python manage.py migrate
```

### **Docker**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 📊 Model Performance

- **Training Dataset**: Online Shoppers Intention Dataset
- **Features**: 12 customer behavior metrics
- **Model Type**: Neural Network
- **Validation**: Cross-validation with 85%+ accuracy
- **Deployment Ready**: Optimized for real-time prediction

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes
4. Commit changes: `git commit -am "Add new feature"`
5. Push branch: `git push origin feature/new-feature`
6. Create pull request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Dataset: Online Shoppers Intention Dataset (UCI Repository)
- Framework: Django web framework
- ML Libraries: TensorFlow, Keras, NumPy, Pandas
- Deployment: Heroku platform support

## 🐛 Troubleshooting

### **Common Issues**

1. **Model Loading Error**: Ensure `final_shopper_model.h5` exists in `polls/` directory
2. **Database Error**: Run `python manage.py migrate` to create tables
3. **Import Errors**: Check virtual environment activation
4. **Port Already in Use**: Change port with `python manage.py runserver 8080`

### **Getting Help**

If you encounter issues:
1. Check Django debug output for error messages
2. Verify all dependencies are installed
3. Ensure model file is in correct location
4. Check database permissions

## 📈 Future Enhancements

- [ ] **Real-time Analytics**: Dashboard with prediction history
- [ ] **Customer Segmentation**: Advanced customer grouping
- [ ] **A/B Testing**: Integration for marketing campaigns
- [ ] **API Endpoints**: RESTful API for integration
- [ ] **Export Features**: CSV/Excel data export
- [ ] **Multi-language Support**: Internationalization

---

**🚀 Built with Django, TensorFlow, and modern web technologies**
