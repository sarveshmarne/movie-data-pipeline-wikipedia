import pandas as pd
import requests

url = "https://en.wikipedia.org/wiki/List_of_Hindi_films_of_2025"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Fetch page
response = requests.get(url, headers=headers)

# Pass HTML to pandas
tables = pd.read_html(response.text)

print(len(tables))

df = tables[0]
print(df.head())