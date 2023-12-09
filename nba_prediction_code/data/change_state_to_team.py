import json
import pandas as pd

with open('data.txt', 'r') as data_file:
    json_data = data_file.read()

data = json.loads(json_data)

team_dict = {item["location"]: item["teamName"] for item in data}
df = pd.read_csv('NBA_Team_Stats.csv')
df['team'] = df['team'].map(team_dict)
df['year'] = df['year'].map(lambda x: x[:4])

df.to_csv('nba-team-stats-replaced-names.csv', index=False)

