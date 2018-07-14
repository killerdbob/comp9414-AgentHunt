from collections import *
from state import *
class getmap():
    __instance = None
    def __init__(self,size=180):
        self.map=[['^' for _ in range(size)] for _ in range(size)]
        self.sta=state.get_instance()
        self.begin=[90,90]
        self.map[90][90]=' '
    @staticmethod
    def get_instance():
        if getmap.__instance is None:
            getmap.__instance = getmap()
        return getmap.__instance

    def change_dirn(self,a):
        if(a=='F' or not a):
            return
        elif(a=='L'):
            self.sta.dirn = (self.sta.dirn-1)%4
        elif(a=='R'):
            self.sta.dirn = (self.sta.dirn+1)%4
    def ground_neighbor(self,x, y):
        near = [[x, y]]
        not_in_search = {'.', self.map[x][y]}
        for i in {-1, 1}:
            if (self.map[x + i][y] not in not_in_search):
                near.append([x + i, y, self.map[x + i][y]])
            if (self.map[x][y + i] not in not_in_search):
                near.append([x, y + i, self.map[x][y + i]])
        for i in range(2,-3,-1):
            if (self.map[x + i][y + i] == '^' and [x + i, y + i, self.map[x + i][y + i]] not in near):
                near.append([x + i, y + i, self.map[x + i][y + i]])
            if (self.map[x + i][y - i] == '^' and [x + i, y - i, self.map[x + i][y - i]] not in near):
                near.append([x + i, y - i, self.map[x + i][y - i]])

        if len(near) >=2:
            return near
        else:
            return []
    def get_all_choice(self,x, y):
        u = deque()
        lxcion = []
        trash = []
        u.append([x, y])
        while (u):
            [x, y] = u.popleft()
            temp = self.ground_neighbor(x, y)
            if (temp):
                lxcion.append(temp)
            if ([x, y] == self.begin and [x, y] not in trash and [x, y] not in u):
                lxcion.append([[x, y]])
            trash.append([x, y])
            if (self.map[x][y - 1] == self.map[x][y] and [x, y - 1] not in trash and [x, y - 1] not in u):
                u.append([x, y - 1])
            if (self.map[x][y + 1] == self.map[x][y] and [x, y + 1] not in trash and [x, y + 1] not in u):
                u.append([x, y + 1])
            if (self.map[x - 1][y] == self.map[x][y] and [x - 1, y] not in trash and [x - 1, y] not in u):
                u.append([x - 1, y])
            if (self.map[x + 1][y] == self.map[x][y] and [x + 1, y] not in trash and [x + 1, y] not in u):
                u.append([x + 1, y])
        return lxcion