import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances
import matplotlib.pyplot as plt
import numpy as np

n_clusters=8

df = pd.read_csv('dataset/Mall_Customers.csv')

###PULISCI I DATI E STANDARDIZZA
# controlla nan
if df.isnull().values.any():
    df = df.dropna()

X = df[['Annual Income (k$)', 'Spending Score (1-100)']]

# standardizza
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


### K-Means
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

# Aggiungi il cluster ai dati
df['Cluster'] = clusters

centroids_originali = scaler.inverse_transform(kmeans.cluster_centers_)

###VISUALIZZA IL KMEAN

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
#print("Centroidi dei cluster:")
#print(kmeans.cluster_centers_)

### CLUSTER AD ALTO POTENZIALE

centroids = kmeans.cluster_centers_
high_value_clusters = []
for idx, (income, score) in enumerate(centroids):
    # Se il punteggio di spesa è maggiore del reddito il centroide è a sinistra della retta
    if score > income:
        high_value_clusters.append(idx)

print(f"Cluster ad alto potenziale:{high_value_clusters}")

distanze=[]
for cluster in range(kmeans.n_clusters):
    points = X_scaled[df['Cluster'] == cluster]
    dists = euclidean_distances(points, kmeans.cluster_centers_[cluster].reshape(1, -1))
    distanza_media = np.mean(dists)
    distanze.append(distanza_media)

distanze = np.array(distanze).round(5)

print("Distanze medie dai centroidi:")
print(distanze)