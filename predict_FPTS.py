import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Load the historical data from the CSV file
file_path = "data/2018-19.csv"
df = pd.read_csv(file_path)

# Shift the FPTS values to represent past performance (e.g., using data from the previous game)
df['FPTS_shifted'] = df.groupby('Player')['FPTS'].shift(1)

# Drop the first row as it will have NaN values after shifting
df = df.dropna()

# Select features (X) and target variable (y)
features = ["PTS", "TRB", "AST", "STL", "BLK", "TOV"]
target = "FPTS_shifted"  # Use shifted FPTS as the target variable

# Create a dictionary to store models for each player
player_models = {}

# Iterate over unique players and train individual models
for player in df['Player'].unique():
    player_df = df[df['Player'] == player]

    # Check if there are enough samples for training
    if len(player_df) > 1:
        X = player_df[features]
        y = player_df[target]

        # Normalize features using Min-Max scaling
        scaler = MinMaxScaler()
        X_normalized = scaler.fit_transform(X)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.2, random_state=42)

        # Create a linear regression model
        model = LinearRegression()

        # Train the model
        model.fit(X_train, y_train)

        # Make predictions on the test set
        y_pred = model.predict(X_test)

        # Evaluate the model
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Store the model in the dictionary
        player_models[player] = {
            'model': model,
            'mse': mse,
            'r2': r2
        }

# Example: Retrieve the model for a specific player (replace 'PlayerName' with the actual player's name)
# specific_player_model = player_models['PlayerName']['model']

# Print or analyze the performance metrics for each player's model
for player, model_info in player_models.items():
    print(f"Player: {player}")
    print(f"Mean Squared Error: {model_info['mse']}")
    print(f"R-squared: {model_info['r2']}")
    print("------")

# You can also visualize the results for a specific player using a scatter plot
# For example, replace 'PlayerName' with the actual player's name
player_name = 'PlayerName'
player_df = df[df['Player'] == player_name]
X_player = player_df[features]
y_player = player_df[target]
X_player_normalized = scaler.transform(X_player)
y_player_pred = player_models[player_name]['model'].predict(X_player_normalized)

plt.scatter(y_player, y_player_pred, alpha=0.5)
plt.title(f'Actual vs. Predicted FPTS for {player_name} (Shifted)')
plt.xlabel('Actual FPTS (Shifted)')
plt.ylabel('Predicted FPTS (Shifted)')
plt.show()
