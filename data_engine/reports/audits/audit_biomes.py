import pandas as pd
from pathlib import Path

def check_biomes():
    print("🔬 --- BIOME SCIENTIFIC AUDIT --- 🔬\n")

    # 1. GPS Setup: Navigate from reports/audits/ up to the project root
    # .parent is audits/, .parent.parent is reports/, .parent.parent.parent is data_engine/
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    PROCESSED_DIR = ROOT_DIR / "data" / "processed"
    
    input_path = PROCESSED_DIR / "clustered_planets.csv"

    # 2. Load your clustered data
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"❌ Error: {input_path} not found! Did you run the clustering script?")
        return

    # 3. Group by biome_id and calculate the 'Physics Profile'
    stats = df.groupby('biome_id').agg({
        'pl_dens': ['mean', 'min', 'max'],
        'pl_eqt': ['mean', 'min', 'max'],
        'pl_rade': ['mean', 'count'] 
    }).round(2)

    print(stats)

    print("\n📝 --- INTERPRETATION GUIDE ---")
    print("1. High Temp (>1000K) = INFERNO (Fire/Dragon)")
    print("2. Low Density (<2.0) + High Radius (>4.0) = ATMOSPHERIC (Flying/Ghost)")
    print("3. Mid Density (~5.5) + Mid Temp (250K-400K) = TEMPERATE (Grass/Water/Bug)")
    print("4. High Density (>8.0) = IRON CORE (Steel/Fighting)")

    # 4. Optional: See the 'Poster Child' for each biome
    print("\n🌟 --- REPRESENTATIVE PLANETS ---")
    for b_id in sorted(df['biome_id'].unique()):
        sample = df[df['biome_id'] == b_id].iloc[0]
        print(f"Biome {b_id}: e.g., {sample['pl_name']} (Temp: {sample['pl_eqt']}K, Dens: {sample['pl_dens']})")

if __name__ == "__main__":
    check_biomes()