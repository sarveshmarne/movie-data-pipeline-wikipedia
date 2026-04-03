import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_American_films_of_2025"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all("table", {"class": "wikitable"})

df_list = []

# Skip Top 10 table
for table in tables[1:]:
    df = pd.read_html(str(table))[0]
    df_list.append(df)

final_df = pd.concat(df_list, ignore_index=True)

# Clean column names
final_df.columns = [col[0] if isinstance(col, tuple) else col for col in final_df.columns]

# Remove unwanted columns
final_df = final_df.loc[:, ~final_df.columns.str.contains("Ref")]
final_df = final_df.drop(columns=["Opening", "Opening.1"], errors="ignore")

# Add Year column
final_df["Year"] = 2025

# Save file
final_df.to_excel(r"D:\american_movies_2025_clean.xlsx", index=False)

print("Final cleaned dataset ready ✅")