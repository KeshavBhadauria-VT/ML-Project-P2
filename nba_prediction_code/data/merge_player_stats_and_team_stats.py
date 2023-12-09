import pandas as pd

def read_csv_to_dict_with_pandas(df):
    data_dict = {}

    for index, row in df.iterrows():
        key = (row['year'], row['team'])
        row_dict = row.to_dict()
        row_dict.pop('year', None)
        row_dict.pop('team', None)
        data_dict[key] = row_dict
        print(key) 

    return data_dict

player_stat_file = 'nba_player_stats_replaced_team_and_year.csv'
season_averages_file = 'nba-team-stats-replaced-names.csv'

player_stat_df = pd.read_csv(player_stat_file)
season_df = pd.read_csv(season_averages_file)

# we need the season stats to the in a dictionary with
# the key being a tuple with (year, name) = row
season_dictionary = read_csv_to_dict_with_pandas(season_df)

merged_df = pd.DataFrame()

for index, player in player_stat_df.iterrows():
    season = int(player['year'])
    team_name = str(player['tm'])

    # find it in the dictionary:
    if ((season, team_name) in season_dictionary):
        row_to_add = season_dictionary[(season, team_name)]
        new_row = {**player, **row_to_add}
        merged_df = pd.concat([merged_df, pd.DataFrame([new_row])], ignore_index=True)
        
merged_df.to_csv('merged_data_player_and_team.csv', index=False)
