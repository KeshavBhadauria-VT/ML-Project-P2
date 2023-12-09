import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler

# Load data from CSV file
df = pd.read_csv('data/merged_data.csv')  # Replace 'your_data.csv' with the actual file path

features = "HOME_no,HOME_g,HOME_min,HOME_pts,HOME_reb,HOME_ast,HOME_stl,HOME_blk,HOME_to,HOME_pf,HOME_dreb,HOME_oreb,HOME_pct,HOME_pct_2,HOME_pct_3,HOME_eff,HOME_deff,AWAY_no,AWAY_g,AWAY_min,AWAY_pts,AWAY_reb,AWAY_ast,AWAY_stl,AWAY_blk,AWAY_to,AWAY_pf,AWAY_dreb,AWAY_oreb,AWAY_pct,AWAY_pct_2,AWAY_pct_3,AWAY_eff,AWAY_deff".split(",")
target = 'HOME_TEAM_WINS'

# Create a StandardScaler
scaler = StandardScaler()

# Fit the scaler on the entire dataset
X_scaled = scaler.fit_transform(df[features])

# Create a Linear Support Vector Classifier (LinearSVC)
model_svc = LinearSVC(random_state=42, dual=False)

# Fit the model on the entire dataset
model_svc.fit(X_scaled, df[target])

# Function to predict the outcome of a game between two teams
def predict_game(team1_stats, team2_stats):
    # Scale the input data using the same scaler
    team1_scaled = scaler.transform([team1_stats])
    team2_scaled = scaler.transform([team2_stats])

    # Predict the outcome for each team
    outcome_team1 = model_svc.predict(team1_scaled)[0]
    outcome_team2 = model_svc.predict(team2_scaled)[0]

    # Return the predicted outcomes
    return outcome_team1, outcome_team2

# User input for team names
team1_name = input("Enter the name of Team 1: ")
team2_name = input("Enter the name of Team 2: ")
    
# Fetch statistics for the specified teams
team1_stats = df[df['HOME_TEAM_ID'] == team1_name][features].values[0]
team2_stats = df[df['VISITOR_TEAM_ID'] == team2_name][features].values[0]

# Predict the outcome
outcome_team1, outcome_team2 = predict_game(team1_stats, team2_stats)

# Output the predictions
print(outcome_team1, outcome_team2)
# print(f"{team1_name} is {'likely to win' if outcome_team1 else 'not likely to win'}")
# print(f"{team2_name} is {'likely to win' if outcome_team2 else 'not likely to win'}")
