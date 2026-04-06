import pandas as pd
import requests
from bs4 import BeautifulSoup

# 🔹 CONFIG
YEAR = 2025
LANGUAGE = "hindi"

URL = f"https://en.wikipedia.org/wiki/List_of_Hindi_films_of_{YEAR}"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_wikipedia():
    print(f"Processing {LANGUAGE.upper()} movies for {YEAR}...")

    try:
        response = requests.get(URL, headers=HEADERS)

        if response.status_code != 200:
            print("❌ Failed to fetch data")
            return

        # 🔥 Read ALL tables directly
        tables = pd.read_html(response.text)

        valid_tables = []

        for table in tables:

            # ✅ Keep ONLY tables with 'Title' column
            if "Title" in table.columns:

                # ❌ Skip top grossing table
                if "Rank" in table.columns:
                    continue

                # Add metadata
                table["Year"] = YEAR
                table["Language"] = LANGUAGE

                valid_tables.append(table)

        if not valid_tables:
            print("⚠️ No valid movie tables found")
            return

        # 🔥 Combine all valid tables
        final_df = pd.concat(valid_tables, ignore_index=True)

        # 🔥 Save RAW data
        import os
        os.makedirs("data/raw", exist_ok=True)

        file_path = f"data/raw/movies_wikipedia_{YEAR}_{LANGUAGE}.csv"
        final_df.to_csv(file_path, index=False)

        print(f"✅ Raw data saved at: {file_path}")

    except Exception as e:
        print(f"❌ Error: {e}")


# 🔹 RUN
if __name__ == "__main__":
    scrape_wikipedia()