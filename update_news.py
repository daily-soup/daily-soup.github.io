import feedparser
import json
from datetime import datetime
from yahooquery import search  # Yahoo Finance API 사용

# ✅ 1. RSS 피드 목록 (기술 뉴스)
RSS_FEEDS = [
    "https://feeds.feedburner.com/TechCrunch/",
    "https://feeds.bbci.co.uk/news/technology/rss.xml"
]

# ✅ 2. Yahoo Finance를 활용하여 기업명 → 주식 티커 변환
def get_stock_ticker(company_name):
    result = search(company_name)  # Yahoo Finance API 검색
    if "quotes" in result and result["quotes"]:
        return result["quotes"][0]["symbol"]  # 첫 번째 검색 결과의 티커 반환
    return "N/A"  # 없으면 N/A 반환

# ✅ 3. 뉴스 데이터 가져오기
news_list = []
for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:5]:  # 최신 5개 뉴스 가져오기
        title = entry.title
        summary = entry.summary if "summary" in entry else "내용 없음"

        # ✅ 4. 뉴스 제목에서 기업명 추출 및 주식 티커 찾기
        words = title.split()  # 제목을 단어 단위로 분리
        matched_ticker = None
        for word in words:
            matched_ticker = get_stock_ticker(word)
            if matched_ticker != "N/A":
                break  # 첫 번째로 매칭된 주식 티커 사용

        # ✅ 5. 뉴스 영향 분석 (간단한 키워드 기반)
        impact = "호재" if "up" in summary.lower() else "악재" if "down" in summary.lower() else "평범함"

        # ✅ 6. 뉴스 데이터 저장
        news_list.append({
            "title": title,
            "summary": summary,
            "tags": ["기술"],  # 현재는 임시 태그
            "stock_ticker": matched_ticker,
            "impact": impact
        })

# ✅ 7. JSON 파일 저장
news_data = {
    "date": datetime.today().strftime('%Y-%m-%d'),
    "news": news_list
}

with open("news.json", "w", encoding="utf-8") as json_file:
    json.dump(news_data, json_file, ensure_ascii=False, indent=4)

print("✅ news.json 자동 업데이트 완료!")