from openpyxl import load_workbook
import pandas as pd
import numpy as np
import sys
from queue import Queue
import matplotlib.pyplot as plt
import time

wb = load_workbook(filename='data.xlsx',
                   read_only=True)

ws1 = wb['Points ']

# Read the cell values into a list of lists
data_rows1 = []
for row in ws1['A2':'B51']:
    data_cols = []
    for cell in row:
        data_cols.append(cell.value)
    data_rows1.append(data_cols)

ws2 = wb['Blocks']
data_rows2 = []
for row in ws2['A3':'D22']:
    data_cols = []
    for cell in row:
        data_cols.append(cell.value)
    data_rows2.append(data_cols)


df1 = pd.DataFrame(data_rows1)
df2 = pd.DataFrame(data_rows2)


x_len = -1
y_len = -1
x_1 = df1[0].max()
x_2 = df2[0].max()
y_1 = df1[1].max()
y_2 = df2[1].max()

x_len = x_2 if (x_1 < x_2) else x_1
y_len = y_2 if (y_1 < y_2) else y_1

np.set_printoptions(threshold=sys.maxsize)
grid = np.zeros((y_len,x_len))
#print(grid)

def convert(x, y):
    return y_len - y, x - 1

def convert2(x,y):
    return 3 - y, x-1

for row in data_rows2:
    x1, y1, off1, off2 = row
    for i in range(off1+1):
        for j in range(off2+1):
            grid[convert(x1 + i, y1 + j)] = 1
    #grid[x1:x1+off1 + 1, y1:y1 + off2 + 1] = 1
print(grid.shape)


for row in data_rows1:
    #print(row)
    #print(convert(row[0],row[1]))
    #time.sleep(1)
    grid[convert(row[0], row[1])] = 2


for i in range(len(grid)):
    for j in range(len(grid[0])):
        print(int(grid[i][j]), " ", end="")
    print()

test = np.zeros((3,3))
test[convert2(2,3)] = 1
test[convert2(3,2)] = 1
print(test)
plt.imshow(grid,cmap=plt.get_cmap('binary'), origin='upper')
plt.grid('on')
#plt.xticks(np.arange(50))
#plt.yticks(np.arange(51))
plt.show()

rowNum = [-1, 0, 0, 1]
colNum = [0, -1, 1, 0]
arr = [[0,0,0,0],
       [1,1,0,0],
       [0,0,0,1],
       [0,0,0,0]]

#x_len = len(arr[0])
#y_len = len(arr)




def path_exists(arr, source, dest):
    source = convert(source[0], source[1])
    dest = convert(dest[0], dest[1])
    x_len = abs(dest[0] - source[0])
    y_len = abs(dest[1] - source[1])
    visited = np.zeros((x_len+1,y_len+1), dtype=bool)
    minx = min(source[0], dest[0])
    miny = min(source[1], dest[1])
    visited[source[0] - minx, source[1] - miny] = True


    def isValid(row, col):
        #print(row, col)
        return (row >= minx) and (row < minx + x_len+1) and (col >= miny) and (col < miny + y_len+1)
    q = []

    queueNode = (source, 0)
    q.append(queueNode)
    dist = -1
    while len(q) != 0 :
        curr = q[0]
        pt = curr[0]
        if pt[0] == dest[0] and pt[1] == dest[1]:
            dist = curr[1]
            break

        q.pop(0)

        """
        for i in range(x_len):
            for j in range(y_len):
                print(visited[i,j], " ", end="")
            print()

        time.sleep(5)
        """
        for i in range(4):
            row = pt[0] + rowNum[i]
            col = pt[1] + colNum[i]
            if isValid(row, col) and  (arr[row][col] == 0 or arr[row][col] == 2) and  not visited[row-minx][col-miny]:
                visited[row - minx, col - miny] = True
                adjCell = ((row,col), curr[1] + 1)
                q.append(adjCell)

    return dist == (abs(dest[0] - source[0]) + abs(dest[1] - source[1])), dist

#val = path_exists(arr, (3, 0), (0, 1))

result = []

result = [None]*len(data_rows1)
for i in range(len(data_rows1)):
    result[i] = [(False,-1)]*len(data_rows1)

f = open('params2.dat', 'w')
f2 = open('no_paths.txt', 'w')

f.write("n = " + str(len(data_rows1)) + ";\n")
dist = []
blocked = []
for i in range(len(data_rows1)):
    for j in range(len(data_rows1)):
        if i != j:
            print("<",i+1, ",", j+1,">")
            result[i][j] = path_exists(grid, data_rows1[i], data_rows1[j])
            dist.append(result[i][j][1])
            if not result[i][j][0]:
                blocked.append("<" + str(i+1) + "," + str(j+1) + ">")
                print("i: ", data_rows1[i], "j: ", data_rows1[j], "Result: ", result[i][j])

f.write("dist = [\n")
for item in dist:
    f.write("" + str(item) + "\n")
f.write("];\n")

f.write("blocked = {\n")
for item in blocked:
    f.write("" + str(item) + "\n")
f.write("};\n")
#print(path_exists(grid, data_rows1[1], data_rows1[3]))
