from argparse import ArgumentParser

filename='C:\\Users\hw\Desktop\game\s6.in'
temp=[]
with open(filename) as f:
    for line in f:
        k = 0
        temp_map = []
        for c in line:
            k+=1
            temp_map.append(c)
            print(c,end=' ')
        temp.append(temp_map)
print('[')
for i in temp:
    print(i,end=',\n')
print(']')


