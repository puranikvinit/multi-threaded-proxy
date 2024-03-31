import socket
import threading
import queue
import logging

logging.basicConfig(level=logging.INFO)

class WorkerThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            client_socket, backend_servers = self.queue.get()
            logging.info(f"Thread {threading.current_thread().name} handling client")
            self.handle_client(client_socket, backend_servers)
            self.queue.task_done()

    def handle_client(self, client_socket, backend_servers):
        request = client_socket.recv(1024)
        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_socket.connect(backend_servers)
        backend_socket.send(request)
        response = backend_socket.recv(1024)
        client_socket.send(response)
        client_socket.close()
        backend_socket.close()

def start_proxy(num_workers, backend_servers):
    task_queue = queue.Queue()
    for _ in range(num_workers):
        worker = WorkerThread(task_queue)
        worker.setDaemon(True)
        worker.start()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8080))
    server_socket.listen(5)

    round_robin_counter = 0
    while True:
        (client_socket, _) = server_socket.accept()
        task_queue.put((client_socket, backend_servers[round_robin_counter % len(backend_servers)]))
        round_robin_counter += 1

# Usage
number_of_workers = 10
number_of_servers = 5

backend_servers = []
for i in range(number_of_servers):
    backend_servers.append(('multi-threaded-proxy-backend-' + str(i + 1), 8000))

start_proxy(number_of_workers, backend_servers)