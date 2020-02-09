#server
import socket,sys,threading
from select import select
from setting import *

def listen(s_serv, p_serv):
    rlst = [s_serv, p_serv]
    wlst = []
    print("listening...")
    
    while True:
        rd, wd, ex = select(rlst, wlst, rlst)
        for h in rd:
            if h is s_serv:
                conn, addr = h.accept()
                print(conn)
                rlst.append(conn)
            elif h is p_serv:
                conn, addr = w.accept()
                data = conn.recv(1024)
                print('data',data)
                for i in rlst[2:]:
                    i.send(data)
                conn.close()

            
            else:
                data = h.recv(1024)
                print(data.decode('utf-8'
                ), end=' ')
                for c in rlst[2:]:
                    c.send(data)
          
            
if __name__ == "__main__":
    s_serv = sock_serv(SOCK_SERV)
    p_serv = sock_serv(PIPE_SERV)
    
    t = threading.Thread(target=listen, args=(s_serv, p_serv))
    t.setDaemon(True)
    t.start()
    
    while True:
        try:
            data = sys.stdin.readline()
        except KeyboardInterrupt:
            s_serv.close()
            p_serv.close()
            break
        if not data:
            continue
        else:
            print("inputed ",data)
            p_cli = sock_cli(PIPE_SERV)
            p_cli.send(bytes('manager : '+ data, 'utf-8'))
            p_cli.close()
        
