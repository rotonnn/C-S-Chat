#client
import socket,sys,threading
from select import select
from setting import *
import random


def connect(s_cli,p_serv):
    rlst = [s_cli,p_serv]
    wlst = []
   
    while True:
        rd, wd, ex = select(rlst, wlst, rlst)
        for r in rd:
            if r is s_cli:
                try:
                    data = r.recv(1024)
                    print(data.decode('utf-8'))
                except Exception:
                    continue
                
            else:
                conn, addr = r.accept()
                data = conn.recv(1024)
                s_cli.send(data)
                conn.close()

if __name__ == "__main__":
    name=input("input your nickname: ")
    s_cli = sock_cli(SOCK_SERV)
    s_cli.send(bytes('{} connection...'.format(name),'utf-8'))
 
    while True:
        PORT = random.randint(5000, 10000)
        if PORT not in PORTS:break
    P_ADDR=('127.0.0.1',PORT)
    p_serv = sock_serv(P_ADDR)

    t = threading.Thread(target=connect, args=(s_cli,p_serv))
    t.setDaemon(True)
    t.start()

    while True:
        try:
            
            data =input()
            
        except KeyboardInterrupt:
            s_cli.close()
            p_serv.close()
            break
        if not data:
            break
        else:
            p_cli = sock_cli(P_ADDR)
            p_cli.send(bytes(name+' : '+data, 'utf-8'))
            p_cli.close()