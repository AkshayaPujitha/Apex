import threading
from queue import Queue
from crawler.webcrawl import Crawler
import socket
import json

# Function to run a crawler within a thread
def thread_crawler(url, keyword, queue):
    print(f"Starting crawler for: {url}")
    crawler_instance = Crawler(url, keyword)
    results = crawler_instance.run()
    queue.put((url, results))

def main(url, keywords):
    queue = Queue()
    threads = []

    # Create and start a thread for each URL
    for keyword in keywords:
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
    
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        # Receive data from the client
        data = conn.recv(1024).decode('utf-8')
        request = json.loads(data)

        url = request.get('url', '')
        keywords = request.get('keywords', [])

        results=main(url,keywords)
        response = json.dumps(results)
        conn.sendall(response.encode('utf-8'))


    except Exception as e:
        error_message = f"[ERROR] Exception occurred: {e}"
        print(error_message)
        conn.sendall(json.dumps({"error": error_message}).encode('utf-8'))
    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")


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
