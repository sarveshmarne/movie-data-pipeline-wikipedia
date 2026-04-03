import pandas as pd
import requests
from bs4 import BeautifulSoup

base_url = "https://en.wikipedia.org/wiki/List_of_American_films_of_{}"

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_data = []

# Loop from 2025 to 1900
for year in range(2025, 1899, -1):
    print(f"Processing {year}...")

    url = base_url.format(year)

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Skipping {year} (status {response.status_code})")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        tables = soup.find_all("table", {"class": "wikitable"})

        for table in tables:
            df = pd.read_html(str(table))[0]

            # ❌ Skip Top grossing table
            if "Rank" in df.columns:
                continue

            # Flatten multi-index columns
            df.columns = [
                col[0] if isinstance(col, tuple) else col
                for col in df.columns
            ]

            # ❌ Remove Ref columns
            df = df.loc[:, ~df.columns.str.contains("Ref", case=False)]

            # ❌ Remove Opening columns if exist
            df = df.drop(columns=["Opening", "Opening.1"], errors="ignore")

            # ✅ Add Year dynamically
            df["Year"] = year

            all_data.append(df)

    except Exception as e:
        print(f"Error in {year}: {e}")
        continue

# 🔥 Combine all years
final_df = pd.concat(all_data, ignore_index=True)

# 🚀 Normalize columns (IMPORTANT)
# Keep only common useful columns
common_cols = ["Title", "Director", "Cast", "Distributor", "Year"]

for col in common_cols:
    if col not in final_df.columns:
        final_df[col] = None

final_df = final_df[common_cols]

# 💾 Save final dataset
final_df.to_excel(r"D:\american_movies_1900_2025.xlsx", index=False)

print("Final dataset created successfully ✅")