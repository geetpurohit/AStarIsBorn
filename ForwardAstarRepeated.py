import HelperFunctions as hf
import time as t
import BinaryHeapMin as bh


# Forward A* algorithm
def ComputePath(openHeap, closedHeap, goalState, expandedStates, counter, states):
    while goalState.gValue > openHeap.peek().f:
        minState = openHeap.pop()  # Remove a state s with the smallest f-value g(s) + h(s) from openHeap
        expandedStates.append(minState.location)
        closedHeap.push(minState)
        actionList = hf.listofactions(minState, states, closedHeap)  # Generate action list for the state
        
        for action in actionList:
            searchedState = hf.postmovestate(minState, action, states)  # Get the state after taking a specific action
            if searchedState.search < counter:
                searchedState.gValue = 99999
                searchedState.search = counter
            if searchedState.gValue > minState.gValue + 1:
                searchedState.gValue = minState.gValue + 1  # Update the cost
                searchedState.treePointer = minState  # Build a forward link pointing to the last state

                if openHeap.contains(searchedState):
                    openHeap.remove(searchedState)  # Remove existed state from opehHeap
                
                searchedState.updatef()
                openHeap.push(searchedState)

        if openHeap.isEmpty():
            break


# main function
def repeatedForwardAStar(states, startLocation, goalLocation, isLargerGFirst: bool, totaltimestep, totalactualcost, totalnumberofastarinteractions,totaltimecsost, totalnumberofexpandedcells,numMazeNoPath):
    counter = 0  # A star counter
    agentPath = []  # Path recorder
    timeStep = 0  # Time step counter
    expandedStates = []  # Expanded states during the whole repeated A star search

    # Respectively label the states at start location and at goal location as start state and goal state
    startState = states[startLocation[0]][startLocation[1]]
    goalState = states[goalLocation[0]][goalLocation[1]]

    hf.checknearbycell(startState, states)  # Check the status of nearby states

    agentPath.append(startLocation)  # Add the start location to the path

    # Compute and set heuristic value for all states
    for stateList in states:
        for state in stateList:
            state.h = hf.manhattan(state, goalState)

    startTime = t.time()  # Record start time
    while startState != goalState:
        counter += 1

        startState.gValue = 0  # record cost for start state to reach start state, which is 0
        startState.search = counter  #
        goalState.gValue = 99999  # record cost for goal state to reach start state, which uses 999 as infinity
        goalState.search = counter  #

        # initialize open heap and closed heap
        openHeap = bh.minheap(isLargerGFirst)
        closedHeap = bh.minheap(isLargerGFirst)

        # calculate f value
        startState.updatef()
        # print("State f Value: %d" % startState.f)

        openHeap.push(startState)  # insert start state into open heap

        ComputePath(openHeap, closedHeap, goalState, expandedStates, counter, states)  # Run forwardA*

        # if open heap is empty, report that can't reach the target
        if openHeap.size() == 0:
            numMazeNoPath += 1
            return False,totaltimestep,totalactualcost,totalnumberofastarinteractions,totaltimecsost, totalnumberofexpandedcells,numMazeNoPath

        # A star search finds the start state and move start location according to the tree pointer
        # Track the tree pointers from goal state to start state
        while startState != goalState:
            timeStep += 1
            nextState = goalState

            # Find the next state
            while (nextState.treePointer is not None) & (nextState != startState):
                if nextState.treePointer == startState:
                    break
                nextState = nextState.treePointer

            if nextState.discoveredBlockStatus is False:
                startState = nextState
                agentPath.append(startState.location)
                hf.checknearbycell(startState, states)
            else:
                break

    expandedStates.append(goalState.location)
    endTime = t.time()  # Record end time
    totaltimestep = totaltimestep + timeStep
    totalactualcost += (len(agentPath) - 1)
    totalnumberofastarinteractions += counter
    totaltimecsost += (endTime - startTime)
    totalnumberofexpandedcells += len(expandedStates)

    return agentPath, totaltimestep,totalactualcost,totalnumberofastarinteractions,totaltimecsost, totalnumberofexpandedcells, numMazeNoPath
