import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        connexion, addr = s.accept()
        with connexion:
            print('Connected by', addr)
            while True:
                data = connexion.recv(1024)
                if not data:
                    break
                connexion.sendall(data)