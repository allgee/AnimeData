import sys
import os
sys.path.append(os.path.abspath("."))

import streamlit as st
st.set_page_config(page_title="Anime Explorer", layout="wide")  # Set page layout and title

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

from analysis.recommendation import recommend_by_genre, recommend_similar_titles
from analysis.smart_recommendation import smart_recommend_by_title

# Load environment variables
load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

# Create database connection
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

# Load data from database with caching
@st.cache_data
def load_data():
    query = "SELECT * FROM anime"
    return pd.read_sql(query, con=engine)

df = load_data()

# App title
st.title("🎌 Anime Explorer")
st.markdown("Explore top anime, filter by score, and get recommendations by genre or title.")

# Manual refresh button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    df = load_data()
    st.success("✅ Data refreshed successfully.")

# Score filtering
st.subheader("⭐ Filter Anime by Score")
score_range = st.slider("Select score range", 0.0, 10.0, (8.0, 10.0), 0.1)
filtered_score_df = df[(df['score'] >= score_range[0]) & (df['score'] <= score_range[1])]
st.markdown(f"Anime with score between **{score_range[0]}** and **{score_range[1]}**:")
st.dataframe(filtered_score_df[['title', 'score', 'episodes', 'members', 'genres']])

# Search by title
st.subheader("🔎 Search Anime by Title")
search_query = st.text_input("Enter anime title to search")
if search_query:
    search_results = df[df['title'].str.contains(search_query, case=False, na=False)]
    if not search_results.empty:
        st.subheader("📖 Search Results")
        st.dataframe(search_results[['title', 'score', 'episodes', 'members', 'genres']])
    else:
        st.warning("No matching anime found.")

# Full anime table
st.subheader("📋 All Anime")
st.dataframe(df)

# Genre-based recommendations
st.subheader("🔥 Top Anime by Genre")
genres = sorted(set(g.strip() for genre_list in df['genres'].dropna() for g in genre_list.split(',')))
selected_genre = st.selectbox("Choose a genre", genres)
top_filtered = recommend_by_genre(df, selected_genre)

for _, row in top_filtered.iterrows():
    st.image(row['image_url'], width=150)
    st.markdown(f"**{row['title']}**")
    st.markdown(f"⭐ Score: {row['score']} | 🎬 Episodes: {row['episodes']} | 👥 Members: {row['members']}")
    st.markdown("---")

# Similar title recommendations
st.subheader("🤝 Similar Anime by Title")
similar_query = st.text_input("Enter anime title to find similar ones")
if similar_query:
    similar_df = recommend_similar_titles(df, similar_query)
    if not similar_df.empty:
        for _, row in similar_df.iterrows():
            st.image(row['image_url'], width=150)
            st.markdown(f"**{row['title']}**")
            st.markdown(f"⭐ Score: {row['score']} | 🎬 Episodes: {row['episodes']} | 👥 Members: {row['members']}")
            st.markdown("---")
    else:
        st.warning("❌ No similar anime found.")

# Smart recommendations using NLP
st.subheader("🤖 Smart Recommendations (NLP)")
smart_title = st.text_input("🎯 Enter anime title for smart recommendations")
if smart_title:
    smart_results = smart_recommend_by_title(df, smart_title)
    if not smart_results.empty:
        for _, row in smart_results.iterrows():
            st.image(row['image_url'], width=150)
            st.markdown(f"**{row['title']}**")
            st.markdown(f"⭐ Score: {row['score']} | 🎬 Episodes: {row['episodes']} | 👥 Members: {row['members']}")
            st.markdown("---")
    else:
        st.warning("❌ No smart recommendations found.")

# Genre popularity chart
st.subheader("📊 Genre Popularity")
genre_counts = {}
for genre_list in df['genres'].dropna():
    for genre in genre_list.split(','):
        genre = genre.strip()
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

genre_df = pd.DataFrame(list(genre_counts.items()), columns=['Genre', 'Count'])
genre_df = genre_df.sort_values(by='Count', ascending=False)
st.bar_chart(genre_df.set_index('Genre'))
