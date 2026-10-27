import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def load_players_data(file_path):
    #Loading and preprocess player data from the provided Excel file.
    players = pd.read_excel(file_path)
    # Calculating age based on DOB
    players['Age'] = players['DOB'].apply(lambda x: datetime.now().year - x.year if pd.notnull(x) else None)
    return players

def load_matches_data(file_path):
    #Loading match data from the provided CSV file.
    matches = pd.read_csv(file_path)
    return matches

def plot_nationality_distribution(players):
    #Plotting the distribution of players by nationality.
    nationality_counts = players['Country'].value_counts()
    plt.figure(figsize=(8, 5))
    sns.barplot(y=nationality_counts.index, x=nationality_counts.values,hue=nationality_counts.index, palette="viridis")
    plt.title("Player Nationality Distribution")
    plt.xlabel("Number of Players")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.show()

def plot_age_distribution(players):
    #Plotting the distribution of players by age."""
    plt.figure(figsize=(8, 5))
    sns.histplot(players['Age'].dropna(), bins=10, kde=True, color="skyblue")
    plt.title("Player Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Number of Players")
    plt.tight_layout()
    plt.show()

def plot_match_locations(matches):
    #Plotting the distribution of matches by city.
    city_counts = matches['city'].value_counts()
    plt.figure(figsize=(8, 5))
    sns.barplot(x=city_counts.values, y=city_counts.index, palette="pastel", hue=city_counts.index, dodge=False)
    plt.title("Match Locations (City-Wise)")
    plt.xlabel("Number of Matches")
    plt.ylabel("City")
    plt.tight_layout()
    plt.show()

# Providing the file paths
players_file_path = r"C:\Users\sahum\Downloads\IPL_Dataset\Players.xlsx"
matches_file_path = r"C:\Users\sahum\Downloads\IPL_Dataset\matches.csv"

# Loading the data
players = load_players_data(players_file_path)
matches = load_matches_data(matches_file_path)

# Performing analysis
plot_nationality_distribution(players)
plot_age_distribution(players)
plot_match_locations(matches)
