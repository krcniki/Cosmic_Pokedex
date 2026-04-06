import pandas as pd
from pathlib import Path
from sklearn.preprocessing import PowerTransformer, MinMaxScaler

def clean_data():
    print("🧹 Starting Balanced Normalization...")
    
    # 1. GPS Setup: Find the folders from inside scripts/processing/
    # .parent is scripts/, .parent.parent is data_engine/
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    RAW_DIR = ROOT_DIR / "data" / "raw"
    PROCESSED_DIR = ROOT_DIR / "data" / "processed"

    # 2. Load the raw datasets using the new paths
    try:
        planets = pd.read_csv(RAW_DIR / "raw_exoplanet_data.csv")
        pokemon = pd.read_csv(RAW_DIR / "raw_pokemon_data.csv")
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find the raw files! {e}")
        return

    # 3. Handle Missing Values
    planets = planets.fillna(planets.median(numeric_only=True))
    
    # 4. Power Transformation 🚀
    pt = PowerTransformer(method='yeo-johnson')
    scaler = MinMaxScaler()
    
    p_cols = ['pl_rade', 'pl_bmasse', 'pl_dens', 'pl_eqt', 'st_teff']
    pk_cols = [
        'height', 'weight', 'hp', 'attack', 'defense', 
        'special_attack', 'special_defense', 'speed'
    ]   
    
    # Transform and then ensure 0-1 range
    planets[p_cols] = pt.fit_transform(planets[p_cols])
    planets[p_cols] = scaler.fit_transform(planets[p_cols])
    
    pokemon[pk_cols] = pt.fit_transform(pokemon[pk_cols])
    pokemon[pk_cols] = scaler.fit_transform(pokemon[pk_cols])

    # 5. Save to the 'processed' folder
    # Ensure the directory exists just in case
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    planets.to_csv(PROCESSED_DIR / "clean_planets.csv", index=False)
    pokemon.to_csv(PROCESSED_DIR / "clean_pokemon.csv", index=False)
    
    print(f"✨ Success! Files saved to {PROCESSED_DIR}")

if __name__ == "__main__":
    clean_data()