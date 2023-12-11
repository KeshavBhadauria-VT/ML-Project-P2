import pandas as pd


def read_csv_to_dict_with_pandas(df):

    # Initialize an empty dictionary
    data_dict = {}

    # Iterate over DataFrame rows
    for index, row in df.iterrows():
        # Use (year, team) as the key
        key = (row['year'], row['team'])

        row_dict = row.to_dict()

        row_dict.pop('year', None)
        row_dict.pop('team', None)
        # Convert the row to a dictionary and assign it to the key
        data_dict[key] = row_dict
        print(key)
        

    return data_dict
# Paths to your CSV files
game_data_file = 'games_filtered_from_2010_2019_id_replaced.csv'
season_averages_file = 'nba-team-stats-replaced-names.csv'

# Read the CSV files
game_df = pd.read_csv(game_data_file)
season_df = pd.read_csv(season_averages_file)

#We need the season stats to the in a dictionary with the key being
#a tuple with (year, name) = row
season_dictionary = read_csv_to_dict_with_pandas(season_df)



# Merge the dataframes
merged_df = pd.DataFrame()

for index, game in game_df.iterrows():
    season = str(game['SEASON'])
    home_team = game['HOME_TEAM_ID']
    away_team = game['VISITOR_TEAM_ID']


    #get information relating to home team
    if ((int(season), home_team) in season_dictionary and (int(season), away_team) in season_dictionary):
        home_team_data = {f'HOME_{key}': value for key, value in season_dictionary[(int(season), home_team)].items()}
        away_team_data = {f'AWAY_{key}': value for key, value in season_dictionary[(int(season), away_team)].items()}
        new_row = {**game, **home_team_data, **away_team_data}
        # merged_df.append(new_row, ignore_index=True)
        merged_df = pd.concat([merged_df, pd.DataFrame([new_row])], ignore_index=True)


merged_df.to_csv('merged_data.csv', index=False)
