import socket
import sys
import time

host = 'localhost' 
port = 13337              

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((host, port))
s.sendall(b'Meoooooo !')

data = s.recv(1024)

s.close()

if data :
    print(f"Le serveur a répondu {repr(data)}")

sys.exit()