import pandas as pd
import requests

url = "https://en.wikipedia.org/wiki/List_of_Hindi_films_of_2025"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Fetch page
response = requests.get(url, headers=headers)

# ✅ Check if request worked
if response.status_code != 200:
    print("Failed to fetch page:", response.status_code)
    exit()

# Read tables
tables = pd.read_html(response.text)

print("Total tables found:", len(tables))

# ✅ Combine all tables (IMPORTANT)
df = pd.concat(tables, ignore_index=True)

# Preview
print(df.head())

# Save to Excel
df.to_excel("hindi_movies_2025.xlsx", index=False)

print("File saved successfully ✅")