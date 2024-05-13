import threading
from queue import Queue
from crawler.webcrawl import Crawler
import socket
import json

# Function to run a crawler within a thread for a single keyword
def thread_crawler(url, keyword, queue):
    print(f"Starting crawler for: {url} with keyword: {keyword}")
    crawler_instance = Crawler(url, keyword)
    results = crawler_instance.run()
    queue.put(results)  # Just push results without keyword

# Function to manage crawling for a single URL with multiple keywords
def url_crawler(url, keywords, queue):
    sub_queue = Queue()
    threads = []

    # Create and start a thread for each keyword
    for keyword in keywords:
        thread = threading.Thread(target=thread_crawler, args=(url, keyword, sub_queue))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Aggregate results for this URL
    aggregated_results = []
    while not sub_queue.empty():
        results = sub_queue.get()
        aggregated_results.extend(results)  # Combine all results into one list

    # Push aggregated results to the main queue
    queue.put((url, aggregated_results))

# Main function to handle multiple URLs and their keywords
def main(urls, keywords):
    queue = Queue()
    threads = []

    # Create and start a thread for each URL
    for url in urls:
        thread = threading.Thread(target=url_crawler, args=(url, keywords, queue))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Collect all results
    all_results = {}
    while not queue.empty():
        url, results = queue.get()
        all_results[url] = results
    #print(all_results)
    return all_results

# Function to handle client connections
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        # Receive data from the client
        data = conn.recv(1024).decode('utf-8')
        request = json.loads(data)
        urls = request.get('url', [])
        keywords = request.get('keywords', [])

        results = main(urls, keywords)
        response = json.dumps(results)
        conn.sendall(response.encode('utf-8'))

    except Exception as e:
        error_message = f"[ERROR] Exception occurred: {e}"
        print(error_message)
        conn.sendall(json.dumps({"error": error_message}).encode('utf-8'))
    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

# Function to start the server
def start_server(host='127.0.0.1', port=65432):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"[LISTENING] Server is listening on {host}:{port}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
