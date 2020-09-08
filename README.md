# Pathfinding Visualizer
A PyGame project that allows you to visualize a pathfinding algorithm in real-time.

## Features
#### Algorithms
This project features four basic pathfinding algorithms: a*, dijkstra, BFS, and DFS. The heuristics for a* and dijkstra are either the manhattan distance or time. Both of them break ties by normalizing with (unit path length / max expected path length). The time heuristic does not guarantee a path with the shortest amount of time, but it consistently outperforms manhattan distance. Note, in this case, because the unit distance is constant (1), BFS and dijstra w/manhattan distance perform the exact same. The performance of the algorithm (time, distance) is displayed on the top right.

#### Board Functionalities
There are three main board handling functionalities. Unless the algorithm is running, one can create a new board, erase a board, or reset a board (i.e. after the algorithm is done, erasing the drawn path). They can either call these explicilty with key commands or the navigation menu. Or, if the algorithm has completed and the user provides clicked or typed input, the board will reset. One can also enter fullscreen mode, however, it is slightly glitchy with this version of PyGame.

#### User Interaction
There are built in features that make using this tool easier to use. When the algorithm is done running, and the user provides any clicked or typed input, the board will automatically reset. When placing the start, end, and boundary tiles, the user can decide to move certain pieces, and there is priority for the start and end nodes. 

## Code Design
#### Navigation Bar and Buttons
The code has been written to be compatible with future added functionality and modifications. I built the navigation bar from scratch - including the buttons (i.e. rendering the text and text box, handling button functionality once clicked). The navigation bar has been modularized such that the button functionalities and presentation, as well as the menu dropdown entries are easily modifiable - in the future, clicking a button can trigger any function for default and pressed statuses. For example, the same button function can be used to exit the game and to color the background blue, for example. 

The nav_bar.py file contains functions for each dropdown menu that are clients of an automatic dropdown menu-maker function, which simply requires a list of entries and statuses. The individual dropdown menu function are then called in an encompassing function that handles the status variables and is called in the gui.py file. In the future, one could keep adding functionalities to the game, and they can add these functionalities seamlessly to the navigation bar as well.
#### Visual Flexibility
The screen can be resized from the main method, and the board can have added rows as an argument as well. The code will automatically adjust to these parameters. There is additionally a config file that allows the color scheme to change, the speeds of nodes to change, the font, render speeds, etc. 
#### Improvements
The use of global variables for menu status, algorithm status, and results, would declutter the code and allow future additions to be even simpler than they already are. In the future, I will make these variables global, but for now, they are all passed in as arguments.
 
