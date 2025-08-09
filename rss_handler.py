import feedparser
from bs4 import BeautifulSoup

def extract_thumbnail(summary):
    """Extract the first image URL from the summary HTML, if any."""
    soup = BeautifulSoup(summary, 'html.parser')
    img = soup.find('img')
    if img and img.get('src'):
        return img['src']
    return None

def fetch_feed(url):
    """Fetch a single RSS feed and return parsed articles."""
    feed = feedparser.parse(url, request_headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    })
    status = getattr(feed, 'status', 'unknown')
    print(f"Parsing feed: {url}, status: {status}, entries: {len(feed.entries)}")
    articles = []
    for entry in feed.entries:
        print(f"Entry title: {entry.get('title')}")
        summary = entry.get('summary') or entry.get('description') or ''
        thumbnail = extract_thumbnail(summary)
        articles.append({
            'title': entry.get('title', 'No Title'),
            'summary': summary,
            'thumbnail': thumbnail,
            'link': entry.get('link', '')
        })
    return articles

def fetch_all_feeds(feed_list):
    """
    feed_list: List of dicts with keys: url, category/tag (optional)
    Returns a dict keyed by URL with values containing articles and category.
    """
    print("DEBUG: fetch_all_feeds called")
    all_feeds = {}
    for feed in feed_list:
        url = feed.get('url')
        if not url:
            continue
        articles = fetch_feed(url)
        all_feeds[url] = {
            'articles': articles,
            'category': feed.get('category', '')
        }
    return all_feeds
