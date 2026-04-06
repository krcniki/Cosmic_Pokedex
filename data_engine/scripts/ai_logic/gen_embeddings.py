import os
import time
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from groq import Groq 

# find_dotenv() is smart—it will look upwards until it finds your .env file
load_dotenv(find_dotenv(), override=True)

def generate_logs():
    # 1. GPS Setup: Find the folders from inside scripts/ai_logic/
    script_dir = Path(__file__).resolve().parent
    data_engine_dir = script_dir.parent.parent
    processed_dir = data_engine_dir / "data" / "processed"
    
    # Define our input and output file paths
    input_file = processed_dir / "clustered_planets.csv"
    output_file = processed_dir / "planets_with_logs.csv"

    api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key)
    current_model = 'llama-3.1-8b-instant'
    
    try:
        # Load the clustered data from the 'processed' folder
        if not input_file.exists():
            print(f"❌ Error: {input_file} not found! Did you run the clustering script?")
            return
            
        df = pd.read_csv(input_file)
        
        # 🔄 CHECKPOINT LOGIC
        if output_file.exists():
            print(f"📂 Found existing progress. Loading {output_file}...")
            df_progress = pd.read_csv(output_file)
            mask = df_progress['discovery_log'].isna()
            indices_to_process = df_progress[mask].index
            df = df_progress 
        else:
            print("🆕 Starting fresh run...")
            df['discovery_log'] = None
            indices_to_process = df.index

    except Exception as e:
        print(f"❌ Error during file loading: {e}")
        return

    print(f"🚀 MISSION: Processing {len(indices_to_process)} remaining planets via Groq...")

    for i, index in enumerate(indices_to_process):
        row = df.loc[index]
        prompt = f"Exoplanet {row['pl_name']}: Write 1 short, extreme scientific fun fact for a high schooler. No intro."
        
        success = False
        for attempt in range(3):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=current_model,
                    temperature=0.7,
                    max_tokens=100
                )
                
                fact = chat_completion.choices[0].message.content.strip()
                df.at[index, 'discovery_log'] = fact
                print(f"✅ [{i+1}/{len(indices_to_process)}] Logged {row['pl_name']}")
                success = True
                break 
                
            except Exception as e:
                if "429" in str(e):
                    print(f"🛑 Groq Rate Limit. Cooling down 30s (Attempt {attempt+1})...")
                    time.sleep(30)
                else:
                    print(f"❌ Groq API Error: {e}")
                    break

        # 💾 SAVE PROGRESS EVERY 5 PLANETS
        if (i + 1) % 5 == 0:
            df.to_csv(output_file, index=False)
            print(f"💾 Checkpoint saved to {output_file}")

        # ⏳ Groq is fast; 2s is plenty
        if success:
            time.sleep(2) 

    # Final Save
    df.to_csv(output_file, index=False)
    print(f"\n✨ Mission Status: Final data secured in {output_file}!")

if __name__ == "__main__":
    generate_logs()