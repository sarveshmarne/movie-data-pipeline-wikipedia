import pandas as pd
import re
import os
import numpy as np

def clean_text(text):
    if pd.isna(text):
        return np.nan
    text = str(text).strip()
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"^\d+\s*,?\s*", "", text)  # Remove leading numbers + comma
    text = re.sub(r",?\s*[\[\]]", "", text)
    return text.strip() if text.strip() else np.nan

df = pd.read_csv("data/raw/movies_wikipedia_2025_full_dump.csv")

print("Raw shape:", df.shape)
print("Raw head:\n", df.head(20))

# Find monthly table starts (rows with "Title" in col1)
monthly_starts = []
for idx in df.index:
    row = df.iloc[idx]
    if pd.notna(row.iloc[1]) and 'Title' in str(row.iloc[1]):
        monthly_starts.append(idx)

print("Monthly table headers at rows:", monthly_starts)

# Take data from first monthly table onwards (skip top grossing + headers)
if monthly_starts:
    start_row = monthly_starts[0] + 1
else:
    start_row = 13

df_monthly = df.iloc[start_row:].reset_index(drop=True)
print(f"Monthly data shape: {df_monthly.shape}")
print("Monthly head:\n", df_monthly.head(10))

# Filter valid movie rows: Name col (idx1) looks like movie title
def is_valid_movie_row(row):
    name = str(row.iloc[1]).strip(', ')
    if pd.isna(row.iloc[1]) or len(name) < 3 or name.isdigit() or name == 'Title':
        return False
    if re.search(r'^(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)', name, re.I):
        return False
    # Must have director or cast (not all empty)
    dir_cast = pd.notna(row.iloc[2]) or pd.notna(row.iloc[3])
    return dir_cast

df_clean = df_monthly[df_monthly.apply(is_valid_movie_row, axis=1)].reset_index(drop=True)

print(f"Valid movies: {len(df_clean)}")
print("Clean head:\n", df_clean.head())

# Extract columns: Title(1), Director(2), Cast(3), Studio(4)
df_final = pd.DataFrame({
    'Name': df_clean.iloc[:, 1].apply(clean_text),
    'Director': df_clean.iloc[:, 2].apply(clean_text),
    'Cast': df_clean.iloc[:, 3].apply(clean_text),
    'Studio': df_clean.iloc[:, 4].apply(clean_text) if len(df_clean.columns) > 4 else np.nan
})

# Split cast
def split_cast(cast):
    if pd.isna(cast):
        return [np.nan, np.nan, np.nan]
    cast_list = [c.strip() for c in str(cast).split(',') if c.strip()]
    return cast_list[:3] + [np.nan] * (3 - len(cast_list))

cast_split = df_final['Cast'].apply(split_cast).apply(pd.Series)
df_final[['Cast_1', 'Cast_2', 'Cast_3']] = cast_split

# Add metadata
df_final['Year'] = 2025
df_final['Language'] = 'hindi'

# Select final columns, drop rows where Name is NaN/empty
final_cols = ['Year', 'Name', 'Director', 'Cast_1', 'Cast_2', 'Cast_3', 'Studio', 'Language']
df_final = df_final[final_cols].dropna(subset=['Name'])

print("Final shape:", df_final.shape)
print(df_final.head(15))
print("\nSample movies:")
print(df_final[['Name', 'Director', 'Cast_1']].head(10))

os.makedirs("data/processed", exist_ok=True)
df_final.to_csv("data/processed/movies_cleaned_2025_hindi.csv", index=False)
print("\n✅ Super clean data saved! High quality 2025 Hindi movies dataset.")

