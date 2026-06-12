# 🛍️ Myntra Customer Intelligence Dashboard

> An end-to-end customer review analytics platform built with Python, NLP, SQLite, and Streamlit.

🔗 **Live Demo:** [Click here to view dashboard](YOUR_STREAMLIT_URL_HERE)

![Dashboard Preview](https://img.shields.io/badge/Status-Live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58-red)
![NLP](https://img.shields.io/badge/NLP-Pipeline-purple)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue)

---

## 📌 Project Overview

This is an end-to-end Data Analytics portfolio project that:
- Collects customer reviews from Myntra using web scraping
- Processes unstructured review text through an **NLP enrichment pipeline**
- Stores structured data in a **SQLite** database
- Displays business insights on a live interactive **Streamlit** dashboard

---

## 🏗️ Project Architecture

```
Data Collection       NLP Enrichment         Storage           Dashboard
────────────────      ──────────────         ───────           ─────────
Web Scraping    →     NLP Pipeline   →       SQLite DB   →     Streamlit
(BeautifulSoup)       (Sentiment,            (customer_        (Plotly
                       Topic,                 intelligence      Charts +
                       Urgency,               .db)              Filters)
                       Summary)
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.12** | Core language |
| **BeautifulSoup + Requests** | Web scraping |
| **Pandas** | Data cleaning and manipulation |
| **NLP Pipeline** | Sentiment scoring, topic classification, urgency detection |
| **SQLite** | Local database engine |
| **Plotly** | Interactive charts |
| **Streamlit** | Web dashboard |

---

## 📊 Dashboard Features

- 🎯 **Sidebar Filters** — Filter by Topic, Urgency Level, Sentiment Score
- 📈 **KPI Cards** — Total Reviews, Avg Sentiment, High Urgency Count, Avg Star Rating
- 📊 **Bar Chart** — Review distribution across topics
- 🍩 **Donut Chart** — Urgency level breakdown
- 📉 **Line Chart** — Sentiment trend over time
- 🔥 **Pain Point Radar** — Topics ranked by lowest sentiment
- 📋 **Review Cards** — Full review detail with AI-generated summaries
- ⬇️ **CSV Export** — Download filtered data

---

## 🔍 Key Business Insights

- **Product Quality** is the #1 complaint driver — 73% of all reviews
- **High Urgency** issues account for 23% of total reviews
- **Average Sentiment Score** is 6.2/10 — indicating room for improvement
- Sentiment **dropped significantly** for reviews mentioning returns/refunds

---

## 🤖 NLP Enrichment Pipeline

Each review was processed through an NLP pipeline that extracts:

```
Input  → Raw unstructured review text

Output → {
    "sentiment_score"   : 1–10 (very negative to very positive),
    "primary_topic"     : Product Quality / Customer Service /
                          Pricing / Shipping / Other,
    "urgency_level"     : Low / Medium / High,
    "key_issue_summary" : One sentence summary of main complaint
}
```

This transforms raw text into structured data ready for business analysis.

---

## 🚀 Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/AshutoshPratapSingh17/myntra-customer-intelligence.git
cd myntra-customer-intelligence
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the dashboard
```bash
streamlit run app.py
```

### 4. Open in browser
```
http://localhost:8501
```

---

## 📁 Project Structure

```
myntra-customer-intelligence/
├── app.py                  # Main Streamlit dashboard
├── setup_db.py             # Auto-creates SQLite database from CSV
├── enriched_reviews.csv    # NLP-enriched review dataset
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 📈 Future Improvements

- [ ] Scrape real-time reviews using Selenium
- [ ] Scale to 10,000+ reviews using larger dataset
- [ ] Add ML model to predict review sentiment
- [ ] Deploy with Docker on AWS
- [ ] Add email alerts for High Urgency spikes
- [ ] Integrate with live Myntra product API

---

## 👨‍💻 Author

**Ashutosh Pratap Singh**
- GitHub: [@AshutoshPratapSingh17](https://github.com/AshutoshPratapSingh17)
  

---

⭐ **If you found this useful, please star the repository!**
