import logging.handlers
import pathlib
import sqlite3
import sys

from main_reader import helper

VERSION = 2.0


def main():
    # Creating logger
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler('../logs.txt')
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logging.disable()

    db = str(pathlib.Path(__file__).parent.absolute()) + '\\news.db'
    connection = sqlite3.connect(db)
    helper.init_database(connection)

    args = helper.parce_command_line_arguments()

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
            print(article_json)
        logger.info('The list of news was created successfully!')
    else:
        logger.info('Creating the list of news...')
        for article in news:
            print(article)
        logger.info('The list of news was created successfully!')


if __name__ == '__main__':
    main()
