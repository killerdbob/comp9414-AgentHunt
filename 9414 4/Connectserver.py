import socket
from iworld import *

class Connectsever():
    __instance = None

    @staticmethod
    def get_instance(port):#获取单例模式
        if Connectsever.__instance is None:
            Connectsever.__instance = Connectsever(port)
        return Connectsever.__instance

    def __init__(self,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost',port))
        self.view=[['' for _ in range(5)] for _ in range(5)]
        self.sta=state.get_instance()
        self.m = getmap.get_instance()

    def read_view(self):#从服务器接收数据，并生成地图
        for i in range(5):
            for j in range(5):
                if (i *5 +j ==12):
                    continue
                r = str(self.sock.recv(1), encoding='utf-8')
                if (self.sta.dirn == 0):
                    self.view[4 - j][i] = r
                if (self.sta.dirn -1 ==0):
                    self.view[i][j] = r
                if (self.sta.dirn -2 == 0):
                    self.view[j][4 - i] = r
                if (self.sta.dirn -3 == 0):
                    self.view[4 - i][4 - j] = r
        for i in range(2,-3,-1):
            for j in range(2,-3,-1):
                if (i != 0 or j != 0):
                    self.m.map[self.sta.row + i][self.sta.col + j] = self.view[2 + i][2 + j]

    def action(self,a):#发送数据到服务器
        if not a :
            return
        else:
            t=bytes(a, encoding='utf-8')
            self.sock.send(t)