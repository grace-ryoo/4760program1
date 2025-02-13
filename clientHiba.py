# Client Code
def start_client(host='127.0.0.1', port=5001):
    client_name = "Client of Hiba Ayub"
    client_number = int(input("Enter a number between 1 and 100: "))
    
    if not (1 <= client_number <= 100):
        print("Invalid input. Must be between 1 and 100.")
        return
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        message = f"{client_name},{client_number}"
        client_socket.sendall(message.encode())
        
        data = client_socket.recv(1024).decode()
        server_name, server_number = data.split(',')
        server_number = int(server_number)
        
        print(f"Server Name: {server_name}")
        print(f"Client Number: {client_number}, Server Number: {server_number}")
        print(f"Sum: {client_number + server_number}")

if __name__ == "__main__":
    choice = input("Start as (server/client): ").strip().lower()
    if choice == "server":
        start_server()
    elif choice == "client":
        start_client()
    else:
        print("Invalid choice. Use 'server' or 'client'.")
