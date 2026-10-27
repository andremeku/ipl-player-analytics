import pandas as pd
from datetime import datetime

#Loading datasets
players_data = pd.read_excel('Players.xlsx')  # Adjust path as needed
most_runs_data = pd.read_csv('most_runs_average_strikerate.csv')

#Calculating age from DOB
current_year = datetime.now().year
players_data['Age'] = players_data['DOB'].apply(lambda x: current_year - x.year if pd.notnull(x) else None)

#Summarizing  player demographics
print("Nationality Distribution:")
print(players_data['Country'].value_counts())

print("\nBatting Style Distribution:")
players_data['Batting_Hand'] = players_data['Batting_Hand'].str.replace('_hand', '_Hand').str.strip()  # Standardize
print(players_data['Batting_Hand'].value_counts())

print("\nBowling Skill Distribution:")
print(players_data['Bowling_Skill'].value_counts())

print("\nAge Summary:")
print(players_data['Age'].describe())


