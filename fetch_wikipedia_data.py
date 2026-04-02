import pandas as pd
import requests

url = "https://en.wikipedia.org/wiki/List_of_Hindi_films_of_2025"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("Failed to fetch page:", response.status_code)
    exit()

tables = pd.read_html(response.text)

df = pd.concat(tables, ignore_index=True)

# Save to D drive
df.to_excel(r"D:\hindi_movies_2025.xlsx", index=False)

print("File saved in D drive ✅")