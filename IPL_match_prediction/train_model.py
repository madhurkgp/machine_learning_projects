import pickle

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def build_training_frame(matches_path: str = "matches.csv", deliveries_path: str = "deliveries.csv") -> pd.DataFrame:
    matches = pd.read_csv(matches_path)
    deliveries = pd.read_csv(deliveries_path)

    # Total 1st-innings score per match (used as target for chase)
    total_runs = deliveries.groupby(["match_id", "inning"], as_index=False)["total_runs"].sum()
    first_innings = total_runs[total_runs["inning"] == 1].copy()
    first_innings["total_runs"] = first_innings["total_runs"] + 1  # as in notebook

    match_df = matches.merge(
        first_innings[["match_id", "total_runs"]],
        left_on="id",
        right_on="match_id",
        how="inner",
    )
    match_df = match_df[["match_id", "city", "winner", "total_runs"]]

    # Merge with ball-by-ball deliveries; keep only 2nd innings (chase)
    delivery_df = match_df.merge(deliveries, on="match_id", how="inner")
    delivery_df = delivery_df[delivery_df["inning"] == 2].copy()

    # Feature engineering (matches notebook intent)
    delivery_df["current_score"] = delivery_df.groupby("match_id")["total_runs_y"].cumsum()
    delivery_df["runs_left"] = delivery_df["total_runs_x"] - delivery_df["current_score"]

    # Dataset has over starting at 1 and ball starting at 1 (and can exceed 6 for extra deliveries)
    balls_bowled = (delivery_df["over"] - 1) * 6 + delivery_df["ball"]
    delivery_df["balls_left"] = 120 - balls_bowled

    delivery_df["player_dismissed"] = delivery_df["player_dismissed"].notna().astype(int)
    wickets_fallen = delivery_df.groupby("match_id")["player_dismissed"].cumsum()
    delivery_df["wickets"] = 10 - wickets_fallen

    # Rates
    balls_done = 120 - delivery_df["balls_left"]
    delivery_df["cur_run_rate"] = (delivery_df["current_score"] * 6) / balls_done.replace(0, np.nan)
    delivery_df["req_run_rate"] = (delivery_df["runs_left"] * 6) / delivery_df["balls_left"].replace(0, np.nan)

    delivery_df["result"] = (delivery_df["batting_team"] == delivery_df["winner"]).astype(int)

    final_df = delivery_df[
        [
            "batting_team",
            "bowling_team",
            "city",
            "runs_left",
            "balls_left",
            "wickets",
            "total_runs_x",
            "cur_run_rate",
            "req_run_rate",
            "result",
        ]
    ].copy()

    final_df = final_df.replace([np.inf, -np.inf], np.nan).dropna()
    final_df = final_df[final_df["balls_left"] != 0]
    return final_df


def train_and_save_model(out_path: str = "pipe.pkl") -> None:
    final_df = build_training_frame()
    X = final_df.drop(columns=["result"])
    y = final_df["result"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    ohe = OneHotEncoder(sparse_output=False, drop="first", handle_unknown="ignore")
    ct = ColumnTransformer(
        [("trf", ohe, ["batting_team", "bowling_team", "city"])],
        remainder="passthrough",
    )

    model = LogisticRegression(solver="liblinear", max_iter=1000)
    pipe = Pipeline([("step1", ct), ("step2", model)])

    pipe.fit(X_train, y_train)
    acc = pipe.score(X_test, y_test)
    print(f"Validation accuracy: {acc:.4f}  (rows={len(final_df)})")

    # Fit on all data for final artifact
    pipe.fit(X, y)
    with open(out_path, "wb") as f:
        pickle.dump(pipe, f)
    print(f"Saved model to: {out_path}")


if __name__ == "__main__":
    train_and_save_model()

