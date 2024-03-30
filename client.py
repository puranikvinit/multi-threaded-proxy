import socket

def send_request():
    count = 0

    while count < 10:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('proxy', 8080))
        request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
        client_socket.send(request.encode())

        response = client_socket.recv(1024)
        print("Received response:")
        print(response.decode())
        print("\n --------------- \n")

        client_socket.close()
        count += 1


# Usage
send_request()