import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 37426  # The port used by the server

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            cmd = input("Please enter your command (help for options): ")
            if cmd == 'help':
                print("3 commands available.\n" \
                        "c - Check connection\n" \
                        "Returns 'MAC ADDRESS: {MAC} | Still Up'\n" \
                        "e - Execute command\n" \
                        "Syntax: e cmd param1 param2\n" \
                        "d - Destroy the machine\n")
            else:
                break
        s.sendall(cmd.encode())
        data = s.recv(1024).decode()
        print(f"Received {data}")