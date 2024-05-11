import scrapy
from urllib.parse import urlparse

class LinkCollectorSpider(scrapy.Spider):
    name = 'link_collector'
    #allowed_domains = ['kaggle.com'] 

    def __init__(self, start_url='', keyword=None, *args, **kwargs):
        super(LinkCollectorSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.keyword = keyword.lower() if keyword else None
        self.allowed_domains = [urlparse(start_url).netloc]  # Dynamically set the allowed domain

    def parse(self, response):
        # Extract all links from the page
        for link in response.css('a::attr(href)').getall():
            full_url = response.urljoin(link)
            # Only process the URL if it's from an allowed domain
            if urlparse(full_url).netloc in self.allowed_domains:
                yield scrapy.Request(full_url, callback=self.parse_link, meta={'parent_url': response.url})

    def parse_link(self, response):
        # Extract text snippets from each link
        text = response.css('::text').getall()
        text_snippet = ' '.join(text[:10])  # Collecting a snippet of text from the page

        if self.keyword and self.keyword in ' '.join(text):
            yield {
                'url': response.url,
                'snippet': text_snippet
            }
        elif not self.keyword:
            yield {
                'url': response.url,
                'snippet': text_snippet
            }
