from argparse import ArgumentParser
from Connectserver import *
from evaluate import *
import sys

class agent():
    def __init__(self,port):
        self.sta=state.get_instance()
        self.m=getmap.get_instance()
        self.pat=findpath.get_instance()
        self.comm=Connectsever.get_instance(port)
        self.place=guide.get_instance()
        self.eva=eval()

    def shift(self, x, y, target_x, target_y, act=''):
        if (act == 'C'):#做事情
            self.sta.have_raft += 1
        if (act == 'B'):
            self.sta.num_dynamites_held -= 1
        if (act):
            temp = self.pat.change(self.sta.row, self.sta.col, x, y)#查找路径
        else:
            if (self.m.map[self.sta.row][self.sta.col] == '~' and self.m.map[target_x][target_y] == ' '):
                self.sta.have_raft = 0
            temp = self.pat.change(self.sta.row, self.sta.col, target_x, target_y)
        for p in temp:#每一步做事情
            action_str = self.pat.next_step(self.sta.row, self.sta.col, p[0], p[1])
            if (not action_str):
                continue
            for a_s in action_str:
                if (a_s == 'F'):#如果向前走 改变自己的坐标
                    [self.sta.row, self.sta.col] = [p[0], p[1]]
                self.comm.action(a_s)
                self.m.change_dirn(a_s)
                self.comm.read_view()
        if (self.m.map[self.sta.row][self.sta.col] == '$'):#如果是钱 改变状态
            self.sta.have_treasure =True
            self.m.map[self.sta.row][self.sta.col] = ' '
        elif (self.m.map[self.sta.row][self.sta.col] == 'd'):#同上
            self.sta.num_dynamites_held += 1
            self.m.map[self.sta.row][self.sta.col] = ' '
        elif (self.m.map[self.sta.row][self.sta.col] == 'k'):#同上
            self.sta.have_key += 1
            self.m.map[self.sta.row][self.sta.col] = ' '
        elif (self.m.map[self.sta.row][self.sta.col] == 'a'):#同上
            self.sta.have_axe += 1
            self.m.map[self.sta.row][self.sta.col] = ' '
        if bool(act):
            action_str = self.pat.next_step(self.sta.row, self.sta.col, target_x, target_y, action=act)
            for a_s in action_str:
                if (a_s == 'F'):#如果向前走 改变自己的坐标
                    [self.sta.row, self.sta.col] = [target_x, target_y]
                self.comm.action(a_s)#发送指令给服务器
                self.m.change_dirn(a_s)#改变方向
                self.comm.read_view()#接收服务器的地图

        return
    def crack(self):
        self.comm.read_view()
        try:
            while(True):
                final_decision_1=[]
                final_decision_2=[]
                if (self.m.map[self.sta.row][self.sta.col] == '~'):#如果是海
                    final_decision=self.m.get_all_choice(self.sta.row,self.sta.col)
                    temp=[]
                    for gjy in final_decision:
                        for p in gjy[1:]:
                            if (p[2] == '^'):#找未探索地点
                                final_decision_1 = gjy[0]
                                self.sta.refresh_place=True
                                break
                    if(final_decision_1):
                        self.shift(self.sta.row,self.sta.col,final_decision_1[0],final_decision_1[1])
                        continue
                    elif(self.sta.refresh_place):
                        self.place.chg_habour(self.sta.row,self.sta.col)
                        self.sta.refresh_place = False
                else:
                    final_decision=self.m.get_all_choice(self.sta.row,self.sta.col)
                    for gjy in final_decision:
                        for p in gjy[1:]:
                            if ( self.sta.have_axe and p[2] == 'T' and self.eva.need_to_cut(p[0],p[1])):#砍树
                                final_decision_1 = gjy[0]
                                final_decision_2 = [p[0],p[1]]
                                break
                            if (p[2] == '^' and not final_decision_2):#找未探索地点
                                final_decision_1 = gjy[0]
                                final_decision_2=[]
                                self.sta.refresh_place=True
                                break
                            if (p[2] in {'d', '$', 'k', 'a'} and not final_decision_2):#捡各种宝物
                                final_decision_1 = [p[0], p[1]]
                                final_decision_2 = []
                                break
                            if (self.sta.have_treasure and gjy[0]==[self.m.begin]):#有宝藏了，回家
                                final_decision_1 = [gjy[0][0], gjy[0][1]]
                                final_decision_2 = []
                                break
                        if(final_decision_1):
                            break
                    if(final_decision_1):
                        if(final_decision_2 ):
                            if(self.m.map[final_decision_2[0]][final_decision_2[1]]=='T'):
                                self.shift(final_decision_1[0], final_decision_1[1], final_decision_2[0], final_decision_2[1],act='C')
                        self.shift(self.sta.row, self.sta.col, final_decision_1[0], final_decision_1[1])
                        continue
                    elif(self.sta.refresh_place):
                        self.sta.refresh_place=False
                        self.place.chg_habour(self.sta.row,self.sta.col)
                if (not final_decision_1):
                    self.eva.change_goal(self.sta.row,self.sta.col)
                    for i in self.eva.path:
                        if(i[-1] in {'C','U','B'}):
                            self.shift(i[0][0], i[0][1], i[1][0], i[1][1],act=i[-1])
                        else:
                            self.shift(self.sta.row,self.sta.col,i[0][0],i[0][1])
                            if(i[-1]=='~'):
                                self.shift(self.sta.row, self.sta.col, i[1][0], i[1][1])
        except ConnectionResetError:
            sys.exit()

if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', type=int, dest='port', required=True)
    args = parser.parse_args()
    test=agent(args.port)
    test.crack()