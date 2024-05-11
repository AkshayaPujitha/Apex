import logging
import requests
import functools
import sys
from urllib.parse import urljoin
from bs4 import BeautifulSoup

#logging.basicConfig(
 #   format='%(asctime)s %(levelname)s:%(message)s',
  #  level=logging.INFO)

class Crawler:
    def __init__(self, url, keyword=None):
        self.original_url = url
        self.keyword = keyword.lower() if keyword else None
        self.visited_urls = []
        self.keyword_url = []
        self.urls_to_visit = [url]

    def get_html_content(self, url):
        """Fetches HTML content of the given URL."""
        return session.get(url).text

    def get_linked_urls(self, url, html):
        """Extracts all linked URLs from the page HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a', href=True):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

        for button in soup.find_all('button'):
            path = button.get('onclick')
            if path:
                path = path.replace(' ', '').replace('location.href=', '').strip('\'"`')
                if path.startswith('/'):
                    path = urljoin(url, path)
                yield path

    def add_url_to_visit(self, url):
        """Adds a URL to the queue if it's not visited yet."""
        if url and (url not in self.visited_urls) and (url not in self.urls_to_visit):
            self.urls_to_visit.append(url)

    def crawl(self, url):
        """Crawls the given URL and adds relevant links to the queue."""
        html = self.get_html_content(url)
        soup = BeautifulSoup(html, 'html.parser')
        text_snippet = ' '.join(soup.get_text().split()[:10])  # Capture the first 10 words

        if self.keyword and (self.keyword in text_snippet.lower() or self.keyword in url.lower()):
            #logging.info(f"Found keyword in: {url}")
            self.keyword_url.append({'url': url, 'snippet': text_snippet})
            self.visited_urls.append(url)
        elif not self.keyword:
            self.visited_urls.append({'url': url, 'snippet': text_snippet})

        for link in self.get_linked_urls(url, html):
            if link and '://' not in link:
                link = urljoin(url, link)
            self.add_url_to_visit(link)

    def run(self):
        """Processes the queue until all URLs are visited."""
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            try:
                if url.startswith(self.original_url):
                    #logging.info(f'Crawling: {url}')
                    if self.keyword and len(self.keyword_url) == 10:
                        return self.keyword_url
                    elif not self.keyword and len(self.visited_urls) == 100:
                        return self.visited_urls
                    self.crawl(url)
            except Exception as e:
                pass
                #logging.info(f'Failed to crawl: {url} due to {e}')
                

        if self.keyword:
            return self.keyword_url
        return self.visited_urls


if __name__ == "__main__":
    url_to_crawl = 'https://www.w3schools.com/'
    keyword = None  # Default keyword
    use_tor_network = False

    # Update URL and keyword from command-line arguments if provided
    if len(sys.argv) > 1:
        url_to_crawl = sys.argv[1]
    if len(sys.argv) > 2:
        keyword = sys.argv[2]

    session = requests.session()
    if use_tor_network:
        session.request = functools.partial(session.request, timeout=30)
        session.proxies = {
            'http': 'socks5h://localhost:9050',
            'https': 'socks5h://localhost:9050'
        }

    sitemap = Crawler(url_to_crawl, keyword).run()

    print(f'\nCrawled {len(sitemap)} URLs:\n')
    for entry in sitemap:
        print(f"URL: {entry['url']}\nSnippet: {entry['snippet']}\n")
