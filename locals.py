import pandas as pd
import os.path
import numpy as np
from pandas.io.parsers import read_csv
from scrape import *

# Function to get matches of specific team
def Get_Team_Matches():
    filename=''
    country=''

    while country.casefold() != 'N'.casefold():
        team=''
        country = input('\nEnter a country you want to get (Enter N to exit this function): ')
        if country.casefold() == 'N'.casefold():
            return
        country = country.capitalize()

        # Check if requested data exist locally
        if os.path.isfile(f'{country}/{country}_data.csv'):
            filename = f'{country}/{country}_data.csv'
            print(filename)
        else:
            print(f'\nERROR: Country {country} not found in local files.\n')
            continue

        while team.casefold() != 'N'.casefold():
            df = pd.read_csv(filename)
            team = input('\nEnter a team of the country you selected (Enter N to go back to country selection): ')
            if team.casefold() == 'N'.casefold():
                break
            team = team.capitalize()

            # Check if team inserted is only numbers
            if team.isdecimal(): 
                print(f'\nERROR: Inserted team cannot be a number')
                continue

            # Get rows that contain team
            df = df[df.apply(lambda row: row.astype(str).str.contains(f'{team.casefold()}', case=False).any(), axis=1)]

            if df.empty:
                print(f'\nERROR: Team {team} not found\n')
                continue

            # Sort dataframe by date
            df['date'] = pd.to_datetime(df['date'], dayfirst=True)
            df = df.sort_values(by=['date'])
            df['date'] = df['date'].dt.strftime('%d-%m-%Y')
            # Divide score into home score and away score
            score_split = df['score'].str.split(" - ", n = 1, expand = True)
            df['home_score'] = score_split[0]
            df['away_score'] = score_split[1]

            # Find results of selected team matches (won/lost/draw)
            df['result'] = np.where(((df['home'].str.casefold() == f'{team.casefold()}') & (df["home_score"] > df["away_score"])) |
            ((df['away'].str.casefold() == f'{team.casefold()}') & (df["home_score"] < df["away_score"])), 'Win', 
            np.where(df["home_score"] == '?', 'N/A', 
            np.where(df["home_score"] == df["away_score"], 'Draw',  'Loss')))
            
            df = df.drop(columns=['score'])
            df = df[['date','home', 'home_score', 'away_score', 'away', 'result']]

            df = df.drop_duplicates()

            if not os.path.exists(f'{country}/team_matches'):
                try: 
                    os.mkdir(f'{country}/team_matches')
                except OSError as error: 
                    print(error)

            df.to_csv(f'{country}/team_matches/{team}_matches.csv', index=False)    
            print(df)

#Function that shows the upcoming matches in a specific league (offline)
def Get_Upcoming_Matches():
    country = ''
    while country.casefold() != 'N'.casefold():
        country = input('Enter the country you want to retrieve the matches from (or enter N to exit function): ')
        if country.casefold() == 'N'.casefold():
            return
        country = country.capitalize()
        if os.path.isfile(f'{country}/{country}_data.csv'):
            df = read_csv(f'{country}/{country}_data.csv')
        else:
            print(f'\n{country} not found in dataset\n')
            continue
        
        print(f'\nSelected {country}\n')
        df['date'] = pd.to_datetime(df['date'], dayfirst=True)
        df = df.sort_values(by=['date'])
        df['date'] = df['date'].dt.strftime('%d-%m-%Y')
        #get matches that have ? as score
        df = df[df['score'].str[0].isin(['?'])]
        print(df[df['score'].str[0].isin(['?'])])

        team = ''
        while team.casefold() != 'N'.casefold():
            team = input("To show a secific team's upcoming matches, enter team name (or enter N to select another country):\n")
            if team.casefold() == 'N'.casefold():
                break
            team_df = df[df.apply(lambda row: row.astype(str).str.contains(f'{team.casefold()}', case=False).any(), axis=1)]
            if team_df.empty:
                print(f'\n{team.capitalize()} has no upcoming matches \n')
                continue
            
            print('\n')
            print(team_df)

#Function that displays team stats of a country (offline)
def Get_Team_Stats():
    country = ''
    while country.casefold() != 'N'.casefold():
        country = input('Enter the country you want to retrieve its team stats from (or enter N to exit function): ')
        if country.casefold() == 'N'.casefold():
            return

        if os.path.isfile(f'{country}/{country}_teams_stats.csv'):
            df = read_csv(f'{country}/{country}_teams_stats.csv')
            print(df)
            team = input("To only show a secific team's stats, enter team name (or enter N to go back):\n")
            while team.casefold() != 'N'.casefold():
                teamdf = df[df['team'].str.contains(f'{team}', case=False)]
                if teamdf.empty:
                    print(f'\n{team.capitalize()} is not found in the dataset. \n')
                else:
                    print(teamdf)

                team = input("Enter new team name (or enter N to go back):\n")
        else:
            print('\nCountry team stats not found in local dataset.')
            user_response = ''
            while (country.casefold() != 'N'.casefold()) or (country.casefold() != 'Y'.casefold()):
                user_response = input("Do you want to search for the country in the website? (Y/N):\n")
                if user_response.casefold() == 'Y'.casefold(): 
                    Update_Country_Team_Stats() #attempt to scrape data
                    break
                elif user_response.casefold() == 'N'.casefold():
                    break #ask about another country
                else:
                    print('Unidentified response. Please enter Y or N.')

        
    print('\nFunction finished.\n')


# Put local function names in list
funcs_offline = []
for key, value in list(locals().items()):
    if callable(value) and value.__module__ == __name__ and str(key):
        funcs_offline.append(key)

funcs_dict_offline = dict(enumerate(funcs_offline, start=len(funcs)))