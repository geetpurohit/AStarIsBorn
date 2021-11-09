import numpy as np
import random as rr
import matplotlib.pyplot as plt
import multiprocessing

def Mazebt(args): #backtracker
    number = args[0]
    w = args[1] 
    h = args[2]
    shape = (h, w)
    # Build actual maze
    Z = np.ones(shape, dtype=bool)  # Maze-grid: 1's are black, 0's are white

    # Initially set all cells as unvisited.
    Y = np.zeros(shape, dtype=bool)  # Visited or not

    # stack of visited cells
    stack = []
    # Recursive parent back tracker node treee thingy
    # 1 Make the initial cell the current cell and mark it as visited.
    # Random Initial cell
    A, B = rr.choice(range(0, (shape[0]), 2)), rr.choice(range(0, (shape[1]), 2))

    # Making it the current cell   
    Z[A][B] = 0
    # Marking it as visited 
    Y[A][B] = 1
    stack.append([A, B])

    # 2 While there are unvisited cells
    while (not Y.all()):
        # print(A,B)
        # 2.1 If the current cell has any neighbors which have not been visited
        nebs = []
        walls = []

        if A + 2 in range(h) and Y[A + 2][B] == 0:
            nebs.append([A + 2, B])
            walls.append([A + 1, B])
        if A - 2 in range(h) and Y[A - 2][B] == 0:
            nebs.append([A - 2, B])
            walls.append([A - 1, B])
        if B + 2 in range(w) and Y[A][B + 2] == 0:
            nebs.append([A, B + 2])
            walls.append([A, B + 1])
        if B - 2 in range(w) and Y[A][B - 2] == 0:
            nebs.append([A, B - 2])
            walls.append([A, B - 1])
        if nebs:
            # 2.1.1 Choose randomly one of the unvisited neighbors
            cho = rr.choice(range(len(nebs)))
            # 2.1.2 Push the current cell to the stack
            stack.append([A, B])
            # 2.1.3 Remove the wall between the current cell and the chosen cell
            Z[nebs[cho][0]][nebs[cho][1]] = 0
            Z[walls[cho][0]][walls[cho][1]] = 0
            # 2.1.4 Make the chosen cell the current cell and mark it as visited
            A = nebs[cho][0]
            B = nebs[cho][1]
            Y[nebs[cho][0]][nebs[cho][1]] = 1
            Y[walls[cho][0]][walls[cho][1]] = 1

            stack.append([A, B])
        # 2.2. Else if stack is not empty
        elif stack:
            if A + 1 in range(h):
                Y[A + 1][B] = 1
            if A - 1 in range(h):
                Y[A - 1][B] = 1
            if B + 1 in range(w):
                Y[A][B + 1] = 1
            if B - 1 in range(w):
                Y[A][B - 1] = 1
            # 2.2.1 Pop a cell from the stack
            p = stack.pop()
            # 2.2.2 Make it the current cell
            A = p[0]
            B = p[1]
        else:
            break

    plt.figure()
    plt.imshow(Z, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    np.savetxt("parentbacktrackmazes/{0:0=d}.txt".format(number), Z, fmt='%d')


def randommaze(args):
    number = args[0]
    w = args[1]
    h = args[2]
    shape = (h, w)
    Z = np.random.choice([0, 1], size=shape, p=[.70, .30])
    plt.figure()
    plt.imshow(Z, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    np.savetxt("{0:0=d}.txt".format(number), Z, fmt='%d')


def MazeGenerate(number: int, mazeSize: int):

    # specify the number of grids you want to generate
    n_grids = int(number)
    multiprocessing.freeze_support()
    num_proc = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_proc)
    temp = [(i, mazeSize, mazeSize) for i in range(n_grids)]
    pool.map(randommaze, temp)
    temp2 = [i for i in temp]
    pool.map(Mazebt, temp2)
    pool.close()
    pool.join()
