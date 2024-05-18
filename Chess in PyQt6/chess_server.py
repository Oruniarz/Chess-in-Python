import socket
import threading

DATA_SIZE = 2000
HOST = "localhost"
PORT = 80
SERVER_ADDRESS = (HOST, PORT)
tura = "Gracz 1"


def handle_client(client_socket, addr, clients):
    client_name = f"Gracz {len(clients)}"
    client_socket.send(f"{client_name}".encode("utf-8"))
    while True:
        try:
            data = client_socket.recv(DATA_SIZE).decode("utf-8")
            if not data:
                clients.remove(client_socket)
                client_socket.close()
                break
            print(f"{client_name} {addr}: {data}")
            for client in clients:
                if client != client_socket:
                    client.send(data.encode("utf-8"))
        except:
            clients.remove(client_socket)
            client_socket.close()
            break
    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(5)

    print(f"Server listening on port {PORT}...")

    clients = []

    while True:
        client_socket, addr = server_socket.accept()
        print("Accepted connection from:", addr)

        clients.append(client_socket)

        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, clients))
        client_thread.start()


if __name__ == "__main__":
    main()
