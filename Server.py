import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


def receive_messages(connection):
    while True:
        try:
            data = connection.recv(1024)

            if not data:
                print("\nClient disconnected.")
                break

            message = data.decode().strip()
            print(f"\nClient: {message}")

            if message.lower() == "exit":
                print("Client ended the conversation.")
                break

        except OSError:
            break

    connection.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server listening on {HOST}:{PORT}")
    connection, address = server.accept()
    print(f"Connected by {address}")
    print("Type messages to reply. Type 'exit' to quit.")

    receiver = threading.Thread(
        target=receive_messages,
        args=(connection,),
        daemon=True
    )
    receiver.start()

    try:
        while True:
            message = input("Server: ")
            connection.sendall(message.encode())

            if message.lower() == "exit":
                break
    except (OSError, EOFError):
        pass
    finally:
        connection.close()

print("Server closed.")