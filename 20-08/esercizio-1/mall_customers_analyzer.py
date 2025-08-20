import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances
import matplotlib.pyplot as plt
import numpy as np

def load_and_preprocess_data(filepath):
    """
    Carica il dataset e lo pre-elabora (rimuove i NaN, standardizza le feature).

    Parametri
    ---------
    filepath : str
        Percorso del file CSV.

    Restituisce
    -----------
    df : pandas.DataFrame
        DataFrame pulito.
    X : pandas.DataFrame
        DataFrame con le feature selezionate.
    X_scaled : np.ndarray
        Feature standardizzate.
    scaler : StandardScaler
        Oggetto scaler addestrato.
    """
    df = pd.read_csv(filepath)
    if df.isnull().values.any():
        df = df.dropna()
    X = df[['Annual Income (k$)', 'Spending Score (1-100)']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return df, X, X_scaled, scaler

def run_kmeans(X_scaled, n_clusters=8):
    """
    Esegue il clustering K-Means.

    Parametri
    ---------
    X_scaled : np.ndarray
        Feature standardizzate.
    n_clusters : int, opzionale
        Numero di cluster (default 8).

    Restituisce
    -----------
    kmeans : KMeans
        Oggetto KMeans addestrato.
    clusters : np.ndarray
        Etichette di cluster per ogni campione.
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    return kmeans, clusters

def plot_clusters(X, df, centroids_originali, n_clusters):
    """
    Visualizza i cluster e i centroidi.

    Parametri
    ---------
    X : pandas.DataFrame
        DataFrame delle feature.
    df : pandas.DataFrame
        DataFrame con le etichette di cluster.
    centroids_originali : np.ndarray
        Centroidi in scala originale.
    n_clusters : int
        Numero di cluster.
    """
    plt.figure(figsize=(8,6))
    for cluster in range(n_clusters):
        plt.scatter(
            X[df['Cluster'] == cluster]['Annual Income (k$)'],
            X[df['Cluster'] == cluster]['Spending Score (1-100)'],
            label=f'Cluster {cluster}'
        )
    plt.scatter(
        centroids_originali[:,0], centroids_originali[:,1],
        s=200, c='black', marker='X', label='Centroidi'
    )
    plt.xlabel('Annual Income (k$)')
    plt.ylabel('Spending Score (1-100)')
    plt.legend()
    plt.title('Clustering clienti (K-Means)')
    plt.show()

def find_high_value_clusters(centroids):
    """
    Identifica i cluster ad alto potenziale (score < income).

    Parametri
    ---------
    centroids : np.ndarray
        Centroidi dei cluster.

    Restituisce
    -----------
    high_value_clusters : list di int
        Indici dei cluster ad alto potenziale.
    """
    high_value_clusters = []
    for idx, (income, score) in enumerate(centroids):
        if score < income:
            high_value_clusters.append(idx)
    return high_value_clusters

def compute_cluster_distances(X_scaled, df, kmeans):
    """
    Calcola la distanza media dei punti dal proprio centroide di cluster.

    Parametri
    ---------
    X_scaled : np.ndarray
        Feature standardizzate.
    df : pandas.DataFrame
        DataFrame con le etichette di cluster.
    kmeans : KMeans
        Oggetto KMeans addestrato.

    Restituisce
    -----------
    distanze : np.ndarray
        Distanze medie per ogni cluster.
    """
    distanze=[]
    for cluster in range(kmeans.n_clusters):
        points = X_scaled[df['Cluster'] == cluster]
        dists = euclidean_distances(points, kmeans.cluster_centers_[cluster].reshape(1, -1))
        distanza_media = np.mean(dists)
        distanze.append(distanza_media)
    distanze = np.array(distanze).round(5)
    return distanze

def plot_high_value_clusters(X, df, centroids_originali, high_value_clusters, n_clusters):
    """
    Visualizza i cluster, i centroidi e evidenzia i centroidi ad alto potenziale.

    Parametri
    ---------
    X : pandas.DataFrame
        DataFrame delle feature.
    df : pandas.DataFrame
        DataFrame con le etichette di cluster.
    centroids_originali : np.ndarray
        Centroidi in scala originale.
    high_value_clusters : list di int
        Indici dei cluster ad alto potenziale.
    n_clusters : int
        Numero di cluster.
    """
    plt.figure(figsize=(8,6))
    for cluster in range(n_clusters):
        plt.scatter(
            X[df['Cluster'] == cluster]['Annual Income (k$)'],
            X[df['Cluster'] == cluster]['Spending Score (1-100)'],
            label=f'Cluster {cluster}'
        )
    plt.scatter(
        centroids_originali[:,0], centroids_originali[:,1],
        s=200, c='black', marker='X', label='Centroidi'
    )
    plt.scatter(
        centroids_originali[high_value_clusters,0], centroids_originali[high_value_clusters,1],
        s=250, c='red', marker='X', label='Centroidi alto potenziale'
    )
    min_val = min(X['Annual Income (k$)'].min(), X['Spending Score (1-100)'].min())
    max_val = max(X['Annual Income (k$)'].max(), X['Spending Score (1-100)'].max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', label='y = x')
    plt.xlabel('Annual Income (k$)')
    plt.ylabel('Spending Score (1-100)')
    plt.legend()
    plt.title('Cluster clienti - Alto potenziale evidenziato')
    plt.show()

def main():
    """
    Funzione principale per eseguire la pipeline di analisi.
    """
    n_clusters = 8
    df, X, X_scaled, scaler = load_and_preprocess_data('dataset/Mall_Customers.csv')
    kmeans, clusters = run_kmeans(X_scaled, n_clusters)
    df['Cluster'] = clusters
    centroids_originali = scaler.inverse_transform(kmeans.cluster_centers_)
    plot_clusters(X, df, centroids_originali, n_clusters)
    high_value_clusters = find_high_value_clusters(kmeans.cluster_centers_)
    print(f"Cluster ad alto potenziale:{high_value_clusters}")
    distanze = compute_cluster_distances(X_scaled, df, kmeans)
    print("Distanze medie dai centroidi:")
    print(distanze)
    plot_high_value_clusters(X, df, centroids_originali, high_value_clusters, n_clusters)

if __name__ == "__main__":
    main()