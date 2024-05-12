import socket
import json

def crawl_request(url,keywords):
    host = '127.0.0.1'
    port = 65432

    request_data = json.dumps({'url': url, 'keywords': keywords})
    print("hereeeee")
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((host,port))

    try:
        # Send data to the server
        client.sendall(request_data.encode('utf-8'))

        # Receive response from the server
        response = client.recv(4096)  # Adjust this if needed
        results = json.loads(response.decode('utf-8'))

        return results
    except Exception as e:
        return {"error": str(e)}
    finally:
        client.close()