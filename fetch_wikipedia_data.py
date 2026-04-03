import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_American_films_of_2025"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

# ✅ Only get movie tables
tables = soup.find_all("table", {"class": "wikitable"})

df_list = []

for table in tables:
    df = pd.read_html(str(table))[0]
    df_list.append(df)

# ✅ Combine all quarters
final_df = pd.concat(df_list, ignore_index=True)

# Preview
print(final_df.head())

# Save clean file
final_df.to_excel(r"D:\american_movies_2025_clean.xlsx", index=False)

print("Clean file saved ✅")