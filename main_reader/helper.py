import argparse
import datetime
import json
import logging.handlers
import os
import sys
import urllib.error

from dominate import tags
from pathlib import Path
from xhtml2pdf import pisa

import feedparser

from main_reader.article import Article
from main_reader.rss_reader import VERSION


def check_limit(limit_str):
    """Validating limit"""

    try:
        limit = int(limit_str)
    except ValueError:
        raise SystemExit('The argument "limit" should be a number')
    else:
        if limit < 1:
            raise SystemExit('The argument "limit" should be greater than 0')
        else:
            return limit


def check_date(date):
    """Checks date format is YYYYMMDD"""
    try:
        (datetime.datetime.strptime(date, '%Y%m%d')).date()
        return True
    except Exception:
        raise SystemExit('Please, enter the date in "YYYYMMDD" format')


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
    json_article = json.dumps(article.to_dict(), indent=4)
    return json_article


def get_cashed_news(date, connection, url):
    """Retrieves news for the selected date and url"""
    check_date(date)
    cursor = connection.cursor()
    if url:
        cursor.execute('SELECT title, link, full_date, source, image, url FROM news WHERE date=:date and url=:url',
                       {'date': date, 'url': url})
    else:
        cursor.execute('SELECT title, link, full_date, source, image, url FROM news WHERE date=:date',
                       {'date': date})
    articles = list()
    records = cursor.fetchall()
    for title, link, full_date, source, image, url in records:
        articles.append(Article(title, link, full_date, source, image))
    return articles


def init_database(connection):
    cursor = connection.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS news (title text, link text UNIQUE, full_date text, date text, source text, ' \
          'image text, url text)'
    cursor.execute(sql)
    connection.commit()


def save_news(list_of_news, connection, url):
    """Save news into database"""
    cursor = connection.cursor()
    for item in list_of_news:
        new_date = item.date.strftime('%Y%m%d')
        query = "INSERT OR REPLACE INTO news VALUES (?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (item.title, item.link, item.date, new_date, item.source, item.image, url))
    connection.commit()


def parce_command_line_arguments():
    """ Parse command line arguments.
        :return: parsed arguments
    """
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader')
    parser.add_argument('source', type=str, nargs='?', default=None, help='RSS URL')
    parser.add_argument('--version', action='version', version='Version ' + str(VERSION), help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', help='Limit news topics if this parameter provided')
    parser.add_argument('--date', type=str, nargs='?', default='', help='Get news on a specified date')
    parser.add_argument('--to_html', type=Path, help='The absolute path where new .html file will be saved')
    parser.add_argument('--to_pdf', type=Path, help='The absolute path where new .pdf file will be saved')
    args = parser.parse_args()
    return args


def create_logger():
    # Creating logger
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler('../logs.txt')
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logging.disable()
    return logger


def check_directory_exists(dir_path, logger):
    """Checks that directory exists by specified path"""
    logger.info('Checking the entered path...')
    if os.path.isdir(dir_path) is False:
        err_message = f'Invalid path: {dir_path} is not a directory'
        logger.error(err_message)
        raise NotADirectoryError(err_message)
    else:
        return True


def add_article_html(article, html_file):
    """Template for article"""
    with html_file:
        tags.h1(article.title)
        tags.p(tags.b('Title: '), article.title)
        tags.p(tags.b('Link: ', tags.a(tags.b(article.link), href=article.link, )))
        tags.p(tags.b('Date: '), article.date.strftime("%a, %d %B, %Y"))
        tags.p(tags.b('Source: '), article.source)
        if article.image != '---':
            tags.p(tags.img(style="width:360px", src=article.image))
        else:
            tags.p(tags.b('No images'))
    return html_file


def save_news_html(news, path_to_html, logger):
    """Convert news to HTML"""
    check_directory_exists(path_to_html, logger)
    html_file = tags.html(title='RSS news')
    html_file.add(tags.head(tags.meta(charset='utf-8')))

    logger.info('Converting news to HTML...')
    for article in news:
        add_article_html(article, html_file)

    path = os.path.join(path_to_html, 'news.html')
    logger.info('Creating html file...')
    with open(path, 'w', encoding='utf-8') as file:
        file.write(str(html_file))
    logger.info('Html file created successfully!')
    return file


def save_news_pdf(news, path_to_pdf, logger):
    html_file = save_news_html(news, path_to_pdf, logger)
    path = os.path.join(path_to_pdf, 'news.pdf')
    try:
        with open(path, 'wb') as pdf_file, open(html_file.name, 'r', encoding='utf-8') as html_file:
            logger.info('Creating pdf-file...')
            pisa.CreatePDF(src=html_file, dest=pdf_file)
            logger.info("Pdf-file created successfully!")
            html_file.close()
            os.remove(html_file.name)
            logger.info("Temporary html-file deleted")
        return pdf_file
    except FileNotFoundError:
        raise SystemExit('Please, check the existing of file')
