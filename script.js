document.addEventListener("DOMContentLoaded", function () {
    fetch("https://daily-soup.github.io/news.json") // JSON 파일 불러오기
        .then(response => response.json()) // JSON 형식으로 변환
        .then(data => {
            const newsContainer = document.getElementById("news-container");
            newsContainer.innerHTML = ""; // 기존 내용 초기화

            data.news.forEach(newsItem => {
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
        })
        .catch(error => console.error("JSON 데이터를 불러오는 중 오류 발생:", error));
});