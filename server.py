import socket
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5050
SERVER_NAME = "Server of Grace Ryoo"
SERVER_NUMBER = 42  # Fixed number for consistency
QUIT = False

class ClientThread(threading.Thread):

    def __init__(self, client_sock):
        super().__init__()
        self.client = client_sock

    def run(self):
        global QUIT
        try:
            data = self.client.recv(1024).decode().strip()
            if not data:
                return
            
            client_name, client_number = data.split(":")
            client_number = int(client_number)

            if client_number < 1 or client_number > 100:
                print("Out-of-range number received. Shutting down server...")
                QUIT = True
                return
            
            print(f"Received from {client_name}: {client_number}")
            print(f"{SERVER_NAME} chose: {SERVER_NUMBER}")
            print(f"Sum: {client_number + SERVER_NUMBER}")

            response = f"{SERVER_NAME}:{SERVER_NUMBER}"
            self.client.send(response.encode())

        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            self.client.close()

class Server:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        global QUIT
        try:
            self.sock.bind((SERVER_HOST, SERVER_PORT))
            self.sock.listen(5)
            print(f"{SERVER_NAME} is listening on {SERVER_HOST}:{SERVER_PORT}...")

            while not QUIT:
                client, _ = self.sock.accept()
                new_thread = ClientThread(client)
                new_thread.start()

        except KeyboardInterrupt:
            print("\nServer shutting down...")
        finally:
            self.sock.close()

if __name__ == "__main__":
    server = Server()
    server.run()
