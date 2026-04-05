import pyvo as vo
import pandas as pd

def extract_nasa_data():
    print("🚀 Initiating connection to NASA Exoplanet Archive API...")
    
    # 1. Connect to the NASA TAP (Table Access Protocol) Service
    service = vo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")

    # 2. Write the ADQL (Astronomical Data Query Language) query
    # We filter for planets where essential ML stats are NOT NULL to ensure quality data.
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
    # 3. Execute the query
    results = service.search(query)

    # 4. Convert the raw astronomical data into a clean Pandas DataFrame
    df = results.to_table().to_pandas()

    # Clean up byte strings (NASA API sometimes returns text as b'text')
    for col in df.select_dtypes([object]).columns:
        df[col] = df[col].apply(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)

    print(f"✅ Success! Extracted {len(df)} exoplanets.")
    
    # 5. Save a local raw copy for caching
    csv_filename = "raw_exoplanet_data.csv"
    df.to_csv(csv_filename, index=False)
    print(f"💾 Raw data cached locally as '{csv_filename}'")
    
    return df

# Execute the extraction
if __name__ == "__main__":
    raw_df = extract_nasa_data()
    print("\nData Preview (First 5 Rows):")
    print(raw_df.head())