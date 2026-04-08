import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

# -----------------------------
# 🔹 CONFIG
# -----------------------------
url = "https://en.wikipedia.org/wiki/List_of_Hindi_films_of_2025"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# -----------------------------
# 🔹 FETCH PAGE
# -----------------------------
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all("table", {"class": "wikitable"})

all_movies = []

# -----------------------------
# 🔥 LOOP TABLES
# -----------------------------
for table in tables:

    header_text = table.get_text().lower()

    # ✅ Only select correct tables
    if "director" not in header_text or "cast" not in header_text:
        continue

    rows = table.find_all("tr")

    for row in rows[1:]:   # skip header row
        cols = row.find_all("td")

        if len(cols) < 3:
            continue

        try:
            name = cols[0].get_text(strip=True)

            # 🔥 FILTER BAD ROWS
            if (
                name.isupper() or   # JAN, FEB
                name.isdigit() or   # 10, 24
                name == "" or
                len(name) < 2
            ):
                continue

            # -----------------------------
            # 🔥 EXTRACT CLEAN DATA
            # -----------------------------
            director = cols[1].get_text(separator=", ").strip()
            cast = cols[2].get_text(separator=", ").strip()

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

        except Exception as e:
            continue

# -----------------------------
# 🔥 CREATE DATAFRAME
# -----------------------------
df = pd.DataFrame(all_movies)

# Remove duplicates (good practice)
df = df.drop_duplicates()

# -----------------------------
# 🔥 SAVE FILE
# -----------------------------
os.makedirs("data/raw", exist_ok=True)

df.to_csv("data/raw/movies_wikipedia_2025_hindi_clean.csv", index=False)

print("✅ Data saved!")
print("Shape:", df.shape)
print(df.head())