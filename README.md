# C-S-Chat
网络多人聊天室

为了巩固网络编程知识点，写了一个不带界面的多人聊天程序

>![](../images/演示.png)
#### 结构
![](/images/chat结构.png)

#### Setting
setting.py 包含初始化套接字的参数和方法
```py
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
```
#### Server
服务器运行流程：
- 服务器创建套接字s_serv，该套接字用于接收用户连接。将s_serv放进rlst侦听
- select 函数侦听rlst，如果侦听到s_serv可读，说明有新用户发起了连接。s_serv.accpet()接受用户连接，产生两个返回值，分别是连接句柄和对端的地址元组；
- 将连接句柄放入rlst，这样select也会侦听这个与客户端的连接句柄，如果客户端通过这个连接发送消息，会被select侦听到；
- select有三个返回值，三个值分别是可读列表、可写列表和异常列表，它会将侦听符合状态的socket分别放进这三个列表中；
- 通过for循环可以遍历返回的列表；
- 这样，服务端便实现了接收新用户连接和接收已连接用户消息的功能；
- 收到消息后，遍历rlst ，得到所有与客户端的连接句柄，用连接句柄向每一个客户端发送消息，这样就实现了接受用户消息并将消息发送给所有在线用户的功能。

```py
#server
import socket,sys,threading
from select import select
from setting import *
     
if __name__ == "__main__":
    #创建服务器套接字用户接收客户端连接
    s_serv = sock_serv(SOCK_SERV)
    #将服务器放入侦听读列表中
    rlst = [s_serv]
    wlst = []
    print("listening...")
    
    while True:
        '''
        select.select()接受三个类型为iterator的参数，分别对他们
        侦听可读状态、侦听可写状态、侦听异常状态
        并用列表分别返回满足状态的socket
        '''
        rd, wd, ex = select(rlst, wlst, rlst)
        #轮询满足可读状态的socket
        for h in rd:
            if h is s_serv:
            #如果是s_serv可读，说明收到了新用户的连接
            #将用户套接字放进 rlst 侦听
                print('s-SERV')
                conn, addr = h.accept()
                print(conn.recv(1024))
                rlst.append(conn)
            else:
            #否则是收到已连接用户发来的消息
                print('s-CLI')
                data = h.recv(1024)
                #如果收到的消息为空，证明有用户终止连接，将它移除
                if data == b'':
                    print("user leave")
                    rlst.remove(h)
                    continue
                 #将消息发给所有已连接对象
                for i in rlst[1:]:
                    i.send(data)
```
#### Client
客户端运行流程：
- 客户端创建s_cli 和p_serv两个套接字，前者用于与服务器通信，后者用于接收键盘输入
- 创建子线程，令子线程运行select ，侦听s_cli 和 p_serv 的状态；
- 主线程等待用户输入；
- 主线程收到用户输入后，创建p_cli，用p_cli带着用户输入的数据连接p_serv ，p_serv收到p_cli 的连接，变成可读状态，被select装进列表返回；
- for循环遍历可读列表，如果元素为p_serv，p_serv.accept()得到连接，再通过连接取出其中的数据，最后通过s_cli.send()将数据发送给服务端；
- 如果刻度列表中有s_cli，则客户端收到了从服务端发来的数据，通过s_cli.recv()取出
- 这样就实现了侦听键盘输入并发送和接收服务器的工作。
- 实际上，p_serv不是必要的，如果想要简化代码的话，可以在接收键盘输入后直接通过s_cli.send(data)把数据发送给服务端。但个人感觉这样在程序设计上不太合理，因为数据传输和用户输入是两个行为，应该做区分。


```py
#client.py
import socket,sys,threading
from select import select
from setting import *
import random

def connect(s_cli,p_serv):
    rlst = [s_cli,p_serv]
    wlst = []
   
    while True:
    #侦听s_cli 和 p_serv
        rd, wd, ex = select(rlst, wlst, rlst)
        for r in rd:
            if r is s_cli:
            #如果是s_cli 则是收到了从server发来的消息
                try:
                    data = r.recv(1024)
                    print(data.decode('utf-8'))
                except Exception:
                    continue
            else:
            #如果是 p_serv则是收到主线程的键盘输入
            #将键盘输入数据通过s_cli 发给Server 
                conn, addr = r.accept()
                data = conn.recv(1024)
                s_cli.send(data)
                conn.close()

if __name__ == "__main__":
    name=input("input your nickname: ")
    #创建与server连接的套接字，这个套接字用于与server收发消息
    s_cli = sock_cli(SOCK_SERV)
    s_cli.send(bytes('{} connection...'.format(name),'utf-8'))
    #创建pipe_server套接字，这个套接字用于线程间通信，
    #接收键盘输入的消息并把它发送给与server连接的套接字
    while True:
    #因为是在127.0.0.1环境下运行，每个client都要有自己的pipe_server端口
    #为了端口不重复所以要这样获取端口。
    #如果不是在同一个主机上运行可以用这一步
        PORT = random.randint(5000, 10000)
        if PORT not in PORTS:break
    P_ADDR=('127.0.0.1',PORT)
    p_serv = sock_serv(P_ADDR)

    #创建线程，线程去监听p_serv 和s_serv 两个套接字
    t = threading.Thread(target=connect, args=(s_cli,p_serv))
    t.setDaemon(True)
    t.start()
    #主线程用于监听键盘输入
    while True:
        try:
            data = sys.stdin.readline()
        except KeyboardInterrupt:
            s_cli.close()
            p_serv.close()
            break
        if not data:
            break
        else:
        #得到data之后，创建pipe_client，连接p_serv
        #子线程中的select()会捕捉到这个连接，接收其中的data
            p_cli = sock_cli(P_ADDR)
            p_cli.send(bytes(name+' : '+data, 'utf-8'))
            p_cli.close()
```
