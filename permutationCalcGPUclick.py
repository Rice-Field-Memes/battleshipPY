from sys import stdout
import os

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.widgets import Button
matplotlib.use('Qt5agg')

import random
from random import getrandbits
from time import time
from numba import jit, cuda
from numba.typed import List

from functools import partial

os.system("cls")

def onclick(event):
    ix, iy = event.xdata, event.ydata
    if ix!=None and iy!=None and event.inaxes.label != "sinkbutton":
        if event.button == 1:
            shotax.pcolormesh(simulation.attack((int(ix),int(iy)),2), cmap=shotcolor, norm=shotnorm, edgecolors="k", linewidths=1)
            plt.draw()
        elif event.button == 3:
            shotax.pcolormesh(simulation.attack((int(ix),int(iy)),1), cmap=shotcolor, norm=shotnorm, edgecolors="k", linewidths=1)
            plt.draw()

def press(event):
#    print('press', event.key)
    ix, iy = event.xdata, event.ydata
    if event.key == 'x':
        if ix!=None and iy!=None and event.inaxes.label != "sinkbutton":
            shotax.pcolormesh(simulation.attack((int(ix),int(iy)),0), cmap=shotcolor, norm=shotnorm, edgecolors="k", linewidths=1)
            plt.draw()
    elif event.key == 'e':
        simulation.runSim()
    elif event.key == 's':
        if ix!=None and iy!=None and event.inaxes.label != "sinkbutton":
            shotax.pcolormesh(simulation.attack((int(ix),int(iy)),3), cmap=shotcolor, norm=shotnorm, edgecolors="k", linewidths=1)
            plt.draw()
    elif event.key == 'p':
        simulation.resetShips()



boardProb = [[0 for _ in range(10)] for _ in range(10)]

board = [[0 for _ in range(10)] for _ in range(10)]

#board[2][7] = 2
#board[4][4] = 1
#board[7][2] = 1

#board[7][7] = 2

def stringGrid(g):
    f = ""
    for x in g:
        f+=''.join(["██" if _==1 else "  " for _ in x]) + "\n"
    return f

def readSave(inp):
    if inp != "":
        #TEST: 0000000000000000000000000000000000000000000020000000000000000000000000000000000010000000000000000000_44-80_54332
        interpretParts = inp.split('_')
        if len(interpretParts) != 3: return False
        #Board
        boardArray = [list(interpretParts[0][x*10:(x+1)*10]) for x in range(10)]
        boardArray = np.array([list(map(lambda y: int(y), x)) for x in boardArray])

        #Shotcoords
        shotCoords = [(int(x[0]),int(x[1])) for x in interpretParts[1].split("-")]

        #LiveShips
        liveShips = [int(x) for x in interpretParts[2]]

        return boardArray, shotCoords, liveShips
    else: return False

@jit(nopython=True,fastmath=True)
def shipLoop(len,occupied):
    shouldRun = True
    xocc = [x for x in occupied for x in x]
    while shouldRun:
        #sh_t = allCoords(int(10*random.random()),int(10*random.random()),len,not getrandbits(1))
        x,y = int(10*random.random()), int(10*random.random())
        sh_t = [(x,a) for a in range(y,y+len)] if not getrandbits(1) else [(a,y) for a in range(x,x+len)]
        shouldRun = True in [c in xocc or c[0]>9 or c[1]>9 for c in sh_t]
    return sh_t

@jit(nopython=True,fastmath=True)
def monteHunt(n, bb, ships):
    # n: recursions, bb: board, 
    #st1 = time()
    #print("Process ID {} spawned!".format(tr))
    freqBoard = [[0 for _ in range(10)] for _ in range(10)]
    hitSpots = []
    occupied = []
    tries = 0
    for i,a in enumerate(bb):
        for e,s in enumerate(a):
            if s == 2: hitSpots.append((i,e))
            elif s == 1 or s == 3: occupied.append([(i,e)])

    for x in range(n):
        sr = True
        while sr:
            #Hitspots: Each tile that has a hit attack, all must be in tempOccupied, if any
            #Tempoccupied: List of all occupied coordinates, after each recursion is set to missed attacks
            tempOccupied = list(occupied)
            #Appending each individually is necessary, as each one needs the most recent occupied coordintes
            for s in ships: tempOccupied+=[shipLoop(s,tempOccupied)]
            tries+=1
            #List of if each hitSpot has a place in tempOccupied, should not be false in it
            #If it is all true, each hit spot has been taken, should stop looping
            #Will return false if false in list, meaning it is not all true
            tempOccFixed = [x for x in tempOccupied for x in x]
            sr = False in [elem in tempOccFixed for elem in hitSpots]
        for a,b in tempOccFixed: freqBoard[a][b]+=1
    #print("Avg. per run: " + str(tries/n))
    return freqBoard, tries/n

def npa(perc):
    pMax = max([x for x in perc for x in x])
    pMin = min([x for x in perc for x in x])
    bp = [[(y-pMin)/(pMax-pMin) for y in x] for x in perc]
    return np.array(bp)

def combineBoards(*args):
    retBoard = [[0 for _ in range(10)] for _ in range(10)]
    for a in range(10):
        for b in range(10):
            retBoard[a][b] = sum([x[a][b] for x in args[0]])
    return retBoard

def renderMap(board, liveShips=[5,4,3,3,2]):
    st = time()
    resultTen,tpn = monteHunt(20000, board, List(liveShips))
    print('Time taken = {} seconds'.format(time() - st))
    print("Average tries per recursion: {}".format(tpn))
    return npa(resultTen)

class Simulation:
    def __init__(self):
        self.bbb = np.zeros((10,10))
        self.shotCoords = []
        self.liveShips = [5,4,3,3,2]
        self.shots = 0
    def runSim(self):
        if simulation.liveShips == []:
            print("You win!\n{} rounds!".format(self.shots))
            return
        boardRendered = renderMap(self.bbb,self.liveShips)
        for x,y in self.shotCoords: boardRendered[x][y] = 0

        boardRendered = np.array(boardRendered)

        ax.pcolormesh(boardRendered, cmap="hot")

        plt.draw()
        maxind = np.unravel_index(boardRendered.argmax(),boardRendered.shape)
        print("Recommended attack: {1}{0}".format(10-maxind[0], list(ltn.keys())[maxind[1]]))
        return
    def attack(self, xy, result):
        #0: not shot, 1: shot missed, 2: shot hit, 3: sunk (treated as missed)
        if result == 0: #If removing attack
            if (xy[1],xy[0]) in self.shotCoords:
                self.shotCoords.remove((xy[1],xy[0]))
            self.bbb[xy[1]][xy[0]] = 0
        else:
            if not (xy[1],xy[0]) in self.shotCoords:
                self.shotCoords.append((xy[1],xy[0]))
                self.shots+=1
            self.bbb[xy[1]][xy[0]] = result
        return self.bbb
    def sinkShip(self,length,_):
        if length in self.liveShips:
            self.liveShips.remove(length)
            print("SIZE {} SHIP SUNK".format(length))
        return
    def resetShips(self):
        self.liveShips = [5,4,3,3,2]
        print("SHIPS RESET")
        return

def inpt():
    plt.show()


if __name__=="__main__":
    #board[7][8] = 2
    shotcolor,shotnorm = colors.from_levels_and_colors([0,1,2,3,4],["Blue", "Red", "Lime", "Yellow"])
    ltn = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
    numpyTen = renderMap(np.zeros((10,10)))
    
    simulation = Simulation()

    matplotlib.rcParams['toolbar'] = 'None'
    fig, (ax, shotax) = plt.subplots(1,2,figsize=(13,6), sharex=True)
    ax.label = "heatmap"
    shotax.label = "attackmap"
    fig.canvas.mpl_connect('key_press_event', press)
    fig.canvas.mpl_connect('button_press_event', onclick)

    letterAxes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    plt.xticks(list(map(lambda x: x+0.5, range(10))), letterAxes)

    ax.axes.set_yticks(list(map(lambda x: x+0.5, range(10))))
    shotax.axes.set_yticks(list(map(lambda x: x+0.5, range(10))))
    ax.axes.set_yticklabels(range(1,11)[::-1])
    shotax.axes.set_yticklabels(range(1,11)[::-1])
    
    ax.tick_params(length=0, labelsize=16)
    shotax.tick_params(length=0, labelsize=16)

    ax.xaxis.tick_top()
    shotax.xaxis.tick_top()

    pcm = ax.pcolormesh(numpyTen,cmap = 'hot')
    fig.tight_layout()
    plt.subplots_adjust(bottom=0.1)


    shotpcm = shotax.pcolormesh(np.zeros((10,10)), cmap=shotcolor, norm=shotnorm, edgecolors="k", linewidths=1)
    sinkButtons = []
    for i,x in enumerate([5,4,3,2]):
        sinkButtons.append(Button(plt.axes([0.55+0.1*i, 0.01, 0.075, 0.08]),"Sink a {}".format(x)))
        sinkButtons[-1].on_clicked(partial(simulation.sinkShip, x))
        sinkButtons[-1].ax.label = "sinkbutton"
    fig.canvas.set_window_title('Probability heatmap')
    print(inpt())