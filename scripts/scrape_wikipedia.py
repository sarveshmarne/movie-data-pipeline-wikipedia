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

if response.status_code != 200:
    print("Failed to fetch page")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# -----------------------------
# 🔥 FIND ALL TABLES
# -----------------------------
tables = soup.find_all("table", {"class": "wikitable"})

all_movies = []

# -----------------------------
# 🔥 LOOP THROUGH TABLES
# -----------------------------
for table in tables:

    headers_row = table.find_all("th")
    header_texts = [th.get_text(strip=True).lower() for th in headers_row]

    # ✅ ONLY pick movie detail tables
    if not ("director" in " ".join(header_texts) and "cast" in " ".join(header_texts)):
        continue

    rows = table.find_all("tr")

    for row in rows[1:]:  # skip header
        cols = row.find_all("td")

        if len(cols) < 3:
            continue

        try:
            # -----------------------------
            # 🔥 EXTRACT DATA
            # -----------------------------
            title = cols[0].get_text(strip=True)

            # Some tables shift columns → adjust carefully
            director = cols[-3].get_text(separator=", ").strip()
            cast = cols[-2].get_text(separator=", ").strip()
            studio = cols[-1].get_text(separator=", ").strip()

            all_movies.append({
                "Year": 2025,
                "Name": title,
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

# -----------------------------
# 🔥 SAVE RAW DATA
# -----------------------------
os.makedirs("data/raw", exist_ok=True)

df.to_csv("data/raw/movies_wikipedia_2025_hindi_clean.csv", index=False)

print("✅ Clean raw data saved!")
print("Shape:", df.shape)
print(df.head())