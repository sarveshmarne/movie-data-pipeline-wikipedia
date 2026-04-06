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

def scrape_wikipedia_hindi_2025():
    print(f"Processing {LANGUAGE.upper()} movies for {YEAR}...")

    try:
        response = requests.get(URL, headers=HEADERS)

        if response.status_code != 200:
            print("❌ Failed to fetch data")
            return

        soup = BeautifulSoup(response.text, "html.parser")

        tables = soup.find_all("table", {"class": "wikitable"})

        all_data = []

        for table in tables:
            df = pd.read_html(str(table))[0]

            # ❌ Skip unwanted tables (like Top grossing)
            if "Rank" in df.columns:
                continue

            # Flatten multi-level columns
            df.columns = [
                col[0] if isinstance(col, tuple) else col
                for col in df.columns
            ]

            # Add metadata
            df["Year"] = YEAR
            df["Language"] = LANGUAGE

            all_data.append(df)

        if not all_data:
            print("⚠️ No valid tables found")
            return

        final_df = pd.concat(all_data, ignore_index=True)

        # 🔥 Save RAW file (IMPORTANT: CSV, not Excel)
        file_path = f"data/raw/movies_wikipedia_{YEAR}_{LANGUAGE}.csv"
        final_df.to_csv(file_path, index=False)

        print(f"✅ Raw data saved at: {file_path}")

    except Exception as e:
        print(f"❌ Error: {e}")


# 🔹 RUN
if __name__ == "__main__":
    scrape_wikipedia_hindi_2025()