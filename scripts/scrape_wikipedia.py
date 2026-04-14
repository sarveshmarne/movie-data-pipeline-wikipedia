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

all_rows = []

for table in tables:
    rows = table.find_all("tr")

    for row in rows:
        cols = row.find_all(["td", "th"])

        if not cols:
            continue

        row_data = []

        for col in cols:
            text = col.get_text(separator=", ").strip()
            row_data.append(text)

        all_rows.append(row_data)

# -----------------------------
# 🔥 CONVERT TO DATAFRAME
# -----------------------------
df = pd.DataFrame(all_rows)

# -----------------------------
# 🔥 SAVE RAW DATA (FULL DUMP)
# -----------------------------
os.makedirs("data/raw", exist_ok=True)

df.to_json("data/raw/movies_wikipedia_2025_full_dump.json", orient='records', lines=True, date_format='iso')

print("✅ Full raw dump saved as JSON!")
print("Shape:", df.shape)
print(df.head(10))