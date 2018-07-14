#!/usr/bin/env python3
# agent.py
import socket
from argparse import ArgumentParser
import os
import sys

view=[[str('@') for i in range(5) ] for _ in range(5)]
size=80
best_path=[]
ls_path=[]
reduce_mark=0

parser = ArgumentParser()
parser.add_argument('-p', type=int,dest = 'port', required = True)
args = parser.parse_args()
port = args.port

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost',port))

row=40
col=40
east = 2
north = 1
west = 0
south = 3
direction = 1
world=[['@' for _ in range(size)] for _ in range(size)]
world[row][col]=' '
have_axe = False
have_key = False
have_raft = False
game_won = False
game_lost = False
have_treasure = False
num_dynamites_held = 0

#return a value of power of Euler distance
def Euler_distance(x, y, next_x, next_y):
    return (x - next_x)**2 + (y - next_y)**2

#get the map recieved from server
def get_view():
    global view
    for u in range(5):
        for v in range(5):
            if ((u == 2) and (v == 2)):
                continue
            t = str(sock.recv(1), encoding='utf-8')
            view[u][v]=t

#To find out a wall if it is worth of blow up
#if it is, then blow
def worthy_wall(x,y):
    global world
    if(world[x-2][y-2] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x-2][y-1] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x-2][y] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x-2][y+1] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x-2][y+2] in {'d', 'k', 'a', '$','m'}):
        return True
    ##################
    if(world[x-1][y-2] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x-1][y-1] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x-1][y] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x-1][y+1] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x-1][y+2] in {'d', 'k', 'a', '$','m'}):
        return True
    ######################
    if(world[x][y-2] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x][y-1] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x][y] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x][y+1] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x][y+2] in {'d', 'k', 'a', '$','m'}):
        return True
    ######################
    if(world[x+1][y-2] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x+1][y-1] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x+1][y] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x+1][y+1] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x+1][y+2] in {'d', 'k', 'a', '$','m'}):
        return True
    #########################
    if(world[x+2][y-2] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x+2][y-1] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x+2][y] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x+2][y+1] in {'d', 'k', 'a', '$','m'}):
        return True
    if(world[x+2][y+2] in {'d', 'k', 'a', '$','m'}):
        return True

#draw the map onto matrix[world]
def draw_world():
    global world
    global view
    global row
    global col
    def rotate( matrix):
        matrix[:] = map(list, zip(*matrix[::-1]))
    ls=[[str(i) for i in range(5) ] for _ in range(5)]
    if(direction==0):
        rotate(view)
        rotate(view)
        rotate(view)
        ls = view
    if (direction == 1):
        ls = view
    if (direction == 2):
        rotate(view)
        ls = view
    if (direction == 3):
        rotate(view)
        rotate(view)
        ls = view
    for i in range(-2,3):
        for j in range(-2,3):
            if(i!=0 or j!=0):
                world[row + i][col + j] = ls[2+i][2+j]

#figure out the next
def next_step(x,y,next_x,next_y,a=None):
    ls=0
    global direction
    if(x-1==next_x and y==next_y):
        ls=1
    if(x+1==next_x and y==next_y):
        ls=3
    if(x==next_x and y+1==next_y):
        ls=2
    if(x==next_x and y-1==next_y):
        ls=0
    if(x==next_x and y==next_y):
        return ''
    temp=(direction-ls)%4*'L'
    if(a in {'C','U','B'}):
        return temp+a+'F'
    return temp+'F'

#change current direction
def modify_direction(T):
    global direction
    if(T=='R'):
        direction = (direction+1)%4
    elif(T=='L'):
        direction = (direction-1)%4

#find out what could be done
def choose(x,y):
    global world
    stack = []
    option=[]
    used=[]
    if(world[x][y] ==' '):
        stack.append([x,y])
    else :
        return []

    #find out the stuff near a place
    def near(x, y):
        neighbor = [[x, y]]
        for i in range(-2, 3):
            for j in range(-2, 3):
                if (world[x + i][y + j] == '@' and [x + i, y + j, world[x + i][y + j]] not in neighbor) and (
                        i != 0 or j != 0):
                    neighbor.append([x + i, y + j, world[x + i][y + j]])
        if (world[x - 1][y] not in {' ', '.'}):
            neighbor.append([x - 1, y, world[x - 1][y]])
        if (world[x][y + 1] not in {' ', '.'}):
            neighbor.append([x, y + 1, world[x][y + 1]])
        if (world[x + 1][y] not in {' ', '.'}):
            neighbor.append([x + 1, y, world[x + 1][y]])
        if (world[x][y - 1] not in {' ', '.'}):
            neighbor.append([x, y - 1, world[x][y - 1]])

        if len(neighbor) > 1:
            return neighbor
        else:
            return []
    while(stack):
        [x, y]=stack.pop()
        ls=near(x,y)
        if (ls):
            option.append(ls)
        if([x,y]==[40,40] and [x,y] not in used  and [x,y] not in stack):
            option.append([[x,y]])
        used.append([x, y])
        if (world[x-1][y] == ' ' and [x-1,y] not in used and [x-1,y] not in stack):
            stack.append([x-1, y])
        if (world[x][y+1] == ' ' and [x,y+1] not in used and [x,y+1] not in stack):
            stack.append([x, y+1])
        if (world[x+1][y] == ' ' and [x+1,y] not in used and [x+1,y] not in stack):
            stack.append([x+1, y])
        if (world[x][y-1] == ' ' and [x,y-1] not in used and [x,y-1] not in stack):
            stack.append([x, y-1])
    return option
# find a path between two points
def get_the_path(x,y,dx,dy):
    waste = []
    path1 = []
    global world
    temp1=''
    temp2=''
    if (world[x][y] in {'d', 'k', 'a', '$'}):
        temp1 = world[x][y]
        world[x][y] = ' '
    if (world[dx][dy] in {'d', 'k', 'a', '$'}):
        temp2 = world[dx][dy]
        world[dx][dy] = ' '
    def try_path(cx,cy):
        nonlocal path1
        nonlocal waste
        nonlocal x
        nonlocal y
        nonlocal dx
        nonlocal dy
        global w
        path1.append([cx,cy])
        waste.append([cx,cy])
        for _ in range(4):
            a_star = []
            temp = []
            if( [cx-1,cy] not in waste and world[cx-1][cy] == ' '):
                if ([cx - 1, cy] == [dx, dy]):
                    path1.append([cx - 1, cy])
                    return True
                a_star.append([cx-1,cy,Euler_distance(dx,dy,cx-1,cy)])
            if([cx,cy+1] not in waste and world[cx][cy+1] == ' '):
                if ([cx, cy + 1] == [dx, dy]):
                    path1.append([cx, cy + 1])
                    return True
                a_star.append([cx,cy+1,Euler_distance(dx,dy,cx,cy+1)])
            if([cx+1,cy] not in waste and world[cx+1][cy] == ' '):
                if ([cx + 1, cy] == [dx, dy]):
                    path1.append([cx + 1, cy])
                    return True
                a_star.append([cx+1,cy,Euler_distance(dx,dy,cx+1,cy)])
            if([cx,cy-1] not in waste and world[cx][cy-1] == ' '):
                if ([cx, cy - 1] == [dx, dy]):
                    path1.append([cx, cy - 1])
                    return True
                a_star.append([cx,cy-1,Euler_distance(dx,dy,cx,cy-1)])
            if(a_star):
                temp=min(a_star,key=lambda x:x[2])
            if(temp):
                if( try_path(temp[0],temp[1])):
                    return True
                else:
                    path1.pop()
        return False

    if(try_path(x,y)):
        if (temp1):
            world[x][y]=temp1
        if (temp2):
            world[dx][dy]=temp2
        return path1
    else:
        if (temp1):
            world[x][y]=temp1
        if (temp2):
            world[dx][dy]=temp2
        return []
# do everything in this function
def do(x,y,next_x,next_y,act=''):
    global row
    global col
    global have_axe
    global have_key
    global have_raft
    global have_treasure
    global num_dynamites_held
    global world
    action_string=''
    if (act):
        ls = get_the_path(row, col, x, y)
    else:
        ls = get_the_path(row, col, next_x, next_y)
    for p in ls:
        action_string=next_step(row,col,p[0],p[1])
        if(not action_string):
            continue
        for temp in action_string:
            if(temp == 'F'):
                [row, col] = [p[0], p[1]]
            if(temp):
                sock.send(bytes(temp, encoding='utf-8'))
            modify_direction(temp)
            get_view()
            draw_world()
    if bool(act):
        action_str=next_step(row,col,next_x,next_y,a=act)
        for temp in action_str:
            if(temp == 'F'):
                [row,col]=[next_x,next_y]
            if(temp):
                sock.send(bytes(temp, encoding='utf-8'))
            modify_direction(temp)
            get_view()
            draw_world()
    if(world[row][col]=='d'):
        world[row][col]=' '
        num_dynamites_held += 1
    if(world[row][col]=='k'):
        world[row][col]=' '
        have_key = True
    if(world[row][col]=='a'):
        world[row][col]=' '
        have_axe = True
    if(world[row][col]=='$'):
        world[row][col]=' '
        have_treasure = True
    return
main_option=[]
main_path=[]
main_ls1=[]
get_view()
draw_world()
try:
    while(not game_won):
        main_ls1=[]
        main_ls2=[]
        main_option=choose(row,col)
        if(not have_treasure):
            for opt in main_option:
                for o in opt[1:]:
                    if (have_axe and o[2] == 'T' ):
                        if ((main_ls1 and Euler_distance(row, col, main_ls1[0], main_ls1[1])
                            > Euler_distance(row, col, opt[0][0], opt[0][1])) or not main_ls1):
                            main_ls1 = opt[0]
                            main_ls2 = [o[0],o[1]]
                    if (num_dynamites_held and o[2] == '*' and worthy_wall(o[0],o[1])):
                        if ((main_ls1 and Euler_distance(row, col, main_ls1[0], main_ls1[1])
                            > Euler_distance(row, col, opt[0][0], opt[0][1])) or not main_ls1):
                            num_dynamites_held -= 1
                            main_ls1 = opt[0]
                            main_ls2 = [o[0],o[1]]
                    if (o[2] == '@' and not main_ls2):
                        if ((main_ls1 and Euler_distance(row, col, main_ls1[0], main_ls1[1])
                            > Euler_distance(row, col, opt[0][0], opt[0][1])) or not main_ls1):
                            main_ls1 = opt[0]
                    if (o[2] in {'d', 'a', '$', 'k'} and not main_ls2):
                        if ((main_ls1 and Euler_distance(row, col, main_ls1[0], main_ls1[1])
                            > Euler_distance(row, col, opt[0][0], opt[0][1])) or not main_ls1):
                            main_ls1 = [o[0], o[1]]
            if(main_ls1 and not have_treasure):
                if(main_ls2 and world[main_ls2[0]][main_ls2[1]]=='T'):
                    do(main_ls1[0], main_ls1[1], main_ls2[0], main_ls2[1],act='C')
                    continue
                if(main_ls2 and world[main_ls2[0]][main_ls2[1]]=='*'):
                    do(main_ls1[0], main_ls1[1], main_ls2[0], main_ls2[1],act='B')
                    continue
                do(row, col, main_ls1[0], main_ls1[1])
                continue
        else:
            do(row, col, 40, 40)
except ConnectionResetError:
    sys.exit()


