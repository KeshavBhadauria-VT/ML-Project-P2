import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, OneHotEncoder
import numpy as np

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor

# List of file paths for each season
season_files = [
    "data/2013-14.csv",
    "data/2014-15.csv",
    "data/2015-16.csv",
    "data/2016-17.csv",
    "data/2017-18.csv",
]

# Concatenate DataFrames and reset the index
all_seasons_df = pd.concat(
    [pd.read_csv(file) for file in season_files], ignore_index=True
)

all_seasons_df = all_seasons_df.drop_duplicates()

all_seasons_df.reset_index(drop=True, inplace=True)

all_seasons_df["FPTS_shifted"] = all_seasons_df.groupby("Player")["FPTS"].shift(1)

all_seasons_df = all_seasons_df.dropna()

features = ["PTS", "TRB", "AST", "STL", "BLK", "TOV", "Team", "Against"]
target = "FPTS_shifted"  # Use shifted FPTS as the target variable
label_encoder = LabelEncoder()
all_seasons_df["Team"] = label_encoder.fit_transform(all_seasons_df["Team"])
all_seasons_df["Against"] = label_encoder.fit_transform(all_seasons_df["Against"])

# One-hot encode categorical variables
one_hot_encoder = OneHotEncoder(drop="first", sparse=False)
encoded_features = pd.DataFrame(
    one_hot_encoder.fit_transform(all_seasons_df[["Team", "Against"]])
)
encoded_features.columns = one_hot_encoder.get_feature_names_out(["Team", "Against"])
all_seasons_df = pd.concat([all_seasons_df, encoded_features], axis=1)

all_seasons_df.reset_index(drop=True, inplace=True)

features += list(encoded_features.columns)

player_models = {}
predicted_fpts_dict = {}

for player in all_seasons_df["Player"].unique():
    player_df = all_seasons_df[all_seasons_df["Player"] == player]

    # Check if there are enough samples for training
    if len(player_df) > 1:
        X = player_df[features]
        y = player_df[target]

        # Check for constant or near-constant target variable
        if np.isclose(np.std(y), 0).any():
            print(
                f"Skipping {player} due to constant or near-constant target variable."
            )
            continue

        # Normalize features using Min-Max scaling
        scaler = MinMaxScaler()
        X_normalized = scaler.fit_transform(X)

        # Check for missing or infinite values
        if (
            X.isnull().any().any()
            or y.isnull().any().any()
            or np.isinf(X).any().any()
            or np.isinf(y).any().any()
        ):
            print(f"Skipping {player} due to missing or infinite values.")
            continue

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X_normalized, y, test_size=0.2, random_state=42
        )

        # Create a linear regression model
        model = RandomForestRegressor(n_estimators=100, random_state=42)

        # Train the model
        model.fit(X_train, y_train)

        # Make predictions on the test set
        y_pred = model.predict(X_test)

        # Check for constant or near-constant predictions
        if np.isclose(np.std(y_pred), 0).any():
            print(f"Skipping {player} due to constant or near-constant predictions.")
            continue

        # Evaluate the model
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Check for NaN values in metrics
        if np.isnan(r2).any():
            print(f"Skipping {player} due to NaN values in R-squared.")
            continue

        # Store the model in the dictionary
        player_models[player] = {"model": model, "mse": mse, "r2": r2}

        # Retrieve the model for the player
        if player in player_models:
            model = player_models[player]["model"]

            # Iterate through each game for the player
            for index, row in player_df.iterrows():
                game_features = row[features].values.reshape(1, -1)

                predicted_fpts = model.predict(game_features)[0]


                predicted_fpts_dict[f"{player} - Game_{index}"] = predicted_fpts

print("Predicted FPTS for player-game matchups:")
for player_game, predicted_fpts in predicted_fpts_dict.items():
    print(f"{player_game}: {predicted_fpts}")
