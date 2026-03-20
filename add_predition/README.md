# Advertising Click Prediction App

A machine learning web application that predicts whether a user will click on an advertisement based on their demographic and behavioral data.

## Overview

This Flask-based application uses IBM Cloud Machine Learning to predict advertisement clicks. It analyzes user characteristics such as age, time spent on site, area income, and internet usage patterns to determine the likelihood of ad engagement.

## Features

- **Web Interface**: Clean, responsive UI for inputting user data
- **Real-time Predictions**: Instant predictions using IBM Cloud ML deployment
- **Probability Analysis**: Shows the confidence score for each prediction
- **Health Check**: API endpoint for monitoring application status

## Tech Stack

- **Backend**: Flask (Python)
- **Machine Learning**: IBM Cloud Watson Machine Learning
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: IBM Cloud

## Dataset

The application uses advertising data with the following features:
- Daily Time Spent on Site (minutes)
- Age (years)
- Area Income (average income of geographical area)
- Daily Internet Usage (minutes)
- Ad Topic Line
- City
- Gender
- Country
- Timestamp
- Clicked on Ad (target variable)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ayushjaiswal21/advertising-click-prediction.git
cd advertising-click-prediction
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up IBM Cloud credentials in `app.py`:
   - Update `API_KEY` with your IBM Cloud API key
   - Update endpoint URLs if using a different deployment

## Usage

1. Run the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Fill in the user information form and click "Predict" to get results

## API Endpoints

- `GET /` - Main application page
- `POST /predict` - Make prediction based on form data
- `GET /health` - Health check endpoint

## Configuration

The application requires the following IBM Cloud configurations:
- Watson Machine Learning service instance
- Deployed model endpoint
- IBM Cloud API key with appropriate permissions

## File Structure

```
advertising-click-prediction/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── advertising.csv     # Dataset file
├── datasetdesc.md      # Dataset description
├── setup.sh           # Setup script
└── templates/
    └── index.html     # Frontend template
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.
