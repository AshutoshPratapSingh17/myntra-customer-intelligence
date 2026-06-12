import sqlite3
import pandas as pd
from pathlib import Path

def setup():
    # Only run if database doesn't exist
    if Path("customer_intelligence.db").exists():
        print("Database already exists.")
        return

    print("Creating database from CSV...")
    
    # Read the enriched CSV
    df = pd.read_csv("enriched_reviews.csv")
    
    # Clean column names
    df.columns = (df.columns.str.strip().str.lower()
                  .str.replace(r'[\s\-]+', '_', regex=True))
    
    # Rename columns to match database schema
    rename_map = {"date": "review_date", "rating": "star_rating"}
    df.rename(columns={k: v for k, v in rename_map.items() 
                       if k in df.columns}, inplace=True)
    
    # Parse dates to ISO format
    if "review_date" in df.columns:
        df["review_date"] = pd.to_datetime(
            df["review_date"], dayfirst=True, errors="coerce"
        ).dt.strftime("%Y-%m-%d")
    
    # Create database and table
    conn = sqlite3.connect("customer_intelligence.db")
    conn.execute("PRAGMA journal_mode=WAL;")
    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id                INTEGER PRIMARY KEY AUTOINCREMENT,
        product_url       TEXT,
        reviewer_name     TEXT,
        star_rating       REAL,
        review_date       TEXT,
        review_title      TEXT,
        review_text       TEXT,
        helpful_count     TEXT,
        page_number       INTEGER,
        sentiment_score   INTEGER,
        primary_topic     TEXT,
        urgency_level     TEXT,
        key_issue_summary TEXT,
        loaded_at         TEXT DEFAULT (datetime('now'))
    )""")
    
    # Only insert columns that exist in both CSV and DB
    db_cols = ["product_url","reviewer_name","star_rating",
               "review_date","review_title","review_text",
               "helpful_count","page_number","sentiment_score",
               "primary_topic","urgency_level","key_issue_summary"]
    available = [c for c in db_cols if c in df.columns]
    
    df[available].to_sql("reviews", conn, 
                          if_exists="append", index=False)
    conn.commit()
    conn.close()
    print(f"Database created with {len(df)} rows!")

if __name__ == "__main__":
    setup()
