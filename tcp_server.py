import socket

def create_tcp_server(host='127.0.0.1', port=65432):
    # 1. Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 2. Bind the socket to the host and port
        s.bind((host, port))
        
        # 3. Listen for incoming connections
        s.listen()
        print(f"Server listening on {host}:{port}")
        
        # 4. Accept connections
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                # 5. Receive data
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode()}")
                
                # 6. Send response
                conn.sendall(b"Message received")

if __name__ == "__main__":
    create_tcp_server()