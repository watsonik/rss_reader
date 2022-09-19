""" Main test module for basic reading news from external resources and cache. """
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import MagicMock
from unittest.mock import patch
from urllib.error import URLError
import os

from main_reader.article import Article
from main_reader import helper


class TestHelper(unittest.TestCase):
    """Test cases to test helper methods"""

    def setUp(self):
        self.url = 'test_url'
        self.url_b = 'https://news.yahoo.com/rss/'
        self.article_a = Article('Thousands march in Turkey to demand ban on LGBTQ groups',
                                 'https://news.yahoo.com/anti-lgbtq-protest-turkey-backs-171156220.html',
                                 '2022-09-18T17:11:56Z', 'Associated Press',
                                 'https://s.yimg.com/uu/api/res/1.2/6M2SVMAN8wV455r.zujgUA--~B'
                                 '/aD01MTM5O3c9NzcwOTthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org'
                                 '/a6153c6d90d9815a61dacbde53e89cb3')
        self.article_b = Article('Title_B', 'Link_B', '2021-05-22T15:03:25Z', 'Source_B', 'Image_B')
        self.entries = [{'title': 'Thousands march in Turkey to demand ban on LGBTQ groups',
                         'title_detail': {'type': 'text/plain', 'language': None, 'base': 'https://news.yahoo.com/rss/',
                                          'value': 'Thousands march in Turkey to demand ban on LGBTQ groups'},
                         'links': [{'rel': 'alternate',
                                    'type': 'text/html',
                                    'href': 'https://news.yahoo.com/anti-lgbtq-protest-turkey-backs-171156220.html'}],
                         'link': 'https://news.yahoo.com/anti-lgbtq-protest-turkey-backs-171156220.html',
                         'published': '2022-09-18T17:11:56Z',
                         'published_parsed': 'time.struct_time(tm_year=2022, tm_mon=9, tm_mday=18, tm_hour=17, '
                                             'tm_min=11, tm_sec=56, tm_wday=6, tm_yday=261, tm_isdst=0)',
                         'source': {'href': 'http://www.ap.org/', 'title': 'Associated Press'},
                         'id': 'anti-lgbtq-protest-turkey-backs-171156220.html', 'guidislink': False,
                         'media_content': [{'height': '86',
                                            'url': 'https://s.yimg.com/uu/api/res/1.2/6M2SVMAN8wV455r.zujgUA--~B'
                                                   '/aD01MTM5O3c9NzcwOTthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com'
                                                   '/en/ap.org/a6153c6d90d9815a61dacbde53e89cb3',
                                            'width': '130'}], 'media_credit': [{'role': 'publishing company'}],
                         'credit': ''}]
        self.json = '{\n    "Title": "Thousands march in Turkey to demand ban on LGBTQ groups",\n' \
                    '    "Link": "https://news.yahoo.com/anti-lgbtq-protest-turkey-backs-171156220.html",\n' \
                    '    "Date": "Sun, 18 September, 2022",\n' \
                    '    "Source": "Associated Press",\n' \
                    '    "Image": "https://s.yimg.com/uu/api/res/1.2/6M2SVMAN8wV455r.zujgUA--~B' \
                    '/aD01MTM5O3c9NzcwOTthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org' \
                    '/a6153c6d90d9815a61dacbde53e89cb3"\n}'
        self.html = '<html title="RSS news">\n\
  <head>\n\
    <meta charset="utf-8">\n\
  </head>\n\
  <h1>Thousands march in Turkey to demand ban on LGBTQ groups</h1>\n\
  <p>\n\
    <b>Title: </b>Thousands march in Turkey to demand ban on LGBTQ groups\n\
  </p>\n\
  <p>\n\
    <b>Link: \n\
      <a href="https://news.yahoo.com/anti-lgbtq-protest-turkey-backs-171156220.html">\n\
        <b>https://news.yahoo.com/anti-lgbtq-protest-turkey-backs-171156220.html</b>\n\
      </a>\n\
    </b>\n\
  </p>\n\
  <p>\n\
    <b>Date: </b>Sun, 18 September, 2022\n\
  </p>\n\
  <p>\n\
    <b>Source: </b>Associated Press\n\
  </p>\n\
  <p>\n\
    <img src="https://s.yimg.com/uu/api/res/1.2/6M2SVMAN8wV455r.zujgUA--~B/aD01MTM5O3c9NzcwOTthcHBpZD15dGFjaHlvbg--\
/https://media.zenfs.com/en/ap.org/a6153c6d90d9815a61dacbde53e89cb3" style="width:360px">\n\
  </p>\n\
</html>'

    def test_create_articles(self):
        """Checks that processing the entries creates an object of the Article class"""
        self.actual = helper.create_articles(self.entries)[0]
        self.assertEqual(self.article_a, self.actual)

    def test_empty_news(self):
        """Checks that the program creates empty list after receiving an empty input"""
        self.assertEqual([], helper.create_articles([]))

    def test_make_json(self):
        """Checks that news is converted to json format correctly"""
        self.assertEqual(self.json, helper.make_json(self.article_a))

    def test_check_limit(self):
        """Tests check_limit method with valid values (positive numbers)"""
        self.assertEqual(2, helper.check_limit('2'))

    def test_check_limit_value_error(self):
        """Tests check_limit method with invalid values (letters)"""
        with self.assertRaises(SystemExit) as cl:
            helper.check_limit('one')

        exc = cl.exception
        self.assertEqual('The argument "limit" should be a number', exc.args[0])

    def test_check_limit_negative(self):
        """Tests check_limit method with invalid values (negative numbers)"""
        with self.assertRaises(SystemExit) as cl:
            helper.check_limit('-1')

        exc = cl.exception
        self.assertEqual('The argument "limit" should be greater than 0', exc.args[0])

    def test_check_limit_zero(self):
        """Tests check_limit method with invalid values (zero)"""
        with self.assertRaises(SystemExit) as cl:
            helper.check_limit('0')

        exc = cl.exception
        self.assertEqual('The argument "limit" should be greater than 0', exc.args[0])

    @patch('feedparser.parse')
    def test_bad_link(self, mocked_object):
        """Tests get_news method if url returns empty news list"""
        mocked_object.return_value = {'entries': []}
        with self.assertRaises(SystemExit) as cl:
            helper.get_news(self.url)

        exc = cl.exception
        self.assertEqual("Please, check the entered link is correct!", exc.args[0])

    @patch('feedparser.parse')
    def test_invalid_url(self, mocked_object):
        """Tests get_news method if url is not available"""
        mocked_object.side_effect = MagicMock(side_effect=URLError('foo'))
        with self.assertRaises(SystemExit) as cl:
            helper.get_news(self.url)

        exc = cl.exception
        self.assertEqual("Source isn't available", exc.args[0])

    @patch('feedparser.parse')
    def test_valid_url(self, parser):
        """Tests get_news method if url returns correct news list"""
        parser.return_value = {'entries': self.entries}

        self.actual = helper.get_news(self.entries)
        self.assertEqual(self.article_a, self.actual[0])

    def test_execute_news(self):
        """Checks the get_cashed_news method will execute the required sql query if date and url specified"""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        # mock_logger = MagicMock()
        date = '20220919'
        helper.get_cashed_news(date, mock_connection, self.url)
        # helper.get_cashed_news(date, mock_connection, self.url, mock_logger)
        self.assertEqual('SELECT title, link, full_date, source, image, url FROM news WHERE date=:date and url=:url',
                         mock_cursor.execute.call_args.args[0])
        self.assertEqual(date, mock_cursor.execute.call_args.args[1]['date'])
        self.assertEqual(self.url, mock_cursor.execute.call_args.args[1]['url'])

    def test_execute_news_without_url(self):
        """Checks the get_cashed_news method will execute the required sql query if only date specified"""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        date = '20220919'
        helper.get_cashed_news(date, mock_connection, None)
        self.assertEqual('SELECT title, link, full_date, source, image, url FROM news WHERE date=:date',
                         mock_cursor.execute.call_args.args[0])
        self.assertEqual(date, mock_cursor.execute.call_args.args[1]['date'])

    def test_valid_path_to_directory(self):
        """Checks that the specified path exists"""
        path = os.path.abspath(os.curdir)
        mock_logger = MagicMock(return_value=None)
        self.actual = helper.check_directory_exists(path, mock_logger)
        self.assertEqual(True, self.actual)

    def test_non_existent_folder(self):
        """Tests check_directory_exists method if the directory does not exist"""
        path = 'C:/nodir'
        mock_logger = MagicMock(return_value=None)
        with self.assertRaises(NotADirectoryError) as cl:
            helper.check_directory_exists(path, mock_logger)

        exc = cl.exception
        self.assertEqual(f'Invalid path: {path} is not a directory', exc.args[0])

    @patch('main_reader.helper.check_directory_exists')
    def test_save_news_in_html(self, checker):
        """Checks that save_news_html method is converting the passed object to html-format"""
        checker.return_value = True
        path = os.path.abspath(os.curdir)
        mock_logger = MagicMock(return_value=None)
        html = helper.save_news_html([self.article_a], path, mock_logger)
        with io.StringIO() as temp_value, redirect_stdout(temp_value):
            f = open(html.name, 'r')
            print(f.read())
            self.assertEqual(self.html + '\n', temp_value.getvalue())
            f.close()
        os.remove(html.name)

    @patch('main_reader.helper.save_news_html')
    @patch('xhtml2pdf.pisa.CreatePDF')
    def test_save_news_in_pdf(self, pisa, html_saver):
        """Checks that the save_news_pdf method is converting the passed object to pdf-format"""
        pisa.return_value = ''
        path = os.path.abspath(os.curdir)
        mock_logger = MagicMock(return_value=None)
        html_file = os.path.join(path, 'test.html')
        with open(html_file, 'x', encoding='utf-8') as html:
            html.write(self.html)
        html_saver.return_value = html
        pdf = helper.save_news_pdf(self.article_a, path, mock_logger)
        self.assertTrue(os.path.join(path, 'news.pdf'))
        os.remove(pdf.name)

    def test_check_date(self):
        """Tests check_date method with valid values (date in YYYYMMDD format)"""
        self.assertEqual(True, helper.check_date('20220919'))

    def test_check_invalid_format_date(self):
        """Tests check_date method with invalid values"""
        date = '55555555'
        with self.assertRaises(SystemExit) as cl:
            helper.check_date(date)

        exc = cl.exception
        self.assertEqual('Please, enter the date in "YYYYMMDD" format', exc.args[0])


if __name__ == "__main__":
    unittest.main()
