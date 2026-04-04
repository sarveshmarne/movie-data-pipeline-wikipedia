import pandas as pd
import requests
from bs4 import BeautifulSoup

base_url = "https://en.wikipedia.org/wiki/List_of_American_films_of_{}"

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_data = []

for year in range(2025, 1899, -1):
    print(f"Processing {year}...")

    url = base_url.format(year)

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Skipping {year}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        tables = soup.find_all("table", {"class": "wikitable"})

        for table in tables:
            df = pd.read_html(str(table))[0]

            # ❌ Skip top grossing table
            if "Rank" in df.columns:
                continue

            # Flatten columns
            df.columns = [
                col[0] if isinstance(col, tuple) else col
                for col in df.columns
            ]

            # ✅ ADD YEAR
            df["Year"] = year

            # ✅ Keep raw data (no cleaning yet)
            all_data.append(df)

    except Exception as e:
        print(f"Error in {year}: {e}")
        continue

# 🔥 Combine everything (RAW DATA)
final_df = pd.concat(all_data, ignore_index=True)

# Save RAW dataset
final_df.to_excel(r"D:\american_movies_raw_1900_2025.xlsx", index=False)

print("Raw dataset saved ✅")