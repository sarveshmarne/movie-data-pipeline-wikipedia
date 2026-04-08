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

    header_text = table.get_text().lower()

    # ✅ Only pick correct table (filter)
    if "director" not in header_text or "cast" not in header_text:
        continue

    rows = table.find_all("tr")

    for row in rows[1:]:
        cols = row.find_all("td")

        if len(cols) < 4:
            continue

        try:
            name = cols[0].get_text(strip=True)

            # 👇 Based on 2025 structure
            director = cols[1].get_text(separator=", ").strip()
            cast = cols[2].get_text(separator=", ").strip()

            # Studio may or may not exist
            studio = None
            if len(cols) >= 4:
                studio = cols[3].get_text(separator=", ").strip()

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
# SAVE FILE
# -----------------------------
df = pd.DataFrame(all_movies)

os.makedirs("data/raw", exist_ok=True)

df.to_csv("data/raw/movies_wikipedia_2025_hindi_clean.csv", index=False)

print("✅ Data saved!")
print("Shape:", df.shape)
print(df.head())