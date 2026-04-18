import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import re

def is_valid_movie_row(name):
    """Filter out invalid rows for 2025 data"""
    if not name or not name.strip():
        return False
    
    name = name.strip()
    
    # Skip month headers
    if re.match(r'^(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)', name, re.I):
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

# Fetch Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_Hindi_films_of_2025"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

response = requests.get(url, headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# Find all wikitable elements
tables = soup.find_all("table", {"class": "wikitable"})

all_movies = []

# HARDCODED: Only process monthly tables (tables 2, 3, 4, 5) which have correct structure
monthly_table_indices = [2, 3, 4, 5]
for i, table in enumerate(tables):
    if i not in monthly_table_indices:
        continue
        
    # Process data rows (skip header row)
    rows = table.find_all("tr")[1:]

    for row in rows:
        cols = row.find_all("td")
        
        if not cols or len(cols) < 3:
            continue

        try:
            # HARDCODED 2025 COLUMN MAPPING for monthly tables
            # cols[0] = Opening, cols[1] = Title, cols[2] = Director, cols[3] = Cast, cols[4] = Studio
            name = cols[1].get_text(strip=True) if len(cols) > 1 else None
            director = cols[2].get_text(strip=True) if len(cols) > 2 else None
            cast = cols[3].get_text(strip=True) if len(cols) > 3 else None
            studio = cols[4].get_text(strip=True) if len(cols) > 4 else None
            
            # Validate row before processing
            if not is_valid_movie_row(name):
                continue

            all_movies.append({
                "Name": name,
                "Director": director,
                "Cast": cast,
                "Studio": studio
            })

        except Exception as e:
            continue

# Create DataFrame
df = pd.DataFrame(all_movies)

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