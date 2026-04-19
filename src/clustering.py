import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

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


def main():
    df = load_data()
    X = select_features(df)
    X_scaled = scale_data(X)

    # find_k(X_scaled)  # Run once to visually pick K, then comment out

    labels = apply_kmeans(X_scaled, k=1)
    df = attach_cluster(df, labels)
    save_data(df)
    print("Clustering complete. Output saved.")


if __name__ == "__main__":
    main()