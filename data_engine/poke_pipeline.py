import requests
import pandas as pd

def fetch_pokemon_data(limit=151):
    print(f"🐾 Catching data for the first {limit} Pokémon...")
    poke_data = []

    for i in range(1, limit + 1):
        # Hit the individual endpoint for each Pokémon
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}")
        if response.status_code == 200:
            data = response.json()
            
            # Extracting the "Core Stats" that map well to planetary physics
            stats = {
                "name": data["name"],
                "type": data["types"][0]["type"]["name"],
                "hp": data["stats"][0]["base_stat"],
                "attack": data["stats"][1]["base_stat"],
                "defense": data["stats"][2]["base_stat"],
                "special_attack": data["stats"][3]["base_stat"],
                "special_defense": data["stats"][4]["base_stat"],
                "speed": data["stats"][5]["base_stat"],
                "weight": data["weight"] / 10,  # Convert hectograms to kg
                "height": data["height"] / 10   # Convert decimeters to meters
            }
            poke_data.append(stats)
            if i % 50 == 0:
                print(f"✅ Loaded {i} Pokémon...")

    df = pd.DataFrame(poke_data)
    df.to_csv("raw_pokemon_data.csv", index=False)
    print("💾 Pokémon dataset saved as 'raw_pokemon_data.csv'")
    return df

if __name__ == "__main__":
    fetch_pokemon_data()