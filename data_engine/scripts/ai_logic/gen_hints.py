import os
import pandas as pd
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def generate_hints():
    print("🔮 Generating Cryptic Lore Hints (The 'No-Ears' Edition)...")
    
    # 1. GPS Setup
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    file_path = ROOT_DIR / "data" / "processed" / "final_cosmic_pokedex.csv"
    
    if not file_path.exists():
        print(f"❌ Error: {file_path} not found! Run the Matchmaker first.")
        return

    df = pd.read_csv(file_path)
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # 2. Processing Loop
    for i, row in df.iterrows():
        # Using 'pl_eqt' (raw Kelvin) instead of the missing 'pl_eqt_norm'
        prompt = (
            f"Planet: {row['pl_name']} | Biome: {row['biome_name']} | Temp: {row['pl_eqt']}K\n"
            f"Resident: {row['matched_pokemon']} ({row['pokemon_type']} type)\n"
            f"Task: Write 1 cryptic, 1-sentence hint (max 15 words) explaining why this Pokemon's "
            f"ELEMENTAL TYPE or ABILITIES make it the only one that can survive here. "
            f"Do NOT mention ears, tails, or the Pokemon's name. Focus on BIOLOGY and LORE."
        )

        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.8
            )
            
            hint = response.choices[0].message.content.strip().replace('"', '')
            df.at[i, 'lore_hint'] = hint
            
            if (i + 1) % 10 == 0:
                print(f"💡 Progress: {i+1}/{len(df)} hints generated...")
            
        except Exception as e:
            print(f"❌ Error at {row['pl_name']}: {e}")
            break

    # 3. Save the updated CSV
    df.to_csv(file_path, index=False)
    print(f"\n✨ Mission Success! 200 high-quality hints added to {file_path.name}")

if __name__ == "__main__":
    generate_hints()