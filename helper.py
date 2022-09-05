import json


def check_limit(limit):
    """Validating limit"""
    return int(limit)


def get_news(link):
    """Get list of RSS"""
    return list()


def make_json(article):
    """Converts article to JSON format"""
    json_article = json.dumps(article.to_dict())
    return json_article
