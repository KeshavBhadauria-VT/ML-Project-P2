import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Load data from CSV file
df = pd.read_csv('data/merged_data.csv')  # Replace 'your_data.csv' with the actual file path

features = "HOME_no,HOME_g,HOME_min,HOME_pts,HOME_reb,HOME_ast,HOME_stl,HOME_blk,HOME_to,HOME_pf,HOME_dreb,HOME_oreb,HOME_pct,HOME_pct_2,HOME_pct_3,HOME_eff,HOME_deff,AWAY_no,AWAY_g,AWAY_min,AWAY_pts,AWAY_reb,AWAY_ast,AWAY_stl,AWAY_blk,AWAY_to,AWAY_pf,AWAY_dreb,AWAY_oreb,AWAY_pct,AWAY_pct_2,AWAY_pct_3,AWAY_eff,AWAY_deff".split(",")
target = 'HOME_TEAM_WINS'

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

# Create a k-Nearest Neighbors (KNN) classifier
k_value = 3  # Change the value of k as needed
model = KNeighborsClassifier(n_neighbors=k_value)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy}")

if len(features) == 2:
    plt.figure(figsize=(10, 6))
    plt.scatter(X_test[features[0]], X_test[features[1]], c=predictions, cmap='viridis', s=50)
    plt.title(f'Decision Boundaries (KNN with k={k_value})')
    plt.xlabel(features[0])
    plt.ylabel(features[1])
    plt.show()
