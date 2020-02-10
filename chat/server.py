#server
import socket,sys,threading
from select import select
from setting import *

 
            
if __name__ == "__main__":
    s_serv = sock_serv(SOCK_SERV)
   
    rlst = [s_serv]
    wlst = []
    print("listening...")
    
    while True:
        rd, wd, ex = select(rlst, wlst, rlst)
        for h in rd:
            if h is s_serv:
                print('s-SERV')
                conn, addr = h.accept()
                print(conn.recv(1024))
                rlst.append(conn)
            else:
                print('s-CLI')
               
                data = h.recv(1024)
                if data == b'':
                    print("user leave")
                    rlst.remove(h)
                    continue
                for i in rlst[1:]:
                    i.send(data)
    
               