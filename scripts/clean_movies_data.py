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
    text = re.sub(r",?\s*\(α\)", "", text)
    text = re.sub(r"[\[\]]", "", text)
    text = re.sub(r"[,;]+", ", ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip() if text.strip() else np.nan

df = pd.read_json("data/raw/movies_wikipedia_2025_full_dump.json", lines=True)

print("Raw shape:", df.shape)
print("Raw head:\n", df.head(20))

# Find monthly table starts (rows with "Director" in col2)
monthly_starts = []
for idx in df.index:
    row = df.iloc[idx]
    if pd.notna(row.iloc[2]) and 'Director' in str(row.iloc[2]):
        monthly_starts.append(idx)

print("Monthly table headers at rows:", monthly_starts)

# Process top-grossing films separately (first 12 rows after header)
df_top_grossing = df.iloc[2:12].reset_index(drop=True)  # Skip header rows
print(f"Top-grossing data shape: {df_top_grossing.shape}")

# Process monthly release films
if monthly_starts:
    start_row = monthly_starts[0] + 1
else:
    start_row = 13

df_monthly = df.iloc[start_row:].reset_index(drop=True)
print(f"Monthly data shape: {df_monthly.shape}")
print("Monthly head:\n", df_monthly.head(10))

# Filter valid movie rows from monthly tables only
def is_valid_movie_row(row):
    name_raw = row.iloc[1]
    if pd.isna(name_raw):
        return False
    name = str(name_raw).strip(', ')
    if len(name) < 3 or name.isdigit() or name == 'Title' or name == 'Ref.':
        return False
    if re.search(r'^(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)', name, re.I):
        return False
    # Skip if name is just number like "3," "10," "17,"
    if re.match(r'^\d+[\,\s]*$', name):
        return False
    # Must have director or cast content
    dir_content = pd.notna(row.iloc[2]) and str(row.iloc[2]).strip()
    cast_content = pd.notna(row.iloc[3]) and str(row.iloc[3]).strip()
    return bool(dir_content or cast_content)

df_monthly_clean = df_monthly[df_monthly.apply(is_valid_movie_row, axis=1)].reset_index(drop=True)

print(f"Valid monthly movies: {len(df_monthly_clean)}")

# Process top-grossing films (different column structure)
def process_top_grossing(row):
    if pd.isna(row.iloc[1]) or str(row.iloc[1]).strip() == 'Title':
        return None
    return {
        'Name': clean_text(row.iloc[1]),
        'Director': np.nan,  # Not available in top-grossing table
        'Cast': np.nan,      # Not available in top-grossing table  
        'Studio': clean_text(row.iloc[2]),  # Production company
        'Worldwide_Gross': clean_text(row.iloc[4])  # Box office
    }

top_grossing_movies = []
for idx, row in df_top_grossing.iterrows():
    movie = process_top_grossing(row)
    if movie and movie['Name'] and not pd.isna(movie['Name']):
        top_grossing_movies.append(movie)

df_top_clean = pd.DataFrame(top_grossing_movies)
print(f"Clean top-grossing movies: {len(df_top_clean)}")

# Process monthly films (correct column mapping)
df_monthly_final = pd.DataFrame({
    'Name': df_monthly_clean.iloc[:, 1].apply(clean_text),
    'Director': df_monthly_clean.iloc[:, 2].apply(clean_text),
    'Cast': df_monthly_clean.iloc[:, 3].apply(clean_text),
    'Studio': df_monthly_clean.iloc[:, 4].apply(clean_text) if len(df_monthly_clean.columns) > 4 else np.nan
})

# Combine both datasets
df_final = pd.concat([df_monthly_final, df_top_clean], ignore_index=True)
print(f"Combined movies: {len(df_final)}")

# Add metadata
df_final['Year'] = 2025
df_final['Language'] = 'hindi'

# Select final columns, drop rows where Name is NaN/empty
final_cols = ['Year', 'Name', 'Director', 'Cast', 'Studio', 'Language']
df_final = df_final[final_cols].dropna(subset=['Name'])

print("Final shape:", df_final.shape)
print(df_final.head(15))
print("\nSample movies:")
print(df_final[['Name', 'Director', 'Cast']].head(10))

os.makedirs("data/processed", exist_ok=True)
df_final.to_json("data/processed/movies_cleaned_2025_hindi.json", orient='records', indent=2)
print("\n✅ Super clean data saved as JSON! High quality 2025 Hindi movies dataset.")
