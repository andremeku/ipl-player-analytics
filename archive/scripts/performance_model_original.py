# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
try:
    import openpyxl
except ImportError as e:
    raise ImportError(
        "Missing optional dependency 'openpyxl'. Install it using 'pip install openpyxl'."
    ) from e
# Load datasets
deliveries = pd.read_csv('/Users/yaocong/Desktop/Python_Project/Project_of_Cricket_Player/deliveries.csv')
matches = pd.read_csv('/Users/yaocong/Desktop/Python_Project/Project_of_Cricket_Player/matches.csv')
most_runs_average_strikerate = pd.read_csv('/Users/yaocong/Desktop/Python_Project/Project_of_Cricket_Player/most_runs_average_strikerate.csv')
players = pd.read_excel('/Users/yaocong/Desktop/Python_Project/Project_of_Cricket_Player/Players.xlsx')
teams = pd.read_csv('/Users/yaocong/Desktop/Python_Project/Project_of_Cricket_Player/teams.csv')
teamwise_home_and_away = pd.read_csv('/Users/yaocong/Desktop/Python_Project/Project_of_Cricket_Player/teamwise_home_and_away.csv')

# Data Cleaning
deliveries.dropna(axis=0, inplace=True)
matches.dropna(axis=0, inplace=True)
most_runs_average_strikerate.dropna(axis=0, inplace=True)
players.dropna(axis=0, inplace=True)
teams.dropna(axis=0, inplace=True)
teamwise_home_and_away.dropna(axis=0, inplace=True)

# Add season information to deliveries dataset
deliveries['year'] = deliveries['match_id'].map(matches.set_index('id')['Season'])

# --- Goal 1: Player's Trends and Patterns ---
# Extract yearly runs for all players
player_yearly_data = deliveries.groupby(['batsman', 'year']).agg({'batsman_runs': 'sum'}).reset_index()

# Select top 5 batsmen by total runs for visualization
top_players = player_yearly_data.groupby('batsman')['batsman_runs'].sum().nlargest(5).index
top_players_data = player_yearly_data[player_yearly_data['batsman'].isin(top_players)]

# Pivot for visualization
trend_data = top_players_data.pivot(index='year', columns='batsman', values='batsman_runs').fillna(0)

# Visualization: Each player's yearly trends
plt.figure(figsize=(12, 6))
trend_data.plot(kind='line', marker='o', figsize=(12, 6))
plt.title("Player's Trends and Patterns (Top 5 Batsmen)", fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Total Runs", fontsize=14)
plt.legend(title="Player", fontsize=12)
plt.grid(True)
plt.show()

# --- Goal 2: Player Performance Prediction ---
# Prepare data for performance prediction
player_performance_data = deliveries.groupby('batsman').agg({
    'batsman_runs': 'sum',
    'ball': 'count',
    'match_id': 'nunique'
}).reset_index()
player_performance_data.rename(columns={
    'batsman_runs': 'total_runs', 
    'ball': 'balls_faced', 
    'match_id': 'matches_played'
}, inplace=True)

# Add calculated feature: strike rate
player_performance_data['strike_rate'] = (player_performance_data['total_runs'] / player_performance_data['balls_faced']) * 100

# Model data
X = player_performance_data[['balls_faced', 'matches_played', 'strike_rate']]
y = player_performance_data['total_runs']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest Regressor model
model = RandomForestRegressor(random_state=42, n_estimators=100)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Visualize actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.7, color='blue')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], '--r', linewidth=2)
plt.title("Player Performance Prediction: Actual vs Predicted", fontsize=16)
plt.xlabel("Actual Total Runs", fontsize=14)
plt.ylabel("Predicted Total Runs", fontsize=14)
plt.grid(True)
plt.show()

# Display feature importance
feature_importance = model.feature_importances_
features = X.columns
plt.figure(figsize=(8, 5))
plt.bar(features, feature_importance, color='skyblue')
plt.title("Feature Importance in Player Performance Prediction", fontsize=16)
plt.xlabel("Features", fontsize=14)
plt.ylabel("Importance", fontsize=14)
plt.grid(axis='y')
plt.show()