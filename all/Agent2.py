#!/usr/bin/env python3
# Agent.py
import socket
from argparse import ArgumentParser
from collections import deque
import os
import sys
import math

view=[[str('?') for i in range(5) ] for _ in range(5)]
view[2][2]='I'
inavigation=90
The_one=[]
ls_trace=[]
trash_wall=[]
trash_tree=[]
trash_ground_mist=[]
trash_ocean_mist=[]
island_ocean_index=[]
reduce_score=0

important_choice=[]
main_path=[]
important_choice_1=[]
land_flag = False
ocean_flag = False
parser = ArgumentParser()
parser.add_argument('-p', type=int,dest = 'port', required = True)
args = parser.parse_args()
port = args.port

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost',port))

row=45
col=45
E = 2
N = 1
W = 0
S = 3
compass = 1
navigation=[['?' for _ in range(inavigation+1)] for _ in range(inavigation+1)]
navigation[45][45]=' '
num_of_axe = 0
num_of_key = 0
num_of_raft = 0
game_won = False
game_lost = False
is_money = 0
num_dynamites_held = 0
calculation_score=0

def recieve_view():
    global view
    for i in range(25):
        if not i==12:
            k = str(sock.recv(1), encoding='utf-8')
            view[i//5][i%5] = k
def draw_navigation():
    global navigation
    global view
    global row
    global col
    def rot90(tt):
        tt[:] = map(list, zip(*tt[::-1]))
    for _ in range((compass-1)%4):
        rot90(view)
    for i in {0,1,-1,2,-2}:
        for j in {0,1,-1,2,-2}:
            if not (i==0 and j==0):
                navigation[row + i][col + j] = view[i+2][j+2]

def M_distance(x, y, target_x, target_y):
    return abs(y - target_y) + abs(x - target_x)

def judge_move(x,y,target_x,target_y,action=''):
    dd=0
    global compass
    if(x==target_x and y==target_y ):
        return ''
    if(x-1==target_x and y==target_y):
        dd=1
    elif(x+1==target_x and y==target_y):
        dd=3
    elif(x==target_x and y+1==target_y):
        dd=2
    else:
        dd=0
    return (compass-dd)%4*'L'+action+'F'

def chg_compass(b):
    global compass
    if(b=='L'):
        compass = (compass-1)%4
    if(b=='R'):
        compass = (compass+1)%4

def record_bibliography(x,y):
    pcwions = get_all_choice(x,y)
    ls_bibliography =[]
    bibliography=[]
    global navigation
    def looking_for_land(x,y,gx=None,gy=None):
        nonlocal ls_bibliography
        nonlocal bibliography
        global navigation
        temp=[]
        for i in range(len(ls_bibliography)):
            for j in range(len(ls_bibliography[i])):
                if (ls_bibliography[i][j] == [x, y] and gx ):
                    bibliography[i].append([[gx,gy],[x, y],'~'])
                    return
                elif(ls_bibliography[i][j] == [x,y]):
                    bibliography[i].append([[x,y],' '])
                    return
        new_land = get_all_choice(x,y)
        for n in new_land:
            temp.append(n[0])
        ls_bibliography.append(temp)
        if(gx):
            bibliography.append([[[gx, gy], [x, y], '~']])
        else:
            bibliography.append([[[x,y],' ']])
    for pcw in pcwions:
        for p in pcw[1:]:
            if (p[2] == '~'):
                looking_for_land(p[0], p[1],pcw[0][0],pcw[0][1])
            elif(p[2] == ' '):
                looking_for_land(p[0],p[1])
    return bibliography

def get_all_choice(x,y):
    def ground_neighbor(x, y):
        neighbor = [[x, y]]
        not_in_search = {'.', navigation[x][y]}
        for i in {-2,-1,2,1}:
            if (navigation[x + i][y + i] == '?' and [x + i, y, navigation[x + i][y + i]] not in neighbor):
                neighbor.append([x + i, y + i, navigation[x + i][y + i]])
            if (navigation[x + i][y - i] == '?' and [x + i, y, navigation[x + i][y - i]] not in neighbor):
                neighbor.append([x + i, y - i, navigation[x + i][y - i]])
        for i in {-1,1}:
            if (navigation[x + i][y] not in not_in_search):
                neighbor.append([x + i, y, navigation[x + i][y]])
            if (navigation[x][y + i] not in not_in_search):
                neighbor.append([x, y + i, navigation[x][y + i]])
        if len(neighbor) > 1:
            return neighbor
        else:
            return []
    u = deque()
    temp=[]
    pcwion=[]
    trash=[]
    global navigation
    u.append([x,y])
    while(u):
        [x, y]=u.popleft()
        temp = ground_neighbor(x, y)
        if (temp):
            pcwion.append(temp)
        if([x,y]==[45,45] and [x,y] not in trash  and [x,y] not in u):
            pcwion.append([[x,y]])
        trash.append([x, y])
        if (navigation[x-1][y] == navigation[x][y] and [x-1,y] not in trash and [x-1,y] not in u):
            u.append([x-1, y])
        if (navigation[x][y+1] == navigation[x][y] and [x,y+1] not in trash and [x,y+1] not in u):
            u.append([x, y+1])
        if (navigation[x+1][y] == navigation[x][y] and [x+1,y] not in trash and [x+1,y] not in u):
            u.append([x+1, y])
        if (navigation[x][y-1] == navigation[x][y] and [x,y-1] not in trash and [x,y-1] not in u):
            u.append([x, y-1])
    return pcwion

def find_path(x,y,target_x,target_y):
    trash_path = []
    path1 = []
    global navigation
    def recursion(cx,cy):
        nonlocal path1
        nonlocal trash_path
        nonlocal x
        nonlocal y
        nonlocal target_x
        nonlocal target_y
        path1.append([cx,cy])
        trash_path.append([cx,cy])
        if([cx-1,cy]==[target_x,target_y]):
            path1.append([cx-1, cy])
            return True
        if([cx,cy+1]==[target_x,target_y]):
            path1.append([cx,cy+1])
            return True
        if([cx+1,cy]==[target_x,target_y]):
            path1.append([cx+1,cy])
            return True
        if([cx,cy-1]==[target_x,target_y]):
            path1.append([cx,cy-1])
            return True
        a_star = []
        temp = []
        if(navigation[cx-1][cy] == navigation[x][y] and [cx-1,cy] not in trash_path):
            a_star.append([cx-1,cy,M_distance(target_x,target_y,cx-1,cy)])
        if(navigation[cx][cy+1] == navigation[x][y] and [cx,cy+1] not in trash_path):
            a_star.append([cx,cy+1,M_distance(target_x,target_y,cx,cy+1)])
        if(navigation[cx+1][cy] == navigation[x][y] and [cx+1,cy] not in trash_path):
            a_star.append([cx+1,cy,M_distance(target_x,target_y,cx+1,cy)])
        if(navigation[cx][cy-1] == navigation[x][y] and [cx,cy-1] not in trash_path):
            a_star.append([cx,cy-1,M_distance(target_x,target_y,cx,cy-1)])
        a_star.sort(key=lambda x:x[2],reverse=True)
        while(a_star):
            if(a_star):
                temp=a_star.pop()
            if(temp):
                if( recursion(temp[0],temp[1])):
                    return True
                else:
                    path1.pop()
        return False
    flag=recursion(x, y)
    if(flag):
        return path1
    else:
        return []

def ground_evaluate(x,y):
    global trash1
    global num_dynamites_held
    global num_of_axe
    global num_of_key
    global is_money
    global game_won
    target_ynamites=[]
    tree=[]
    key=False
    treasure=[]
    pcwion=get_all_choice(x,y)
    for p in pcwion:
        for op in p[1:]:
            if (op[2] == 'd' and [op[0], op[1]] not in target_ynamites):
                target_ynamites.append([op[0], op[1]])
            if (op[2] == 'T' and [op[0], op[1]] not in tree):
                tree.append([op[0], op[1]])
            if (op[2] == '$' and [op[0], op[1]] not in treasure):
                treasure.append([op[0], op[1]])
            if (op[2] == 'k'):
                key=True
    score=len(target_ynamites)*100+num_dynamites_held*200+bool(num_of_axe)*20+bool(num_of_key)*20+key*10
    return score

def num_of_treasure(x,y):
    global navigation
    num=0
    is_important=False
    for i in range(-2,3):
        for j in range(-2, 3):
            if((navigation[x+i][y+j] in {'d', 'k', 'a', '$','?'})and not is_important):
                num+=1
    return num
def important_wall(x1,y1):
    trash_wall1 = []
    def is_import(x,y,x0,y0,depth=num_dynamites_held):
        global num_dynamites_held
        global navigation
        nonlocal trash_wall1
        trash_wall1.append([x, y])
        if (navigation[x][y] in {'d', 'k', 'a', '$','?'}):
            return True
        if(depth<1):
            return False
        if(M_distance(x,y,x0,y0)>4):
            return False
        for i in {-1,1}:
            if ([x + i,y] not in trash_wall1 and navigation[x + i][y] not in {'.','~'}):
                if(navigation[x + i][y]=='*' and num_dynamites_held>1):
                    num_dynamites_held-=1
                    if(is_import(x + i,y,x0,y0)):
                        num_dynamites_held+=1
                        return True
                    num_dynamites_held += 1
                elif(navigation[x + i][y]!='*' and is_import(x + i, y,x0,y0)):
                        return True
            if ([x,y + i] not in trash_wall1 and navigation[x][y + i] not in {'.','~'}):
                if(navigation[x][y + i]=='*' and num_dynamites_held>1):
                    num_dynamites_held-=1
                    if(is_import(x, y + i,x0,y0)):
                        num_dynamites_held+=1
                        return True
                    num_dynamites_held += 1
                elif(navigation[x][y + i]!='*' and is_import(x, y + i,x0,y0)):
                        return True
        trash_wall1.pop()
        return False
    return is_import(x1,y1,x1,y1)

def calculation(x,y):
    global ls_trace
    global num_of_key
    global num_of_raft
    global game_won
    global The_one
    global trash_tree
    global trash_wall
    global trash_ground_mist
    global num_of_axe
    global trash_ocean_mist
    global calculation_score
    global is_money
    global num_dynamites_held
    global island_ocean_index
    ls_choice=get_all_choice(x,y)
    if( The_one == []):
        calculation_score=-100
    if(game_won):
        return
    if (navigation[x][y] == ' ' and is_money):
        if([[45,45]] in ls_choice):
            lzq=[[45,45],' ']
            ls_trace.append(lzq)
            game_won = True
            temp_score = 1000
            if (temp_score>calculation_score or(temp_score==calculation_score and len(ls_trace)<len(The_one))):
                The_one = [i for i in ls_trace]
                calculation_score=temp_score
                ls_trace.pop()
                return
            ls_trace.pop()

    if (navigation[x][y] == ' ' and num_of_key):
        lzq = []
        klnh = []
        for pcw in ls_choice:
            for p in pcw[1:]:
                if(p[2] == '-'):
                    if((lzq and M_distance(x,y,lzq[0],lzq[1])>M_distance(x,y,pcw[0][0],pcw[0][1]))
                       or not lzq):
                        lzq=pcw[0]
                        klnh=[p[0],p[1]]
        if(lzq and klnh ):
            if(navigation[klnh[0]][klnh[1]]=='-'):
                navigation[klnh[0]][klnh[1]] = ' '
                ls_trace.append([lzq,klnh,'U'])
            temp_score = ground_evaluate(x,y)
            if(temp_score > calculation_score or (temp_score == calculation_score and len(ls_trace)<len(The_one))):
                The_one=[i for i in ls_trace]
                calculation_score = temp_score
            calculation(klnh[0],klnh[1])
            ls_trace.pop()
            navigation[klnh[0]][klnh[1]]='-'

    if(navigation[x][y]==' '):
        lzq = []
        klnh = []
        for pcw in ls_choice:
            for p in pcw[1:]:
                if(p[2] in {'d','k','a','$'}):
                    if((klnh and M_distance(x,y,klnh[0],klnh[1])>M_distance(x,y,pcw[0][0],pcw[0][1]))or not klnh):
                        klnh=p
        if(klnh):
            if(navigation[klnh[0]][klnh[1]]=='d'):
                num_dynamites_held+=1
                navigation[klnh[0]][klnh[1]] = ' '
                ls_trace.append([klnh,'d'])
            if(navigation[klnh[0]][klnh[1]]=='$'):
                is_money+=1
                navigation[klnh[0]][klnh[1]] = ' '
                ls_trace.append([klnh,'$'])
            if(navigation[klnh[0]][klnh[1]]=='k'):
                num_of_key+=1
                navigation[klnh[0]][klnh[1]] = ' '
                ls_trace.append([klnh,'k'])
            if(navigation[klnh[0]][klnh[1]]=='a'):
                num_of_axe+=1
                navigation[klnh[0]][klnh[1]] = ' '
                ls_trace.append([klnh,'a'])
            temp_score = ground_evaluate(klnh[0],klnh[1])
            if(temp_score > calculation_score or (temp_score == calculation_score and len(ls_trace)<len(The_one))):
                The_one=[i for i in ls_trace]
                calculation_score=temp_score
            calculation(klnh[0],klnh[1])
            ls_trace.pop()
            navigation[klnh[0]][klnh[1]]=klnh[2]
            if(navigation[klnh[0]][klnh[1]]=='$'):
                is_money-=1
            if(navigation[klnh[0]][klnh[1]]=='d'):
                num_dynamites_held-=1
            if(navigation[klnh[0]][klnh[1]]=='a'):
                num_of_axe-=1
            if(navigation[klnh[0]][klnh[1]]=='k'):
                num_of_key-=1

    if (navigation[x][y] == ' ' and num_of_raft):
        klnh = []
        search_ocean = []
        ttk=[]
        for pcw in ls_choice:
            for p in pcw[1:]:
                if (p[2] =='~' and [pcw[0],[p[0],p[1]],'~'] in island_ocean_index
                    and [pcw[0],[p[0],p[1]],'~'] not in search_ocean):
                    search_ocean.append([pcw[0],[p[0],p[1]],'~'])
        if( not search_ocean):
            for i in record_bibliography(x,y):
                search_ocean.append(i[0])
                if(i[0] not in island_ocean_index):
                    island_ocean_index.append(i[0])
        for ttk in search_ocean:
            if (ttk not in ls_trace):
                klnh = ttk
            else:
                continue
            ls_trace.append(klnh)
            temp_score = ground_evaluate(klnh[1][0], klnh[1][1])
            if (temp_score > calculation_score or (temp_score == calculation_score and len(ls_trace)<len(The_one))):
                The_one = [i for i in ls_trace]
                calculation_score = temp_score
            calculation(klnh[1][0], klnh[1][1])
            ls_trace.pop()

    if (navigation[x][y] == '~'):
        bibli_temp=[]
        for pcw in ls_choice:
            for p in pcw[1:]:
                if (p[2] == ' ' and [[p[0], p[1]], ' '] in island_ocean_index
                    and [[p[0], p[1]], ' '] not in bibli_temp):
                    bibli_temp.append([[p[0], p[1]],  ' '])
        if (not bibli_temp):
            for i in record_bibliography(x,y):
                bibli_temp.append(i[0])
                if (i[0] not in island_ocean_index):
                    island_ocean_index.append(i[0])
        for ttk in bibli_temp:
            if (ttk not in ls_trace):
                klnh=ttk
            else:
                continue
            if (klnh ):
                ls_trace.append(klnh)
                temp_score = ground_evaluate(klnh[0][0],klnh[0][1])
                if (temp_score > calculation_score or (temp_score == calculation_score and len(ls_trace)<len(The_one))):
                    The_one = [i for i in ls_trace]
                    calculation_score = temp_score
                temp = num_of_raft
                num_of_raft = 0
                calculation(klnh[0][0], klnh[0][1])
                num_of_raft = temp
                ls_trace.pop()

    if (navigation[x][y] == ' '):
        if(num_dynamites_held):
            lzq = []
            klnh = []
            for pcw in ls_choice:
                for p in pcw[1:]:
                    if (p[2] == '*' and important_wall(p[0],p[1]) and [p[0], p[1]] not in trash_wall):
                        trash_wall.append([p[0], p[1]])
                        navigation[p[0]][p[1]]=' '
                        num_dynamites_held -= 1
                        ls_trace.append([pcw[0],[p[0], p[1]],'B'])
                        temp_score = ground_evaluate(p[0], p[1])
                        if(temp_score > calculation_score or (temp_score == calculation_score and len(ls_trace)<len(The_one))):
                            The_one=[i for i in ls_trace]
                            calculation_score = temp_score
                        calculation(p[0], p[1])
                        num_dynamites_held +=1
                        ls_trace.pop()
                        navigation[p[0]][p[1]] = '*'
                        trash_wall.pop()

    if (navigation[x][y] == ' '):
        lzq = []
        klnh = []
        if(num_of_axe and not num_of_raft):
            for pcw in ls_choice:
                for p in pcw[1:]:
                    if ([p[0], p[1]] not in trash_tree and p[2] == 'T' and
                            ((lzq and M_distance(x,y,lzq[0],lzq[1])>M_distance(x,y,pcw[0][0],pcw[0][1]))
                             or not lzq)):
                        lzq = pcw[0]
                        klnh = [p[0], p[1]]
            if(lzq):
                trash_tree.append([klnh[0],klnh[1]])
                navigation[klnh[0]][klnh[1]] = ' '
                ls_trace.append([lzq,klnh,'C'])
                num_of_raft += 1
                temp_score = ground_evaluate(klnh[0],klnh[1])
                if(temp_score > calculation_score or (temp_score == calculation_score and len(ls_trace)<len(The_one))):
                    The_one=[i for i in ls_trace]
                    calculation_score=temp_score
                calculation(klnh[0],klnh[1])
                num_of_raft -= 1
                ls_trace.pop()
                trash_tree.pop()
                navigation[klnh[0]][klnh[1]]='T'

def chg_habour(x,y):
    for i in record_bibliography(x, y):
        if (i[0] not in island_ocean_index):
            island_ocean_index.append(i[0])
def move(x,y,target_x,target_y,act=''):
    global row
    global col
    global num_of_axe
    global num_of_key
    global num_of_raft
    global is_money
    global num_dynamites_held
    global navigation
    action_str=''
    def action(a):
        if (a):
            sock.send(bytes(a, encoding='utf-8'))
    if (act == 'C'):
        num_of_raft += 1
    if (act == 'B'):
        num_dynamites_held -= 1
    if( act):
        temp = find_path(row, col, x, y)
    else:
        if (navigation[row][col] == '~' and navigation[target_x][target_y] ==' '):
            num_of_raft = 0
        temp = find_path(row,col, target_x, target_y)
    for p in temp:
        action_str=judge_move(row,col,p[0],p[1])
        if(not action_str):
            continue
        for a_s in action_str:
            if(a_s == 'F'):
                [row, col] = [p[0], p[1]]
            action(a_s)
            chg_compass(a_s)
            recieve_view()
            draw_navigation()

    if bool(act):
        action_str=judge_move(row,col,target_x,target_y,action=act)
        for a_s in action_str:
            if(a_s == 'F'):
                [row,col]=[target_x,target_y]
            action(a_s)
            chg_compass(a_s)
            recieve_view()
            draw_navigation()
    if(navigation[row][col]=='$'):
        is_money += 1
        navigation[row][col]=' '
    elif(navigation[row][col]=='d'):
        num_dynamites_held += 1
        navigation[row][col]=' '
    elif(navigation[row][col]=='k'):
        num_of_key += 1
        navigation[row][col]=' '
    elif(navigation[row][col]=='a'):
        num_of_axe += 1
        navigation[row][col]=' '
    return
recieve_view()
draw_navigation()
try:
    while(True):
        important_choice_1=[]
        important_choice_2=[]
        temp_imp=0
        if (navigation[row][col] == '~'):
            important_choice=get_all_choice(row,col)
            for pcw in important_choice:
                for p in pcw[1:]:
                    if (p[2] == '?'):
                        if ((important_choice_1 and M_distance(row, col, important_choice_1[0], important_choice_1[1])
                            > M_distance(row, col, pcw[0][0], pcw[0][1])) or not important_choice_1):
                            important_choice_1 = pcw[0]
                            ocean_flag=True
                            break
            if(important_choice_1):
                move(row,col,important_choice_1[0],important_choice_1[1])
                continue
            elif(ocean_flag):
                chg_habour(row,col)
                ocean_flag = False
        else:
            important_choice=get_all_choice(row,col)
            for pcw in important_choice:
                for p in pcw[1:]:
                    if ( num_of_axe and p[2] == 'T' and num_of_treasure(p[0],p[1])):
                        if ((important_choice_1 and M_distance(row, col, important_choice_1[0], important_choice_1[1])
                            > M_distance(row, col, pcw[0][0], pcw[0][1])) or not important_choice_1):
                            important_choice_1 = pcw[0]
                            important_choice_2 = [p[0],p[1]]
                        break
                    if (p[2] == '?' and not important_choice_2):
                        if ((important_choice_1 and M_distance(row, col, important_choice_1[0], important_choice_1[1])
                            > M_distance(row, col, pcw[0][0], pcw[0][1])) or not important_choice_1):
                            important_choice_1 = pcw[0]
                            important_choice_2=[]
                            land_flag=True
                        break
                    if (p[2] in {'d', 'a', '$', 'k'} and not important_choice_2):
                        if ((important_choice_1 and M_distance(row, col, important_choice_1[0], important_choice_1[1])
                            > M_distance(row, col, pcw[0][0], pcw[0][1])) or not important_choice_1):
                            important_choice_1 = [p[0], p[1]]
                            important_choice_2 = []
                        break
                    if (is_money and pcw[0]==[[45,45]]):
                        important_choice_1 = [pcw[0][0], pcw[0][1]]
                        important_choice_2 = []
                        break
                if(important_choice_1):
                    break
            if(important_choice_1):
                if(important_choice_2 ):
                    if(navigation[important_choice_2[0]][important_choice_2[1]]=='T'):
                        move(important_choice_1[0], important_choice_1[1], important_choice_2[0], important_choice_2[1],act='C')
                move(row, col, important_choice_1[0], important_choice_1[1])
                continue
            elif(land_flag):
                land_flag=False
                chg_habour(row,col)
        if (not important_choice_1):
            calculation_score = 0
            The_one = []
            trash_wall = []
            trash_tree = []
            trash_ground_mist = []
            trash_ocean_mist = []
            calculation(row,col)
            for i in range(len(The_one)):
                path=The_one[i]
                if(path[-1] in {'U','B','C'}):
                    move(path[0][0], path[0][1], path[1][0], path[1][1],act=path[-1])
                else:
                    move(row,col,path[0][0],path[0][1])
                    if(path[-1]=='~'):
                        move(row, col, path[1][0], path[1][1])
                    if(path[0]==[45,45]):
                        sock.close()
except ConnectionResetError:
    sys.exit()


