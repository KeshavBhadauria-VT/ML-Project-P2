import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import shap

# Load data from CSV file
df = pd.read_csv('data/merged_data.csv')  # Replace 'your_data.csv' with the actual file path

features = "HOME_no,HOME_g,HOME_min,HOME_pts,HOME_reb,HOME_ast,HOME_stl,HOME_blk,HOME_to,HOME_pf,HOME_dreb,HOME_oreb,HOME_pct,HOME_pct_2,HOME_pct_3,HOME_eff,HOME_deff,AWAY_no,AWAY_g,AWAY_min,AWAY_pts,AWAY_reb,AWAY_ast,AWAY_stl,AWAY_blk,AWAY_to,AWAY_pf,AWAY_dreb,AWAY_oreb,AWAY_pct,AWAY_pct_2,AWAY_pct_3,AWAY_eff,AWAY_deff".split(",")
target = 'HOME_TEAM_WINS'

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

# Create a StandardScaler
scaler = StandardScaler()

# Fit the scaler on the training data and transform both training and test data
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create a Linear Support Vector Classifier (LinearSVC)
model_svc = LinearSVC(random_state=42, dual=False)

# Fit the model on the scaled training data
model_svc.fit(X_train_scaled, y_train)

# Make predictions on the scaled test data
predictions_svc = model_svc.predict(X_test_scaled)

# Evaluate the LinearSVC model's accuracy
accuracy_svc = accuracy_score(y_test, predictions_svc)
print(f"LinearSVC Accuracy: {accuracy_svc}")

# Visualize decision boundaries (example for two features)
# Uncomment the following lines if you have only two features for visualization
if len(features) == 2:
    plt.figure(figsize=(10, 6))
    plt.scatter(X_test_scaled[:, 0], X_test_scaled[:, 1], c=predictions_svc, cmap='viridis', s=50)
    plt.title('Decision Boundaries (LinearSVC with Scaling)')
    plt.xlabel(features[0])
    plt.ylabel(features[1])
    plt.show()

# Plot a heatmap of the correlation matrix
plt.figure(figsize=(12, 10))
sns.heatmap(df[features].corr(), cmap='coolwarm', linewidths=0.5, annot=False)
plt.title('Feature Correlation Heatmap')
plt.show()

# Get feature coefficients for LinearSVC
feature_coefficients = model_svc.coef_[0]

# Create a DataFrame to display feature coefficients
feature_coefficient_df = pd.DataFrame({'Feature': features, 'Coefficient': feature_coefficients})

# Sort the DataFrame by coefficient magnitude in descending order
feature_coefficient_df = feature_coefficient_df.reindex(feature_coefficient_df['Coefficient'].abs().sort_values(ascending=False).index)

# Plot feature coefficients
plt.figure(figsize=(10, 6))
plt.barh(feature_coefficient_df['Feature'], feature_coefficient_df['Coefficient'])
plt.xlabel('Coefficient Magnitude')
plt.title('LinearSVC Feature Coefficients')
plt.show()

# Initialize the SHAP explainer with the trained model and training data
explainer = shap.LinearExplainer(model_svc, X_train_scaled)

# Calculate SHAP values for the training data
shap_values = explainer.shap_values(X_train_scaled)


def predict_game_outcome(home_team_stats, away_team_stats):
    # Combine home and away stats
    game_stats = home_team_stats + away_team_stats
    
    # Convert to a DataFrame (reshape for a single sample)
    game_stats_df = pd.DataFrame([game_stats], columns=features)
    
    # Scale the stats
    game_stats_scaled = scaler.transform(game_stats_df)
    
    # Make prediction
    prediction = model_svc.predict(game_stats_scaled)
    
    # Get SHAP values for this specific prediction
    shap_values_for_prediction = explainer.shap_values(game_stats_scaled)

    # Print the SHAP values for the prediction (explaining the prediction)
    print("SHAP Values for this prediction:")
    shap.force_plot(explainer.expected_value, shap_values_for_prediction[0], game_stats_df.iloc[0], matplotlib=True)

    # Return the prediction
    return "Home Team Wins" if prediction[0] else "Away Team Wins"


# Example stats for a home and away team (fill in with actual stats)
# Example stats for a home team
home_team_stats = [
    1,  # HOME_no (e.g., Team Number)
    82, # HOME_g (games played)
    240,# HOME_min (minutes)
    110,# HOME_pts (points)
    45, # HOME_reb (rebounds)
    25, # HOME_ast (assists)
    7,  # HOME_stl (steals)
    5,  # HOME_blk (blocks)
    12, # HOME_to (turnovers)
    20, # HOME_pf (personal fouls)
    30, # HOME_dreb (defensive rebounds)
    15, # HOME_oreb (offensive rebounds)
    0.5,# HOME_pct (shooting percentage)
    0.5,# HOME_pct_2 (two-point shooting percentage)
    0.35,# HOME_pct_3 (three-point shooting percentage)
    1.2,# HOME_eff (efficiency rating)
    0.9 # HOME_deff (defensive efficiency)
]

# Example stats for an away team
away_team_stats = [
    2,  # AWAY_no
    82, # AWAY_g
    240,# AWAY_min
    105,# AWAY_pts
    50, # AWAY_reb
    30, # AWAY_ast
    8,  # AWAY_stl
    6,  # AWAY_blk
    14, # AWAY_to
    18, # AWAY_pf
    33, # AWAY_dreb
    17, # AWAY_oreb
    0.48,# AWAY_pct
    0.52,# AWAY_pct_2
    0.38,# AWAY_pct_3
    1.3,# AWAY_eff
    0.85 # AWAY_deff
]


# Predict the outcome
outcome = predict_game_outcome(home_team_stats, away_team_stats)
print(outcome)