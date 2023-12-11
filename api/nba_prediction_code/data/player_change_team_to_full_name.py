import json
import pandas as pd

with open('data.txt', 'r') as data_file:
    json_data = data_file.read()

data = json.loads(json_data)

team_dict = {item["abbreviation"]: item["teamName"] for item in data}
# print(team_dict)
df = pd.read_csv('nba-player-stats-2010-2020.csv')
df = df[df['tm'].isin(team_dict.keys())]
df['tm'] = df['tm'].map(team_dict)
df['year'] = df['year'].map(lambda x: x[:4])
# df = df.drop(['fgm_a', 'ftm_a'], axis=0)

df = df.dropna()
df.to_csv('nba_player_stats_replaced_team_and_year.csv', index=False)



