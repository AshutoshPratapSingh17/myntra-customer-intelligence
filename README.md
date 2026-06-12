# 🛍️ Myntra Customer Intelligence Dashboard

> AI-powered customer review analytics platform built with Python, Claude AI, SQLite, and Streamlit.

🔗 **Live Demo:** [Click here to view dashboard](https://myntra-customer-intelligence-fbtktg6v9bcesxxsglpmqk.streamlit.app/)

![Dashboard Preview](https://img.shields.io/badge/Status-Live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58-red)
![Claude AI](https://img.shields.io/badge/Claude-AI-orange)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue)

---

## 📌 Project Overview

This is an end-to-end Data Analytics portfolio project that:
- Scrapes customer reviews from Myntra
- Uses **Claude AI** to enrich unstructured review text into structured data
- Stores everything in a **SQLite** database
- Displays insights on a live **Streamlit** dashboard

---

## 🏗️ Project Architecture

```
Data Collection          Data Enrichment          Storage            Dashboard
─────────────────        ───────────────          ───────            ─────────
Web Scraping      →      Claude AI API    →       SQLite DB    →     Streamlit
(BeautifulSoup)          (Sentiment,              (customer_         (Plotly
                          Topic,                   intelligence       Charts +
                          Urgency,                 .db)               Filters)
                          Summary)
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.12** | Core language |
| **BeautifulSoup + Requests** | Web scraping |
| **Pandas** | Data cleaning and manipulation |
| **Claude AI (Anthropic API)** | NLP enrichment — sentiment, topic, urgency |
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

## 🤖 How Claude AI Was Used

Each review was passed to Claude API with this prompt structure:

```
Analyse this customer review and return ONLY a JSON object with:
- sentiment_score (1-10)
- primary_topic (Product Quality / Customer Service / Pricing / Shipping / Other)
- urgency_level (Low / Medium / High)
- key_issue_summary (one sentence)
```

Claude returned structured JSON which was parsed and stored in SQLite.

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
├── enriched_reviews.csv    # AI-enriched review dataset
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 📈 Future Improvements

- [ ] Scrape real-time reviews using Selenium
- [ ] Add 1000+ reviews using Kaggle dataset
- [ ] Add ML model to predict review sentiment
- [ ] Deploy with Docker on AWS
- [ ] Add email alerts for High Urgency spikes

---

## 👨‍💻 Author

**Ashutosh Pratap Singh**
- GitHub: [@AshutoshPratapSingh17](https://github.com/AshutoshPratapSingh17)
  

---

## ⭐ If you found this useful, please star the repository!
