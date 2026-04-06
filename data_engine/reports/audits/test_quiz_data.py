import pandas as pd
import json
from pathlib import Path

def test_quiz_flow():
    # 1. GPS Setup
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    file_path = ROOT_DIR / "data" / "processed" / "final_cosmic_pokedex.csv"

    if not file_path.exists():
        print(f"❌ Error: {file_path} not found! Run the Matchmaker first.")
        return

    # 2. Load Data
    df = pd.read_csv(file_path)

    print(f"✅ Loaded {len(df)} planets. Running 3-Planet Audit...\n")

    # 3. Sample and Display
    samples = df.sample(3)

    for i, (_, row) in enumerate(samples.iterrows()):
        # Unpack JSON options
        options = json.loads(row['quiz_options'])
        
        print(f"--- TEST CASE #{i+1} ---")
        print(f"🌎 PLANET: {row['pl_name']}")
        print(f"🏞️  BIOME:  {row['biome_name']}")
        print(f"🔬 FACT:   {row['discovery_log']}")
        print(f"🔮 HINT:   {row['lore_hint']}")
        
        print("\n🎮 QUIZ OPTIONS:")
        for idx, opt in enumerate(options):
            status = "⭐" if opt['isCorrect'] else "  "
            print(f"   {idx+1}. {status} {opt['name'].upper()} ({opt['type']})")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    test_quiz_flow()