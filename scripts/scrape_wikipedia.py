import pandas as pd
import os
import requests

def is_valid_movie_row(name):
    """Filter out invalid rows for 2025 data"""
    if not name or not name.strip():
        return False
    
    name = name.strip()
    
    # Skip month headers
    if name.upper() in ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']:
        return False
    
    # Skip numeric-only rows
    if name.isdigit():
        return False
    
    # Skip common header/footer text
    invalid_texts = ['title', 'ref.', 'opening', 'rank', 'none', 'director', 'cast', 'studio']
    if name.lower() in invalid_texts:
        return False
    
    # Skip very short names (likely junk)
    if len(name) < 3:
        return False
    
    return True

url = "https://en.wikipedia.org/wiki/List_of_Hindi_films_of_2025"

print("Reading tables from Wikipedia...")
# Download HTML first with headers to avoid 403 error
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(url, headers=headers)
response.raise_for_status()

# Read tables from the HTML string
tables = pd.read_html(response.text)

correct_df = None

# Find the correct table (the one with Director & Cast)
for i, df in enumerate(tables):
    cols = [str(c).lower() for c in df.columns]
    
    if "director" in str(cols) and "cast" in str(cols):
        print(f"Found correct table at index {i}")
        print(f"Table columns: {list(df.columns)}")
        correct_df = df
        break

# If not found
if correct_df is None:
    print("Available tables and their columns:")
    for i, df in enumerate(tables):
        print(f"Table {i}: {list(df.columns)}")
    raise Exception("Correct table not found")

# Clean column names
correct_df.columns = [str(c).strip() for c in correct_df.columns]

# Remove junk rows
correct_df = correct_df[correct_df["Title"].notna()]
correct_df = correct_df[~correct_df["Title"].str.contains("JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC", case=False, na=False)]
correct_df = correct_df[~correct_df["Title"].astype(str).str.isdigit()]

# Select correct columns
df = correct_df[["Title", "Director", "Cast", "Studio (production house)"]].copy()
df.columns = ["Name", "Director", "Cast", "Studio"]

# Remove duplicates
df = df.drop_duplicates(subset=['Name'], keep='first')

# Save raw data
os.makedirs("data/raw", exist_ok=True)
output_file = "data/raw/movies_2025_raw.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("2025 Hindi movie scraping completed!")
print(f"Found {len(df)} unique movies")
print("\nSample raw data:")
print(df.head(10).to_string(index=False))