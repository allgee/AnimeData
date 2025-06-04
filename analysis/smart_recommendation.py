# analysis/smart_recommendation.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def smart_recommend_by_title(df: pd.DataFrame, title: str, top_n: int = 5):
    if df.empty or 'title' not in df.columns or 'genres' not in df.columns:
        return pd.DataFrame()

    df = df.copy()
    df = df.dropna(subset=['title', 'genres'])

    # Combine relevant text features (you can expand this)
    df['combined'] = df['title'] + " " + df['genres']

    # Create TF-IDF matrix
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined'])

    # Find index of target anime
    index = df[df['title'].str.lower() == title.lower()].index
    if index.empty:
        return pd.DataFrame()

    cosine_similarities = linear_kernel(tfidf_matrix[index[0]], tfidf_matrix).flatten()

    # Get top similar indices (excluding itself)
    similar_indices = cosine_similarities.argsort()[-top_n-1:-1][::-1]

    return df.iloc[similar_indices][['title', 'score', 'episodes', 'members', 'image_url']]
