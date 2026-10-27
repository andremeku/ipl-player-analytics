import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

#Loading data sets
players_data = pd.read_excel('Players.xlsx')  # Adjust path as needed
most_runs_data = pd.read_csv('most_runs_average_strikerate.csv')  # Adjust path as needed

# next step as follows Calculating age from DOB
current_year = datetime.now().year
players_data['Age'] = players_data['DOB'].apply(lambda x: current_year - x.year if pd.notnull(x) else None)

# Merging player demographics with performance data
role_analysis_data = pd.merge(players_data, most_runs_data, left_on='Player_Name', right_on='batsman', how='left')

#Categorizing players into roles
def categorize_role(row):
    if pd.notnull(row['Bowling_Skill']) and pd.notnull(row['total_runs']):
        return 'All-Rounder'
    elif pd.notnull(row['Bowling_Skill']):
        return 'Bowler'
    elif pd.notnull(row['total_runs']):
        return 'Batsman'
    else:
        return 'Unknown'

role_analysis_data['Player_Role'] = role_analysis_data.apply(categorize_role, axis=1)

# Visualization 1: Role distribution
sns.countplot(y='Player_Role', data=role_analysis_data, order=role_analysis_data['Player_Role'].value_counts().index)
plt.title('Player Role Distribution')
plt.show()

# Visualization 2: Age distribution
sns.histplot(players_data['Age'].dropna(), kde=True, bins=10)
plt.title('Player Age Distribution')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()
