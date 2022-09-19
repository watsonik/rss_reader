import dateparser


class Article:
    """Creates a news instance with the necessary attributes"""

    def __init__(self, title, link, date, source, image):
        self.title = title
        self.link = link
        self.date = dateparser.parse(date)
        self.source = source
        self.image = image

    def date_str(self, formatter):
        """Convert date to a string"""
        return self.date.strftime(formatter)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Article):
            return self.link == other.link
        return False

    def __str__(self):
        """Overrides the default implementation"""
        return 'Title: ' + self.title + '\n' \
               + 'Link: ' + self.link + '\n' \
               + 'Date: ' + self.date_str("%a, %d %B, %Y") + '\n' \
               + 'Source: ' + self.source + '\n' \
               + 'Image: ' + self.image + '\n'

    def to_dict(self):
        """Convert instance of article to a dictionary"""
        fields = {
            'Title': self.title,
            'Link': self.link,
            'Date': self.date_str("%a, %d %B, %Y"),
            'Source': self.source,
            'Image': self.image,
        }
        return fields
