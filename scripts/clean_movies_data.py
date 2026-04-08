import pandas as pd
import re
import os

# -----------------------------
# 🔹 LOAD RAW DATA
# -----------------------------
df = pd.read_csv("data/raw/movies_wikipedia_2025_hindi.csv")

# -----------------------------
# 🔥 STEP 1: STANDARDIZE COLUMN NAMES
# -----------------------------
df.columns = [col.strip() for col in df.columns]

column_map = {}

for col in df.columns:
    col_lower = col.lower()

    if "title" in col_lower:
        column_map[col] = "Name"

    elif "director" in col_lower:
        column_map[col] = "Director"

    elif "cast" in col_lower:
        column_map[col] = "Cast"

# Apply rename
df = df.rename(columns=column_map)

print("Columns after rename:", df.columns.tolist())

# -----------------------------
# 🔥 STEP 2: REMOVE DUPLICATE COLUMNS
# -----------------------------
df = df.loc[:, ~df.columns.duplicated()]

# -----------------------------
# 🔥 STEP 3: REMOVE JUNK ROWS
# -----------------------------
df = df[df["Name"].notna()]
df = df[~df["Name"].str.contains("Implied|multilingual", na=False)]

# Keep only correct movie rows
if "Director" in df.columns:
    df = df[df["Director"].notna()]

# -----------------------------
# 🔥 STEP 4: CLEAN MOVIE NAMES
# -----------------------------
def clean_text(text):
    if pd.isna(text):
        return text

    text = str(text)

    # Remove [Î±], [1], etc.
    text = re.sub(r"\[.*?\]", "", text)

    # Fix encoding issues
    text = text.replace("â€“", "-")
    text = text.replace("–", "-")

    return text.strip()

df["Name"] = df["Name"].apply(clean_text)

# -----------------------------
# 🔥 STEP 5: CLEAN DIRECTOR
# -----------------------------
if "Director" in df.columns:
    df["Director"] = df["Director"].str.split(",").str[0]
else:
    df["Director"] = None

# -----------------------------
# 🔥 STEP 6: CLEAN CAST (TOP 3)
# -----------------------------
def split_cast(cast):
    if pd.isna(cast):
        return pd.Series([None, None, None])

    cast_list = [c.strip() for c in str(cast).split(",")]

    return pd.Series([
        cast_list[0] if len(cast_list) > 0 else None,
        cast_list[1] if len(cast_list) > 1 else None,
        cast_list[2] if len(cast_list) > 2 else None
    ])

if "Cast" in df.columns:
    df[["Cast_1", "Cast_2", "Cast_3"]] = df["Cast"].apply(split_cast)
else:
    df["Cast_1"] = df["Cast_2"] = df["Cast_3"] = None

# -----------------------------
# 🔥 STEP 7: FINAL COLUMNS
# -----------------------------
# Ensure Year & Language exist
if "Year" not in df.columns:
    df["Year"] = 2025

if "Language" not in df.columns:
    df["Language"] = "hindi"

final_columns = [
    "Year",
    "Name",
    "Director",
    "Cast_1",
    "Cast_2",
    "Cast_3",
    "Language"
]

final_df = df[final_columns]

# -----------------------------
# 🔥 STEP 8: SAVE FILE
# -----------------------------
os.makedirs("data/processed", exist_ok=True)

final_df.to_csv("data/processed/movies_cleaned_2025_hindi.csv", index=False)

print("✅ Cleaned data saved successfully!")