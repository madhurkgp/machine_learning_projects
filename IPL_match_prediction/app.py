from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

# Teams and cities data
teams = [
    "Sunrisers Hyderabad", "Mumbai Indians", "Royal Challengers Bangalore",
    "Kolkata Knight Riders", "Kings XI Punjab", "Chennai Super Kings",
    "Rajasthan Royals", "Delhi Capitals",
]

cities = [
    "Hyderabad", "Bangalore", "Mumbai", "Indore", "Kolkata", "Delhi",
    "Chandigarh", "Jaipur", "Chennai", "Cape Town", "Port Elizabeth",
    "Durban", "Centurion", "East London", "Johannesburg", "Kimberley",
    "Bloemfontein", "Ahmedabad", "Cuttack", "Nagpur", "Dharamsala",
    "Visakhapatnam", "Pune", "Raipur", "Ranchi", "Abu Dhabi",
    "Sharjah", "Mohali", "Bengaluru",
]

def _parse_overs_to_balls(overs_str: str) -> int:
    """
    Convert overs input like '10.2' into balls bowled (10 overs + 2 balls = 62).
    Accepts '10', '10.0', '10.2'. Balls part must be 0-5.
    """
    s = (overs_str or "").strip()
    if s == "":
        raise ValueError("Overs completed is required (e.g. 10.2).")

    if "." in s:
        over_part, ball_part = s.split(".", 1)
        overs = int(over_part) if over_part else 0
        balls = int(ball_part) if ball_part else 0
    else:
        overs = int(s)
        balls = 0

    if overs < 0 or overs > 19:
        raise ValueError("Overs must be between 0 and 19.")
    if balls < 0 or balls > 5:
        raise ValueError("Balls must be between 0 and 5 (use format like 10.2).")

    return overs * 6 + balls


def load_model():
    # The model must be trained/saved with the same scikit-learn major version.
    with open("pipe.pkl", "rb") as f:
        return pickle.load(f)


pipe = load_model()


@app.route("/")
def index():
    return render_template("index.html", teams=sorted(teams), cities=sorted(cities))


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        
        batting_team = data.get("batting_team")
        bowling_team = data.get("bowling_team")
        city = data.get("city")
        target = float(data.get("target", 0))
        score = float(data.get("score", 0))
        overs_done_raw = str(data.get("overs_done", ""))
        wickets_fallen = int(data.get("wickets_fallen", 0))
        
        # Validation
        if batting_team == bowling_team:
            return jsonify({"error": "Batting and bowling team must be different."}), 400

        balls_bowled = _parse_overs_to_balls(overs_done_raw)
        if balls_bowled <= 0:
            return jsonify({"error": "Enter overs completed (e.g. 10.2)."}), 400
        
        # Calculate features
        runs_left = target - score
        balls_left = max(0, 120 - balls_bowled)
        wickets_left = 10 - wickets_fallen
        current_rr = (score * 6) / balls_bowled if balls_bowled else 0
        required_rr = (runs_left * 6) / balls_left if balls_left else 0
        
        # Prepare input dataframe
        input_df = pd.DataFrame({
            "batting_team": [batting_team],
            "bowling_team": [bowling_team],
            "city": [city],
            "runs_left": [runs_left],
            "balls_left": [balls_left],
            "wickets": [wickets_left],
            "total_runs_x": [target],
            "cur_run_rate": [current_rr],
            "req_run_rate": [required_rr],
        })
        
        # Predict
        proba = pipe.predict_proba(input_df)
        loss_prob = proba[0][0]
        win_prob = proba[0][1]
        
        return jsonify({
            "success": True,
            "batting_team": batting_team,
            "bowling_team": bowling_team,
            "win_prob": round(win_prob * 100),
            "loss_prob": round(loss_prob * 100),
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
