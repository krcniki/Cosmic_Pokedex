import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

def run_clustering(n_clusters=5):
    print("⚖️ Applying Feature Weighting to separate Rock from Gas...")
    df = pd.read_csv("clean_planets.csv")

    # 1. Feature Selection
    features = ['pl_rade', 'pl_dens', 'pl_eqt']
    X = df[features].copy()

    # 2. FEATURE WEIGHTING 🚀
    # We multiply Density by 3 to make it the dominant factor.
    # We multiply Radius by 2 because size also distinguishes Gas Giants.
    X['pl_dens'] = X['pl_dens'] * 3.0
    X['pl_rade'] = X['pl_rade'] * 2.0
    # Temperature stays at 1.0 (it's important, but not for "Type")

    # 3. Cluster on the Weighted Data
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42, n_init=20)
    df['biome_id'] = kmeans.fit_predict(X)

    # 4. Save
    df.to_csv("clustered_planets.csv", index=False)
    
    # 5. Visualization (Back to Temp vs Density to see the separation)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='pl_eqt', y='pl_dens', hue='biome_id', palette='bright', s=80)
    plt.title("Weighted Biome Clusters (Separated by Density)")
    plt.savefig("biome_clusters.png")
    print("🖼️ Weighted cluster map saved!")

if __name__ == "__main__":
    run_clustering()