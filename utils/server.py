import threading
from queue import Queue
from crawler.webcrawl import Crawler
import socket
import json

def thread_crawler(url, keyword, queue):
    print(f"Starting crawler for: {url} with keyword: {keyword}")
    crawler_instance = Crawler(url, keyword)
    results = crawler_instance.run()
    queue.put(results)  

def url_crawler(url, keywords, queue):
    sub_queue = Queue()
    threads = []

    for keyword in keywords:
        thread = threading.Thread(target=thread_crawler, args=(url, keyword, sub_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    aggregated_results = []
    while not sub_queue.empty():
        results = sub_queue.get()
        aggregated_results.extend(results)  

    queue.put((url, aggregated_results))

def main(urls, keywords):
    queue = Queue()
    threads = []

    for url in urls:
        thread = threading.Thread(target=url_crawler, args=(url, keywords, queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    all_results = {}
    while not queue.empty():
        url, results = queue.get()
        all_results[url] = results
    #print(all_results)
    return all_results

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
