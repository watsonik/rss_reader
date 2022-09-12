import argparse
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

    args = parce_command_line_arguments()

    if args.limit:
        limit = helper.check_limit(args.limit)
    else:
        limit = 0

    if args.verbose:
        logging.disable(0)
        logger.info('Verbose mode is ON')

    news = helper.get_news(args.source)
    helper.save_news(news, connection, args.source)
    if args.date:
        try:
            logger.info(f"Retrieve news from cache for the date {args.date}")
            news = helper.get_cashed_news(args.date, connection)
            if len(news)==0:
                print(f"Cached news not found for the date {args.date}")
        except ValueError:
            logger.error("No valid date provided")
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


def parce_command_line_arguments():
    """ Parse command line arguments.
        :return: parsed arguments
    """
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader')
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--version', action='version', version='Version ' + str(VERSION), help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', help='Limit news topics if this parameter provided')
    parser.add_argument('--date', type=str, nargs='?', default='', help='Get news on a specified date')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
