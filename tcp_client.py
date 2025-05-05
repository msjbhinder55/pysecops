# tcp_client.py - A simple TCP client implementation in Python

import socket

def tcp_client(host='127.0.0.1', port=65432):
    """
    A basic TCP client that connects to a server,
    sends a message, and receives a response.
    """
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # Connect to the server
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")

            # Get user input to send
            message = input("Enter message to send (or 'quit' to exit): ")
            
            while message.lower() != 'quit':
                # Send the message
                client_socket.sendall(message.encode())
                print(f"Sent: {message}")

                # Receive the response
                data = client_socket.recv(1024)
                print(f"Received: {data.decode()}")

                # Get next message
                message = input("Enter message to send (or 'quit' to exit): ")

        except ConnectionRefusedError:
            print(f"Connection refused. Is the server running on {host}:{port}?")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Closing connection")

if __name__ == "__main__":
    # You can change these to match your server configuration
    SERVER_HOST = '127.0.0.1'  # Localhost
    SERVER_PORT = 65432         # Port to connect to
    
    print("Starting TCP Client")
    tcp_client(SERVER_HOST, SERVER_PORT)