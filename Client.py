
import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


def receive_messages(connection):
    while True:
        try:
            data = connection.recv(1024)

            if not data:
                print("\nServer disconnected.")
                break

            message = data.decode().strip()
            print(f"\nServer: {message}")

            if message.lower() == "exit":
                print("Server ended the conversation.")
                break

        except OSError:
            break


with socket.create_connection((HOST, PORT)) as connection:
    print("Connected to the server!")
    print("Type messages to send. Type 'exit' to quit.")

    receiver = threading.Thread(
        target=receive_messages,
        args=(connection,),
        daemon=True
    )
    receiver.start()

    try:
        while True:
            message = input("You: ")
            connection.sendall(message.encode())

            if message.lower() == "exit":
                break
    except (OSError, EOFError):
        pass

print("Client closed.")