import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
import matplotlib.patches as mpatches

# Function to load the dataset from a CSV file
# Input: path (str) - Path to the CSV file
# Output: DataFrame containing the loaded data
def load_data(path):
    df = pd.read_csv(path)
    return df

# Function to preprocess the data by selecting relevant columns and filling missing values
# Input: df (DataFrame) - Original data
# Output: DataFrame containing only relevant columns with missing values filled
def preprocess_data(df):
    relevant_columns = [
        'BALANCE',
        'PURCHASES',
        'CASH_ADVANCE',
        'PURCHASES_FREQUENCY'
    ]
    df = df[relevant_columns]
    df.fillna(df.median(), inplace=True)
    return df

# Function to normalize the data using StandardScaler
# Input: df (DataFrame) - Preprocessed data
# Output: NumPy array with normalized data
def normalize_data(df):
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(df)
    return data_scaled

# Function to find the optimal number of clusters for K-MEANS using Silhouette Score
# Input: data_scaled (array) - Normalized data, max_clusters (int) - Maximum number of clusters to test
# Output: Optimal number of clusters (int)
def find_optimal_k(data_scaled, max_clusters=10):
    silhouette_scores = []
    range_n_clusters = list(range(2, max_clusters + 1))

    for n_clusters in range_n_clusters:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(data_scaled)
        silhouette_avg = silhouette_score(data_scaled, cluster_labels)
        silhouette_scores.append(silhouette_avg)

    plt.plot(range_n_clusters, silhouette_scores, marker='o')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Score for K-MEANS')
    plt.savefig('silhouetteScore.png')
    plt.show()

    optimal_n_clusters = range_n_clusters[np.argmax(silhouette_scores)]
    print(f'Optimal number of clusters: {optimal_n_clusters}')
    return optimal_n_clusters

# Function to apply K-MEANS clustering to the data
# Input: data_scaled (array) - Normalized data, n_clusters (int) - Number of clusters to form
# Output: Labels (array) - Cluster labels for each data point
def apply_kmeans(data_scaled, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(data_scaled)
    return labels

# Function to find the optimal value of eps for DBSCAN using the Elbow Rule
# Input: data_scaled (array) - Normalized data
# Output: Optimal eps value (float)
def find_eps(data_scaled):
    neighbors = NearestNeighbors(n_neighbors=5)
    neighbors_fit = neighbors.fit(data_scaled)
    distances, indices = neighbors_fit.kneighbors(data_scaled)
    distances = np.sort(distances[:, 4], axis=0)

    plt.figure(figsize=(8, 6))
    plt.plot(distances)
    plt.xlabel('Samples')
    plt.ylabel('Distance to 5th Nearest Neighbor')
    plt.title('Elbow Plot for Determining Optimal Eps')
    plt.savefig('elbow.png')
    plt.show()

    elbow_index = int(len(distances) * 0.90)
    eps_value_percentil = distances[elbow_index]
    eps_value_median = np.median(distances)

    print(f'Optimal eps value from Elbow Method (90th percentile): {eps_value_percentil}')
    print(f'Optimal eps value from Median Distance: {eps_value_median}')

    return eps_value_percentil

# Function to apply DBSCAN clustering to the data
# Input: data_scaled (array) - Normalized data, eps_value (float) - Maximum distance between points for a cluster,
#        min_samples_value (int) - Minimum number of points to form a cluster
# Output: Labels (array) - Cluster labels for each data point (including noise as -1)
def apply_dbscan(data_scaled, eps_value, min_samples_value):
    dbscan = DBSCAN(eps=eps_value, min_samples=min_samples_value)
    labels = dbscan.fit_predict(data_scaled)
    return labels

# Function to visualize clustering results using PCA for dimensionality reduction
# Input: data_scaled (array) - Normalized data, labels (array) - Cluster labels for data points,
#        title (str) - Title for the plot, filename (str) - File name for saving the plot,
#        cluster_labels (dict) - Custom cluster labels, is_dbscan (bool) - Flag for DBSCAN-specific settings
# Output: Saves and shows a plot of the clusters
def visualize_clusters(data_scaled, labels, title, filename, cluster_labels=None, is_dbscan=False):
    pca = PCA(n_components=2)
    data_pca = pca.fit_transform(data_scaled)

    unique_labels = np.unique(labels)
    colors = plt.cm.get_cmap('viridis', len(unique_labels))

    legend_handles = []
    for label in unique_labels:
        if label == -1:
            cluster_color = 'gray'
            cluster_label = 'Noise' if cluster_labels is None else cluster_labels.get(label, 'Noise')
        else:
            cluster_color = colors(label)
            cluster_label = f'Cluster {label}' if cluster_labels is None else cluster_labels.get(label, f'Cluster {label}')

        plt.scatter(data_pca[labels == label, 0], data_pca[labels == label, 1], color=cluster_color, alpha=0.5, label=cluster_label)
        legend_handles.append(mpatches.Patch(color=cluster_color, label=cluster_label))

    plt.title(title)
    plt.legend(handles=legend_handles, loc='upper right', title="Clusters", fontsize=8)
    plt.savefig(filename)
    plt.show()

# Function to determine thresholds for categorizing types of users based on the dataset
# Input: df (DataFrame) - Original data
# Output: Dictionary containing threshold values for various user characteristics
def determine_thresholds(df):
    thresholds = {}
    thresholds['heavy_spenders_purchases'] = df['PURCHASES'].quantile(0.70)
    thresholds['heavy_spenders_frequency'] = 0.75
    thresholds['rich_savers_balance'] = df['BALANCE'].quantile(0.75)
    thresholds['cash_advance_users'] = df['CASH_ADVANCE'].quantile(0.80)
    thresholds['balanced_spenders_balance'] = df['BALANCE'].quantile(0.50)
    thresholds['balanced_spenders_purchases'] = df['PURCHASES'].quantile(0.50)

    print("Thresholds determined from the dataset:")
    for key, value in thresholds.items():
        print(f"{key}: {value}")

    return thresholds

# Function to characterize clusters and assign descriptive labels
# Input: df (DataFrame) - Data with cluster labels, cluster_column_name (str) - Name of the column with cluster labels
# Output: Dictionary containing cluster labels with descriptions
def characterize_clusters(df, cluster_column_name):
    thresholds = determine_thresholds(df)
    unique_clusters = df[cluster_column_name].unique()
    cluster_labels = {}
    label_counts = {}

    for cluster in unique_clusters:
        if cluster == -1:
            cluster_labels[cluster] = 'Noise'
            continue

        cluster_data = df[df[cluster_column_name] == cluster]
        cluster_description = cluster_data.describe()
        avg_balance = cluster_description.loc['mean']['BALANCE']
        avg_purchases = cluster_description.loc['mean']['PURCHASES']
        avg_cash_advance = cluster_description.loc['mean']['CASH_ADVANCE']
        avg_purchases_frequency = cluster_description.loc['mean']['PURCHASES_FREQUENCY']

        if (avg_purchases > thresholds['heavy_spenders_purchases'] and avg_purchases_frequency > thresholds['heavy_spenders_frequency']):
            label = 'Heavy Spenders'
        elif avg_cash_advance > thresholds['cash_advance_users']:
            label = 'Cash Advance Users'
        elif avg_purchases < thresholds['balanced_spenders_purchases'] and avg_balance > thresholds['rich_savers_balance']:
            label = 'Rich Savers'
        elif avg_purchases > thresholds['balanced_spenders_purchases'] and avg_balance > thresholds['balanced_spenders_balance']:
            label = 'Balanced Spenders & Savers'
        else:
            label = 'Average Users'

        if label not in label_counts:
            label_counts[label] = 1
        else:
            label_counts[label] += 1

        unique_label = f"{label} - {label_counts[label]}"
        cluster_labels[cluster] = unique_label

        print(f'\nCluster {cluster} ({unique_label}) characteristics:')
        print(cluster_description.to_string())

    return cluster_labels

# Main function to execute all steps of the analysis
# Input: None
# Output: Generates visualizations and outputs clustering analysis
def main():
    data_path = 'CC_GENERAL.csv'
    df = load_data(data_path)
    df = preprocess_data(df)
    data_scaled = normalize_data(df)

    optimal_n_clusters = find_optimal_k(data_scaled)
    kmeans_labels = apply_kmeans(data_scaled, optimal_n_clusters)
    df['KMeans_Cluster'] = kmeans_labels
    kmeans_cluster_labels = characterize_clusters(df, 'KMeans_Cluster')
    visualize_clusters(data_scaled, kmeans_labels, 'K-MEANS Clustering', 'kMeans.png', kmeans_cluster_labels)

    eps_value = find_eps(data_scaled)
    min_samples_value = 2 * data_scaled.shape[1]
    dbscan_labels = apply_dbscan(data_scaled, eps_value, min_samples_value)
    df['DBSCAN_Cluster'] = dbscan_labels
    dbscan_cluster_labels = characterize_clusters(df, 'DBSCAN_Cluster')
    visualize_clusters(data_scaled, dbscan_labels, f'DBSCAN Clustering (eps={eps_value}, min_samples={min_samples_value})', f'dbscan.png', dbscan_cluster_labels, is_dbscan=True)

if __name__ == "__main__":
    main()
