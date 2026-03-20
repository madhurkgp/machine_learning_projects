# IPL Win Probability Predictor

A Flask web application that predicts the win probability of an IPL cricket match during the second innings based on current match conditions.

## Features

- Real-time win probability prediction
- Clean, responsive web interface
- Machine learning model using Logistic Regression
- RESTful API endpoint

## Requirements

- Python 3.8+
- Flask
- Scikit-learn
- Pandas
- NumPy

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Train the model (if pipe.pkl doesn't exist):
```bash
python train_model.py
```

3. Run the Flask application:
```bash
python app.py
```

4. Open http://localhost:5000 in your browser

## API Usage

### POST /predict

Predict win probability based on current match conditions.

**Request Body:**
```json
{
    "batting_team": "Chennai Super Kings",
    "bowling_team": "Mumbai Indians", 
    "city": "Mumbai",
    "target": 180,
    "score": 120,
    "overs_done": "14.2",
    "wickets_fallen": 5
}
```

**Response:**
```json
{
    "success": true,
    "batting_team": "Chennai Super Kings",
    "bowling_team": "Mumbai Indians",
    "win_prob": 75,
    "loss_prob": 25
}
```

## Files

- `app.py` - Flask web application
- `train_model.py` - Model training script
- `pipe.pkl` - Trained machine learning model
- `matches.csv` - IPL match data
- `deliveries.csv` - Ball-by-ball delivery data
- `IPL Win Probability Predictor.ipynb` - Jupyter notebook with analysis
- `templates/index.html` - Frontend interface
- `requirements.txt` - Python dependencies

## Model

The model uses Logistic Regression with the following features:
- Batting team
- Bowling team  
- City
- Runs left to chase
- Balls remaining
- Wickets remaining
- Target score
- Current run rate
- Required run rate

## Teams Supported

- Sunrisers Hyderabad
- Mumbai Indians  
- Royal Challengers Bangalore
- Kolkata Knight Riders
- Kings XI Punjab
- Chennai Super Kings
- Rajasthan Royals
- Delhi Capitals
