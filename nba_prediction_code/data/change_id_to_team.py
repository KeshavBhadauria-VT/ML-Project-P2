import json
import pandas as pd

with open('data.txt', 'r') as data_file:
    json_data = data_file.read()

data = json.loads(json_data)

team_dict = {item["teamId"]: item["teamName"] for item in data}
df = pd.read_csv('games_filtered_for_2010_2020.csv')
df['HOME_TEAM_ID'] = df['HOME_TEAM_ID'].map(team_dict)
df['VISITOR_TEAM_ID'] = df['VISITOR_TEAM_ID'].map(team_dict)
df.to_csv('games_filtered_from_2010_2019_id_replaced.csv', index=False)



