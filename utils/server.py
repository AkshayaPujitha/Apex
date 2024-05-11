import threading
from queue import Queue
from utils.crawler.webcrawl import Crawler

# Function to run a crawler within a thread
def thread_crawler(url, keyword, queue):
    print(f"Starting crawler for: {url}")
    crawler_instance = Crawler(url, keyword)
    results = crawler_instance.run()
    queue.put((url, results))

def main(urls, keywords):
    queue = Queue()
    threads = []

    # Create and start a thread for each URL
    for url,keyword in zip(urls,keywords):
        thread = threading.Thread(target=thread_crawler, args=(url, keyword, queue))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Print results from all threads
    while not queue.empty():
        url, sitemap = queue.get()
        print(f"Results for {url}:")
        for entry in sitemap:
            print(f"URL: {entry['url']} - Snippet: {entry['snippet']}")
        return sitemap

if __name__ == "__main__":
    urls_to_crawl = [
        "https://www.w3schools.com/",
        "https://www.geeksforgeeks.org/"
    ]
    keyword = ["python"]
    main(urls_to_crawl, keyword)
