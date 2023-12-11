import os
import pandas as pd

# Specify the directory containing the CSV files
directory_path = "data"

# Get a list of all files in the directory
csv_files = [file for file in os.listdir(directory_path) if file.endswith(".csv")]

# Loop through each CSV file
for csv_file in csv_files:
    file_path = os.path.join(directory_path, csv_file)

    df = pd.read_csv(file_path)

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

    # Print a message indicating the completion of processing for each file
    print(f"Null rows in 'pts' column removed from {csv_file}")
