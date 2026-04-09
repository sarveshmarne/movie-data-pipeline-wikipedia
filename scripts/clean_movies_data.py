import pandas as pd
import re
import os

df = pd.read_csv("data/raw/movies_wikipedia_2025_full_dump.csv")

# STEP 1: Remove top junk rows
df = df.iloc[13:].reset_index(drop=True)

# STEP 2: Remove empty rows
df = df.dropna(how="all")

# DEBUG
print("Shape:", df.shape)
print(df.head())

# -----------------------------
# 🔥 STEP 3: SELECT REQUIRED COLUMNS
# -----------------------------
# Based on your data structure (adjust if needed)

name_col = df.columns[1]
director_col = df.columns[3]
cast_col = df.columns[4]
studio_col = df.columns[5] if len(df.columns) > 5 else None

df = df[[name_col, director_col, cast_col, studio_col]]

df.columns = ["Name", "Director", "Cast", "Studio"]

# -----------------------------
# 🔥 STEP 4: REMOVE NON-MOVIE ROWS
# -----------------------------
df = df[df["Name"].notna()]

df = df[
    ~df["Name"].str.contains(
        "JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC",
        case=False,
        na=False
    )
]

df = df[~df["Name"].str.isdigit()]

# -----------------------------
# 🔥 STEP 5: CLEAN TEXT
# -----------------------------
def clean_text(text):
    if pd.isna(text):
        return text
    return re.sub(r"\[.*?\]", "", str(text)).strip()

df["Name"] = df["Name"].apply(clean_text)
df["Director"] = df["Director"].apply(clean_text)
df["Cast"] = df["Cast"].apply(clean_text)

# -----------------------------
# 🔥 STEP 6: SPLIT CAST
# -----------------------------
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

# -----------------------------
# 🔥 STEP 7: FINAL STRUCTURE
# -----------------------------
df["Year"] = 2025
df["Language"] = "hindi"

final_df = df[
    ["Year", "Name", "Director", "Cast_1", "Cast_2", "Cast_3", "Studio", "Language"]
]

# -----------------------------
# 🔥 STEP 8: SAVE
# -----------------------------
os.makedirs("data/processed", exist_ok=True)

final_df.to_csv("data/processed/movies_cleaned_2025_hindi.csv", index=False)

print("✅ Cleaned data saved!")
print("Final shape:", final_df.shape)