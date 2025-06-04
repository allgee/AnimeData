# etl/transform.py

import pandas as pd

def transform_data(data):
    print("🧼 Transforming data...")

    # Return empty DataFrame if no data provided
    if not data:
        print("⚠️ No data to transform.")
        return pd.DataFrame()

    # Extract and simplify only the relevant fields from the raw data
    simplified = []
    for anime in data:
        simplified.append({
            "id": anime.get("mal_id"),
            "title": anime.get("title"),
            "image_url": anime.get("images", {}).get("jpg", {}).get("image_url"),
            "score": anime.get("score"),
            "episodes": anime.get("episodes"),
            "members": anime.get("members"),
            "genres": ", ".join([g["name"] for g in anime.get("genres", [])]),
            "synopsis": anime.get("synopsis")
        })

    # Convert the simplified list into a DataFrame
    df = pd.DataFrame(simplified)

    # Drop rows with missing essential fields
    df = df.dropna(subset=["title", "score"])

    # Clean string columns to remove any invalid UTF-8 characters
    def clean_text(value):
        if isinstance(value, str):
            return value.encode("utf-8", errors="ignore").decode("utf-8")
        return value

    for col in df.select_dtypes(include='object'):
        df[col] = df[col].map(clean_text)

    print(f"✅ Transformed {len(df)} rows of anime data.")
    return df
