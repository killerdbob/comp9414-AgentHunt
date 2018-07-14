#!/usr/bin/env python3
# agent.py
#This program is realised by evaluation and tree. First, it search all the possibility, such as, searching the mist,
#blowing up the wall, make aboat, blow up wall,blow up door. Every possible step ,it will find out.
#Second, it is to pruning the tree, for instance, record a harbour for a island, and this could reduce the possiblity of
#tree.
#Third, it is to find out wich wall need to explode,if we consider every wall, it will be exponential.
#We recorded the searched place and try to search the unknown place.
#The evaluation part is to customized the score by state. For example, if I have dynamites, it will be high score. if I
#used a dynamites wronly, it will score low.
#
#This program can be invoke by some hidden parament,  [-print] could show everystep , --w [float] could show the algorithm
#between greegy and uniform search, when the float value is one, then it is A* search
#We finished this assignment by 7 days after the assinment has released.
#Huang,Wei z5119435 ChengWen, Peng z5103407
#
#
import socket
from argparse import ArgumentParser
from collections import deque
import os
import sys
import math

view=[[str('m') for i in range(5) ] for _ in range(5)]
view[2][2]='I'
imap=15
w=1
best_path=[]
temp_path=[]
used_wall=[]
used_tree=[]
used_ground_mist=[]
used_ocean_mist=[]
island_ocean_index=[]
center_x=round(imap/2)
center_y=round(imap/2)
off_x=0
off_y=0
reduce_mark=0
sys.setrecursionlimit(2147483640)

parser = ArgumentParser()
parser.add_argument('-p', type=int,dest = 'port', required = True)
parser.add_argument('--imap', type=int,dest = 'imap', required = False)
parser.add_argument('--w', type=float,dest = 'w', required = False)
parser.add_argument('-print', dest = 'print', action='store_true',required = False)
args = parser.parse_args()
port = args.port
if(args.imap):
    imap=args.imap
if(args.w):
    w=args.w
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost',port))

irow=round(imap/2)-1
icol=round(imap/2)
row=round(imap/2)
col=round(imap/2)
east = 2
north = 1
west = 0
south = 3
dirn = 1
map=[['m' for _ in range(imap+1)] for _ in range(imap+1)]
map[round(imap/2)][round(imap/2)]=' '
have_axe = 0
have_key = 0
have_raft = 0
game_won = False
game_lost = False
have_treasure = 0
num_dynamites_held = 0
simulate_mark=0

def action(a):
    if(a):
        #print('take action:',a)
        sock.send(bytes(a,encoding='utf-8'))

def print_view():
    global view
    for i in view:
        print(i)

def manhattan_dist(x, y, dx, dy):
    return abs(x - dx) + abs(y - dy)

def read_view():
    global view
    for i in range(5):
        for j in range(5):
            if ((i == 2) and (j == 2)):
                continue
            k = str(sock.recv(1), encoding='utf-8')
            view[i][j]=k
def draw_map():
    global map
    global view
    global row
    global col
    temp=[[str(i) for i in range(5) ] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            if(dirn==0):
               temp[4 - j][ i] = view[i][j]
            if (dirn == 1):
              temp[i][j] = view[i][j]
            if (dirn == 2):
                temp[j][4 - i] = view[i][j]
            if (dirn == 3):
               temp[4 - i][4 - j] = view[i][j]
    for i in range(-2,3):
        for j in range(-2,3):
            if(i!=0 or j!=0):
                map[row + i][col + j] = temp[2+i][2+j]

def forward_step():
    global irow
    global icol
    if(dirn==0):
        irow = row;
        icol = col - 1;
    if (dirn == 1):
        irow = row - 1;
        icol = col;
    if (dirn == 2):
        irow = row;
        icol = col + 1;
    if (dirn == 3):
        irow = row + 1;
        icol = col;

def judge_move(x,y,dx,dy,action=None):
    dd=0
    global dirn
    op = [['', 'R', 'RR', 'L'],
          ['L', '', 'R', 'RR'],
          ['RR', 'L', '', 'R'],
          ['R', 'RR', 'L', '']]
    if(x==dx and y==dy ):
        return ''
    if(x-1==dx and y==dy):#1
        dd=1
    if(x+1==dx and y==dy):#3
        dd=3
    if(x==dx and y+1==dy):#2
        dd=2
    if(x==dx and y-1==dy):#0
        dd=0
    if(action in {'C','U','B'}):
        return op[dirn][dd]+action+'F'
    return op[dirn][dd]+'F'

def change_dirn(a):
    global dirn
    if(a=='L'):
        dirn = (dirn-1)%4
    if(a=='R'):
       dirn = (dirn+1)%4

################################################################################
def find_all_continents(x,y):
    options = find_ocean_options(x,y)
    temp_all_continents =[]
    all_continents=[]
    def looking_for_land(x,y):
        nonlocal temp_all_continents
        nonlocal all_continents
        new_land=[]
        temp=[]
        for i in range(len(temp_all_continents)):
            for j in range(len(temp_all_continents[i])):
                if(temp_all_continents[i][j]==[x,y]):
                    all_continents[i].append([[x,y],' '])
                    return
        new_land = find_ground_options(x,y)
        for n in new_land:
            temp.append(n[0])
        temp_all_continents.append(temp)
        all_continents.append([[[x,y],' ']])
    for opt in options:
        for o in opt[1:]:
            if(o[2]==' '):
                looking_for_land(o[0],o[1])
    return all_continents

def find_all_oceans(x,y):
    options = find_ground_options(x,y)
    temp_all_ocean = []
    all_oceans=[]
    def looking_for_ocean(gx,gy,x, y):
        nonlocal all_oceans
        nonlocal temp_all_ocean
        new_ocean = []
        temp = []
        for i in range(len(temp_all_ocean)):
            for j in range(len(temp_all_ocean[i])):
                if (temp_all_ocean[i][j] == [x, y]):
                    all_oceans[i].append([[gx,gy],[x, y],'~'])
                    return
        new_ocean = find_ocean_options(x, y)
        for n in new_ocean:
            temp.append(n[0])
        temp_all_ocean.append(temp)
        all_oceans.append([[[gx,gy],[x, y],'~']])

    for opt in options:
        for o in opt[1:]:
            if (o[2] == '~'):
                looking_for_ocean(opt[0][0],opt[0][1],o[0], o[1])
    return all_oceans
################################################################################
def ground_neighbor(x,y):
    neighbor=[[x,y]]
    if (map[x - 1][y] not in {' ','.'}):
        neighbor.append([x - 1,y,map[x - 1][y]])
    if (map[x][y + 1] not in {' ','.'}):
        neighbor.append([x, y+1, map[x][y+1]])
    if (map[x + 1][y] not in {' ','.'}):
        neighbor.append([x+1, y, map[x+1][y]])
    if (map[x][y - 1] not in {' ','.'}):
        neighbor.append([x, y-1, map[x][y-1]])

    for i in range(-2,3):
        for j in range(-2,3):
            if (map[x + i][y +j] == 'm' and [x + i, y + j, map[x + i][y + j]] not in neighbor) and (i!=0 or j!=0):
                neighbor.append([x + i, y + j, map[x + i][y + j]])
    if len(neighbor)>1:
        return neighbor
    else:
        return []

def find_ground_options(x,y):
    u = deque()
    temp=[]
    option=[]
    used=[]
    global map
    if(map[x][y] ==' '):
        u.append([x,y])
    else :
        return []

    while(u):
        [x, y]=u.popleft()
        temp=ground_neighbor(x,y)
        if (temp):
            option.append(temp)
        if([x,y]==[center_x,center_y] and [x,y] not in used  and [x,y] not in u):
            option.append([[x,y]])
        used.append([x, y])
        if (map[x-1][y] == ' ' and [x-1,y] not in used and [x-1,y] not in u):
            u.append([x-1, y])
        if (map[x][y+1] == ' ' and [x,y+1] not in used and [x,y+1] not in u):
            u.append([x, y+1])
        if (map[x+1][y] == ' ' and [x+1,y] not in used and [x+1,y] not in u):
            u.append([x+1, y])
        if (map[x][y-1] == ' ' and [x,y-1] not in used and [x,y-1] not in u):
            u.append([x, y-1])
    return option

def ocean_neighbor(x,y):
    neighbor=[[x,y]]
    if (map[x - 1][y] not in {'~','.'}):
        neighbor.append([x - 1, y, map[x - 1][y]])
    if (map[x][y + 1] not in {'~','.'}):
        neighbor.append([x, y + 1, map[x][y + 1]])
    if (map[x + 1][y] not in {'~','.'}):
        neighbor.append([x + 1, y, map[x + 1][y]])
    if (map[x][y - 1] not in {'~','.'}):
        neighbor.append([x, y - 1, map[x][y - 1]])

    for i in range(-2,3):
        for j in range(-2,3):
            if (map[x + i][y +j] == 'm' and [x + i, y + j, map[x + i][y + j]] not in neighbor)and (i!=0 or j!=0):
                neighbor.append([x + i, y + j, map[x + i][y + j]])
    if len(neighbor)>1:
        return neighbor
    else:
        return []

def find_ocean_options(x,y):
    u = deque()
    option=[]
    temp=[]
    used=[]
    global map

    if(map[x][y] =='~'):
        u.append([x,y])
    else :
        return []

    while(u):
        [x, y]=u.popleft()
        temp=ocean_neighbor(x,y)
        if (temp ):
            option.append(temp)
        used.append([x,y])
        if (map[x-1][y] =='~' and [x-1,y] not in used and [x-1,y] not in u):
            u.append([x-1,y])
        if (map[x][y+1] =='~' and [x,y+1] not in used and [x,y+1] not in u):
            u.append([x,y+1])
        if (map[x+1][y] =='~' and [x+1,y] not in used and [x+1,y] not in u):
            u.append([x+1, y])
        if (map[x][y-1] =='~' and [x,y-1] not in used and [x,y-1] not in u):
            u.append([x, y-1])
    return option



def find_path(x,y,dx,dy):

    used_path = []
    path1 = []
    global map
    temp1=''
    temp2=''
    if (map[x][y] in {'d', 'k', 'a', '$'}):
        temp1 = map[x][y]
        map[x][y] = ' '
    if (map[dx][dy] in {'d', 'k', 'a', '$'}):
        temp2 = map[dx][dy]
        map[dx][dy] = ' '
    current_state = map[x][y]

    if (current_state != map[dx][dy] and current_state in {' ','~'} and map[dx][dy] in {' ','~'} and
            ((dx - 1 == x and dy == y) or (dx + 1 == x and dy == y) or (dx == x and dy - 1 == y)
             or (dx == x and dy + 1 == y))):
        return [[x, y], [dx, dy]]
    def recursive_path(cx,cy):
        nonlocal path1
        nonlocal used_path
        nonlocal current_state
        nonlocal x
        nonlocal y
        nonlocal dx
        nonlocal dy
        global w
        path1.append([cx,cy])
        used_path.append([cx,cy])
        if([cx-1,cy]==[dx,dy]):
            path1.append([cx-1, cy])
            return True
        if([cx,cy+1]==[dx,dy]):
            path1.append([cx,cy+1])
            return True
        if([cx+1,cy]==[dx,dy]):
            path1.append([cx+1,cy])
            return True
        if([cx,cy-1]==[dx,dy]):
            path1.append([cx,cy-1])
            return True
        for _ in range(4):
            a_star = []
            temp = []
            if(map[cx-1][cy] == current_state and [cx-1,cy] not in used_path):
                a_star.append([cx-1,cy,w*manhattan_dist(x,y,cx-1,cy)+(2-w)*manhattan_dist(dx,dy,cx-1,cy)])
            if(map[cx][cy+1] == current_state and [cx,cy+1] not in used_path):
                a_star.append([cx,cy+1,w*manhattan_dist(x,y,cx,cy+1)+(2-w)*manhattan_dist(dx,dy,cx,cy+1)])
            if(map[cx+1][cy] == current_state and [cx+1,cy] not in used_path):
                a_star.append([cx+1,cy,w*manhattan_dist(x,y,cx+1,cy)+(2-w)*manhattan_dist(dx,dy,cx+1,cy)])
            if(map[cx][cy-1] == current_state and [cx,cy-1] not in used_path):
                a_star.append([cx,cy-1,w*manhattan_dist(x,y,cx,cy-1)+(2-w)*manhattan_dist(dx,dy,cx,cy-1)])
            if(a_star):
                temp=min(a_star,key=lambda x:x[2])
            if(temp):
                if( recursive_path(temp[0],temp[1])):
                    return True
                else:
                    path1.pop()
        return False

    if(recursive_path(x,y)):
        if (temp1):
            map[x][y]=temp1
        if (temp2):
            map[dx][dy]=temp2
        return path1
    else:
        if (temp1):
            map[x][y]=temp1
        if (temp2):
            map[dx][dy]=temp2
        return []

def ground_evaluate(x,y):
    option=[]
    global used1
    global num_dynamites_held#mark=100
    global have_raft#mark=20
    global have_axe#mark=5
    global have_key#mark=10
    global have_treasure  # mark=99999
    global game_won
    mist=[]
    mark=0
    dynamites=[]
    tree=[]
    key=False
    axe=False
    treasure=[]
    temp_raft=0
    if(map[x][y]==' '):
        option=find_ground_options(x,y)
        for o in option:
            for op in o[1:]:
                if (op[2]=='m' and [op[0],op[1]] not in mist):
                    mist.append([op[0],op[1]])
                if (op[2] == 'd' and [op[0], op[1]] not in dynamites):
                    dynamites.append([op[0], op[1]])
                if (op[2] == 'T' and [op[0], op[1]] not in tree):
                    tree.append([op[0], op[1]])
                if (op[2] == '$' and [op[0], op[1]] not in treasure):
                    treasure.append([op[0], op[1]])
                if (op[2] == 'k'):
                    key=True
                if(op[2]=='a' ):
                    axe=True
        #if([[center_x,center_y]] in option and have_treasure ):
        #    mark=99999
        #    return mark
        mark=len(dynamites)*100+num_dynamites_held*200+((axe or have_axe) and len(tree)>=1)*20\
             +axe*5+ bool(have_axe)*20+bool(have_raft)*4+bool(have_key)*20\
             +key*10+len(mist)*2
    return mark

def ocean_evaluate(x,y):
    global used1
    global num_dynamites_held#mark=100
    global have_raft#mark=20
    global have_axe#mark=5
    global have_key#mark=10
    used1=[]
    mist=[]
    mark = 0
    if(map[x][y]=='~'):
        option = find_ocean_options(x,y)
        for o in option:
            for op in o[1:]:
                if (op[2] == 'm' and [op[0],op[1]] not in mist):
                    mist.append([op[0],op[1]])
        mark = len(mist) + num_dynamites_held * 200 +bool(have_axe) * 20 \
               + bool(have_raft) * 4 + len(mist)*2  + bool(have_key) * 20
    return mark

def is_value_tree(x,y):
    global map
    for i in range(-3,4):
        for j in range(-3, 4):
            if(map[x+i][y+j] in {'d', 'k', 'a', '$','m'}):
                return True
    return False
def is_value(x1,y1):
    used_wall1 = []
    def is_v(x,y,x0,y0,depth=num_dynamites_held):
        global num_dynamites_held
        global map
        nonlocal used_wall1
        used_wall1.append([x, y])
        if (map[x][y] in {'d', 'k', 'a', '$','m'}):
            return True
        if(depth<1):
            return False
        if(manhattan_dist(x,y,x0,y0)>4):
            return False
        for i in {-1,1}:
            if ([x + i,y] not in used_wall1 and map[x + i][y] not in {'.','~'}):
                if(map[x + i][y]=='*' and num_dynamites_held>1):
                    num_dynamites_held-=1
                    if(is_v(x + i,y,x0,y0)):
                        num_dynamites_held+=1
                        return True
                    num_dynamites_held += 1
                elif(map[x + i][y]!='*' and is_v(x + i, y,x0,y0)):
                        return True
            if ([x,y + i] not in used_wall1 and map[x][y + i] not in {'.','~'}):
                if(map[x][y + i]=='*' and num_dynamites_held>1):
                    num_dynamites_held-=1
                    if(is_v(x, y + i,x0,y0)):
                        num_dynamites_held+=1
                        return True
                    num_dynamites_held += 1
                elif(map[x][y + i]!='*' and is_v(x, y + i,x0,y0)):
                        return True
        used_wall1.pop()
        return False
    return is_v(x1,y1,x1,y1)

def init_value():
    global simulate_mark
    global best_path
    global used_wall
    global used_tree
    global used_ground_mist
    global used_ocean_mist
    simulate_mark=0
    best_path = []
    used_wall = []
    used_tree = []
    used_ground_mist=[]
    used_ocean_mist=[]

def simulate(x,y):
    global temp_path
    global best_path
    global used_tree
    global used_wall
    global used_ground_mist
    global used_ocean_mist
    global simulate_mark
    global have_axe
    global have_key
    global have_raft
    global game_won
    global have_treasure
    global num_dynamites_held
    global island_ocean_index
    global reduce_mark
    option=[]
    if(map[x][y] == ' '):
        g_option=find_ground_options(x,y)
    if (map[x][y] == '~'):
        o_option=find_ocean_options(x,y)
    if( best_path == []):# do nothing ,just waiting for death
        simulate_mark=-99999
    if (game_won):
        return
    if (map[x][y] == ' '):  # find the treasure and go home
        if(have_treasure and [[center_x,center_y]] in g_option):
            temp1=[[center_x,center_y],' ']
            temp_path.append(temp1)
            game_won = True
            temp_mark = 99999
            if (temp_mark>simulate_mark or(temp_mark==simulate_mark and len(temp_path)<len(best_path))):
                best_path = [i for i in temp_path]
                simulate_mark=temp_mark
                temp_path.pop()
                return
            temp_path.pop()

    if (map[x][y] == ' '):  # open door
        if(have_key):
            temp1 = []
            temp2 = []
            for opt in g_option:
                for o in opt[1:]:
                    if(o[2] == '-'):
                        if((temp1 and manhattan_dist(x,y,temp1[0],temp1[1])>manhattan_dist(x,y,opt[0][0],opt[0][1]))
                           or not temp1):
                            temp1=opt[0]
                            temp2=[o[0],o[1]]
                            break
            if(temp1 and temp2 ):
                if(map[temp2[0]][temp2[1]]=='-'):
                    map[temp2[0]][temp2[1]] = ' '
                    temp_path.append([temp1,temp2,'U'])
                temp_mark = ground_evaluate(x,y)
                if(temp_mark > simulate_mark or (temp_mark == simulate_mark and len(temp_path)<len(best_path))):
                    best_path=[i for i in temp_path]
                    simulate_mark = temp_mark
                simulate(temp2[0],temp2[1])
                temp_path.pop()
                map[temp2[0]][temp2[1]]='-'

    if(map[x][y]==' '):#pick treasure
        temp1 = []
        temp2 = []
        for opt in g_option:
            for o in opt[1:]:
                if(o[2] in {'d','k','a','$'}):
                    if((temp2 and manhattan_dist(x,y,temp2[0],temp2[1])>manhattan_dist(x,y,opt[0][0],opt[0][1]))or not temp2):
                        temp2=o
                        break
        if(temp2):
            if(map[temp2[0]][temp2[1]]=='d'):
                num_dynamites_held+=1
                map[temp2[0]][temp2[1]] = ' '
                temp_path.append([temp2,'d'])
            if(map[temp2[0]][temp2[1]]=='k'):
                have_key+=1
                map[temp2[0]][temp2[1]] = ' '
                temp_path.append([temp2,'k'])
            if(map[temp2[0]][temp2[1]]=='a'):
                have_axe+=1
                map[temp2[0]][temp2[1]] = ' '
                temp_path.append([temp2,'a'])
            if(map[temp2[0]][temp2[1]]=='$'):
                have_treasure+=1
                map[temp2[0]][temp2[1]] = ' '
                temp_path.append([temp2,'$'])
            temp_mark = ground_evaluate(temp2[0],temp2[1])
            if(temp_mark > simulate_mark or (temp_mark == simulate_mark and len(temp_path)<len(best_path))):
                best_path=[i for i in temp_path]
                simulate_mark=temp_mark
            simulate(temp2[0],temp2[1])
            temp_path.pop()
            map[temp2[0]][temp2[1]]=temp2[2]
            if(map[temp2[0]][temp2[1]]=='d'):
                num_dynamites_held-=1
            if(map[temp2[0]][temp2[1]]=='k'):
                have_key-=1
            if(map[temp2[0]][temp2[1]]=='a'):
                have_axe-=1
            if(map[temp2[0]][temp2[1]]=='$'):
                have_treasure-=1

    if (map[x][y] == ' '):  # prepare for sailing
        if(have_raft):
            temp2 = []
            search_ocean = []
            sc=[]
            for opt in g_option:
                for o in opt[1:]:
                    if (o[2] =='~' and [opt[0],[o[0],o[1]],'~'] in island_ocean_index
                        and [opt[0],[o[0],o[1]],'~'] not in search_ocean):
                        search_ocean.append([opt[0],[o[0],o[1]],'~'])
            if( not search_ocean):
                for i in find_all_oceans(x,y):
                    search_ocean.append(i[0])
                    if(i[0] not in island_ocean_index):
                        island_ocean_index.append(i[0])
            for sc in search_ocean:
                if (sc not in temp_path):
                    temp2 = sc
                else:
                    continue
                temp_path.append(temp2)
                temp_mark = ocean_evaluate(temp2[1][0], temp2[1][1])
                if (temp_mark > simulate_mark or (temp_mark == simulate_mark and len(temp_path)<len(best_path))):
                    best_path = [i for i in temp_path]
                    simulate_mark = temp_mark
                simulate(temp2[1][0], temp2[1][1])
                temp_path.pop()

    if (map[x][y] == '~'):  # find a new continent
        temp1 = []
        temp2 = []
        search_continent=[]
        for opt in o_option:
            for o in opt[1:]:
                if (o[2] == ' ' and [[o[0], o[1]], ' '] in island_ocean_index
                    and [[o[0], o[1]], ' '] not in search_continent):
                    search_continent.append([[o[0], o[1]],  ' '])
        if (not search_continent):
            for i in find_all_continents(x,y):
                search_continent.append(i[0])
                if (i[0] not in island_ocean_index):
                    island_ocean_index.append(i[0])
        for sc in search_continent:
            if (sc not in temp_path):
                temp2=sc
            else:
                continue
            if (temp2 ):
                temp_path.append(temp2)
                temp_mark = ground_evaluate(temp2[0][0],temp2[0][1])
                u_wall=used_wall
                used_wall=[]
                if (temp_mark > simulate_mark or (temp_mark == simulate_mark and len(temp_path)<len(best_path))):
                    best_path = [i for i in temp_path]
                    simulate_mark = temp_mark
                temp = have_raft
                have_raft = 0
                simulate(temp2[0][0], temp2[0][1])
                used_wall = u_wall
                have_raft = temp
                temp_path.pop()
    if (map[x][y] == ' '):  # blow up wall
        if(num_dynamites_held):
            temp1 = []
            temp2 = []
            for opt in g_option:
                for o in opt[1:]:
                    if (o[2] == '*' and is_value(o[0],o[1]) and [o[0], o[1]] not in used_wall):
                        used_wall.append([o[0], o[1]])
                        temp1 = opt[0]
                        temp2 = [o[0], o[1]]
                        map[temp2[0]][temp2[1]]=' '
                        num_dynamites_held -= 1
                        temp_path.append([temp1,temp2,'B'])
                        temp_mark = ground_evaluate(temp2[0],temp2[1])
                        if(temp_mark > simulate_mark or (temp_mark == simulate_mark and len(temp_path)<len(best_path))):
                            best_path=[i for i in temp_path]
                            simulate_mark = temp_mark
                        simulate(temp2[0],temp2[1])
                        num_dynamites_held +=1
                        temp_path.pop()
                        map[temp2[0]][temp2[1]] = '*'
                        used_wall.pop()

    if (map[x][y] == ' '):  # make a boat
        temp1 = []
        temp2 = []
        if(have_axe and not have_raft):
            for opt in g_option:
                for o in opt[1:]:
                    if ([o[0], o[1]] not in used_tree and o[2] == 'T' and
                            ((temp1 and manhattan_dist(x,y,temp1[0],temp1[1])>manhattan_dist(x,y,opt[0][0],opt[0][1]))
                             or not temp1)):
                        temp1 = opt[0]
                        temp2 = [o[0], o[1]]
            if(temp1):
                used_tree.append([temp2[0],temp2[1]])
                map[temp2[0]][temp2[1]] = ' '
                temp_path.append([temp1,temp2,'C'])
                have_raft += 1
                temp_mark = ground_evaluate(temp2[0],temp2[1])
                if(temp_mark > simulate_mark or (temp_mark == simulate_mark and len(temp_path)<len(best_path))):
                    best_path=[i for i in temp_path]
                    simulate_mark=temp_mark
                simulate(temp2[0],temp2[1])
                have_raft -= 1
                temp_path.pop()
                map[temp2[0]][temp2[1]]='T'

def print_map():
    os.system('clear')
    for i in range(len(map)):
        for j in range(len(map[0])):
            if(i==row and j==col):
                print('I', end='')
            else:
                print(map[i][j],end='')
        print()

def move(x,y,dx,dy,act=''):
    global row
    global col
    global have_axe
    global have_key
    global have_raft
    global have_treasure
    global num_dynamites_held
    global center_x
    global center_y
    global map
    global off_x
    global off_y
    action_str=''
    if (act == 'C'):
        have_raft += 1
    if (act == 'B'):
        num_dynamites_held -= 1
    if( act):
        temp = find_path(row, col, x, y)
    else:
        if (map[row][col] == '~' and map[dx][dy] in {' ','d','$','a','k','-','T','*'} ):
            have_raft = 0
        temp = find_path(row,col, dx, dy)
    for p in temp:
        action_str=judge_move(row,col,p[0]+off_x,p[1]+off_y)
        if(not action_str):
            continue
        for a_s in action_str:
            if(a_s == 'F'):
                if (row + 6 >= len(map)):
                    temp_map = [['m' for _ in range(len(map[0]))] for _ in range(len(map) + 2)]
                    for i in range(len(map)):
                        for j in range(len(map[0])):
                            temp_map[i][j] = map[i][j]
                    map = [[i for i in temp_map[j]] for j in range(len(temp_map))]
                elif (row - 6 < 0):
                    temp_map = [['m' for _ in range(len(map[0]))] for _ in range(len(map) + 2)]
                    for i in range(len(map)):
                        for j in range(len(map[0])):
                            temp_map[i + 2][j] = map[i][j]
                    map = [[i for i in temp_map[j]] for j in range(len(temp_map))]
                    center_x += 2
                    off_x += 2
                elif (col + 6 >= len(map[0])):
                    temp_map = [['m' for _ in range(len(map[0]) + 2)] for _ in range(len(map))]
                    for i in range(len(map)):
                        for j in range(len(map[0])):
                            temp_map[i][j] = map[i][j]
                    map = [[i for i in temp_map[j]] for j in range(len(temp_map))]
                elif (col - 6 < 0):
                    temp_map = [['m' for _ in range(len(map[0]) + 2)] for _ in range(len(map))]
                    for i in range(len(map)):
                        for j in range(len(map[0])):
                            temp_map[i][j + 2] = map[i][j]
                    map = [[i for i in temp_map[j]] for j in range(len(temp_map))]
                    center_y += 2
                    off_y += 2
                [row, col] = [p[0]+off_x, p[1]+off_y]
            action(a_s)
            change_dirn(a_s)
            read_view()
            draw_map()
            forward_step()
            if(args.print):
                print_map()
    [x, y] = [x + off_x, y + off_y]
    [dx, dy] = [dx + off_x, dy + off_y]
    if bool(act):
        action_str=judge_move(row,col,dx,dy,action=act)
        for a_s in action_str:
            if(a_s == 'F'):
                if (row + 6 > len(map)):
                    temp_map = [['m' for _ in range(len(map[0]))] for _ in range(len(map) + 2)]
                    for i in range(len(map)):
                        for j in range(len(map[0])):
                            temp_map[i][j] = map[i][j]
                    map = [[i for i in temp_map[j]] for j in range(len(temp_map))]
                elif (row - 6 < 0):
                    temp_map = [['m' for _ in range(len(map[0]))] for _ in range(len(map) + 2)]
                    for i in range(len(map)):
                        for j in range(len(map[0])):
                            temp_map[i + 2][j] = map[i][j]
                    map = [[i for i in temp_map[j]] for j in range(len(temp_map))]
                    center_x += 2
                    off_x += 2
                    row+=1
                elif (col + 6 > len(map[0])):
                    temp_map = [['m' for _ in range(len(map[0]) + 2)] for _ in range(len(map))]
                    for i in range(len(map)):
                        for j in range(len(map[0])):
                            temp_map[i][j] = map[i][j]
                    map = [[i for i in temp_map[j]] for j in range(len(temp_map))]
                elif (col - 6 < 0):
                    temp_map = [['m' for _ in range(len(map[0]) + 2)] for _ in range(len(map))]
                    for i in range(len(map)):
                        for j in range(len(map[0])):
                            temp_map[i][j + 2] = map[i][j]
                    map = [[i for i in temp_map[j]] for j in range(len(temp_map))]
                    center_y += 2
                    off_y += 2
                    col+=1
                else:
                    [row,col]=[dx,dy]
            action(a_s)
            change_dirn(a_s)
            read_view()
            draw_map()
            forward_step()

    if(map[row][col]=='d'):
        map[row][col]=' '
        num_dynamites_held += 1
    if(map[row][col]=='k'):
        map[row][col]=' '
        have_key += 1
    if(map[row][col]=='a'):
        map[row][col]=' '
        have_axe += 1
    if(map[row][col]=='$'):
        map[row][col]=' '
        have_treasure += 1
    return
main_option=[]
main_path=[]
main_temp1=[]
g_think = False
o_think = False
read_view()
draw_map()
try:
    while(not game_won):
        #print('direction: ',dirn)
        #print_view()
        #print_map()
        #print('boat##############################',have_raft)
        #print('num_dynamites_held:',num_dynamites_held)
        main_temp1=[]

        #print('current location:',map[row][col])
        if (map[row][col] ==' '):
            off_x = 0
            off_y = 0
            main_option=find_ground_options(row,col)
            #print('options:',main_option)
            #print(main_option)
            #print('current_location:'[row,col])
            for opt in main_option:
                for o in opt[1:]:
                    if (o[2] == 'm'):
                        if ((main_temp1 and manhattan_dist(row, col, main_temp1[0], main_temp1[1])
                            > manhattan_dist(row, col, opt[0][0], opt[0][1])) or not main_temp1):
                            main_temp1 = opt[0]
                            g_think=True
            if(main_temp1):
                move(row,col,main_temp1[0],main_temp1[1])
                continue
            elif(g_think):
                g_think=False
                for i in find_all_oceans(row, col):
                    if (i[0] not in island_ocean_index):
                        island_ocean_index.append(i[0])
        if (map[row][col] == '~'):
            off_x = 0
            off_y = 0
            main_option=find_ocean_options(row,col)
            for opt in main_option:
                for o in opt[1:]:
                    if (o[2] == 'm'):
                        if ((main_temp1 and manhattan_dist(row, col, main_temp1[0], main_temp1[1])
                            > manhattan_dist(row, col, opt[0][0], opt[0][1])) or not main_temp1):
                            main_temp1 = opt[0]
                            o_think=True
            if(main_temp1):
                move(row,col,main_temp1[0],main_temp1[1])
                continue
            elif(o_think):
                o_think=False
                for i in find_all_continents(row, col):
                    if (i[0] not in island_ocean_index):
                        island_ocean_index.append(i[0])
        if (not main_temp1):
            #print('have_axe:',str(have_axe))
            #print(find_ground_options(row,col))
            init_value()
            temp_off_x=0
            temp_off_y=0
            simulate(row,col)
            #print('best_path:', best_path, 'simulate_mark:', simulate_mark)
            for i in range(len(best_path)):
                off_x=0
                off_y=0
                path=best_path[i]
                if(path[-1] not in {'U','B','C'}):
                    #print('path[' + str(i) + ']:', path[0], path[1])
                    move(row,col,path[0][0]+temp_off_x,path[0][1]+temp_off_y)
                    temp_off_x += off_x
                    temp_off_y += off_y
                    if(path[-1]=='~'):
                        move(row, col, path[1][0]+temp_off_x, path[1][1]+temp_off_y)
                        temp_off_x += off_x
                        temp_off_y += off_y
                    if(path[0]==[center_x,center_y]):
                        sock.close()
                if(path[-1] in {'U','B','C'}):
                    #print('path[0][0], path[0][1],path[1][0],path[1][1],a=path[2]:',path[0][0], path[0][1], path[1][0], path[1][1],path[-1])
                    move(path[0][0]+temp_off_x, path[0][1]+temp_off_y, path[1][0]+temp_off_x, path[1][1]+temp_off_y,act=path[-1])
                    temp_off_x += off_x
                    temp_off_y += off_y
        #print('main_best_path:', best_path)
except ConnectionResetError:
    os.system('clear')
    sys.exit()


