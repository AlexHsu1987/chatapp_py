import socket,select
class chatserver():
    """
    聊天室服务器端
    """
    def __init__(self,host,port,numofclient):
        self.Host=host
        self.Port=port
        self.server_socket=socket.socket()
        #绑定到SERVERADDRESS以及绑定的端口号
        self.server_socket.bind((self.Host,self.Port))
        #设置最大监听数
        self.server_socket.listen(numofclient)
        self.socket_list=[]
        self.client_names={}
        self.socket_list.append(self.server_socket)
        print("聊天室已打开")
        
    def connect(self):
        #响应一个客户端的连接请求，建立一个连接，用来接收/发送数据
        client_conn,client_addr=self.server_socket.accept()
        try:
            #向新连接的客户端发送欢迎信息
            welcome_msg='欢迎来到聊天室，请输入昵称'
            client_conn.send(welcome_msg.encode('utf-8'))
            #接收客户端发来的用户名，最大接收字符为4096
            client_name=client_conn.recv(4096).decode('utf-8')
            self.socket_list.append(client_conn)
            self.client_names[client_conn]=client_name
            msg='现在有'+str(len(self.client_names))+'名用户在聊天室：['+','.join(list(self.client_names.values()))+']'
            client_conn.send(msg.encode('utf-8'))
            #向所有客户端发送新成员加入信息
            for sock in self.client_names.keys():
                if (not sock==client_conn):
                    msg=self.client_names[client_conn]+'加入聊天室'
                    sock.send(msg.encode('utf-8'))
        except Exception as e:
            print(e)

    def disconnection():
        self.server_socket.close()

    def run(self):
        #响应客户端的连接和传输数据
        while True:
            #如果只是服务器开启，36000秒之内没有客户端连接，则会超时关闭
            readlist,writelist,errorlist=select.select(self.socket_list,[],[],36000)
            #当读入列表readlist中没有可读信息时，即没有用户接入聊天室，则退出服务器
            if not readlist:
                print('没有用户连接，聊天室关闭。。。')
                self.disconnection() #关闭服务器端socket
                break
            for client_socket in readlist:
                if client_socket is self.server_socket:
                    self.connect()
                else:
                    #表示一个client连接上有数据到达服务器
                    disconnection=False
                    try:
                        #接收客户端data，数据buffer大小设置为4096
                        data=client_socket.recv(4096).decode('utf-8')
                        data=self.client_names[client_socket]+'：'+data
                    except socket.error as err:
                        #客户端连接异常，则认为该用户已经离线，即离开聊天室
                        data=self.client_names[client_socket]+'离开聊天室。'
                        disconnection=True
                    if disconnection:
                        #如果用户离开聊天室，则将其对应的客户端从读入列表readlist中移除
                        self.socket_list.remove(client_socket)
                        print(data)
                        for sock in self.socket_list:
                            if (not sock==self.server_socket) and (not sock==client_socket):
                                try:
                                    sock.send(data.encode('utf-8'))
                                except Exception as e:
                                    print(e)
                        del self.client_names[client_socket]
                    else:
                        print(data)
                        #向其他成员发送相同的信息
                        for sock in self.socket_list:
                            if (not sock==self.server_socket) and (not sock==client_socket):
                                try:
                                    sock.send(data.encode('utf-8'))
                                except Exception as e:
                                    print(e)
HOST=socket.gethostname()
PORT=8888
server=chatserver(HOST, PORT, 10)
server.run()
                            
            
