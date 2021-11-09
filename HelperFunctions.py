import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
import CurrentSTate as st

# Generate states from files
def genstates(i):
    dataset = np.loadtxt('%d.txt' % (i), dtype=np.int32)
    # convert list to states list and return
    return [[st.currstate(x, y, True if int(dataset[x][y]) == 1 else False) for y in range(len(dataset[0]))] for x in range(len(dataset))]


# heuristic function (Manhattan distance)
def manhattan(s1: st.currstate, s2: st.currstate):
    return abs(s1.location[0] - s2.location[0]) + abs(s1.location[1] - s2.location[1])


# generate a list of possible actions for current state
# 1: down; 2: up; 3: right; 4: left
def listofactions(state: st.currstate, states, closedHeap):
    possibleActions = []
    row = state.location[0]
    column = state.location[1]

    #   Check possible actions
    #   Check down
    if row + 1 <= len(states) - 1:
        if (states[row + 1][column].discoveredBlockStatus is False) & (not closedHeap.contains(states[row + 1][column])):
            possibleActions.append(1)

    #   Check up
    if row - 1 >= 0:
        if (states[row - 1][column].discoveredBlockStatus is False) & (not closedHeap.contains(states[row - 1][column])):
            possibleActions.append(2)

    #   Check right
    if column + 1 <= len(states) - 1:
        if (states[row][column + 1].discoveredBlockStatus is False) & (not closedHeap.contains(states[row][column + 1])):
            possibleActions.append(3)

    #   Check left
    if column - 1 >= 0:
        if (states[row][column - 1].discoveredBlockStatus is False) & (not closedHeap.contains(states[row][column - 1])):
            possibleActions.append(4)

    return possibleActions


# return a state after moving to a direction
def postmovestate(state, action, states):
    row = state.location[0]
    column = state.location[1]
    # down
    if action == 1:
        return states[row + 1][column]
    # up
    elif action == 2:
        return states[row - 1][column]
    # right
    elif action == 3:
        return states[row][column + 1]
    # left
    elif action == 4:
        return states[row][column - 1]
    else:
        return None


# Check nearby cell and update their block status
def checknearbycell(s: st.currstate, states):
    row = s.location[0]
    column = s.location[1]
    # Check down
    if row + 1 <= len(states) - 1:
        states[row + 1][column].discoveredBlockStatus = states[row + 1][column].actualBlockStatus
    # Check up
    if row - 1 >= 0:
        states[row - 1][column].discoveredBlockStatus = states[row - 1][column].actualBlockStatus
    # Check right
    if column + 1 <= len(states) - 1:
        states[row][column + 1].discoveredBlockStatus = states[row][column + 1].actualBlockStatus
    # Check left
    if column - 1 >= 0:
        states[row][column - 1].discoveredBlockStatus = states[row][column - 1].actualBlockStatus


# Randomly generate a location that is unblocked
def genunblocked(states):
    statesEdgeSize = len(states)
    location = np.random.randint(0, statesEdgeSize, 2)
    while states[location[0]][location[1]].actualBlockStatus is True:
        location = np.random.randint(0, statesEdgeSize, 2)
    return location




# Tie breaker that prioritizes state with larger g value
def bG(s: st):
    return 999 * s.f - s.g


# Tie breaker that prioritizes state with smaller g value
def sG(s: st):
    return 999 * s.f + s.g