import os
import time
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

load_dotenv(find_dotenv(), override=True)

def generate_logs():
    output_file = "planets_with_logs.csv"
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    # 🚀 Using LITE for maximum stability and separate quota
    current_model = 'models/gemini-2.0-flash-lite'
    
    try:
        # Load the original data
        df = pd.read_csv("clustered_planets.csv")
        
        # 🔄 CHECKPOINT LOGIC: 
        # If output file exists, load it so we don't repeat work
        if os.path.exists(output_file):
            print(f"📂 Found existing progress. Loading {output_file}...")
            df_progress = pd.read_csv(output_file)
            # Find rows where discovery_log is still empty/NaN
            mask = df_progress['discovery_log'].isna()
            indices_to_process = df_progress[mask].index
            df = df_progress # Work on the existing file
        else:
            print("🆕 Starting fresh run...")
            df['discovery_log'] = None
            indices_to_process = df.index

    except FileNotFoundError:
        print("❌ Error: clustered_planets.csv not found!")
        return

    print(f"🚀 MISSION: Processing {len(indices_to_process)} remaining planets...")

    for i, index in enumerate(indices_to_process):
        row = df.loc[index]
        
        # The Nano-Prompt for maximum token efficiency
        prompt = f"Exoplanet {row['pl_name']}: Write 1 short, extreme scientific fun fact for a high schooler. No intro."
        
        success = False
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=current_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.8,
                        max_output_tokens=60
                    )
                )
                
                df.at[index, 'discovery_log'] = response.text.strip()
                print(f"✅ [{i+1}/{len(indices_to_process)}] Logged {row['pl_name']}")
                success = True
                break 
                
            except APIError as e:
                if "429" in str(e):
                    # 🛑 Aggressive cooldown to flatten your dashboard traffic
                    print(f"🛑 Quota hit. Deep cooldown for 90s (Attempt {attempt+1})...")
                    time.sleep(90)
                else:
                    print(f"❌ API Error: {e}")
                    break

        # 💾 SAVE PROGRESS EVERY 5 PLANETS
        if (i + 1) % 5 == 0:
            df.to_csv(output_file, index=False)
            print(f"💾 Checkpoint saved: {output_file}")

        # ⏳ Cruising Speed: 20 seconds to ensure a flat line on your graph
        if success:
            time.sleep(20) 

    # Final Save
    df.to_csv(output_file, index=False)
    print(f"\n✨ Mission Status: Final data secured in {output_file}!")

if __name__ == "__main__":
    generate_logs()