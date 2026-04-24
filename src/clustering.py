# PREET SONAR 
# PRN : 20240802258

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

def load_data():
    df = pd.read_csv(INPUT_PATH)
    print(f"Dataset shape: {df.shape}")  # Shows (rows, columns)
    print(f"First few rows:\n{df.head()}")
    print(f"Data types:\n{df.dtypes}")
    return df

INPUT_PATH = "C:/Users/LENOVO/OneDrive/Desktop/DMW project/data/processed/features.csv"
OUTPUT_PATH = "C:/Users/LENOVO/OneDrive/Desktop/DMW project/data/processed/clusters.csv"


def load_data():
    return pd.read_csv(INPUT_PATH)


def select_features(df):
    # Drop non-numeric identifier before clustering
    X = df.drop(columns=['User_ID'])
    return X


def scale_data(X):
    # KMeans is distance-based — scaling is required
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled


def find_k(X_scaled):
    # Elbow method to find optimal K
    inertia = []
    for k in range(1, 10):
        km = KMeans(n_clusters=k, random_state=42)
        km.fit(X_scaled)
        inertia.append(km.inertia_)

    plt.plot(range(1, 10), inertia, marker='o')  # 'o' not '0'
    plt.title("Elbow Method")
    plt.xlabel("K")
    plt.ylabel("Inertia")
    plt.show()


def apply_kmeans(X_scaled, k=3):
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    return labels


def attach_cluster(df, labels):
    df['cluster'] = labels
    return df


def save_data(df):
    df.to_csv(OUTPUT_PATH, index=False)


def calculate_basic_metrics(X_scaled, labels, df):
    """
    Calculate basic clustering metrics to evaluate quality
    """
    print("\n" + "="*50)
    print(" BASIC CLUSTERING METRICS")
    print("="*50)
    
    # Silhouette Score: Measures how similar an object is to its own cluster compared to other clusters
    # Range: -1 to 1, where 1 is perfect clustering
    silhouette_avg = silhouette_score(X_scaled, labels)
    print(f"Silhouette Score: {silhouette_avg:.3f}")
    
    if silhouette_avg > 0.5:
        print(" Good cluster separation")
    elif silhouette_avg > 0.25:
        print(" Moderate cluster separation")
    else:
        print(" Poor cluster separation")
    
    # Cluster sizes - show how many users in each cluster
    print(f"\n Cluster Sizes:")
    unique_labels, counts = np.unique(labels, return_counts=True)
    for label, count in zip(unique_labels, counts):
        print(f"Cluster {label}: {count} users")
    
    # Show average spending per cluster
    print(f"\n Average Spending by Cluster:")
    df_with_clusters = df.copy()
    df_with_clusters['cluster'] = labels
    
    for cluster_id in sorted(unique_labels):
        cluster_data = df_with_clusters[df_with_clusters['cluster'] == cluster_id]
        avg_spend = cluster_data['total_spend'].mean()
        print(f"Cluster {cluster_id}: {avg_spend:.2f}")
    
    return silhouette_avg


def main():
    """
    Main clustering function with basic metrics
    """
    # Load and prepare data
    df = load_data()
    X = select_features(df)
    X_scaled = scale_data(X)

    # Apply K-Means clustering with k=3
    print(f"\n Applying K-Means with K=3...")
    labels = apply_kmeans(X_scaled, k=3)
    
    # Calculate and display basic metrics
    calculate_basic_metrics(X_scaled, labels, df)
    
    # Attach clusters and save results
    df = attach_cluster(df, labels)
    save_data(df)
    
    print(f"\n Clustering complete! Results saved to: {OUTPUT_PATH}")
    print(" Check the clusters.csv file for user cluster assignments")


if __name__ == "__main__":
    main()