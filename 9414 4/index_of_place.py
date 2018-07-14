from iworld import *

class guide():
    __instance = None
    def __init__(self):
        self.m=getmap.get_instance()
        self.island_ocean_index=[]
        self.ls_place_index = []
        self.place_index = []#保存各个港口信息

    @staticmethod
    def get_instance():
        if guide.__instance is None:
            guide.__instance = guide()
        return guide.__instance

    def chg_habour(self,x, y):#查找港口信息
        for i in self.record_place_index(x, y):
            if (i[-1] not in self.island_ocean_index):
                self.island_ocean_index.append(i[-1])

    def finding_new_place(self,x, y, gx=None, gy=None):
        temp = []
        for i in range(len(self.ls_place_index)):
            for j in range(len(self.ls_place_index[i])):
                if (self.ls_place_index[i][j] == [x, y] and gx):
                    self.place_index[i].append([[gx, gy], [x, y], '~'])
                    return
                elif (self.ls_place_index[i][j] == [x, y]):
                    self.place_index[i].append([[x, y], ' '])
                    return
        new_land = self.m.get_all_choice(x, y)
        for n in new_land:
            temp.append(n[0])
        self.ls_place_index.append(temp)
        if (gx):
            self.place_index.append([[[gx, gy], [x, y], '~']])
        else:
            self.place_index.append([[[x, y], ' ']])

    def record_place_index(self,x, y):#记录港口信息
        temp = self.m.get_all_choice(x, y)
        self.place_index=[]
        self.ls_place_index = []
        for lxc in temp:
            for p in lxc[1:]:
                if (p[2] == '~'):
                    self.finding_new_place(p[0], p[1], lxc[0][0], lxc[0][1])
                elif (p[2] == ' '):
                    self.finding_new_place(p[0], p[1])
        return self.place_index



