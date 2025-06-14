import pandas as pd
import os

# Detect base directory
if os.path.exists("data/baby_names_cleaned.csv"):
    CLEANED_CSV = "data/baby_names_cleaned.csv"
else:
    CLEANED_CSV = "implementation_visu/data/baby_names_cleaned.csv"

# Load cleaned data
df = pd.read_csv(CLEANED_CSV)

# Show first 10 rows
print("First 10 rows :")
print(df.head(10))
