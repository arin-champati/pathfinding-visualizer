# Pathfinding Visualizer
A PyGame project that allows you to visualize a pathfinding algorithm in real-time.

## Algorithms
This project features four basic pathfinding algorithms: a*, dijkstra, BFS, and DFS. The heuristics for a* and dijkstra are either the manhattan distance or time. Both of them break ties by normalizing with (unit path length / max expected path length). The time heuristic does not guarantee a path with the shortest amount of time, but it consistently outperforms manhattan distance. Note, in this case, because the unit is constant, BFS and dijstra w/manhattan distance perform the exact same. 

## Features


## Code Design
#### Visual Flexibility
The screen can be resized from the main method, and the board can have added rows as an argument as well. There is a config file that allows the color scheme to change, the speeds of nodes to change, the font, render speeds, etc. 
#### Improvements
The use of global variables for menu status, algorithm status, and results, would declutter the code and allow future additions to be even simpler than they already are. In the future, I will make these variables global, but for now, they are all passed in as arguments.
 
