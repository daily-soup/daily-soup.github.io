import feedparser
import json
from datetime import datetime
from yahooquery import search
from transformers import pipeline

# ✅ AI Summarization Model (Hugging Face)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# ✅ U.S. Stock Market News RSS Feeds
RSS_FEEDS = [
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",  # CNBC U.S. Markets
    "https://www.marketwatch.com/rss/topstories",  # MarketWatch Top Stories
    "https://www.reutersagency.com/feed/?best-sectors=stocks&post_type=best",  # Reuters Stocks
]

# ✅ Function to Find Stock Ticker
def get_stock_ticker(company_name):
    result = search(company_name)
    if "quotes" in result and result["quotes"]:
        return result["quotes"][0]["symbol"]
    return "N/A"

# ✅ Fetch News Data
news_list = []
for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:5]:  # Fetch latest 5 articles
        title = entry.title
        summary = entry.summary if "summary" in entry else "No description available"
        link = entry.link if "link" in entry else "#"  # ✅ RSS 원문 뉴스 링크 저장

        # ✅ AI Summarization
        ai_summary = summarizer(summary, max_length=100, min_length=30, do_sample=False)[0]['summary_text']

        # ✅ Find Stock Ticker from Title
        words = title.split()
        matched_ticker = None
        for word in words:
            matched_ticker = get_stock_ticker(word)
            if matched_ticker != "N/A":
                break

        # ✅ Market Sentiment Analysis (Simple Keyword-Based)
        impact = "Bullish" if "up" in summary.lower() else "Bearish" if "down" in summary.lower() else "Neutral"

        # ✅ Store News Data
        news_list.append({
            "title": title,
            "link": link,  # ✅ 뉴스 원문 링크 추가
            "summary": ai_summary,
            "date": entry.published if "published" in entry else datetime.today().strftime('%Y-%m-%d'),
            "tags": ["Finance", "Stocks"],  # Default tags
            "stock_ticker": matched_ticker,
            "impact": impact
        })

# ✅ Save JSON File
news_data = {
    "date": datetime.today().strftime('%Y-%m-%d'),
    "news": news_list
}

with open("news.json", "w", encoding="utf-8") as json_file:
    json.dump(news_data, json_file, ensure_ascii=False, indent=4)

print("✅ news.json updated successfully!")