import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import dash_bootstrap_components as dbc

# --- Data Loading and Preparation ---
# Load datasets
deliveries = pd.read_csv('/Users/yaocong/Desktop/Python_Project/Project_of_Cricket_Player/deliveries.csv')
matches = pd.read_csv('/Users/yaocong/Desktop/Python_Project/Project_of_Cricket_Player/matches.csv')
player_stats = pd.read_csv(
    '/Users/yaocong/Desktop/Python_Project/Project_of_Cricket_Player/most_runs_average_strikerate.csv')

# Data Cleaning
deliveries['Season'] = deliveries['match_id'].map(matches.set_index('id')['Season'])
player_season_stats = deliveries.groupby(['Season', 'batsman'])['batsman_runs'].sum().reset_index()

deliveries.dropna(axis=0, inplace=True)
matches.dropna(axis=0, inplace=True)
player_stats = player_stats.dropna(subset=['average', 'strikerate', 'total_runs'])

# Prepare features and target for the model
features = player_stats[['average', 'strikerate']]
target = player_stats['total_runs']


# Split data for training and testing
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train the Random Forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

# --- Dash Application Setup ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("IPL Player Statistics Dashboard", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Select Player:"),
            dcc.Dropdown(
                id='player-dropdown',
                options=[{'label': player, 'value': player} for player in player_season_stats['batsman'].unique()],
                value=player_season_stats['batsman'].unique()[0],
                style={'width': '100%'}
            )
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='player-summary', className="mt-4"),
            dcc.Graph(id='player-trend-graph')
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.H3("Player Performance Prediction", className="text-center mt-4"),
            html.Div(id='prediction-summary', className="text-center")
        ], width=12)
    ])
], fluid=True)


# --- Callback Functions ---
@app.callback(
    [Output('player-summary', 'children'),
     Output('player-trend-graph', 'figure'),
     Output('prediction-summary', 'children')],
    [Input('player-dropdown', 'value')]
)
def update_player_data(selected_player):
    # Filter player data
    player_data = player_season_stats[player_season_stats['batsman'] == selected_player]
    total_runs = player_data['batsman_runs'].sum()
    player_record = player_stats[player_stats['batsman'] == selected_player]

    # Handle missing data for prediction
    if not player_record.empty:
        average = player_record['average'].values[0]
        strike_rate = player_record['strikerate'].values[0]
    else:
        average, strike_rate = None, None

    # Player Summary
    summary = dbc.Card([
        dbc.CardBody([
            html.H4(f"Player: {selected_player}", className="card-title"),
            html.P(f"Total Runs: {total_runs}", className="card-text"),
            html.P(f"Average: {average:.2f}" if average else "Average: N/A", className="card-text"),
            html.P(f"Strike Rate: {strike_rate:.2f}" if strike_rate else "Strike Rate: N/A", className="card-text")
        ])
    ], color="light", inverse=False)

    # Trend Graph
    trend_figure = px.line(
        player_data,
        x='Season',
        y='batsman_runs',
        title=f'{selected_player} - Runs Trends Over Seasons',
        labels={'batsman_runs': 'Total Runs', 'Season': 'Season'}
    )

    # Prediction
    if average and strike_rate:
        prediction_input = pd.DataFrame([[average, strike_rate]], columns=['average', 'strikerate'])
        predicted_runs = model.predict(prediction_input)[0]
        prediction_text = f"Predicted Runs for Next Match: {predicted_runs:.2f}"
    else:
        prediction_text = "Insufficient Data for Prediction"

    prediction_summary = html.Div([
        html.P(prediction_text),
        html.P(f"Model Mean Squared Error: {mse:.2f}")
    ])

    return summary, trend_figure, prediction_summary


# --- Run the Application ---
if __name__ == '__main__':
    app.run_server(debug=True)