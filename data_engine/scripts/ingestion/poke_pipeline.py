import requests
import pandas as pd
from pathlib import Path

def fetch_pokemon_data(limit=151):
    print(f"🐾 Catching data for the first {limit} Pokémon...")
    
    # 1. GPS Setup: Find the folders from inside scripts/ingestion/
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    RAW_DIR = ROOT_DIR / "data" / "raw"
    
    # Ensure the raw directory exists
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    poke_data = []

    for i in range(1, limit + 1):
        # Hit the individual endpoint for each Pokémon
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}")
        if response.status_code == 200:
            data = response.json()
            
            # Extracting the "Core Stats"
            stats = {
                "pokemon_id": data["id"],  # 🆔 Added for easier image loading later!
                "name": data["name"],
                "type": data["types"][0]["type"]["name"],
                "hp": data["stats"][0]["base_stat"],
                "attack": data["stats"][1]["base_stat"],
                "defense": data["stats"][2]["base_stat"],
                "special_attack": data["stats"][3]["base_stat"],
                "special_defense": data["stats"][4]["base_stat"],
                "speed": data["stats"][5]["base_stat"],
                "weight": data["weight"] / 10,  # kg
                "height": data["height"] / 10   # m
            }
            poke_data.append(stats)
            
            if i % 50 == 0:
                print(f"✅ Loaded {i} Pokémon...")

    # 2. Save to the 'raw' folder
    output_path = RAW_DIR / "raw_pokemon_data.csv"
    df = pd.DataFrame(poke_data)
    df.to_csv(output_path, index=False)
    
    print(f"💾 Pokémon dataset saved to {output_path}")
    return df

if __name__ == "__main__":
    fetch_pokemon_data()