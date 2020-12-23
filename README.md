# Files
## BattleshipPY
Main Python file for running basic battleship game. Uses pyglet for GUI
## Board, Game, Cursor, Ship
Python class files, used by battleshipPY
## AI Files
There are several different versions of the Battleship AI, represented by different python files. The version have different methods of input and intended uses  
All versions currently use a Monte Carlo-esque simulation of Battleship board placements  
Uses a loop for each type of ship. It randomly places a ship, and when it does not collide with anything, it progresses to the next ship.  
If there is a hit tile, it will check if this hit block is occupied. If not, it returns to the beginning.  
Processing power and calculation time are based on efficiency of the algorithm and the average amount of failed placements.  
The function is given an amount of placements, and only correct placements are counted, meaning a certain amount of recursions can have many more attempted placements, effecting efficiency  
In the future, optimization methods will be explored.  
Currently, 20000 recursions is sufficient.  
All of the verions use Matplotlib to display the probability heatmap and the board showing the attacks  
All GPU files use Numba @jit to run the Monte Carlo simulation code on GPU. This increases performance drastically

### permutationCalcGPU
Most basic version of the AI. 
Uses manual entry to play the game  
As the user plays the game, they enter the results of their attacks (hit, miss, sink)  
To have the AI calculate the optimal attack, run the simulation and the AI will print the best move  
The commands are as following (capitalization not important)  
Hit: type `H + the coordinates of the attack (eg: HE4)`  
Miss: type `M + the coordinates of the attack (eg: MA1)`  
When a ship is sunk, type `S + the length of the ship (eg: S3)` Then for each tile of the sunk ship, type `R + the coordinates`  
To run the simulation, simply press enter with no input or "GO"   

### permutationCalcGPUclick
Similar to permutationCalcGPU, but has a different input method  
This version allows input via interaction with the Matplotlib graph.  
To input a hit, simply left click on the hit tile. For a miss, right click on the tile  
When a ship is sunk, click the button on the bottom corresponding to the ship length. Then, press S over each tile of the ship  
To recalculate, simply press E  

If a tile is accidentally marked as attacked, press x over the tile to reset it.  
If a ship is accidentally sunk, pressing P will reset all the ships.  

### permutationCalcGPUauto
Intended for testing, statistics gathering, or to possibly integrate into a python Battleship game internally  
Has no input, as the AI automatically attacks based on its calculated move  
Reads from the file "boardsave" which should be in the same directory. This file can be saved to by battleshipPY by pressing Z during board placement  
Because this version has the full board to begin with, it includes a third heatmap on Matplotlib, showing the ships positions  

### permutationCalc (Legacy)
This version does not use GPU integration, and therefore has the original code for the simulation  
The GPU and CPU implementations had to be seperated as Numba Jit has limited support for python's built in functions, meaning that much of the code had to be rewritten  
This version is not recommended as it is much slower, even compared to a bad graphics card

## Installation
This project was coded in Python 3.7.2  
First, install the dependencies  
`python -m install -r requirements.txt`  
Then run the Python file  
`python permutationCalcGPUclick.py`