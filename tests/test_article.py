import unittest

from main_reader.article import Article

DATE = '2022-09-05T22:27:25Z'
DATE_STR = 'Mon, 05 September, 2022'
IMAGE = 'test_image'
LINK = 'test_link'
SOURCE = 'test_source'
TITLE = 'test_title'

"""Test cases for testing methods of Article class"""


class TestArticle(unittest.TestCase):

    def setUp(self) -> None:
        self.article = Article(TITLE, LINK, DATE, SOURCE, IMAGE)

    def test_date_str(self):
        expected_result = DATE_STR
        actual_result = self.article.date_str("%a, %d %B, %Y")
        self.assertEqual(expected_result, actual_result)  # add assertion here

    def test_to_dict(self):
        self.assertEqual({
            'Title': TITLE,
            'Link': LINK,
            'Date': DATE_STR,
            'Source': SOURCE,
            'Image': IMAGE,
        }, self.article.to_dict())


if __name__ == '__main__':
    unittest.main()
