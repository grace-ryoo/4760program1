import socket
import random

# Server Code
def start_server(host='127.0.0.1', port=5001):
    server_name = "Server of Hiba Ayub"
    server_number = random.randint(1, 100)  # Fixed number for simplicity
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"{server_name} is listening on {host}:{port}")
        
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024).decode()
            if not data:
                return
            
            client_name, client_number = data.split(',')
            client_number = int(client_number)
            
            if not (1 <= client_number <= 100):
                print("Received out-of-range number. Shutting down server.")
                return
            
            print(f"Client Name: {client_name}")
            print(f"Server Name: {server_name}")
            print(f"Client Number: {client_number}, Server Number: {server_number}")
            print(f"Sum: {client_number + server_number}")
            
            response = f"{server_name},{server_number}"
            conn.sendall(response.encode())
