import socket
import random
SOCK_SERV = '127.0.0.1', 9999
PIPE_SERV = '127.0.0.1', 8888

PORTS =[]

def sock_serv(addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(addr)
    s.listen(3)
    return s

def sock_cli(addr):
    print(addr)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    return s
