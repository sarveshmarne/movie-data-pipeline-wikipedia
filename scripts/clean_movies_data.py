import pandas as pd
import re
import os

# 🔹 Load RAW data
df = pd.read_csv("data/raw/movies_wikipedia_2025_hindi.csv")

# -----------------------------
# 🔥 STEP 1: REMOVE JUNK ROWS
# -----------------------------

# Remove rows where Title is missing
df = df[df["Title"].notna()]

# Remove note rows
df = df[~df["Title"].str.contains("Implied|multilingual", na=False)]

# -----------------------------
# 🔥 STEP 2: REMOVE TOP GROSSING TABLE ROWS
# -----------------------------

# Best logic: keep rows where Director exists
df = df[df["Director"].notna()]

# -----------------------------
# 🔥 STEP 3: RENAME COLUMNS
# -----------------------------
df = df.rename(columns={
    "Title": "Name",
    "Production company": "Studio",
    "Worldwide gross": "Revenue"
})

# -----------------------------
# 🔥 STEP 4: CLEAN TEXT (Name)
# -----------------------------
def clean_text(text):
    if pd.isna(text):
        return text
    
    text = str(text)

    # Remove [Î±], [Î²], [1], etc.
    text = re.sub(r"\[.*?\]", "", text)

    # Fix encoding issues
    text = text.replace("â€“", "-")
    text = text.replace("–", "-")

    # Remove extra spaces
    text = text.strip()

    return text

df["Name"] = df["Name"].apply(clean_text)

# -----------------------------
# 🔥 STEP 5: CLEAN REVENUE
# -----------------------------
def clean_money(value):
    if pd.isna(value):
        return None
    
    value = str(value)

    # Remove ₹ and commas
    value = value.replace("₹", "").replace(",", "")

    # Extract number
    num = re.findall(r"\d+\.?\d*", value)

    if not num:
        return None

    num = float(num[0])

    # Convert crore → actual number
    if "crore" in value.lower():
        return num * 10000000

    return num

df["Revenue"] = df["Revenue"].apply(clean_money)

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

df[["Cast_1", "Cast_2", "Cast_3"]] = df["Cast"].apply(split_cast)

# -----------------------------
# 🔥 STEP 7: CLEAN DIRECTOR
# -----------------------------
df["Director"] = df["Director"].str.split(",").str[0]

# -----------------------------
# 🔥 STEP 8: CLEAN STUDIO
# -----------------------------
df["Studio"] = df["Studio"].astype(str)
df["Studio"] = df["Studio"].str.replace(r"([a-z])([A-Z])", r"\1, \2", regex=True)

# -----------------------------
# 🔥 STEP 9: ADD MISSING COLUMNS
# -----------------------------
df["Budget"] = None
df["Verdict"] = None
df["IMDb_Rating"] = None
df["Genre_1"] = None
df["Genre_2"] = None
df["Certificate"] = None

# -----------------------------
# 🔥 STEP 10: FINAL STRUCTURE
# -----------------------------
final_df = df[[
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
]]

# -----------------------------
# 🔥 STEP 11: SAVE FILE
# -----------------------------
os.makedirs("data/processed", exist_ok=True)

final_df.to_csv("data/processed/movies_cleaned_2025_hindi.csv", index=False)

print("✅ Cleaned data saved successfully!")