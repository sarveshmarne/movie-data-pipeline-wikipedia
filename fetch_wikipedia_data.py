import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_Hindi_films_of_2025"

# Read all tables from page
tables = pd.read_html(url)

# Check how many tables
print(len(tables))

# Example: first table
df = tables[0]

print(df.head())