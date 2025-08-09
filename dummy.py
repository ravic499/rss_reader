# Assume your feeds list
test_feeds = [
    {"url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml", "category": "News"},
    {"url": "https://xkcd.com/rss.xml", "category": "Comics"}
]

from rss_handler import fetch_all_feeds

all_articles = fetch_all_feeds(test_feeds)

for feed in test_feeds:
    url = feed['url']
    articles = all_articles.get(url, {}).get('articles', [])
    print(f"Feed URL: {url}")
    print(f"Number of articles: {len(articles)}")
    if articles:
        print("Sample article title:", articles[0]['title'])
    print('---')
