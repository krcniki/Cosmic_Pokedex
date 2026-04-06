import pandas as pd
import numpy as np
from pathlib import Path
import random
import json

def run_matchmaker():
    print("🧠 Initiating Pokémon-to-Planet Matchmaker (Full Preview Mode)...")

    # 1. GPS Setup: Find folders from inside scripts/ai_logic/
    script_dir = Path(__file__).resolve().parent
    root_dir = script_dir.parent.parent
    processed_dir = root_dir / "data" / "processed"

    # 2. Load Data
    try:
        planets = pd.read_csv(processed_dir / "planets_with_logs.csv")
        pokemon = pd.read_csv(processed_dir / "clean_pokemon.csv")
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find data files. {e}")
        return

    # 3. Biome & Type Definitions
    biome_info = {
        0: {"name": "Iron Core", "types": ['steel', 'fighting', 'rock']},
        1: {"name": "Super-Hot Giant", "types": ['fire', 'dragon']},
        2: {"name": "Gas Giant", "types": ['flying', 'ghost', 'poison', 'psychic']},
        3: {"name": "Temperate Rocky", "types": ['water', 'grass', 'bug', 'normal', 'fairy']},
        4: {"name": "Arid Crust", "types": ['ground', 'rock', 'electric']}
    }

    final_data = []

    print(f"🎯 Building quiz-ready dataset for {len(planets)} planets...")

    for _, planet in planets.iterrows():
        # Get info for this specific biome
        info = biome_info.get(planet['biome_id'], {"name": "Unknown", "types": ['normal']})
        biome_name = info["name"]
        allowed_types = info["types"]

        # --- A. FIND THE WINNER (CORRECT ANSWER) ---
        candidates = pokemon[pokemon['type'].isin(allowed_types)].copy()
        
        # Euclidean Math (Density -> Weight | Temp -> Sp.Atk)
        candidates['match_score'] = np.sqrt(
            (candidates['weight'] - planet['pl_dens'])**2 + 
            (candidates['special_attack'] - planet['pl_eqt'])**2
        )
        candidates = candidates.sort_values('match_score')
        
        # Select winner from Top 5 for variety
        winner = candidates.head(5).sample(n=1).iloc[0]

        # --- B. FIND DISTRACTORS (WRONG ANSWERS) ---
        # 3 Distractors from the SAME biome
        internal_distractors = candidates[candidates['pokemon_id'] != winner['pokemon_id']].sample(n=3)
        
        # 1 Curveball from a DIFFERENT biome
        other_ids = [b for b in biome_info.keys() if b != planet['biome_id']]
        curveball_biome = biome_info[random.choice(other_ids)]
        curveball = pokemon[pokemon['type'].isin(curveball_biome["types"])].sample(n=1).iloc[0]

        # --- C. ASSEMBLE & SHUFFLE QUIZ PACK ---
        quiz_options = [
            {"id": int(winner['pokemon_id']), "name": winner['name'], "isCorrect": True, "type": winner['type']},
            {"id": int(internal_distractors.iloc[0]['pokemon_id']), "name": internal_distractors.iloc[0]['name'], "isCorrect": False, "type": internal_distractors.iloc[0]['type']},
            {"id": int(internal_distractors.iloc[1]['pokemon_id']), "name": internal_distractors.iloc[1]['name'], "isCorrect": False, "type": internal_distractors.iloc[1]['type']},
            {"id": int(internal_distractors.iloc[2]['pokemon_id']), "name": internal_distractors.iloc[2]['name'], "isCorrect": False, "type": internal_distractors.iloc[2]['type']},
            {"id": int(curveball['pokemon_id']), "name": curveball['name'], "isCorrect": False, "type": curveball['type']}
        ]
        random.shuffle(quiz_options)

        # --- D. SAVE THE FINAL ENTRY ---
        planet_entry = planet.to_dict()
        planet_entry.update({
            'biome_name': biome_name,
            'matched_pokemon': winner['name'],
            'pokemon_id': int(winner['pokemon_id']),
            'pokemon_type': winner['type'],
            'quiz_options': json.dumps(quiz_options), # Stored as string for CSV
            'match_confidence': round(1 - winner['match_score'], 3)
        })
        final_data.append(planet_entry)

    # 4. Save Final CSV
    final_df = pd.DataFrame(final_data)
    output_path = processed_dir / "final_cosmic_pokedex.csv"
    final_df.to_csv(output_path, index=False)

    print(f"✨ Mission Complete! Final Pokedex secured at {output_path}")

    # 5. DETAILED VIBE CHECK (The "Visible" Options)
    print("\n🔭 --- SCIENTIFIC QUIZ PREVIEW ---")
    samples = final_df.sample(2)
    
    for _, sample in samples.iterrows():
        # Unpack the JSON string back into a list to print it
        options = json.loads(sample['quiz_options'])
        
        print(f"🌍 Planet: {sample['pl_name']}")
        print(f"🏞️  Biome:  {sample['biome_name']} (Targets: {sample['pokemon_type'].upper()})")
        print(f"📝 Quiz Options:")
        
        for i, opt in enumerate(options):
            marker = "✅" if opt['isCorrect'] else "❌"
            print(f"   {i+1}. {marker} {opt['name'].upper()} ({opt['type']})")
            
        print(f"📜 Fact: {sample['discovery_log'][:75]}...")
        print("-" * 50)

if __name__ == "__main__":
    run_matchmaker()