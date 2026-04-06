import pandas as pd
import re

# 🔹 Load RAW data
df = pd.read_csv("data/raw/movies_wikipedia_2025_hindi.csv")

# -----------------------------
# 🔥 STEP 1: REMOVE JUNK ROWS
# -----------------------------
# Remove rows where Title is missing
df = df[df["Title"].notna()]

# Remove weird header rows / notes
df = df[~df["Title"].str.contains("Implied|multilingual", na=False)]

# -----------------------------
# 🔥 STEP 2: RENAME COLUMNS
# -----------------------------
df = df.rename(columns={
    "Title": "Name",
    "Production company": "Studio",
    "Worldwide gross": "Revenue",
    "Director": "Director",
    "Cast": "Cast"
})

# -----------------------------
# 🔥 STEP 3: CLEAN REVENUE (₹ → number)
# -----------------------------
def clean_money(value):
    if pd.isna(value):
        return None
    
    value = str(value)
    
    # Remove ₹ and commas
    value = value.replace("₹", "").replace(",", "")
    
    # Convert crore to number
    if "crore" in value:
        num = re.findall(r"\d+\.?\d*", value)
        if num:
            return float(num[0]) * 10000000  # crore → number
    
    return None

df["Revenue"] = df["Revenue"].apply(clean_money)

# -----------------------------
# 🔥 STEP 4: CLEAN CAST (TOP 3)
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
# 🔥 STEP 5: CLEAN DIRECTOR
# -----------------------------
df["Director"] = df["Director"].str.split(",").str[0]

# -----------------------------
# 🔥 STEP 6: KEEP ONLY REQUIRED COLUMNS
# -----------------------------
df["Budget"] = None
df["Verdict"] = None
df["IMDb_Rating"] = None
df["Genre_1"] = None
df["Genre_2"] = None
df["Certificate"] = None

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
# 🔥 SAVE CLEAN DATA
# -----------------------------
final_df.to_csv("data/processed/movies_cleaned_2025_hindi.csv", index=False)

print("✅ Cleaned data saved!")