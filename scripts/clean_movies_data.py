import pandas as pd
import re
import os
import numpy as np

def clean_text(text):
    if pd.isna(text):
        return np.nan
    text = str(text).strip()
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"^\d+\s*,?\s*", "", text)
    text = re.sub(r",?\s*\(α\)", "", text)
    text = re.sub(r"[\[\]]", "", text)
    text = re.sub(r"[,;]+", ", ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip() if text.strip() else np.nan

# Load the structured data from new scraper
df = pd.read_csv("data/raw/movies_wikipedia_2025_structured.csv")

print("Raw structured shape:", df.shape)
print("Raw structured head:\n", df.head(10))

# Apply text cleaning to all relevant columns
df_clean = df.copy()
df_clean['Name'] = df_clean['Name'].apply(clean_text)
df_clean['Director'] = df_clean['Director'].apply(clean_text)
df_clean['Cast'] = df_clean['Cast'].apply(clean_text)
df_clean['Studio'] = df_clean['Studio'].apply(clean_text)

# Remove rows with empty names
df_clean = df_clean.dropna(subset=['Name'])
df_clean = df_clean[df_clean['Name'].str.len() > 2]

# Remove duplicates
df_clean = df_clean.drop_duplicates()

print(f"Clean shape: {df_clean.shape}")
print("Clean head:\n", df_clean.head(15))
print("\nSample movies:")
print(df_clean[['Name', 'Director', 'Cast']].head(10))

# Save cleaned data
os.makedirs("data/processed", exist_ok=True)
df_clean.to_json("data/processed/movies_cleaned_2025_hindi.json", orient='records', indent=2)
print("\n Clean data saved as JSON!")
