import os
import pandas as pd

directory_path = "data"

csv_files = [file for file in os.listdir(directory_path) if file.endswith(".csv")]

for csv_file in csv_files:
    file_path = os.path.join(directory_path, csv_file)

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    if "GameLink" in df.columns:
        df = df.drop("GameLink", axis=1)

    # Replace NaN values with 0.0
    df = df.fillna(0.0)

    # Remove rows where the "PTS" column is null
    df = df.dropna(subset=["PTS"])

    column_weights = {
        "PTS": 1.0,
        "TRB": 1.2,
        "AST": 1.5,
        "STL": 3,
        "BLK": 3,
        "TOV": -1.0,
    }

    selected_columns = ["PTS", "TRB", "AST", "STL", "BLK", "TOV"]

    df["FPTS"] = df.apply(
        lambda row: sum(row[col] * column_weights[col] for col in selected_columns),
        axis=1,
    )
    df.to_csv(file_path, index=False)

    print(f"NaN values replaced with 0.0 in {csv_file}, null rows in 'PTS' column removed, and removed GameLink column.")