# analysis/recommendation.py

import pandas as pd

def recommend_by_genre(df: pd.DataFrame, genre: str, top_n: int = 5):
    """
    Recommend top anime based on a specific genre.

    Args:
        df (pd.DataFrame): The anime dataset.
        genre (str): The genre to filter by.
        top_n (int): Number of top recommendations to return.

    Returns:
        pd.DataFrame: Top anime filtered by genre and sorted by score.
    """
    filtered = df[df['genres'].str.contains(genre, case=False, na=False)]
    sorted_df = filtered.sort_values(by="score", ascending=False)
    return sorted_df.head(top_n)


def recommend_similar_titles(df: pd.DataFrame, title: str, top_n: int = 5):
    """
    Recommend anime similar to a given title based on genre overlap.

    Args:
        df (pd.DataFrame): The anime dataset.
        title (str): Reference anime title.
        top_n (int): Number of recommendations to return.

    Returns:
        pd.DataFrame: Anime similar to the input title.
    """
    # Get the reference anime row
    reference = df[df['title'].str.lower() == title.lower()]
    if reference.empty:
        return pd.DataFrame()

    # Extract genres of the reference anime
    target_genres = reference.iloc[0]['genres'].split(',')
    target_genres = [g.strip() for g in target_genres]

    # Score similarity by counting overlapping genres
    def score_similarity(genres):
        if pd.isna(genres):
            return 0
        anime_genres = [g.strip() for g in genres.split(',')]
        return len(set(anime_genres) & set(target_genres))

    # Compute similarity for all rows
    df['similarity'] = df['genres'].apply(score_similarity)

    # Exclude the original anime and sort by similarity + score
    similar = df[df['title'].str.lower() != title.lower()]
    similar_sorted = similar.sort_values(by=['similarity', 'score'], ascending=False)

    return similar_sorted.head(top_n)
