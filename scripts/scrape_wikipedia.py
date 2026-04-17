import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

url = "https://en.wikipedia.org/wiki/List_of_Hindi_films_of_2025"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all("table", {"class": "wikitable"})

all_movies = []

for table in tables:

    # -----------------------------
    # Extract headers
    # -----------------------------
    header_row = table.find("tr")
    headers = [th.get_text(strip=True).lower() for th in header_row.find_all("th")]

    # Skip tables without title
    if "title" not in " ".join(headers):
        continue

    # -----------------------------
    # Map column indexes
    # -----------------------------
    col_map = {}

    for i, h in enumerate(headers):
        if "title" in h:
            col_map["Name"] = i
        elif "director" in h:
            col_map["Director"] = i
        elif "cast" in h:
            col_map["Cast"] = i
        elif "studio" in h or "production" in h:
            col_map["Studio"] = i

    rows = table.find_all("tr")[1:]

    for row in rows:
        cols = row.find_all("td")

        if not cols:
            continue

        try:
            name = cols[col_map.get("Name", -1)].get_text(strip=True) if "Name" in col_map else None

            # Skip junk rows
            if not name or name.isupper() or name.isdigit():
                continue

            director = cols[col_map["Director"]].get_text(separator=", ").strip() if "Director" in col_map else None
            cast = cols[col_map["Cast"]].get_text(separator=", ").strip() if "Cast" in col_map else None
            studio = cols[col_map["Studio"]].get_text(separator=", ").strip() if "Studio" in col_map else None

            all_movies.append({
                "Name": name,
                "Director": director,
                "Cast": cast,
                "Studio": studio
            })

        except:
            continue

# -----------------------------
# SAVE
# -----------------------------
df = pd.DataFrame(all_movies)
df = df.drop_duplicates()

os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/movies_wikipedia_2025_structured.csv", index=False)

print(" Clean structured data saved!")
print(f"Found {len(df)} movies")
print(df.head())