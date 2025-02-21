document.addEventListener("DOMContentLoaded", function () {
    fetch("https://daily-soup.github.io/news.json") // Fetch news JSON
        .then(response => response.json()) // Convert to JSON
        .then(data => {
            const newsContainer = document.getElementById("news-container");
            newsContainer.innerHTML = ""; // Clear previous content

            data.news.forEach(newsItem => {
                // Create news article element
                const article = document.createElement("article");
                article.innerHTML = `
                    <h3><a href="${newsItem.link}" target="_blank">${newsItem.title}</a></h3>
                    <p>${newsItem.summary}</p>
                    <p class="date">📅 ${newsItem.date}</p>
                    <div>
                        ${newsItem.tags.map(tag => `<span class="tag">#${tag}</span>`).join(" ")}
                        <span class="stock">${newsItem.stock_ticker}</span>
                        <span class="impact ${newsItem.impact.toLowerCase()}">${newsItem.impact}</span>
                    </div>
                `;
                newsContainer.appendChild(article);
            });
        })
        .catch(error => console.error("Error fetching news data:", error));
});

// 🔍 Stock ticker search function
function filterNews() {
    const searchInput = document.getElementById("searchInput").value.toUpperCase();
    fetch("https://daily-soup.github.io/news.json")
        .then(response => response.json())
        .then(data => {
            const filteredNews = data.news.filter(newsItem =>
                newsItem.stock_ticker.toUpperCase().includes(searchInput)
            );
            displayNews(filteredNews);
        });
}

// Function to display filtered news
function displayNews(newsArray) {
    const newsContainer = document.getElementById("news-container");
    newsContainer.innerHTML = "";

    newsArray.forEach(newsItem => {
        const article = document.createElement("article");
        article.innerHTML = `
            <h3>${newsItem.title}</h3>
            <p>${newsItem.summary}</p>
            <p class="date">📅 ${newsItem.date}</p>
            <div>
                ${newsItem.tags.map(tag => `<span class="tag">#${tag}</span>`).join(" ")}
                <span class="stock">${newsItem.stock_ticker}</span>
                <span class="impact ${newsItem.impact.toLowerCase()}">${newsItem.impact}</span>
            </div>
        `;
        newsContainer.appendChild(article);
    });
}
