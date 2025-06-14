import pandas as pd
import os

# Detect base directory
if os.path.exists("data/dpt2020.csv"):
    BASE_PATH = "data"
else:
    BASE_PATH = "implementation_visu/data"

RAW_CSV = os.path.join(BASE_PATH, "dpt2020.csv")
CLEANED_CSV = os.path.join(BASE_PATH, "baby_names_cleaned.csv")
NATIONAL_CSV = os.path.join(BASE_PATH, "baby_names_national.csv")

# Load raw data (must be original CSV, not Excel-edited)
df = pd.read_csv(RAW_CSV, sep=";")

# Clean data
df = df[df['preusuel'] != "_PRENOMS_RARES"]
df = df[df['annais'] != 'XXXX']
df['year'] = df['annais'].astype(int)
df['births'] = df['nombre'].astype(int)
df['sex'] = df['sexe'].map({1: 'M', 2: 'F'})
df['dept'] = df['dpt'].astype(str).str.zfill(2)
df = df.rename(columns={'preusuel': 'name'})
df = df[['name', 'year', 'sex', 'dept', 'births']]

# Save cleaned full data
df.to_csv(CLEANED_CSV, index=False)

# Save national-level aggregated version
national_df = df.groupby(['name', 'year', 'sex'], as_index=False)[
    'births'].sum()
national_df.to_csv(NATIONAL_CSV, index=False)

print("Cleaned dataset saved at:", CLEANED_CSV)
print("National dataset saved at:", NATIONAL_CSV)
