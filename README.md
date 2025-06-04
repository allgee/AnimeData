
# Anime Recommender Project 🎌📊

A clean and practical data project that recommends anime titles based on genre using real-world ETL and SQL techniques.

It extracts anime data from MyAnimeList via the Jikan API, transforms it using Python and Pandas, loads it into a PostgreSQL database, and allows filtering and recommendation via a Streamlit interface.

---

## 🎯 Project Goals

- Practice full ETL (Extract → Transform → Load)
- Use SQL for filtering and analysis
- Showcase technical skills in Python, APIs, and data pipelines
- Create a portfolio-ready project for job applications

---

## 🧰 Tech Stack

- **Python** (3.10+)
- **Jikan API** (anime data source)
- **Pandas** for data cleaning
- **PostgreSQL + SQLAlchemy** for storage
- **Streamlit** for interactive interface
- *(Optional)*: Jupyter / matplotlib for deeper analysis

---

## 📁 Project Structure

```
anime-recommender-project/
├── etl/               # ETL scripts: extract, transform, load
├── db/                # DB config files or schemas
├── analysis/          # Recommendation logic
├── data/              # Raw or temp files
├── output/            # Analysis charts or exports
├── main.py            # Runs the ETL pipeline
├── app.py             # Streamlit app to explore data
├── requirements.txt   # Dependencies
├── .gitignore         # Ignored files
└── README.md
```

---

## 🚀 How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the ETL pipeline:
   ```bash
   python main.py
   ```

3. Launch the app:
   ```bash
   streamlit run app.py
   ```



---

## 🤝 License

This project is open-source under the MIT license.
