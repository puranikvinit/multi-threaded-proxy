import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(5)

    hostname = socket.gethostname()
    ipv4_address = socket. gethostbyname(hostname)

    while True:
        client_socket, _ = server_socket.accept()
        request = client_socket.recv(1024)
        print("Received request:")
        print(request.decode())

        response = "HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, this is from " + ipv4_address
        client_socket.send(response.encode())
        client_socket.close()

# Usage
start_server()