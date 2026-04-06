import pandas as pd
from pathlib import Path
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

def run_clustering(n_clusters=5):
    print("⚖️ Applying Feature Weighting to separate Rock from Gas...")

    # 1. GPS Setup: Find the folders from inside scripts/processing/
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    PROCESSED_DIR = ROOT_DIR / "data" / "processed"
    PLOT_DIR = ROOT_DIR / "reports" / "plots"

    # 2. Load the cleaned data
    input_path = PROCESSED_DIR / "clean_planets.csv"
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"❌ Error: Could not find {input_path}. Did you run the cleaner first?")
        return

    # 3. Feature Selection & Weighting 🚀
    features = ['pl_rade', 'pl_dens', 'pl_eqt']
    X = df[features].copy()

    # Weighting: Density (x3), Radius (x2), Temperature (x1)
    X['pl_dens'] = X['pl_dens'] * 3.0
    X['pl_rade'] = X['pl_rade'] * 2.0

    # 4. Cluster on the Weighted Data
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42, n_init=20)
    df['biome_id'] = kmeans.fit_predict(X)

    # 5. Save the clustered data
    output_path = PROCESSED_DIR / "clustered_planets.csv"
    df.to_csv(output_path, index=False)
    print(f"💾 Clustered data saved to {output_path}")
    
    # 6. Visualization
    # Ensure the plots directory exists
    PLOT_DIR.mkdir(parents=True, exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='pl_eqt', y='pl_dens', hue='biome_id', palette='bright', s=80)
    plt.title("Weighted Biome Clusters (Separated by Density)")
    
    plot_path = PLOT_DIR / "biome_clusters.png"
    plt.savefig(plot_path)
    plt.close() # Good practice to close the plot to save memory
    print(f"🖼️ Weighted cluster map saved to {plot_path}")

if __name__ == "__main__":
    run_clustering()