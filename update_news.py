import feedparser
import json
from datetime import datetime

# ✅ 1. 사용할 RSS 피드 목록
RSS_FEEDS = [
    "https://feeds.feedburner.com/TechCrunch/",
    "https://feeds.bbci.co.uk/news/technology/rss.xml"
]

# ✅ 2. 주식 티커 매칭 데이터 (예제)
STOCK_TICKERS = {
    "Apple": "AAPL",
    "Google": "GOOGL",
    "Microsoft": "MSFT",
    "Samsung": "005930.KQ",
    "Tesla": "TSLA"
}

# ✅ 3. 뉴스 데이터 가져오기
news_list = []
for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)
    
    for entry in feed.entries[:5]:  # 최신 5개 뉴스만 가져오기
        title = entry.title
        summary = entry.summary if "summary" in entry else "내용 없음"
        
        # ✅ 4. 관련 주식 찾기
        matched_ticker = None
        for company, ticker in STOCK_TICKERS.items():
            if company.lower() in title.lower():
                matched_ticker = ticker
                break

        # ✅ 5. 뉴스 영향 분석 (임시: 랜덤 값 사용)
        impact = "호재" if "up" in summary.lower() else "악재" if "down" in summary.lower() else "평범함"
        
        # ✅ 6. 뉴스 데이터 저장
        news_list.append({
            "title": title,
            "summary": summary,
            "tags": ["기술"],  # 현재는 임시 태그
            "stock_ticker": matched_ticker if matched_ticker else "N/A",
            "impact": impact
        })

# ✅ 7. JSON 파일 저장
news_data = {
    "date": datetime.today().strftime('%Y-%m-%d'),
    "news": news_list
}

with open("news.json", "w", encoding="utf-8") as json_file:
    json.dump(news_data, json_file, ensure_ascii=False, indent=4)

print("✅ news.json 업데이트 완료!")