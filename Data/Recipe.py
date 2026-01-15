import pandas as pd
import ast
import re
from ingredient_parser import parse_ingredient

df = pd.read_csv("13k-recipes.csv")

df["Cleaned_Ingredients"] = df["Cleaned_Ingredients"].apply(ast.literal_eval)
df = df.explode("Cleaned_Ingredients").rename(columns={"Cleaned_Ingredients": "ingredient_raw"})

def safe_float(x):
    try:
        if x is None:
            return None
        if isinstance(x, str) and x.strip() == "":
            return None
        return float(x)
    except:
        return None

def preprocess_ingredient(text):
    if not isinstance(text, str):
        return ""
    t = text.lower()
    t = re.sub(r"\b\d+\s*[x×]\s*", "", t)
    t = re.sub(r"\b\d+\s*[-]?\s*(oz|g|kg|ml|l)\b", "", t)
    t = re.sub(r"\([^)]*\)", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def parse(row):
    clean = preprocess_ingredient(row)

    if not clean:
        return pd.Series({
            "quantity": None,
            "unit": None,
            "ingredient_name": None
        })

    try:
        parsed = parse_ingredient(clean)

        name = parsed.name[0].text if parsed.name else None

        if parsed.amount:
            amt = parsed.amount[0]
            quantity = safe_float(amt.quantity)
            unit = amt.unit
        else:
            quantity = None
            unit = None

        return pd.Series({
            "quantity": quantity,
            "unit": unit,
            "ingredient_name": name
        })

    except Exception:
        return pd.Series({
            "quantity": None,
            "unit": None,
            "ingredient_name": clean
        })

parsed_cols = df["ingredient_raw"].apply(parse)
df = pd.concat([df, parsed_cols], axis=1)

#Normalization
df["unit_clean"] = (
    df["unit"]
    .astype(str)
    .str.lower()
    .str.strip()
)

UNIT_MAP = {
    "tablespoon": "tbsp",
    "tablespoons": "tbsp",
    "tablespoo": "tbsp",   # FIX typo
    "tbsp": "tbsp",
    "teaspoon": "tsp",
    "teaspoons": "tsp",
    "tsp": "tsp",
    "cup": "cup",
    "cups": "cup",
    "loaf": "loaf",
    "loaves": "loaf",
    "pinch": "pinch",
    "pound": "lb",
    "pounds": "lb",
    "lb": "lb",
    "lbs": "lb",
}

df["unit_norm"] = df["unit_clean"].map(UNIT_MAP)


# Text Standardization - layer 1
def clean_name(text):
    if not isinstance(text, str):
        return None   # or "" if you prefer

    text = text.lower()
    text = re.sub(r"\(.*?\)", "", text)   # remove parentheses
    text = re.sub(r"[^a-z\s]", "", text)  # remove punctuation
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["Cleaned_Ingredients"] = df["ingredient_name"].apply(clean_name)

#Remove descriptors (stop-words) - layer 2
STOPWORDS = {
    "fresh", "ground", "finely", "chopped", "unsalted", "salted", "room", "temperature",
    "extra", "virgin", "organic", "raw", "dried"
}

def remove_descriptors(text):
    if not isinstance(text, str):
        return None
    return " ".join(w for w in text.split() if w not in STOPWORDS)

df["ingredient_base"] = df["Cleaned_Ingredients"].apply(remove_descriptors)


#Automatic grouping using fuzzy matching - layer 3
from rapidfuzz import process, fuzz


CANONICAL = {}
CANONICAL_MAP = {
    "extra virgin olive oil": "olive oil",
    "extravirgin olive oil": "olive oil",
    "unsalted butter": "butter",
    "salted butter": "butter",
    "ground allspice": "allspice",
    "kosher salt": "salt",
    "black pepper": "pepper",
    "goodquality sturdy white bread": "white bread",
    "dry white wine": "white wine",
    "chicken broth": "chicken broth",
    "unsalted chicken broth": "chicken broth",
}

df["ingredient_base2"] = df["ingredient_base"].replace(CANONICAL_MAP)
unique_ingredients = df["ingredient_base2"].unique()

for ing in unique_ingredients:
    if ing in CANONICAL:
        continue

    matches = process.extract(
        ing,
        unique_ingredients,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=90
    )

    canonical = ing
    for match, score, _ in matches:
        CANONICAL[match] = canonical
df["ingredient_norm"] = df["ingredient_base2"].map(CANONICAL)

# df[["ingredient_name", "ingredient_norm"]].drop_duplicates().sample(30)

# df.to_csv("recipes_parsed.csv", index=False)
# df.to_csv("recipes_normalized.csv", index=False)

# FACT TABLE: Recipe – Ingredient
# fact_ingredients = df[
#     ["Title", "ingredient_norm", "quantity", "unit_norm"]
# ].dropna(subset=["ingredient_norm"])


# # DIMENSION TABLES
# dim_ingredients = fact_ingredients[["ingredient_norm"]].drop_duplicates()
# dim_recipes = df[["Title", "Image_Name"]].drop_duplicates()

# DIMENSION TABLES
dim_recipes = (
    df[["Title", "Image_Url", "Instructions"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

dim_recipes["recipe_id"] = dim_recipes.index + 1

dim_ingredients = (
    df[["ingredient_norm"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

dim_ingredients["ingredient_id"] = dim_ingredients.index + 1

# FACT TABLE: Recipe – Ingredient
fact = df.merge(
    dim_recipes,
    on="Title",
    how="left"
)

fact = fact.merge(
    dim_ingredients,
    on="ingredient_norm",
    how="left"
)

fact_ingredients = fact[
    ["recipe_id", "ingredient_id", "quantity", "unit_norm"]
]

# Files export
fact_ingredients.to_csv("fact_ingredients_small.csv", index=False)
dim_ingredients.to_csv("dim_ingredients_small.csv", index=False)
dim_recipes.to_csv("dim_recipes_small.csv", index=False)

print("Fact & dimension tables exported successfully")