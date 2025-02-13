import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5050

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        client_name = "Client of Grace Ryoo"
        user_input = input("Enter an integer (1-100): ")

        try:
            num = int(user_input)
            if num < 1 or num > 100:
                print("Out of range. Closing client...")
                return
        except ValueError:
            print("Invalid input. Closing client...")
            return

        message = f"{client_name}:{num}"
        client_socket.send(message.encode())

        response = client_socket.recv(1024).decode().strip()
        server_name, server_number = response.split(":")
        server_number = int(server_number)

        print(f"Server Name: {server_name}")
        print(f"Your Number: {num}")
        print(f"Server Number: {server_number}")
        print(f"Sum: {num + server_number}")

if __name__ == "__main__":
    start_client()
