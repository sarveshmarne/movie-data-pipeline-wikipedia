import pandas as pd
import re
import os

# -----------------------------
# 🔹 LOAD RAW DATA
# -----------------------------
df = pd.read_csv("data/raw/movies_wikipedia_2025_hindi.csv")

# -----------------------------
# 🔥 STEP 1: BASIC CLEANING
# -----------------------------
if "Title" in df.columns:
    df = df[df["Title"].notna()]

# -----------------------------
# 🔥 STEP 2: STANDARDIZE COLUMN NAMES
# -----------------------------
df.columns = [col.strip() for col in df.columns]

# Dynamic column mapping
column_map = {}

for col in df.columns:
    col_lower = col.lower()

    if "title" in col_lower:
        column_map[col] = "Name"

    elif "production" in col_lower or "studio" in col_lower:
        column_map[col] = "Studio"

    elif "gross" in col_lower or "collection" in col_lower:
        column_map[col] = "Revenue"

    elif "director" in col_lower:
        column_map[col] = "Director"

    elif "cast" in col_lower:
        column_map[col] = "Cast"

# Apply rename
df = df.rename(columns=column_map)

print("Columns after rename:", df.columns.tolist())

# -----------------------------
# 🔥 STEP 3: REMOVE DUPLICATE COLUMNS (CRITICAL FIX)
# -----------------------------
df = df.loc[:, ~df.columns.duplicated()]

# -----------------------------
# 🔥 STEP 4: REMOVE JUNK ROWS
# -----------------------------
df = df[df["Name"].notna()]
df = df[~df["Name"].str.contains("Implied|multilingual", na=False)]

# Remove top grossing rows
if "Director" in df.columns:
    df = df[df["Director"].notna()]

# -----------------------------
# 🔥 STEP 5: CLEAN MOVIE NAMES
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
# 🔥 STEP 6: CLEAN REVENUE
# -----------------------------
def clean_money(value):
    if pd.isna(value):
        return None

    value = str(value)

    # Remove ₹ and commas
    value = value.replace("₹", "").replace(",", "")

    num = re.findall(r"\d+\.?\d*", value)

    if not num:
        return None

    num = float(num[0])

    if "crore" in value.lower():
        return num * 10000000

    return num

if "Revenue" in df.columns:
    df["Revenue"] = df["Revenue"].apply(clean_money)
else:
    df["Revenue"] = None

# -----------------------------
# 🔥 STEP 7: CLEAN CAST (TOP 3)
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
# 🔥 STEP 8: CLEAN DIRECTOR
# -----------------------------
if "Director" in df.columns:
    df["Director"] = df["Director"].str.split(",").str[0]
else:
    df["Director"] = None

# -----------------------------
# 🔥 STEP 9: CLEAN STUDIO
# -----------------------------
if "Studio" in df.columns:

    # If duplicate columns existed, force single column
    if isinstance(df["Studio"], pd.DataFrame):
        df["Studio"] = df["Studio"].iloc[:, 0]

    df["Studio"] = df["Studio"].astype(str)
    df["Studio"] = df["Studio"].str.replace(r"([a-z])([A-Z])", r"\1, \2", regex=True)

else:
    df["Studio"] = None

# -----------------------------
# 🔥 STEP 10: ADD MISSING COLUMNS
# -----------------------------
df["Budget"] = None
df["Verdict"] = None
df["IMDb_Rating"] = None
df["Genre_1"] = None
df["Genre_2"] = None
df["Certificate"] = None

# Ensure Year & Language exist
if "Year" not in df.columns:
    df["Year"] = 2025

if "Language" not in df.columns:
    df["Language"] = "hindi"

# -----------------------------
# 🔥 STEP 11: FINAL STRUCTURE
# -----------------------------
final_columns = [
    "Year",
    "Name",
    "Director",
    "Cast_1",
    "Cast_2",
    "Cast_3",
    "Studio",
    "Budget",
    "Revenue",
    "Verdict",
    "IMDb_Rating",
    "Genre_1",
    "Genre_2",
    "Certificate",
    "Language"
]

final_df = df[final_columns]

# -----------------------------
# 🔥 STEP 12: SAVE FILE
# -----------------------------
os.makedirs("data/processed", exist_ok=True)

final_df.to_csv("data/processed/movies_cleaned_2025_hindi.csv", index=False)

print("✅ Cleaned data saved successfully!")