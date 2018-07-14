from collections import deque
map=[
['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
['.', '.', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '.', '.', '\n'],
['.', '.', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', ' ', ' ', 'T', ' ', ' ', '~', '~', '.', '.', '\n'],
['.', '.', '~', '~', ' ', 'a', ' ', ' ', ' ', '~', '~', '~', '~', '~', '~', '~', ' ', '*', '*', '*', ' ', '~', '~', '.', '.', '\n'],
['.', '.', '~', '~', ' ', ' ', '<', ' ', ' ', '~', '~', '~', '~', '~', '~', '~', ' ', '*', '$', '*', ' ', '~', '~', '.', '.', '\n'],
['.', '.', '~', '~', '~', ' ', 'T', ' ', '~', '~', '~', '~', '~', '~', '~', '~', ' ', '*', '*', '*', ' ', '~', '~', '.', '.', '\n'],
['.', '.', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '.', '.', '\n'],
['.', '.', '~', '~', ' ', ' ', ' ', ' ', ' ', '~', '~', '~', '~', '~', '~', '~', '~', ' ', ' ', ' ', '~', '~', '~', '.', '.', '\n'],
['.', '.', '~', '~', ' ', '*', '-', '*', ' ', '~', '~', '~', '~', '~', '~', '~', ' ', ' ', 'k', ' ', ' ', '~', '~', '.', '.', '\n'],
['.', '.', '~', '~', 'T', '*', 'd', '*', ' ', '~', '~', '~', '~', '~', '~', '~', '~', ' ', ' ', 'T', '~', '~', '~', '.', '.', '\n'],
['.', '.', '~', '~', ' ', '*', '*', '*', ' ', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '.', '.', '\n'],
['.', '.', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '.', '.', '\n'],
['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n']
]

imap=30
all_oceans=[]
row=12
col=16
num_dynamites_held=1
offset_x=0
offset_y=0
center_x=3
center_y=3

def get_all_choice(x,y):
    def ground_neighbor(x, y):
        neighbor = [[x, y]]
        not_in_search = {'.', map[x][y]}
        if (map[x - 1][y] not in not_in_search):
            neighbor.append([x - 1, y, map[x - 1][y]])
        if (map[x][y + 1] not in not_in_search):
            neighbor.append([x, y + 1, map[x][y + 1]])
        if (map[x + 1][y] not in not_in_search):
            neighbor.append([x + 1, y, map[x + 1][y]])
        if (map[x][y - 1] not in not_in_search):
            neighbor.append([x, y - 1, map[x][y - 1]])
        for i in range(-2, 3):
            for j in range(-2, 3):
                if (map[x + i][y + j] == 'm' and [x + i, y + j, map[x + i][y + j]] not in neighbor) and (
                        i != 0 or j != 0):
                    neighbor.append([x + i, y + j, map[x + i][y + j]])
        if len(neighbor) > 1:
            return neighbor
        else:
            return []
    u = []
    temp=[]
    option=[]
    used=[]
    global map
    u.append([x,y])
    while(u):
        [x, y]=u.pop()
        temp = ground_neighbor(x, y)
        if (temp):
            option.append(temp)
        if([x,y]==[center_x,center_y] and [x,y] not in used  and [x,y] not in u):
            option.append([[x,y]])
        used.append([x, y])
        if (map[x-1][y] == map[x][y] and [x-1,y] not in used and [x-1,y] not in u):
            u.append([x-1, y])
        if (map[x][y+1] == map[x][y] and [x,y+1] not in used and [x,y+1] not in u):
            u.append([x, y+1])
        if (map[x+1][y] == map[x][y] and [x+1,y] not in used and [x+1,y] not in u):
            u.append([x+1, y])
        if (map[x][y-1] == map[x][y] and [x,y-1] not in used and [x,y-1] not in u):
            u.append([x, y-1])
    return option

for i in get_all_choice(2,2):
    print(i)
#####################################################
#b=find_ground_options(4,4)
#print(b)
#for i in range(1,len(b[1:])+1):
#    temp=judge_move(b[i-1][0],b[i-1][1],b[i][0],b[i][1])
#    change_dirn(temp)
#    print(temp,end=' ')
#    print(dirn,end=' ')
