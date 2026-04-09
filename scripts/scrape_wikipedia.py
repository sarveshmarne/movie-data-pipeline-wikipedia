import pandas as pd
import re
import os

df = pd.read_csv("data/raw/movies_wikipedia_2025_full_dump.csv")

# STEP 1: Remove top junk
df = df.iloc[13:].reset_index(drop=True)

# STEP 2: Remove empty rows
df = df.dropna(how="all")

# STEP 3: Rename columns (adjust if needed)
df.columns = ["Col1", "Name", "Col3", "Director", "Cast", "Studio"]

# STEP 4: Remove non-movie rows
df = df[df["Name"].notna()]
df = df[~df["Name"].str.contains("JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC", case=False, na=False)]
df = df[~df["Name"].str.isdigit()]

# STEP 5: Clean text
def clean_text(text):
    if pd.isna(text):
        return text
    text = re.sub(r"\[.*?\]", "", str(text))
    return text.strip()

df["Name"] = df["Name"].apply(clean_text)
df["Director"] = df["Director"].apply(clean_text)
df["Cast"] = df["Cast"].apply(clean_text)

# STEP 6: Split cast
def split_cast(cast):
    if pd.isna(cast):
        return pd.Series([None, None, None])
    cast_list = [c.strip() for c in cast.split(",")]
    return pd.Series([
        cast_list[0] if len(cast_list) > 0 else None,
        cast_list[1] if len(cast_list) > 1 else None,
        cast_list[2] if len(cast_list) > 2 else None
    ])

df[["Cast_1", "Cast_2", "Cast_3"]] = df["Cast"].apply(split_cast)

# STEP 7: Final columns
df["Year"] = 2025
df["Language"] = "hindi"

final_df = df[[
    "Year",
    "Name",
    "Director",
    "Cast_1",
    "Cast_2",
    "Cast_3",
    "Studio",
    "Language"
]]

# STEP 8: Save
os.makedirs("data/processed", exist_ok=True)
final_df.to_csv("data/processed/movies_cleaned_2025_hindi.csv", index=False)

print("✅ Cleaned data saved!")