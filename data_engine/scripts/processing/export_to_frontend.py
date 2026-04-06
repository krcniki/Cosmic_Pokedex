import pandas as pd
import json
from pathlib import Path

def export_data():
    print("🚀 Exporting Pokedex to Frontend...")

    # Setup Paths
    ENGINE_DIR = Path(__file__).resolve().parent.parent.parent
    ROOT_DIR = ENGINE_DIR.parent
    
    INPUT_FILE = ENGINE_DIR / "data" / "processed" / "final_cosmic_pokedex.csv"
    # This points to your React project's assets folder
    OUTPUT_FILE = ROOT_DIR / "frontend" / "src" / "assets" / "pokedex.json"

    # Load Data
    if not INPUT_FILE.exists():
        print(f"❌ Error: {INPUT_FILE} not found!")
        return
        
    df = pd.read_csv(INPUT_FILE)

    # Clean up the JSON format
    data_list = df.to_dict(orient='records')
    for row in data_list:
        if isinstance(row['quiz_options'], str):
            row['quiz_options'] = json.loads(row['quiz_options'])

    # Save to Frontend
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, indent=2)

    print(f"✨ Success! {len(data_list)} planets exported to {OUTPUT_FILE}")

if __name__ == "__main__":
    export_data()