import pandas as pd
import re
import os
import numpy as np

def clean_text(text):
    """Clean text by removing unwanted characters and formatting"""
    if pd.isna(text):
        return np.nan
    
    text = str(text).strip()
    
    # Remove Wikipedia references and citations
    text = re.sub(r"\[.*?\]", "", text)
    
    # Remove leading numbers and commas
    text = re.sub(r"^\d+\s*,?\s*", "", text)
    
    # Remove special markers like (alpha)
    text = re.sub(r",?\s*\(.*?\)", "", text)
    
    # Remove remaining brackets
    text = re.sub(r"[\[\]]", "", text)
    
    # Normalize separators
    text = re.sub(r"[,;]+", ", ", text)
    
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)
    
    # Remove trailing commas and spaces
    text = text.strip(" ,")
    
    return text.strip() if text.strip() else np.nan

# Load raw data with proper encoding
try:
    df = pd.read_csv("data/raw/movies_2025_hindi_raw.csv", encoding="utf-8-sig")
except FileNotFoundError:
    print("Error: Raw data file not found. Please run the scraper first.")
    exit(1)

print("Raw data shape:", df.shape)
print("Raw data columns:", list(df.columns))
print("\nRaw data sample:")
print(df.head(10).to_string(index=False))

# Create a copy for cleaning
df_clean = df.copy()

# Apply text cleaning to all text columns
text_columns = ['Name', 'Director', 'Cast', 'Studio', 'Distributor', 'BoxOffice']
for col in text_columns:
    if col in df_clean.columns:
        df_clean[col] = df_clean[col].apply(clean_text)

# Data quality filters
print(f"\nBefore filtering: {len(df_clean)} rows")

# Remove rows with empty or invalid names
df_clean = df_clean.dropna(subset=['Name'])
df_clean = df_clean[df_clean['Name'].str.len() > 2]

# Remove exact duplicates based on movie name
df_clean = df_clean.drop_duplicates(subset=['Name'], keep='first')

print(f"After filtering: {len(df_clean)} rows")

# Display cleaned data sample
print("\nCleaned data sample:")
print(df_clean.head(15).to_string(index=False))

# Show some movie examples
print("\nSample movies with director and cast:")
sample_cols = ['Name', 'Director', 'Cast']
available_cols = [col for col in sample_cols if col in df_clean.columns]
if available_cols:
    print(df_clean[available_cols].head(10).to_string(index=False))

# Save cleaned data in CSV format with proper encoding
os.makedirs("data/processed", exist_ok=True)
output_file = "data/processed/movies_2025_hindi_clean.csv"
df_clean.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"\n Cleaned data saved to: {output_file}")
print(f"Final dataset: {len(df_clean)} movies")
print(f"Columns: {list(df_clean.columns)}")
