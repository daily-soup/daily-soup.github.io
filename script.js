document.addEventListener("DOMContentLoaded", function () {
    fetch("https://daily-soup.github.io/news.json") // JSON 파일 불러오기
        .then(response => response.json()) // JSON 변환
        .then(data => {
            const newsContainer = document.getElementById("news-container");
            newsContainer.innerHTML = ""; // 기존 내용 초기화

            data.news.forEach(newsItem => {
                // 뉴스 항목 생성
                const article = document.createElement("article");
                article.innerHTML = `
                    <h3>${newsItem.title}</h3>
                    <p>${newsItem.summary}</p>
                    <small class="date">🗓 ${newsItem.date}</small>
                    <div>
                        ${newsItem.tags.map(tag => `<span class="tag">#${tag}</span>`).join(" ")}
                        <span class="stock">${newsItem.stock_ticker}</span>
                        <span class="impact ${newsItem.impact}">${newsItem.impact}</span>
                    </div>
                `;
                newsContainer.appendChild(article);
            });
        })
        .catch(error => console.error("JSON 데이터를 불러오는 중 오류 발생:", error));
});

// 뉴스 목록을 표시하는 함수
function displayNews(newsArray) {
    const newsContainer = document.getElementById("news-container");
    newsContainer.innerHTML = ""; // 기존 내용 초기화

    newsArray.forEach(newsItem => {
        // 뉴스 항목 생성
        const article = document.createElement("article");
        article.innerHTML = `
            <h3>${newsItem.title}</h3>
            <p>${newsItem.summary}</p>
            <div>
                ${newsItem.tags.map(tag => `<span class="tag">#${tag}</span>`).join(" ")}
                <span class="stock">${newsItem.stock_ticker}</span>
                <span class="impact ${newsItem.impact}">${newsItem.impact}</span>
            </div>
        `;
        newsContainer.appendChild(article);
    });
}

// 🔍 검색 기능: 사용자가 입력한 티커에 맞는 뉴스만 필터링
function filterNews() {
    const searchInput = document.getElementById("searchInput").value.toUpperCase(); // 입력값 대문자로 변환
    const filteredNews = window.newsData.filter(newsItem =>
        newsItem.stock_ticker.toUpperCase().includes(searchInput)
    );
    displayNews(filteredNews); // 필터링된 결과 출력
}