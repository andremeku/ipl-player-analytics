import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Setting environment variable to avoid KMeans memory leak warning
os.environ["OMP_NUM_THREADS"] = "2"

# Step 1: Loading and reading Data
deliveries_file = r"C:\Users\sahum\Downloads\IPL_Dataset\deliveries.csv"
matches_file = r"C:\Users\sahum\Downloads\IPL_Dataset\matches.csv"
players_file = r"C:\Users\sahum\Downloads\IPL_Dataset\Players.xlsx"
most_runs_file = r"C:\Users\sahum\Downloads\IPL_Dataset\most_runs_average_strikerate.csv"
teams_file = r"C:\Users\sahum\Downloads\IPL_Dataset\teams.csv"
home_away_file = r"C:\Users\sahum\Downloads\IPL_Dataset\teamwise_home_and_away.csv"

deliveries_df = pd.read_csv(deliveries_file)
matches_df = pd.read_csv(matches_file)
players_df = pd.read_excel(players_file)
most_runs_df = pd.read_csv(most_runs_file)
teams_df = pd.read_csv(teams_file)
home_away_df = pd.read_csv(home_away_file)

# Step 2: Cleaning Column Names
players_df.columns = players_df.columns.str.strip()
most_runs_df.columns = most_runs_df.columns.str.strip()

# Step 3: Merging DataFrames based on player names
if 'Player_Name' in players_df.columns and 'batsman' in most_runs_df.columns:
    merged_df = pd.merge(players_df, most_runs_df, left_on='Player_Name', right_on='batsman', how='inner')
    print("DataFrames successfully merged based on player names.")
else:
    print("Merge cannot be performed. Required columns are missing.")
    merged_df = pd.DataFrame()

if not merged_df.empty:
    # Selecting relevant features for clustering
    features = ['total_runs', 'average', 'strikerate']
    data = merged_df[features].dropna()  #For dropping rows with missing values

    # Reset index of data to align clusters later
    data = data.reset_index(drop=True)

    # Standardizing the features
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    # Step 4: K-Means Clustering
    inertia = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(scaled_data)
        inertia.append(kmeans.inertia_)

    # Plotting the Elbow Curve
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), inertia, marker='o')
    plt.title('Elbow Method for Optimal Clusters')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.grid()
    plt.show()

    # Choosing optimal clusters (e.g., k=4)
    kmeans = KMeans(n_clusters=4, random_state=42)
    clusters = kmeans.fit_predict(scaled_data)

    # Create a new DataFrame for cluster results
    data_with_clusters = data.copy()
    data_with_clusters['cluster'] = clusters

    # Merge cluster labels back to the original merged_df
    merged_df = merged_df.merge(data_with_clusters[['cluster']], left_index=True, right_index=True, how='left')

    # Step 5: Visualization
    sns.pairplot(data_with_clusters, vars=features, hue='cluster', palette='Set2', diag_kind='kde', height=2.5)
    plt.suptitle('Clustering Players Based on Preferences', y=1.02)
    plt.show()

    # Cluster summary
    cluster_summary = merged_df.groupby('cluster')[features].mean()
    print("Cluster Summary:")
    print(cluster_summary)

    # For Saving the cluster data
    merged_df.to_csv(r"C:\Users\sahum\Downloads\IPL_Dataset\Players_with_clusters.csv", index=False)
    print("Player clustering completed. Results saved as 'Players_with_clusters.csv'.")
else:
    print("DataFrames could not be merged. Clustering not performed.")
