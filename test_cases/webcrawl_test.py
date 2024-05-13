import unittest
from unittest.mock import MagicMock
from utils.crawler.webcrawl import Crawler

class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.url_to_crawl = 'https://www.w3schools.com/'
        self.keyword = 'python'
        self.crawler = Crawler(self.url_to_crawl, self.keyword)

    def test_get_html_content(self):
        # Mocking the requests.Session.get method to return a sample HTML content
        self.crawler.session.get = MagicMock(return_value=MagicMock(text='<html><body><p>This is a test</p></body></html>'))

        # Asserting that the method returns the expected HTML content
        html_content = self.crawler.get_html_content('https://www.w3schools.com/')
        self.assertEqual(html_content, '<html><body><p>This is a test</p></body></html>')

    

    # Add more test cases as needed

if __name__ == '__main__':
    unittest.main()
