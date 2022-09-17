import logging.handlers
import pathlib
import sqlite3

from main_reader import helper
from main_reader.colorize_logger import ColorizeLogger

VERSION = 5.0


def main():
    logger = ColorizeLogger()

    db = str(pathlib.Path(__file__).parent.absolute()) + '\\news.db'
    connection = sqlite3.connect(db)
    helper.init_database(connection)

    args = helper.parce_command_line_arguments()

    if args.colorize:
        logger.is_colorize = True

    if args.limit:
        limit = helper.check_limit(args.limit)
    else:
        limit = 0

    if args.verbose:
        logging.disable(0)
        logger.info('Verbose mode is ON')

    news = list()
    # helper.save_news(news, connection, args.source)
    if args.date:
        try:
            logger.info(f"Retrieve news from cache for the date {args.date}")
            news = helper.get_cashed_news(args.date, connection, args.source)
            if len(news) == 0:
                raise SystemExit(f"Cached news not found for the date {args.date}")
        except ValueError:
            logger.error("No valid date provided")
    else:
        news = helper.get_news(args.source)
        helper.save_news(news, connection, args.source)
    if limit > 0:
        logger.info(f'The limit of articles is set to {limit}')
        news = news[:limit]
    if args.json:
        logger.info('Creating the list of news in JSON format...')
        for article in news:
            article_json = helper.make_json(article)
            logger.print(article_json)
        logger.info('The list of news was created successfully!')
    else:
        logger.info('Creating the list of news...')
        for article in news:
            logger.print(article)
        logger.info('The list of news was created successfully!')
    if args.to_pdf:
        logger.info('Converting existing list of news to PDF format...')
        # for article in news:
        helper.save_news_pdf(news, args.to_pdf, logger)
        logger.info('The list of news was saved as PDF successfully!')
    if args.to_html:
        logger.info('Converting existing list of news to HTML format...')
        # for article in news:
        helper.save_news_html(news, args.to_html, logger)
        logger.info('The list of news was saved as HTML successfully!')


if __name__ == '__main__':
    main()
