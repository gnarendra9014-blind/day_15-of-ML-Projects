import pandas as pd
import random

# Simulated raw data with intentional issues
def fetch_raw_data() -> pd.DataFrame:
    data = {
        "user_id": [1, 2, 3, None, 5],
        "age": [25, 30, "thirty", 22, 28],  # bug: string in numeric
        "score": [85, 92, 78, 88, None],     # bug: missing value
        "email": ["a@b.com", "bad-email", "c@d.com", "e@f.com", "g@h.com"]
    }
    return pd.DataFrame(data)

def validate_data(df: pd.DataFrame) -> tuple:
    errors = []
    if df["user_id"].isnull().any():
        errors.append("NULL values found in user_id column")
    try:
        df["age"].astype(float)
    except:
        errors.append("Non-numeric values found in age column")
    if df["score"].isnull().any():
        errors.append("NULL values found in score column")
    return len(errors) == 0, errors

def clean_data(df: pd.DataFrame, fixes: list) -> pd.DataFrame:
    for fix in fixes:
        fix_lower = fix.lower()
        if "user_id" in fix_lower and "null" in fix_lower:
            df = df.dropna(subset=["user_id"])
        if "age" in fix_lower and "numeric" in fix_lower:
            df["age"] = pd.to_numeric(df["age"], errors="coerce")
            df = df.dropna(subset=["age"])
        if "score" in fix_lower and "null" in fix_lower:
            df["score"] = df["score"].fillna(df["score"].mean())
    return df

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df["age"] = df["age"].astype(float)
    df["score_grade"] = df["score"].apply(
        lambda x: "A" if x >= 90 else "B" if x >= 80 else "C"
    )
    return df