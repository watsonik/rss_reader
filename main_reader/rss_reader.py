import argparse
import logging.handlers
import sys

from main_reader.helper import check_limit, get_news, make_json

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

    args = parce_command_line_arguments()

    if args.limit:
        limit = check_limit(args.limit)
    else:
        limit = 0

    if args.verbose:
        logging.disable(0)
        logger.info('Verbose mode is ON')

    news = get_news(args.source)
    if limit > 0:
        logger.info(f'The limit of articles is set to {limit}')
        news = news[0:limit]
    if args.json:
        logger.info('Creating the list of news in JSON format...')
        for article in news:
            article_json = make_json(article)
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
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
