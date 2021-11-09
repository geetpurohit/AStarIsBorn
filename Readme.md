<p align="center">
    <title> A Star is Born </title>
</p>


# Overview 

Consider the following problem: an agent in a gridworld has to move from its current cell to the given cell of a non-moving
target, where the gridworld is not fully known. They are discretizations of terrain into square cells that are either blocked
or unblocked.

Similar search challenges arise frequently in real-time computer games, such as ***League of Legends*** shown below, and robotics.
To control characters in such games, the player can click on known or unknown terrain, and the game characters then move
autonomously to the location that the player clicked on. The characters observe the terrain within their limited field of
view and then remember it for future use but do not know the terrain initially (due to “fog of war”). The same situation
arises in robotics, where a mobile platform equipped with sensors builds a map of the world as it traverses an unknown
environment.
![LeagueofLegends](https://technology.riotgames.com/sites/default/files/sr_fow_2.jpg)

Assume that the initial cell of the agent is unblocked. The agent can move from its current cell in the four main compass
directions (east, south, west and north) to any adjacent cell, as long as that cell is unblocked and still part of the gridworld.
All moves take one time step for the agent and thus have cost one. The agent always knows which (unblocked) cell it is in
and which (unblocked) cell the target is in. The agent knows that blocked cells remain blocked and unblocked cells remain
unblocked but does not know initially which cells are blocked. However, it can always observe the blockage status of its
four adjacent cells, which corresponds to its field of view, and remember this information for future use. The objective of
the agent is to reach the target as effectively as possible.

# Setup 
A common-sense and tractable movement strategy for the agent is the following: The agent assumes that cells are unblocked
unless it has already observed them to be blocked and uses search with the “freespace assumption”. In other words, it moves
along a path that satisfies the following three properties:
1. It is a path from the current cell of the agent to the target.
2. It is a path that the agent does not know to be blocked and thus assumes to be unblocked, i.e., a presumed unblocked
path.
3. It is a shortest such path.
Whenever the agent observes additional blocked cells while it follows its current path, it remembers this information for
future use. If such cells block its current path, then its current path might no longer be a “shortest presumed-unblocked
path” from the current cell of the agent to the target. Then, the agent stops moving along its current path, searches for
another “shortest presumed-unblocked path” from its current cell to the target, taking into account the blocked cells that it
knows about, and then moves along this path. The cycle stops when the agent:
• either reaches the target or
• determines that it cannot reach the target because there is no presumed-unblocked path from its current cell to the
target and it is thus separated from the target by blocked cells.

# Algorithms
In this project, I use A* to determine the shortest paths, resulting in Repeated A*.  A* is an informed search algorithm, or a best-first search, meaning that it is formulated in terms of weighted graphs: starting from a specific starting node of a graph, it aims to find a path to the given goal node having the smallest cost (least distance travelled, shortest time, etc.). At each iteration of its main loop, A* needs to determine which of its paths to extend. It does so based on the cost of the path and an estimate of the cost required to extend the path all the way to the goal. Specifically, A* selects the path that minimizes

![image](https://user-images.githubusercontent.com/68968629/141022689-acfaac79-52be-4b44-81a7-88b292365353.png)

### *Repeated Forward A* 

A* can search either from the current
cell of the agent toward the target (= forward), resulting in Repeated Forward A*

Now, it is important to note that Repeated A* has a g-value g(s) (infinity, initially), which is the length of the shortest path from the start state to state s found
by the A* search and thus an upper bound on the distance from the start state to state s. Repeated Forward A* needs to break ties to decide which cell to expand next if several cells have the same smallest f-value. It can either break ties in favor of cells with smaller g-values or in favor of cells with larger g-values. This results in a Repeated Forward A* favoring a smaller g-value versus favoring a larger g-value. 

### *Repeated Backward A*
or from the target toward the current cell
of the agent (= backward), resulting in Repeated Backward A*.

### *Adaptive A* 
Adaptive A* uses A* searches to repeatedly find shortest paths in state spaces with possibly different start states but the
same goal state where action costs can increase (but not decrease) by arbitrary amounts between A* searches.1 It uses its
experience with earlier searches in the sequence to speed up the current A* search and run faster than Repeated Forward A*. 
It first finds the shortest path from the current start state to the goal state according to the current action costs. 


