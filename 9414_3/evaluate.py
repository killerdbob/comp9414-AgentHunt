from path import *
from index_of_place import *

class eval():
    def __init__(self):
        self.path=[]
        self.temp_path=[]
        self.mahattan=findpath.get_instance()
        self.index=guide.get_instance()
        self.alpha=0
        self.d_tree=[]
        self.d_wall=[]
        self.sta=state.get_instance()
        self.m=getmap.get_instance()

    def need_to_cut(self,x, y):
        num = 0
        do_calcant = False
        for i in range(25):
            if ((self.m.map[x + i//5][y + i%5] in {'d', 'k', 'a', '$', '?'}) and not do_calcant):
                num += 1
        return num
    def do_calc(self,x, y, x0, y0, layer):
        self.d_temp_wall.append([x, y])
        if (self.m.map[x][y] in {'d', 'k', 'a', '$'}):
            return True
        if(layer == 0 or self.mahattan.manhattan_dist(x,y,x0,y0)>5):
            return False
        if ([x - 1, y] not in self.d_temp_wall and self.m.map[x - 1][y] not in {'.', '~'}):
            if (self.sta.num_dynamites_held >= 2 and self.m.map[x - 1][y] == '*' ):
                self.sta.num_dynamites_held -= 1
                if (self.do_calc(x - 1, y, x0, y0,self.sta.num_dynamites_held)):
                    self.sta.num_dynamites_held += 1
                    return True
                self.sta.num_dynamites_held += 1
            if (self.m.map[x - 1][y] != '*' and self.do_calc(x - 1, y, x0, y0,self.sta.num_dynamites_held)):
                return True
        if ([x, y - 1] not in self.d_temp_wall and self.m.map[x][y - 1] not in {'.', '~'}):
            if (self.m.map[x][y - 1] == '*' and self.sta.num_dynamites_held >= 2):
                self.sta.num_dynamites_held -= 1
                if (self.do_calc(x, y - 1, x0, y0,self.sta.num_dynamites_held)):
                    self.sta.num_dynamites_held += 1
                    return True
                self.sta.num_dynamites_held += 1
            if (self.m.map[x][y - 1] != '*' and self.do_calc(x, y - 1, x0, y0,self.sta.num_dynamites_held)):
                return True
        if ([x + 1, y] not in self.d_temp_wall and self.m.map[x  + 1][y] not in {'.', '~'}):
            if ( self.sta.num_dynamites_held >= 2 and self.m.map[x  + 1][y] == '*'):
                self.sta.num_dynamites_held -= 1
                if (self.do_calc(x  + 1, y, x0, y0,self.sta.num_dynamites_held)):
                    self.sta.num_dynamites_held += 1
                    return True
                self.sta.num_dynamites_held += 1
            if (self.m.map[x + 1][y] != '*' and self.do_calc(x + 1, y, x0, y0,self.sta.num_dynamites_held)):
                return True
        if ([x, y + 1] not in self.d_temp_wall and self.m.map[x][y  + 1] not in {'.', '~'}):
            if (self.m.map[x][y  + 1] == '*' and self.sta.num_dynamites_held >= 2):
                self.sta.num_dynamites_held -= 1
                if (self.do_calc(x, y  + 1, x0, y0,self.sta.num_dynamites_held)):
                    self.sta.num_dynamites_held += 1
                    return True
                self.sta.num_dynamites_held += 1
            if (self.m.map[x][y  + 1] != '*' and self.do_calc(x, y + 1, x0, y0,self.sta.num_dynamites_held)):
                return True
        self.d_temp_wall.pop()
        return False
    def important_wall(self,x1, y1):
        self.d_temp_wall = []
        if(self.do_calc(x1, y1, x1, y1,self.sta.num_dynamites_held)):
            return True
        else:
            return False

    def ground_evaluate(self,x, y):
        bomb = []
        tree = []
        key = False
        treasure = []
        dywion = self.m.get_all_choice(x, y)
        for p in dywion:
            for op in p[1:]:
                if (op[2] == 'd' and [op[0], op[1]] not in bomb):
                    bomb.append([op[0], op[1]])
                if (op[2] == 'T' and [op[0], op[1]] not in tree):
                    tree.append([op[0], op[1]])
                if (op[2] == '$' and [op[0], op[1]] not in treasure):
                    treasure.append([op[0], op[1]])
                if (op[2] == 'k'):
                    key = True
        return self.sta.have_key * 0.1 + key * 0.1+len(bomb) * 1 \
        + self.sta.num_dynamites_held * 0.2 +self.sta.have_axe * 0.2


    def change_goal(self,x, y):
        self.path=[]
        self.temp_path=[]
        self.d_tree=[]
        self.d_wall=[]
        self.alpha=0
        self.calculation(x, y)

    def calculation(self,x, y):

        ls_choice = self.m.get_all_choice(x, y)
        if (not self.path):
            self.alpha = -1
        elif (self.sta.game_won):
            return
        if (self.m.map[x][y] == ' ' and self.sta.have_treasure):
            if ([self.m.begin] in ls_choice):
                hjy = [self.m.begin, ' ']
                self.temp_path.append(hjy)
                self.sta.game_won = True
                temp_score = 2
                if (temp_score > self.alpha or (
                        temp_score == self.alpha and len(self.temp_path) < len(self.path))):
                    self.path = [i for i in self.temp_path]
                    self.alpha = temp_score
                    self.temp_path.pop()
                    return
                self.temp_path.pop()

        if (self.m.map[x][y] == ' ' and self.sta.have_key):
            hjy = []
            cjc = []
            for dyw in ls_choice:
                for p in dyw[1:]:
                    if (p[2] == '-'):
                        hjy = dyw[0]
                        cjc = [p[0], p[1]]
            if (hjy and cjc):
                if (self.m.map[cjc[0]][cjc[1]] == '-'):
                    self.m.map[cjc[0]][cjc[1]] = ' '
                    self.temp_path.append([hjy, cjc, 'U'])
                temp_score = self.ground_evaluate(x, y)
                if (temp_score > self.alpha):
                    self.path = [i for i in self.temp_path]
                    self.alpha = temp_score
                self.calculation(cjc[0], cjc[1])
                self.temp_path.pop()
                self.m.map[cjc[0]][cjc[1]] = '-'

        if (self.m.map[x][y] == ' '):
            cjc = []
            for dyw in ls_choice:
                for p in dyw[1:]:
                    if (p[2] in {'d', 'k', 'a', '$'}):
                        if ((cjc and self.mahattan.manhattan_dist(x, y, cjc[0], cjc[1]) >
                            self.mahattan.manhattan_dist(x, y, dyw[0][0],dyw[0][1])) or not cjc):
                            cjc = p
            if (cjc):
                if (self.m.map[cjc[0]][cjc[1]] == 'd'):
                    self.sta.num_dynamites_held += 1
                    self.m.map[cjc[0]][cjc[1]] = ' '
                    self.temp_path.append([cjc, 'd'])
                if (self.m.map[cjc[0]][cjc[1]] == '$'):
                    self.sta.have_treasure =True
                    self.m.map[cjc[0]][cjc[1]] = ' '
                    self.temp_path.append([cjc, '$'])
                if (self.m.map[cjc[0]][cjc[1]] == 'k'):
                    self.sta.have_key += 1
                    self.m.map[cjc[0]][cjc[1]] = ' '
                    self.temp_path.append([cjc, 'k'])
                if (self.m.map[cjc[0]][cjc[1]] == 'a'):
                    self.sta.have_axe += 1
                    self.m.map[cjc[0]][cjc[1]] = ' '
                    self.temp_path.append([cjc, 'a'])
                temp_score = self.ground_evaluate(cjc[0], cjc[1])
                if (temp_score > self.alpha ):
                    self.path = [i for i in self.temp_path]
                    self.alpha = temp_score
                self.calculation(cjc[0], cjc[1])
                self.temp_path.pop()
                self.m.map[cjc[0]][cjc[1]] = cjc[2]
                if (self.m.map[cjc[0]][cjc[1]] == '$'):
                    self.sta.have_treasure = False
                if (self.m.map[cjc[0]][cjc[1]] == 'd'):
                    self.sta.num_dynamites_held -= 1
                if (self.m.map[cjc[0]][cjc[1]] == 'a'):
                    self.sta.have_axe -= 1
                if (self.m.map[cjc[0]][cjc[1]] == 'k'):
                    self.sta.have_key -= 1

        if (self.m.map[x][y] == ' ' and self.sta.have_raft):
            search_ocean = []
            for dyw in ls_choice:
                for p in dyw[1:]:
                    if (p[2] == '~' and [dyw[0], [p[0], p[1]], '~'] in self.index.island_ocean_index
                        and [dyw[0], [p[0], p[1]], '~'] not in search_ocean):
                        search_ocean.append([dyw[0], [p[0], p[1]], '~'])
            if (not search_ocean):
                self.index.chg_habour(x, y)
            for ttk in search_ocean:
                if (ttk not in self.temp_path):
                    cjc = ttk
                else:
                    continue
                self.temp_path.append(cjc)
                temp_score = self.ground_evaluate(cjc[1][0], cjc[1][1])
                if (temp_score > self.alpha or
                        (temp_score == self.alpha and len(self.temp_path) < len(self.path))):
                    self.path = [i for i in self.temp_path]
                    self.alpha = temp_score
                self.calculation(cjc[1][0], cjc[1][1])
                self.temp_path.pop()

        if (self.m.map[x][y] == '~'):
            bibli_temp = []
            for dyw in ls_choice:
                for p in dyw[1:]:
                    if (p[2] == ' ' and [[p[0], p[1]], ' '] in self.index.island_ocean_index
                        and [[p[0], p[1]], ' '] not in bibli_temp):
                        bibli_temp.append([[p[0], p[1]], ' '])
            if (not bibli_temp):
                self.index.chg_habour(x, y)
            for ttk in bibli_temp:
                if (ttk not in self.temp_path):
                    cjc = ttk
                else:
                    continue
                if (cjc):
                    self.temp_path.append(cjc)
                    temp_score = self.ground_evaluate(cjc[0][0], cjc[0][1])
                    if (temp_score > self.alpha):
                        self.path = [i for i in self.temp_path]
                        self.alpha = temp_score
                    temp = self.sta.have_raft
                    self.sta.have_raft = 0
                    self.calculation(cjc[0][0], cjc[0][1])
                    self.sta.have_raft = temp
                    self.temp_path.pop()

        if (self.m.map[x][y] == ' '):
            if (self.sta.num_dynamites_held):
                for dyw in ls_choice:
                    for p in dyw[1:]:
                        if (p[2] == '*' and self.important_wall(p[0], p[1]) and [p[0], p[1]] not in self.d_wall):
                            self.d_wall.append([p[0], p[1]])
                            self.m.map[p[0]][p[1]] = ' '
                            self.sta.num_dynamites_held -= 1
                            self.temp_path.append([dyw[0], [p[0], p[1]], 'B'])
                            temp_score = self.ground_evaluate(p[0], p[1])
                            if (temp_score > self.alpha ):
                                self.path = [i for i in self.temp_path]
                                self.alpha = temp_score
                            self.calculation(p[0], p[1])
                            self.sta.num_dynamites_held += 1
                            self.temp_path.pop()
                            self.m.map[p[0]][p[1]] = '*'
                            self.d_wall.pop()

        if (self.m.map[x][y] == ' '):
            hjy = []
            cjc = []
            if (self.sta.have_axe and not self.sta.have_raft):
                for dyw in ls_choice:
                    for p in dyw[1:]:
                        if ([p[0], p[1]] not in self.d_tree and p[2] == 'T'):
                            hjy = dyw[0]
                            cjc = [p[0], p[1]]
                if (hjy):
                    self.d_tree.append([cjc[0], cjc[1]])
                    self.m.map[cjc[0]][cjc[1]] = ' '
                    self.temp_path.append([hjy, cjc, 'C'])
                    self.sta.have_raft += 1
                    temp_score = self.ground_evaluate(cjc[0], cjc[1])
                    if (temp_score > self.alpha or (
                            temp_score == self.alpha and len(self.temp_path) < len(self.path))):
                        self.path = [i for i in self.temp_path]
                        self.alpha = temp_score
                    self.calculation(cjc[0], cjc[1])
                    self.d_tree.pop()
                    self.m.map[cjc[0]][cjc[1]] = 'T'
                    self.sta.have_raft -= 1
                    self.temp_path.pop()

