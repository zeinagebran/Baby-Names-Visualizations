import pandas as pd

# Load raw data
df = pd.read_csv("data/dpt2020.csv", sep=";")

# Filter invalid entries
df = df[df['preusuel'] != "_PRENOMS_RARES"]
df = df[df['annais'] != 'XXXX']

# Clean column types
df['year'] = df['annais'].astype(int)
df['births'] = df['nombre'].astype(int)
df['sex'] = df['sexe'].map({1: 'M', 2: 'F'})
df['dept'] = df['dpt'].astype(str).str.zfill(2)

# Rename columns for clarity
df = df.rename(columns={'preusuel': 'name'})

# Reorder columns for readability
df = df[['name', 'year', 'sex', 'dept', 'births']]

# Save detailed dataset (used for dept-level map and gender analysis)
df.to_csv("data/baby_names_cleaned.csv", index=False)

# Aggregate for national view (no dept, but sex kept)
national_df = df.groupby(['name', 'year', 'sex'], as_index=False)['births'].sum()
national_df.to_csv("data/baby_names_national.csv", index=False)

print("Files saved:")
print("- data/baby_names_cleaned.csv (with dept and sex)")
print("- data/baby_names_national.csv (aggregated without dept)")
