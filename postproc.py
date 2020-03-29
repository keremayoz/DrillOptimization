from openpyxl import load_workbook
import pandas as pd
import numpy as np
import sys
from queue import Queue
import matplotlib.pyplot as plt
import time
start =time.time()
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
grid = np.zeros((x_len + 1,y_len + 1))
#print(grid)



for row in data_rows2:
    x1, y1, off1, off2 = row
    grid[x1:x1+off1 + 1, y1:y1 + off2 + 1] = 1
print(grid.shape)

import numpy as np

tsp = pd.read_csv('tsp_result.txt', sep=",", header=None)
tsp_result = np.zeros((50, 50))
tsp = tsp.values
tsp_result.shape


count = 0 
for i in range(50):
    for j in range(50):
        if i != j:
            print(i,j)
            tsp_result[i][j] = tsp[0][count]
            count += 1

tsp_result = tsp_result.astype(np.bool)



def path_exists(grid, source, dest):
    
    if grid[source[0], source[1]] == 1 or grid[dest[0], dest[1]] ==1:
        return False, -1
    minx = min(source[0], dest[0])
    maxx = max(source[0], dest[0])
    miny = min(source[1], dest[1])
    maxy = max(source[1], dest[1])

    #print(source, dest, minx, miny, maxx, maxy)
    new_source = (source[0]-minx, source[1]-miny)
    new_dest = (dest[0]-minx, dest[1]-miny)

    go_x = -1 if source[0] > dest[0] else 1
    go_y = -1 if source[1] > dest[1] else 1

    new_matrix = grid[minx:(maxx+1), miny:(maxy+1)].copy()
    
    new_matrix[new_matrix == 1] = float("inf") 
    

    i = new_source[0]+go_x
    while 0 <= i < len(new_matrix):
        if new_matrix[i][new_source[1]]  != float("inf"):
            new_matrix[i][new_source[1]] = new_matrix[i-go_x][new_source[1]] + 1
        i += go_x

    i = new_source[1]+go_y
    while 0 <= i < len(new_matrix[0]):
        if new_matrix[new_source[0]][i] != float("inf"):
            new_matrix[new_source[0]][i] =  new_matrix[new_source[0]][i-go_y] + 1
        i += go_y

    i, j = new_source[0]+go_x, 0 

    while 0 <= i < len(new_matrix):
        j = new_source[1]+go_y
        while 0 <= j < len(new_matrix[0]):
            if new_matrix[i][j] != float("inf"):
                new_matrix[i][j] = min(new_matrix[i-go_x][j], new_matrix[i][j-go_y]) + 1
            j += go_y
        i += go_x
    #check destination
    point = new_matrix[new_dest[0], new_dest[1]]
    #path array
    new_arr = np.zeros(new_matrix.shape).astype(np.bool)
    if point == 0 or point == float("inf"):
        return new_arr
    #backtrack the path
    i, j = new_dest
    while i != new_source[0] or j!= new_source[1]:
        new_arr[i][j] = True
        if i != new_source[0] and (new_matrix[i-go_x][j]+1) == new_matrix[i][j]:
            i -= go_x
        elif j != new_source[1] and ( new_matrix[i][j-go_y]+1) == new_matrix[i][j]:
            j -= go_y
    new_arr[new_dest] = False
    new_arr[new_source] = False         
    return new_arr, minx, miny, maxx+1, maxy+1

new_grid = grid.copy()
new_grid[new_grid == 1] = 100
new_grid[new_grid == 0] = 220
new_grid = np.repeat(new_grid[:,:,np.newaxis], 3, axis=-1 ).astype(np.uint8)
#new_grid[ ] = [125, 0, 235]
x_index, y_index = np.where(tsp_result == True)
for i in range(len(x_index)):
    backtrackx, x, y, x_, y_ = path_exists(grid, data_rows1[x_index[i]], data_rows1[y_index[i]])


    new_grid[x:x_, y:y_,:][backtrackx] = [123, 0,0]

for row in data_rows1:
    new_grid[row[0], row[1],:]= [214, 202, 19]

import matplotlib.pyplot as plt 
import matplotlib.animation as animation


x_new = []
y_new = []

x_new.append(x_index[0])
y_new.append(y_index[0])

for i in range(len(x_index)):
    for j in range(len(x_index)):
        if i != j:
            if  data_rows1[y_new[-1]][0] == data_rows1[x_index[j]][0] and data_rows1[y_new[-1]][1] == data_rows1[x_index[j]][1]:
                x_new.append(y_new[-1])
                y_new.append(y_index[j])
x_index = x_new
y_index = y_new

def update(i):
    a = i % 50
    b = a - 1
    backtrackx, x, y, x_, y_ = path_exists(grid, data_rows1[x_index[b]], data_rows1[y_index[b]])
    new_grid[data_rows1[x_index[b]][0], data_rows1[x_index[b]][1],:]= [214, 202, 19]
    new_grid[data_rows1[y_index[b]][0], data_rows1[y_index[b]][1],:]= [214, 202, 19]
    new_grid[x:x_, y:y_,:][backtrackx] = [123, 0,0]
    backtrackx, x, y, x_, y_ = path_exists(grid, data_rows1[x_index[a]], data_rows1[y_index[a]])
    print(data_rows1[x_index[a]], data_rows1[y_index[a]])
    new_grid[x:x_, y:y_,:][backtrackx] = [0,0,0]
    new_grid[data_rows1[x_index[a]][0], data_rows1[x_index[a]][1],:]= [214, 52, 19]
    new_grid[data_rows1[y_index[a]][0], data_rows1[y_index[a]][1],:]= [214, 52, 19]

    
    
    matrice.set_array(np.rot90(new_grid))

    print(i)

fig, ax = plt.subplots()
matrice = ax.imshow(np.rot90(new_grid))

ani = animation.FuncAnimation(fig, update, frames=50, interval=1000)
plt.show()


print(data_rows1[x_index[a]], data_rows1[y_index[a]])




