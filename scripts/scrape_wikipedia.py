import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import re

def is_valid_movie_row(name):
    """Filter out invalid rows while preserving valid movie data"""
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
    invalid_texts = ['title', 'ref.', 'opening', 'rank', 'none']
    if name.lower() in invalid_texts:
        return False
    
    # Skip very short names (likely junk)
    if len(name) < 3:
        return False
    
    return True

# Fetch Wikipedia page with proper headers
url = "https://en.wikipedia.org/wiki/List_of_Hindi_films_of_2025"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers)
response.raise_for_status()  # Ensure request was successful
soup = BeautifulSoup(response.text, "html.parser")

# Find all wikitable elements
tables = soup.find_all("table", {"class": "wikitable"})

all_movies = []

for table in tables:
    # Extract headers from first row
    header_row = table.find("tr")
    if not header_row:
        continue
        
    headers = [th.get_text(strip=True).lower() for th in header_row.find_all("th")]
    
    # Skip tables without movie-related headers
    if not any(keyword in " ".join(headers) for keyword in ["title", "film", "movie"]):
        continue

    # Create column mapping based on headers
    col_map = {}
    for i, h in enumerate(headers):
        if "title" in h or "film" in h:
            col_map["Name"] = i
        elif "director" in h:
            col_map["Director"] = i
        elif "cast" in h:
            col_map["Cast"] = i
        elif "studio" in h or "production" in h or "company" in h:
            col_map["Studio"] = i
        elif "distributor" in h:
            col_map["Distributor"] = i
        elif "gross" in h or "box office" in h:
            col_map["BoxOffice"] = i

    # Process data rows (skip header row)
    rows = table.find_all("tr")[1:]

    for row in rows:
        cols = row.find_all("td")
        
        if not cols or len(cols) < 2:
            continue

        try:
            # Extract movie name using header mapping
            name = None
            if "Name" in col_map:
                name = cols[col_map["Name"]].get_text(strip=True)
            
            # Validate row before processing
            if not is_valid_movie_row(name):
                continue

            # Extract other fields using mapping
            movie_data = {"Name": name}
            
            if "Director" in col_map:
                movie_data["Director"] = cols[col_map["Director"]].get_text(separator=", ").strip()
            else:
                movie_data["Director"] = None
                
            if "Cast" in col_map:
                movie_data["Cast"] = cols[col_map["Cast"]].get_text(separator=", ").strip()
            else:
                movie_data["Cast"] = None
                
            if "Studio" in col_map:
                movie_data["Studio"] = cols[col_map["Studio"]].get_text(separator=", ").strip()
            else:
                movie_data["Studio"] = None
                
            if "Distributor" in col_map:
                movie_data["Distributor"] = cols[col_map["Distributor"]].get_text(separator=", ").strip()
                
            if "BoxOffice" in col_map:
                movie_data["BoxOffice"] = cols[col_map["BoxOffice"]].get_text(strip=True)

            all_movies.append(movie_data)

        except Exception as e:
            # Log error but continue processing other rows
            continue

# Create structured DataFrame
df = pd.DataFrame(all_movies)

# Remove duplicates while preserving data quality
df = df.drop_duplicates(subset=['Name'], keep='first')

# Ensure consistent column order
column_order = ['Name', 'Director', 'Cast', 'Studio', 'Distributor', 'BoxOffice']
existing_columns = [col for col in column_order if col in df.columns]
df = df[existing_columns]

# Save with UTF-8 encoding for special characters
os.makedirs("data/raw", exist_ok=True)
output_file = "data/raw/movies_2025_hindi_raw.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(" Header-based structured scraping completed!")
print(f"Found {len(df)} unique movies")
print(f"Columns extracted: {list(df.columns)}")
print("\nSample data:")
print(df.head(10).to_string(index=False))