# rss_handler.py

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
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        thumbnail = extract_thumbnail(entry.get('summary', ''))
        articles.append({
            'title': entry.get('title', 'No Title'),
            'summary': entry.get('summary', ''),
            'thumbnail': thumbnail,
            'link': entry.get('link', '')
        })
    return articles

def fetch_all_feeds(feed_list):
    """
    feed_list: List of dicts with keys: url, category/tag (optional)
    Returns a dict mapping feed urls to their articles list.
    """
    all_articles = {}
    for feed in feed_list:
        url = feed.get('url')
        if not url:
            continue
        articles = fetch_feed(url)
        all_articles[url] = {
            'articles': articles,
            'category': feed.get('category', '')
        }
    return all_articles

