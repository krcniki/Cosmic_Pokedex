import pandas as pd
from sklearn.preprocessing import PowerTransformer, MinMaxScaler

def clean_data():
    print("🧹 Starting Balanced Normalization...")
    
    # 1. Load the raw datasets
    planets = pd.read_csv("raw_exoplanet_data.csv")
    pokemon = pd.read_csv("raw_pokemon_data.csv")

    # 2. Handle Missing Values
    planets = planets.fillna(planets.median(numeric_only=True))
    
    # 3. Power Transformation 🚀
    # This is the "Goldilocks" scaler—it spreads out the crushed Earths 
    # without making them look randomized.
    pt = PowerTransformer(method='yeo-johnson')
    
    p_cols = ['pl_rade', 'pl_bmasse', 'pl_dens', 'pl_eqt', 'st_teff']
    pk_cols = [
    'height', 'weight', 'hp', 'attack', 'defense', 
    'special_attack', 'special_defense', 'speed'
    ]   
    
    # Transform and then use MinMaxScaler to ensure 0-1 range
    scaler = MinMaxScaler()
    
    planets[p_cols] = pt.fit_transform(planets[p_cols])
    planets[p_cols] = scaler.fit_transform(planets[p_cols])
    
    pokemon[pk_cols] = pt.fit_transform(pokemon[pk_cols])
    pokemon[pk_cols] = scaler.fit_transform(pokemon[pk_cols])

    # 4. Save
    planets.to_csv("clean_planets.csv", index=False)
    pokemon.to_csv("clean_pokemon.csv", index=False)
    
    print("✨ Success! Balanced Power Transformation complete.")

if __name__ == "__main__":
    clean_data()