"""
=============================================================
  Phase 4: Customer Intelligence Dashboard  — Premium UI
=============================================================
Source  : customer_intelligence.db  (SQLite)
Stack   : Streamlit + Plotly + pandas + sqlite3

Run:
    pip install streamlit plotly pandas
    streamlit run app.py
"""

import sqlite3
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from setup_db import setup
setup()

# =============================================================================
# 0.  PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="Customer Intelligence · Myntra",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# 1.  PREMIUM CSS
# =============================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #080C14 !important;
    color: #F1F5F9 !important;
}

/* Force dark background everywhere */
.stApp, .stApp > div, .main, .main > div,
[data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"] {
    background-color: #080C14 !important;
}

/* Boost all body text brightness */
p, span, li { color: #E2E8F0; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0F1623; }
::-webkit-scrollbar-thumb { background: #2D3F5C; border-radius: 3px; }

/* ── Main content padding ── */
.main .block-container {
    padding: 1.5rem 2rem 3rem 2rem;
    max-width: 1400px;
}

/* ═══════════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1520 0%, #0A1018 100%);
    border-right: 1px solid #1E2D42;
}
[data-testid="stSidebar"] > div { padding: 0; }
[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
[data-testid="stSidebar"] strong,
[data-testid="stSidebar"] b { color: #E2E8F0 !important; }

/* Sidebar multiselect */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #131C2B !important;
    border: 1px solid #1E2D42 !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] span { color: #CBD5E1 !important; }
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: rgba(99,179,237,0.12) !important;
    border: 1px solid rgba(99,179,237,0.3) !important;
    border-radius: 4px !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] span { color: #63B3ED !important; }

/* Sidebar slider */
[data-testid="stSidebar"] [data-testid="stSlider"] div[role="slider"] {
    background: #63B3ED !important;
}

/* Sidebar divider */
[data-testid="stSidebar"] hr {
    border-color: #1E2D42 !important;
    margin: 1rem 0 !important;
}

/* ═══════════════════════════════════════════
   METRIC CARDS
═══════════════════════════════════════════ */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0D1520 0%, #111827 100%);
    border: 1px solid #1E2D42;
    border-radius: 16px;
    padding: 1.4rem 1.6rem 1.2rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}
[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #3B82F6, #8B5CF6, #06B6D4);
}
[data-testid="metric-container"]:hover {
    border-color: #3B82F6;
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(59,130,246,0.15);
}
[data-testid="stMetricLabel"] {
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #94A3B8 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 2.1rem !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    line-height: 1.2 !important;
}
[data-testid="stMetricDelta"] {
    font-size: 0.75rem !important;
    font-weight: 500 !important;
}
[data-testid="stMetricDelta"] svg { display: none !important; }

/* ═══════════════════════════════════════════
   CHART CONTAINERS
═══════════════════════════════════════════ */
.chart-card {
    background: linear-gradient(135deg, #0D1520 0%, #0F1A27 100%);
    border: 1px solid #1E2D42;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
}

/* ═══════════════════════════════════════════
   SECTION HEADERS
═══════════════════════════════════════════ */
.section-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #60A5FA;
    margin-bottom: 0.25rem;
}
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 1rem;
    text-shadow: 0 1px 3px rgba(0,0,0,0.5);
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #1E2D42;
}

/* ═══════════════════════════════════════════
   REVIEW CARDS
═══════════════════════════════════════════ */
.review-card {
    background: linear-gradient(135deg, #0D1520 0%, #0F1A27 100%);
    border: 1px solid #1E2D42;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.875rem;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}
.review-card:hover {
    border-color: #2D4A6E;
    box-shadow: 0 4px 24px rgba(59,130,246,0.08);
    transform: translateX(3px);
}
.review-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 3px 0 0 3px;
}
.review-card.high::before   { background: #EF4444; }
.review-card.medium::before { background: #F59E0B; }
.review-card.low::before    { background: #10B981; }

.review-meta {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.6rem;
    flex-wrap: wrap;
}
.reviewer-name {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    color: #FFFFFF;
}
.review-date {
    font-size: 0.75rem;
    color: #64748B;
}
.badge {
    display: inline-flex;
    align-items: center;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.badge-high     { background: rgba(239,68,68,0.12);  color: #FCA5A5; border: 1px solid rgba(239,68,68,0.25); }
.badge-medium   { background: rgba(245,158,11,0.12); color: #FCD34D; border: 1px solid rgba(245,158,11,0.25); }
.badge-low      { background: rgba(16,185,129,0.12); color: #6EE7B7; border: 1px solid rgba(16,185,129,0.25); }
.badge-topic    { background: rgba(59,130,246,0.12); color: #93C5FD; border: 1px solid rgba(59,130,246,0.25); }
.badge-score    { background: rgba(139,92,246,0.12); color: #C4B5FD; border: 1px solid rgba(139,92,246,0.25); }

.stars { color: #FBBF24; font-size: 0.8rem; letter-spacing: 1px; }

.ai-summary {
    font-size: 0.82rem;
    color: #CBD5E1;
    font-style: italic;
    line-height: 1.5;
    padding: 0.5rem 0.75rem;
    background: rgba(59,130,246,0.05);
    border-left: 2px solid rgba(59,130,246,0.3);
    border-radius: 0 6px 6px 0;
    margin: 0.5rem 0;
}
.review-text-content {
    font-size: 0.85rem;
    color: #FFFFFF;
    line-height: 1.6;
    margin-top: 0.5rem;
}

/* ═══════════════════════════════════════════
   DOWNLOAD BUTTON
═══════════════════════════════════════════ */
[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #1D4ED8, #7C3AED) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.03em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(124,58,237,0.3) !important;
}
[data-testid="stDownloadButton"] button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.45) !important;
}

/* ═══════════════════════════════════════════
   INFO / EMPTY STATE
═══════════════════════════════════════════ */
[data-testid="stInfo"] {
    background: rgba(59,130,246,0.08) !important;
    border: 1px solid rgba(59,130,246,0.2) !important;
    border-radius: 12px !important;
    color: #93C5FD !important;
}

/* ── Hide Streamlit chrome ── */
footer, #MainMenu, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 2.  COLOUR PALETTE & THEME
# =============================================================================

PALETTE = {
    "bg":       "#080C14",
    "card":     "#0D1520",
    "card2":    "#0F1A27",
    "border":   "#1E2D42",
    "text":     "#94A3B8",
    "text2":    "#CBD5E1",
    "heading":  "#F1F5F9",
    "accent":   "#3B82F6",
    "purple":   "#8B5CF6",
    "cyan":     "#06B6D4",
    "green":    "#10B981",
    "yellow":   "#F59E0B",
    "red":      "#EF4444",
}

TOPIC_COLOURS = {
    "Product Quality":    "#3B82F6",
    "Customer Service":   "#10B981",
    "Pricing":            "#F59E0B",
    "Shipping/Delivery":  "#EF4444",
    "Other":              "#8B5CF6",
}

URGENCY_COLOURS = {
    "Low":    "#10B981",
    "Medium": "#F59E0B",
    "High":   "#EF4444",
}

def dark_theme(fig: go.Figure, height: int = 340) -> go.Figure:
    fig.update_layout(
        paper_bgcolor=PALETTE["card"],
        plot_bgcolor=PALETTE["card"],
        font=dict(family="Inter", color=PALETTE["text"], size=12),
        xaxis=dict(gridcolor=PALETTE["border"], linecolor=PALETTE["border"],
                   tickfont=dict(color=PALETTE["text"]), showgrid=True,
                   title_font=dict(color=PALETTE["text"])),
        yaxis=dict(gridcolor=PALETTE["border"], linecolor=PALETTE["border"],
                   tickfont=dict(color=PALETTE["text"]), showgrid=True,
                   title_font=dict(color=PALETTE["text"])),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=PALETTE["border"],
                    font=dict(color=PALETTE["text"])),
        margin=dict(l=12, r=12, t=12, b=12),
        height=height,
        hoverlabel=dict(
            bgcolor="#0D1520",
            bordercolor=PALETTE["border"],
            font=dict(color="#F1F5F9", size=13),
        ),
    )
    return fig

# =============================================================================
# 3.  DATA LAYER
# =============================================================================

DB_PATH = "customer_intelligence.db"

@st.cache_resource
def get_connection():
    if not Path(DB_PATH).exists():
        st.error(f"Database '{DB_PATH}' not found. Run `load_to_db.py` first.")
        st.stop()
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@st.cache_data(ttl=60)
def load_reviews() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT id, reviewer_name, star_rating, review_date, review_title,
               review_text, helpful_count, sentiment_score,
               primary_topic, urgency_level, key_issue_summary
        FROM reviews ORDER BY review_date ASC
    """, conn)
    df["review_date_dt"] = pd.to_datetime(df["review_date"], errors="coerce")
    df["month"] = df["review_date_dt"].dt.to_period("M").astype(str)
    return df

# =============================================================================
# 4.  SIDEBAR
# =============================================================================

with st.sidebar:
    # Logo / brand block
    st.markdown("""
    <div style="padding:1.75rem 1.25rem 1rem 1.25rem;">
      <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.35rem;">
        <span style="font-size:1.5rem;">🛍️</span>
        <span style="font-family:'Space Grotesk',sans-serif;font-size:1.05rem;
                     font-weight:700;color:#F1F5F9;letter-spacing:-0.01em;">
          Customer Intel
        </span>
      </div>
      <div style="font-size:0.72rem;color:#334155;letter-spacing:0.08em;
                  text-transform:uppercase;padding-left:0.1rem;">
        Myntra · AI Review Analytics
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    df_full = load_reviews()

    st.markdown('<p style="font-size:0.68rem;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:#3B82F6;margin-bottom:0.5rem;">🎯 Filters</p>', unsafe_allow_html=True)

    all_topics = sorted(df_full["primary_topic"].dropna().unique().tolist())
    sel_topics = st.multiselect("Topic", options=all_topics, default=all_topics)

    all_urgency = ["Low", "Medium", "High"]
    sel_urgency = st.multiselect("Urgency Level", options=all_urgency, default=all_urgency)

    st.markdown('<p style="font-size:0.78rem;font-weight:500;color:#64748B;margin:0.75rem 0 0.25rem 0;">Sentiment Range</p>', unsafe_allow_html=True)
    sent_min, sent_max = st.slider("", min_value=1, max_value=10,
                                    value=(1, 10), label_visibility="collapsed")

    st.divider()
    st.markdown(f"""
    <div style="padding:0 0.25rem;">
      <p style="font-size:0.68rem;color:#1E3A5F;text-transform:uppercase;
                letter-spacing:0.1em;font-weight:600;margin-bottom:0.5rem;">Data Source</p>
      <p style="font-size:0.75rem;color:#334155;">📦 customer_intelligence.db</p>
      <p style="font-size:0.75rem;color:#334155;">🤖 Enriched via Claude AI</p>
      <p style="font-size:0.75rem;color:#334155;">📅 Jan – Mar 2024</p>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# 5.  FILTER DATA
# =============================================================================

mask = (
    df_full["primary_topic"].isin(sel_topics)
    & df_full["urgency_level"].isin(sel_urgency)
    & df_full["sentiment_score"].between(sent_min, sent_max, inclusive="both")
)
df = df_full[mask].copy()

# =============================================================================
# 6.  PAGE HEADER
# =============================================================================

st.markdown("""
<div style="padding:0.5rem 0 1.75rem 0;">
  <p style="font-size:0.7rem;font-weight:600;letter-spacing:0.15em;text-transform:uppercase;
            color:#3B82F6;margin-bottom:0.3rem;">📊 Analytics Dashboard</p>
  <h1 style="font-family:'Space Grotesk',sans-serif;font-size:2.1rem;font-weight:700;
             color:#FFFFFF;margin:0 0 0.3rem 0;line-height:1.1;text-shadow:0 0 60px rgba(59,130,246,0.5),">
    Customer Intelligence
  </h1>
  <p style="font-size:0.9rem;color:#94A3B8;margin:0;">
    AI-powered review analysis · Myntra Product Feedback · Powered by Claude
  </p>
</div>
""", unsafe_allow_html=True)

if df.empty:
    st.info("No reviews match your current filters — try widening the sidebar selections.")
    st.stop()

# =============================================================================
# 7.  KPI CARDS
# =============================================================================

total_reviews = len(df)
avg_sentiment = df["sentiment_score"].mean()
high_urgency  = (df["urgency_level"] == "High").sum()
avg_star      = df["star_rating"].mean()
pct_positive  = int((df["sentiment_score"] >= 7).sum() / total_reviews * 100) if total_reviews else 0

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("📝 Total Reviews", f"{total_reviews:,}")
with c2:
    label = "🟢 Positive" if avg_sentiment >= 6 else "🔴 Negative"
    st.metric("💬 Avg Sentiment", f"{avg_sentiment:.1f} / 10", delta=label)
with c3:
    pct = int(high_urgency / total_reviews * 100) if total_reviews else 0
    st.metric("🚨 High Urgency", f"{high_urgency:,}", delta=f"{pct}% of reviews", delta_color="inverse")
with c4:
    st.metric("⭐ Avg Star Rating", f"{avg_star:.1f} / 5" if pd.notna(avg_star) else "N/A")
with c5:
    st.metric("😊 Positive Reviews", f"{pct_positive}%", delta="sentiment ≥ 7")

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# =============================================================================
# 8.  ROW 1 — Bar + Donut
# =============================================================================

col_l, col_r = st.columns([1.15, 0.85], gap="large")

with col_l:
    st.markdown('<p class="section-label">Distribution</p><p class="section-title">Reviews by Topic</p>', unsafe_allow_html=True)

    tc = (df.groupby("primary_topic", as_index=False)
            .agg(count=("id","count"), avg_sent=("sentiment_score","mean"))
            .sort_values("count", ascending=False))
    tc["color"] = tc["primary_topic"].map(TOPIC_COLOURS)

    fig_bar = go.Figure(go.Bar(
        x=tc["primary_topic"],
        y=tc["count"],
        marker=dict(
            color=tc["color"].tolist(),
            opacity=0.85,
            line=dict(color="rgba(0,0,0,0)", width=0),
        ),
        text=tc["count"],
        textposition="outside",
        textfont=dict(color="#F1F5F9", size=13, family="Space Grotesk"),
        hovertemplate="<b>%{x}</b><br>Reviews: %{y}<br>Avg Sentiment: %{customdata:.1f}<extra></extra>",
        customdata=tc["avg_sent"],
    ))
    fig_bar = dark_theme(fig_bar, height=320)
    fig_bar.update_layout(
        xaxis_title=None, yaxis_title="Reviews",
        showlegend=False,
        bargap=0.35,
    )
    fig_bar.update_traces(marker_line_width=0)
    st.plotly_chart(fig_bar, use_container_width=True)

with col_r:
    st.markdown('<p class="section-label">Breakdown</p><p class="section-title">Urgency Distribution</p>', unsafe_allow_html=True)

    uc = df["urgency_level"].value_counts().reset_index()
    uc.columns = ["urgency_level", "count"]

    fig_donut = go.Figure(go.Pie(
        labels=uc["urgency_level"],
        values=uc["count"],
        hole=0.62,
        marker=dict(
            colors=[URGENCY_COLOURS.get(u, "#888") for u in uc["urgency_level"]],
            line=dict(color=PALETTE["card"], width=3),
        ),
        textinfo="label+percent",
        textfont=dict(color="#F1F5F9", size=12),
        hovertemplate="<b>%{label}</b><br>%{value} reviews (%{percent})<extra></extra>",
        pull=[0.03 if u == "High" else 0 for u in uc["urgency_level"]],
    ))
    fig_donut.add_annotation(
        text=f"<b style='font-size:22px'>{total_reviews}</b><br>reviews",
        x=0.5, y=0.5, showarrow=False,
        font=dict(family="Space Grotesk", size=15, color="#F1F5F9"),
        align="center",
    )
    fig_donut = dark_theme(fig_donut, height=320)
    fig_donut.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5),
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# =============================================================================
# 9.  ROW 2 — Sentiment trend (full width)
# =============================================================================

st.markdown('<p class="section-label">Timeline</p><p class="section-title">Sentiment Trend Over Time</p>', unsafe_allow_html=True)

trend = (df.dropna(subset=["review_date_dt","sentiment_score"])
           .groupby("month", as_index=False)
           .agg(avg_sentiment=("sentiment_score","mean"), count=("id","count"))
           .sort_values("month"))

if len(trend) < 2:
    st.info("Need reviews across at least 2 months to show a trend.")
else:
    fig_line = go.Figure()

    # Gradient fill under the line
    fig_line.add_trace(go.Scatter(
        x=pd.concat([trend["month"], trend["month"].iloc[::-1]]),
        y=pd.concat([trend["avg_sentiment"] + 0.6, (trend["avg_sentiment"] - 0.6).iloc[::-1]]),
        fill="toself",
        fillcolor="rgba(59,130,246,0.07)",
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip", showlegend=False,
    ))
    # Area fill to zero
    fig_line.add_trace(go.Scatter(
        x=trend["month"], y=trend["avg_sentiment"].round(2),
        fill="tozeroy", fillcolor="rgba(59,130,246,0.04)",
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip", showlegend=False,
    ))
    # Main line
    fig_line.add_trace(go.Scatter(
        x=trend["month"], y=trend["avg_sentiment"].round(2),
        mode="lines+markers",
        line=dict(color="#3B82F6", width=3, shape="spline", smoothing=0.8),
        marker=dict(size=9, color="#3B82F6",
                    line=dict(color="#080C14", width=2.5),
                    symbol="circle"),
        name="Avg Sentiment",
        hovertemplate="<b>%{x}</b><br>Avg Sentiment: <b>%{y}</b><br>Reviews: %{customdata}<extra></extra>",
        customdata=trend["count"],
    ))
    # Neutral line
    fig_line.add_hline(y=5.5, line=dict(color="#1E2D42", dash="dot", width=1.5),
                       annotation_text="Neutral 5.5",
                       annotation_font=dict(color="#334155", size=10),
                       annotation_position="bottom right")

    fig_line = dark_theme(fig_line, height=300)
    fig_line.update_layout(
        xaxis_title=None, yaxis_title="Avg Sentiment Score",
        yaxis=dict(range=[0, 11]),
        showlegend=False,
    )
    st.plotly_chart(fig_line, use_container_width=True)

# =============================================================================
# 10.  ROW 3 — Pain-point + Sentiment heatmap
# =============================================================================

col_a, col_b = st.columns([1, 1], gap="large")

with col_a:
    st.markdown('<p class="section-label">Pain Points</p><p class="section-title">Topics by Lowest Sentiment</p>', unsafe_allow_html=True)

    pain = (df.dropna(subset=["primary_topic","sentiment_score"])
              .groupby("primary_topic", as_index=False)
              .agg(avg_sentiment=("sentiment_score","mean"),
                   high_urg=("urgency_level", lambda x:(x=="High").sum()),
                   total=("id","count"))
              .sort_values("avg_sentiment"))

    fig_pain = go.Figure(go.Bar(
        x=pain["avg_sentiment"].round(2),
        y=pain["primary_topic"],
        orientation="h",
        marker=dict(
            color=pain["avg_sentiment"],
            colorscale=[[0,"#EF4444"],[0.5,"#F59E0B"],[1,"#10B981"]],
            cmin=1, cmax=10,
            showscale=True,
            colorbar=dict(
                title=dict(text="Score", font=dict(color=PALETTE["text"], size=10)),
                tickfont=dict(color=PALETTE["text"], size=10),
                thickness=10, len=0.8,
            ),
        ),
        text=[f"{v:.1f}" for v in pain["avg_sentiment"]],
        textposition="outside",
        textfont=dict(color="#F1F5F9", size=12, family="Space Grotesk"),
        hovertemplate="<b>%{y}</b><br>Avg Sentiment: %{x:.1f}<br>High Urgency: %{customdata[0]}<br>Total: %{customdata[1]}<extra></extra>",
        customdata=pain[["high_urg","total"]].values,
    ))
    fig_pain = dark_theme(fig_pain, height=300)
    fig_pain.update_layout(xaxis=dict(title="Avg Sentiment", range=[0,12]), yaxis_title=None, showlegend=False)
    st.plotly_chart(fig_pain, use_container_width=True)

with col_b:
    st.markdown('<p class="section-label">Urgency Mix</p><p class="section-title">Topic × Urgency Breakdown</p>', unsafe_allow_html=True)

    cross = df.groupby(["primary_topic","urgency_level"]).size().reset_index(name="count")
    pivot = cross.pivot(index="primary_topic", columns="urgency_level", values="count").fillna(0)

    fig_stack = go.Figure()
    for urg, colour in URGENCY_COLOURS.items():
        if urg in pivot.columns:
            fig_stack.add_trace(go.Bar(
                name=urg,
                x=pivot.index.tolist(),
                y=pivot[urg].tolist(),
                marker_color=colour,
                marker_opacity=0.85,
                hovertemplate=f"<b>%{{x}}</b><br>{urg}: %{{y}}<extra></extra>",
            ))
    fig_stack = dark_theme(fig_stack, height=300)
    fig_stack.update_layout(
        barmode="stack", xaxis_title=None, yaxis_title="Reviews",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        bargap=0.3,
    )
    st.plotly_chart(fig_stack, use_container_width=True)

# =============================================================================
# 11.  REVIEW CARDS
# =============================================================================

st.markdown('<p class="section-label">Detail View</p><p class="section-title">Customer Reviews</p>', unsafe_allow_html=True)

col_sort, col_count, _ = st.columns([1, 1, 3])
with col_sort:
    sort_by = st.selectbox("Sort by", ["Date (newest)", "Date (oldest)", "Sentiment (high→low)", "Sentiment (low→high)"], label_visibility="collapsed")
with col_count:
    show_n = st.selectbox("Show", [10, 20, 30, "All"], label_visibility="collapsed")

sort_map = {
    "Date (newest)":        ("review_date_dt", False),
    "Date (oldest)":        ("review_date_dt", True),
    "Sentiment (high→low)": ("sentiment_score", False),
    "Sentiment (low→high)": ("sentiment_score", True),
}
s_col, s_asc = sort_map[sort_by]
df_sorted = df.sort_values(s_col, ascending=s_asc)
df_show   = df_sorted if show_n == "All" else df_sorted.head(int(show_n))

def stars(n):
    if pd.isna(n): return ""
    filled = int(n)
    return "★" * filled + "☆" * (5 - filled)

def urgency_badge(u):
    cls = {"High":"badge-high","Medium":"badge-medium","Low":"badge-low"}.get(u,"")
    return f'<span class="badge {cls}">{u}</span>' if u else ""

def score_colour(s):
    if pd.isna(s): return "#64748B"
    if s >= 7: return "#10B981"
    if s >= 5: return "#F59E0B"
    return "#EF4444"

for _, row in df_show.iterrows():
    urg   = str(row.get("urgency_level","") or "")
    score = row.get("sentiment_score")
    topic = str(row.get("primary_topic","") or "")
    name  = str(row.get("reviewer_name","Anonymous") or "Anonymous")
    date  = str(row.get("review_date","") or "")
    star  = row.get("star_rating")
    summ  = str(row.get("key_issue_summary","") or "")
    text  = str(row.get("review_text","") or "")
    title = str(row.get("review_title","") or "")

    card_class = urg.lower() if urg in ["High","Medium","Low"] else "low"
    sc_colour  = score_colour(score)
    score_txt  = f"{int(score)}/10" if pd.notna(score) else "—"

    st.markdown(f"""
    <div class="review-card {card_class}">
      <div class="review-meta">
        <span class="reviewer-name">{name}</span>
        <span class="review-date">📅 {date}</span>
        <span class="stars">{stars(star)}</span>
        <span class="badge badge-topic">{topic}</span>
        {urgency_badge(urg)}
        <span class="badge badge-score" style="color:{sc_colour};border-color:{sc_colour}44;background:{sc_colour}18;">
          🧠 {score_txt}
        </span>
      </div>
      {"<div style='font-size:0.88rem;font-weight:600;color:#CBD5E1;margin-bottom:0.4rem;'>"+title+"</div>" if title else ""}
      {"<div class='ai-summary'>💡 " + summ + "</div>" if summ else ""}
      <div class="review-text-content">{text}</div>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# 12.  DOWNLOAD
# =============================================================================

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

dl_df = df_show[["review_date","reviewer_name","star_rating","primary_topic",
                  "urgency_level","sentiment_score","key_issue_summary","review_text"]].copy()
dl_df.columns = ["Date","Reviewer","Stars","Topic","Urgency","Sentiment","AI Summary","Review"]

st.download_button(
    label="⬇  Download filtered reviews as CSV",
    data=dl_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_reviews.csv",
    mime="text/csv",
)

# Footer
st.markdown("""
<div style="margin-top:3rem;padding-top:1.5rem;border-top:1px solid #1E2D42;
            text-align:center;font-size:0.72rem;color:#1E2D42;">
  Customer Intelligence Dashboard · Built with Streamlit + Claude AI · Myntra Reviews 2024
</div>
""", unsafe_allow_html=True)
