import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

files = ['data/2017-18.csv']
data = pd.concat([pd.read_csv(file) for file in files])

# feature engineering
data['Avg_FPTS'] = data.groupby('Player')['FPTS'].transform('mean')

data_encoded = pd.get_dummies(data, columns=['Date', 'Team', 'Against'])

# Define Features and Target
X = data_encoded.drop(columns=['FPTS'])  # Keep 'Player' in X for identification
y = data_encoded['FPTS']

# Train-Test Split
# Keep 'Player' in X_train and X_test for identification
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Selection (Random Forest as an example)
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Model Training
# Drop 'Player' for training as it's not a feature
model.fit(X_train.drop(columns=['Player']), y_train)

# Model Evaluation
# Drop 'Player' for prediction as it's not a feature
predictions = model.predict(X_test.drop(columns=['Player']))
X_test['Predicted_FPTS'] = predictions  # Add predictions to X_test

# Calculate Mean Squared Error
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')

# Output to a .txt file
output_filepath = 'predictions_output.txt'
with open(output_filepath, 'w') as file:
    file.write(f'Mean Squared Error: {mse}\n')
    file.write('Player Predictions:\n')
    for index, row in X_test[['Player', 'Predicted_FPTS']].iterrows():
        file.write(f"{row['Player']}: {row['Predicted_FPTS']}\n")

print(f"Output written to {output_filepath}")

plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_test, y=predictions)
plt.xlabel('Actual FPTS')
plt.ylabel('Predicted FPTS')
plt.title('Actual vs Predicted FPTS')
plt.show()