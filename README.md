# Files
## BattleshipPY
Main Python file for running basic battleship game. Uses pyglet for GUI
## Board, Game, Cursor, Ship
Python class files, used by battleshipPY
## PermutationCalc
Main Python file for running AI  
Currently uses a Monte Carlo-esque simulation of Battleship board placements  
Uses a loop for each type of ship. It randomly places a ship, and when it does not collide with anything, it progresses to the next ship.  
If there is a hit tile, it will check if this hit block is occupied. If not, it returns to the beginning.  
Processing power and calculation time, are based on efficiency of the algorithm and the average amount of failed placements.  
The function is given an amount of placements, and only correct placements are counted, meaning a certain amount of recursions can have many more attempted placements, effecting efficiency  
In the future, optimization methods will be explored.  
Currently, 5000-20000 recursions is adequate. Multiprocessing pools are used to increase speed.