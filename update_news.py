import feedparser
import json
from datetime import datetime
from yahooquery import search
from transformers import pipeline

# ✅ AI 요약 모델 불러오기 (Hugging Face)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# ✅ RSS 피드 목록
RSS_FEEDS = [
    "https://feeds.feedburner.com/TechCrunch/",
    "https://feeds.bbci.co.uk/news/technology/rss.xml"
]

# ✅ 주식 티커 찾기 함수
def get_stock_ticker(company_name):
    result = search(company_name)
    if "quotes" in result and result["quotes"]:
        return result["quotes"][0]["symbol"]
    return "N/A"

# ✅ 뉴스 데이터 가져오기
news_list = []
for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:5]:  # 최신 5개 뉴스 가져오기
        title = entry.title
        summary = entry.summary if "summary" in entry else "내용 없음"

        # ✅ AI 뉴스 요약 적용
        ai_summary = summarizer(summary, max_length=100, min_length=30, do_sample=False)[0]['summary_text']

        # ✅ 뉴스 제목에서 기업명 추출 및 주식 티커 찾기
        words = title.split()
        matched_ticker = None
        for word in words:
            matched_ticker = get_stock_ticker(word)
            if matched_ticker != "N/A":
                break

        # ✅ 뉴스 영향 분석 (기본 키워드 기반)
        impact = "호재" if "up" in summary.lower() else "악재" if "down" in summary.lower() else "평범함"

        # ✅ 뉴스 데이터 저장
        news_list.append({
            "title": title,
            "summary": ai_summary,  # ✅ AI 요약 적용 (번역 없음)
            "date": entry.published if "published" in entry else datetime.today().strftime('%Y-%m-%d'),
            "tags": ["기술"],  # 기본 태그
            "stock_ticker": matched_ticker,
            "impact": impact
        })

# ✅ JSON 파일 저장
news_data = {
    "date": datetime.today().strftime('%Y-%m-%d'),
    "news": news_list
}

with open("news.json", "w", encoding="utf-8") as json_file:
    json.dump(news_data, json_file, ensure_ascii=False, indent=4)

print("✅ news.json 자동 업데이트 완료!")