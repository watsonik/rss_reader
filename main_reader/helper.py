import json
import urllib.error

import feedparser

from main_reader.article import Article


def check_limit(limit):
    """Validating limit"""
    return int(limit)


def create_articles(news):
    """Creating list of news"""
    default_value = '---'

    articles = []
    for entry in news:
        title = entry.get('title', default_value)
        link = entry.get('link', default_value)
        published = entry.get('published', default_value)
        source = entry.get('source', default_value)
        media_content = entry.get('media_content', default_value)

        source_title = default_value
        if source != default_value:
            source_title = source['title']

        image = default_value
        if media_content != image:
            image = media_content[0]['url']

        article = Article(title, link, published, source_title, image)
        articles.append(article)

    return articles


def get_news(link):
    """Get list of RSS"""

    try:
        rss_news = feedparser.parse(link)
        articles = create_articles(rss_news['entries'])
    except urllib.error.URLError:
        raise SystemExit("Source isn't available")
    else:
        if len(articles) == 0:
            raise SystemExit('Please, check the entered link is correct!')
        else:
            return articles


def make_json(article):
    """Converts article to JSON format"""
    json_article = json.dumps(article.to_dict())
    return json_article
