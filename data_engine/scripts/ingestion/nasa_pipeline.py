import pyvo as vo
import pandas as pd
from pathlib import Path

def extract_nasa_data():
    print("🚀 Initiating connection to NASA Exoplanet Archive API...")
    
    # 1. GPS Setup: Find the folders from inside scripts/ingestion/
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    RAW_DIR = ROOT_DIR / "data" / "raw"
    
    # Ensure the raw directory exists
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # 2. Connect to the NASA TAP Service
    service = vo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")

    # 3. Write the ADQL query
    query = """
        SELECT TOP 200
            pl_name, hostname, sy_snum, sy_pnum, sy_mnum,
            pl_orbper, pl_rade, pl_bmasse, pl_dens, pl_orbeccen,
            pl_insol, pl_eqt, st_teff, disc_year, sy_dist
        FROM
            pscomppars
        WHERE 
            pl_eqt IS NOT NULL 
            AND pl_dens IS NOT NULL
            AND pl_bmasse IS NOT NULL
    """

    print("📡 Executing query... fetching high-quality planetary data...")
    results = service.search(query)

    # 4. Convert to Pandas DataFrame
    df = results.to_table().to_pandas()

    # Clean up byte strings
    for col in df.select_dtypes([object]).columns:
        df[col] = df[col].apply(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)

    print(f"✅ Success! Extracted {len(df)} exoplanets.")
    
    # 5. Save to the 'raw' folder
    output_path = RAW_DIR / "raw_exoplanet_data.csv"
    df.to_csv(output_path, index=False)
    print(f"💾 Raw data cached locally at: {output_path}")
    
    return df

if __name__ == "__main__":
    raw_df = extract_nasa_data()
    print("\nData Preview (First 5 Rows):")
    print(raw_df.head())