from iworld import *

class findpath():
    __instance = None
    @staticmethod
    def get_instance():#单例模式
        if findpath.__instance is None:
            findpath.__instance = findpath()
        return findpath.__instance

    def __init__(self):
        self.used=[]
        self.path1=[]
        self.m=getmap.get_instance()
        self.sta=state.get_instance()
    def change(self, x, y, f_x, f_y):#生成新路径
        self.x=x
        self.y=y
        self.f_x=f_x
        self.f_y=f_y
        self.used=[]
        self.path1=[]
        self.ret_path(self.x,self.y)
        return self.path1

    def manhattan_dist(self,tx,ty,f_x,f_y):
        return abs(tx - f_x) + abs(ty - f_y)
    def near(self,tx,ty):#获取附近信息
        greedy=[]
        if (self.m.map[tx + 1][ty] == self.m.map[tx][ty] and [tx + 1, ty] not in self.used):
            greedy.append([self.manhattan_dist(self.f_x, self.f_y, tx + 1, ty),tx + 1, ty ])
        if (self.m.map[tx][ty - 1] == self.m.map[tx][ty] and [tx, ty - 1] not in self.used):
            greedy.append([self.manhattan_dist(self.f_x, self.f_y, tx, ty - 1),tx, ty - 1 ])
        if (self.m.map[tx - 1][ty] == self.m.map[tx][ty] and [tx - 1, ty] not in self.used):
            greedy.append([self.manhattan_dist(self.f_x, self.f_y, tx - 1, ty), tx - 1, ty])
        if (self.m.map[tx][ty + 1] == self.m.map[tx][ty] and [tx, ty + 1] not in self.used):
            greedy.append([self.manhattan_dist(self.f_x, self.f_y, tx, ty + 1),tx, ty + 1 ])
        return greedy
    def ret_path(self,tx,ty):#找路径
        self.path1.append([tx,ty])
        self.used.append([tx,ty])
        if([tx-1,ty]==[self.f_x,self.f_y] or [tx,ty+1]==[self.f_x,self.f_y]
           or [tx+1,ty]==[self.f_x,self.f_y] or [tx,ty-1]==[self.f_x,self.f_y]):
            self.path1.append([self.f_x,self.f_y])
            return True
        greedy = self.near(tx,ty)
        temp = sorted(greedy, reverse=True)
        while temp:
            yun=temp.pop()
            if( self.ret_path(yun[1],yun[2])):
                return True
            else:
                self.path1.pop()
        return False

    def next_step(self,x, y, dx, dy, action=''):#将路径生成字符
        dd = 0
        op = [' RDL','L RD','DL R','RDL ']
        if (x == dx and y == dy):
            return ''
        if (x == dx +1 and y == dy):
            dd = 1
        if (x == dx and y == dy -1):
            dd = 2
        if (x == dx and y == dy + 1):
            dd = 0
        if (x == dx -1 and y == dy):
            dd = 3
        temp=op[self.sta.dirn][dd]
        if(temp=='D'):
            temp='LL'
        elif(temp==' '):
            temp=''
        return  temp + action + 'F'
