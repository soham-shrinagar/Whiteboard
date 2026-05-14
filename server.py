import socket
import threading

# Logic: A list to keep track of all connected client sockets
clients = []

def handle_client(client_socket):
    while True:
        try:
            # Logic: Receive drawing data (e.g., "x,y,color")
            data = client_socket.recv(1024)
            if not data:
                break
            
            # Logic: Broadcast the received data to every other connected client
            for client in clients:
                if client != client_socket:
                    try:
                        client.send(data)
                    except:
                        clients.remove(client)
        except:
            break
    
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen(5)
    print("Server started on 127.0.0.1:5555")

    while True:
        client_sock, addr = server.accept()
        print(f"Accepted connection from {addr}")
        clients.append(client_sock)
        
        # Logic: Start a new thread for each client so the server 
        # can keep accepting new connections simultaneously.
        thread = threading.Thread(target=handle_client, args=(client_sock,))
        thread.start()

if __name__ == "__main__":
    start_server()