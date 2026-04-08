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
    # 🔥 GET HEADERS
    # -----------------------------
    header_cells = table.find_all("th")
    headers_text = [th.get_text(strip=True).lower() for th in header_cells]

    # Skip irrelevant tables
    if not ("director" in " ".join(headers_text) and "cast" in " ".join(headers_text)):
        continue

    # -----------------------------
    # 🔥 MAP COLUMN INDEXES
    # -----------------------------
    col_index = {}

    for i, h in enumerate(headers_text):
        if "title" in h:
            col_index["Name"] = i
        elif "director" in h:
            col_index["Director"] = i
        elif "cast" in h:
            col_index["Cast"] = i
        elif "studio" in h or "production" in h:
            col_index["Studio"] = i

    rows = table.find_all("tr")

    for row in rows[1:]:
        cols = row.find_all("td")

        if len(cols) < 3:
            continue

        try:
            name = cols[col_index["Name"]].get_text(strip=True)
            director = cols[col_index["Director"]].get_text(separator=", ").strip()
            cast = cols[col_index["Cast"]].get_text(separator=", ").strip()

            studio = None
            if "Studio" in col_index:
                studio = cols[col_index["Studio"]].get_text(separator=", ").strip()

            all_movies.append({
                "Year": 2025,
                "Name": name,
                "Director": director,
                "Cast": cast,
                "Studio": studio,
                "Language": "hindi"
            })

        except:
            continue

# -----------------------------
# 🔥 SAVE DATA
# -----------------------------
df = pd.DataFrame(all_movies)

os.makedirs("data/raw", exist_ok=True)

df.to_csv("data/raw/movies_wikipedia_2025_hindi_clean.csv", index=False)

print("✅ Clean raw data saved!")
print("Shape:", df.shape)
print(df.head())