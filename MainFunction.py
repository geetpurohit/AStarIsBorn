import ForwardAstarRepeated as rfas
import BackwardsAStarRepeated as rbas
import AdaptiveAStarRepeated as raas
import HelperFunctions as hf
import shutil as sh
import matplotlib.pyplot as plt
import matplotlib.font_manager
import numpy as np
import os
from MazeGenerator import MazeGenerate

def visualizePath(agentPath,count):
    data_set = np.loadtxt('%d.txt' % (count), dtype=np.int32)
    for row_index in range(len(data_set)):
        for column_index in range(len(data_set)):
            if data_set[row_index][column_index] == 1:
                data_set[row_index][column_index] = 20  # Set the blocked cell to the darkest color

    plt.ion()   # Turn pyplot interactive mode on
    plt.figure(figsize=(5, 5))  # Initialize figure
    img_artist = plt.imshow(data_set, cmap=plt.cm.binary, vmin=0, vmax=20, interpolation='nearest', extent=(0, len(data_set), 0, len(data_set)))    # Initialize drawer
    count2 = 0
    for index in range(len(agentPath)):
        if data_set[agentPath[index][0]][agentPath[index][1]] == 0:
            data_set[agentPath[index][0]][agentPath[index][1]] = 10
        else:
            # Deepen the color of the cells that have been passed
            data_set[agentPath[index][0]][agentPath[index][1]] += 1

        img_artist.set_data(data_set)   # Update the figure
        plt.savefig('temp/image' + str(count2) + '.png', dpi = 200)
        plt.pause(0.1)     # Pause between each painting
        count2 += 1 

    # Generate the optimal path
    i = 0
    while i < len(agentPath) - 1:
        location = agentPath[i]
        hasDuplicate = False
        for j in range(i + 1, len(agentPath)):
            if all(location == agentPath[j]):
                hasDuplicate = True
                del(agentPath[i + 1: j + 1])
                break
        if not hasDuplicate:
            i += 1
    # Erase all the path
    for row_index in range(len(data_set)):
        for column_index in range(len(data_set)):
            # Reset the color of all the unblocked cells
            if (data_set[row_index][column_index] > 0) & (data_set[row_index][column_index] < 20):
                data_set[row_index][column_index] = 0

    # Show the optimal path
    for index in range(len(agentPath)):
        data_set[agentPath[index][0]][agentPath[index][1]] = 10

    img_artist.set_data(data_set)   # Update the figure

    plt.ioff()  # Turn pyplot interactive mode off
    plt.show()

# Visualize the path of the agent
if __name__ == '__main__':
    mazeNum = 5     # Number of generated mazes
    size = 101   # The height and width of maze
    listtemp = ["%.2d" % i for i in range(mazeNum)] #make a list for all those str as 2d ints (not 2 dimensional)
    list = list(map(int, listtemp)) # map them as integers
    totaltimestep = totalactualcost = totalnumberofastarinteractions = totaltimecsost = totalnumberofexpandedcells = totalcostsforoptimalpath = numMazeNoPath = 0
    
    listforwardAstar = []

    for i in list:
        print("Current Maze Number:", i)
        if not os.path.exists('%d.txt' % (i)):
            MazeGenerate(mazeNum, size)
        else:
            # Checking whether the existing maze satisfies the size requirement
            dataset = np.loadtxt('%d.txt' % (i), dtype=np.int32)

        # Initialize states from grid world
        states = hf.genstates(i)

        # Initialize start location and goal location
        startLocation = hf.genunblocked(states)
        goalLocation = hf.genunblocked(states)

        while (startLocation == goalLocation).all():
            goalLocation = hf.genunblocked(states)
        # Decide if you want a larger Gvalue or a smalelr G value based on Assignment instructions.
        isLargerGFirst = False

        #print("---------------------Current Alogrithm : Repeateed Forward A Star Smaller G---------------------")
        #agentPath, totaltimestep,totalactualcost,totalnumberofastarinteractions,totaltimecsost, totalnumberofexpandedcells, numMazeNoPath = rfas.repeatedForwardAStar(states, startLocation, goalLocation, isLargerGFirst, totaltimestep, totalactualcost, totalnumberofastarinteractions,totaltimecsost, totalnumberofexpandedcells,numMazeNoPath)
        #if agentPath is not False:
        #    #visualizePath(agentPath, i)
        #    print("\tCosts for optimal path: %d" % (len(agentPath) - 1))
        #    totalcostsforoptimalpath += (len(agentPath) - 1)
        #print("")
        
        
        #states = hf.genstates(i)  # Reset the states
        #print("---------------------Current Alogrithm : Repeateed Forward A Star Bigger G---------------------")
        #agentPath, totaltimestep,totalactualcost,totalnumberofastarinteractions,totaltimecsost, totalnumberofexpandedcells, numMazeNoPath = rfas.repeatedForwardAStar(states, startLocation, goalLocation, isLargerGFirst, totaltimestep, totalactualcost, totalnumberofastarinteractions,totaltimecsost, totalnumberofexpandedcells,numMazeNoPath)
        #if agentPath is not False:
        #    #visualizePath(agentPath, i)
        #    print("\tCosts for optimal path: %d" % (len(agentPath) - 1))
        #    totalcostsforoptimalpath += (len(agentPath) - 1)

        #print("")

        #states = hf.genstates(i)  # Reset the states
        #print("---------------------Current Alogrithm : Repeateed Backward A Star---------------------")
        #agentPath, totaltimestep,totalactualcost,totalnumberofastarinteractions,totaltimecsost, totalnumberofexpandedcells, numMazeNoPath = rbas.repeatedBackwardAStar(states, startLocation, goalLocation, isLargerGFirst, totaltimestep, totalactualcost, totalnumberofastarinteractions,totaltimecsost, totalnumberofexpandedcells,numMazeNoPath)
        #if agentPath is not False:
        #    visualizePath(agentPath, i)
        #    print("\tCosts for optimal path: %d" % (len(agentPath) - 1))
        #    totalcostsforoptimalpath += (len(agentPath) - 1)
        #print("")

        states = hf.genstates(i)  # Reset the states
        print("---------------------Current Alogrithm : Adaptive A Star---------------------")
        agentPath, totaltimestep,totalactualcost,totalnumberofastarinteractions,totaltimecsost, totalnumberofexpandedcells, numMazeNoPath = raas.repeatedAdaptiveAStar(states, startLocation, goalLocation, isLargerGFirst, totaltimestep, totalactualcost, totalnumberofastarinteractions,totaltimecsost, totalnumberofexpandedcells,numMazeNoPath)
        if agentPath is not False:
            visualizePath(agentPath, i)
            print("\tCosts for optimal path: %d" % (len(agentPath) - 1))
            totalcostsforoptimalpath += (len(agentPath) - 1)
    # print("")

    print("Total Time Step Averaged over mazeNum Mazes: ",(totaltimestep/(5-numMazeNoPath)))
    print("Total Actual Cost Averaged over mazeNum Mazes: ",(totalactualcost/(5-numMazeNoPath)))
    print("Total Number of A Star Interactions Averaged over mazeNum Mazes: ",(totalnumberofastarinteractions/(5-numMazeNoPath)))
    print("Total Time Cost over mazeNum Mazes: ",(totaltimecsost/(5-numMazeNoPath)))
    print("Total Number of Expanded Cells over mazeNum Mazes: ",(totalnumberofexpandedcells/(5-numMazeNoPath)))
    print("Total Cost for Optimal Path Averaged over mazeNum Mazes: ",(totalcostsforoptimalpath/(5-numMazeNoPath)))