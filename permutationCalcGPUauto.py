import sys
from sys import stdout
import os

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
matplotlib.use('Qt5agg')
import random
from random import getrandbits
#import cProfile
#import re
from time import time,sleep
from numba import jit, cuda
from numba.typed import List

from Ship import Ship
os.system("cls")

boardProb = [[0 for _ in range(10)] for _ in range(10)]

board = [[0 for _ in range(10)] for _ in range(10)]

#board[2][7] = 2
#board[4][4] = 1
#board[7][2] = 1

#board[7][7] = 2
def boardFromCoords(coords):
    na = np.zeros((10,10))
    for x,y in [e for e in coords for e in e]:
        na[x][y] = 1
    return na

def calcShip(len):
    for x in range(10):
        for y in range(11-len):
            aCrds = allCoords(x,y,len,2)
            if all([board[c[0]][c[1]]==0 for c in aCrds]):
                for _ in aCrds: boardProb[_[0]][_[1]]+=1

    for x in range(11-len):
        for y in range(10):
            aCrds = allCoords(x,y,len,3)
            if all([board[c[0]][c[1]]==0 for c in aCrds]):
                for _ in aCrds: boardProb[_[0]][_[1]]+=1
    return None
def stringGrid(g):
    f = ""
    for x in g:
        f+=''.join(["██" if _==1 else "  " for _ in x]) + "\n"
    return f
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
    global allRuns
    allRuns.append((time()-st,tpn))
    return npa(resultTen)

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

def readFileSave(filecont):
    return [[(int(b[0]),int(b[1])) for b in a.split('-')] for a in filecont.split('=')]

def fixCoords(coords):
    return [list(map(lambda xy: (xy[1],xy[0]), e)) for e in coords]

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
    ltn = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
    #Board
    #0: not shot, 1: shot missed, 2: shot hit, 3: sunk (treated as missed)

    simulation = Simulation()
    with open("boardsave","r") as file1:
        hiddenShips = fixCoords(readFileSave(file1.read()))

    if mplo:
        boardpcm = boardax.pcolormesh(boardFromCoords(hiddenShips), cmap=plt.get_cmap("Greys"), edgecolors="k", linewidths=1)
        plt.show(block=False)
    bbb = np.zeros((10,10))
    shotCoords = []
    liveShips = [5,4,3,3,2]
    shots = 0
    #ax.pcolormesh(np.array(renderMap(bbb)),cmap="hot")
    #plt.draw()
    while True:
        if liveShips == []:
            if mplo:
                shotax.pcolormesh(bbb, cmap=shotcolor, norm=shotnorm, edgecolors="k", linewidths=1)
                plt.draw()
                plt.pause(0.01)
            print("\nYou win!\n{} rounds!".format(shots))
            return
        print("\nRound " + str(shots))
#        print(inp[0])
        boardRendered = renderMap(bbb,liveShips)
        for x,y in shotCoords: boardRendered[x][y] = 0

        #boardRendered[10-int(inp[2])][ltn[inp[1].upper()]] = 0
        boardRendered = np.array(boardRendered)

        if mplo:
            shotax.pcolormesh(bbb, cmap=shotcolor, norm=shotnorm, edgecolors="k", linewidths=1)
        
            ax.pcolormesh(boardRendered, cmap="hot")
            plt.draw()
            plt.pause(0.01)

        #fig.canvas.draw()
        maxind = np.unravel_index(boardRendered.argmax(),boardRendered.shape)
        print("Attacking {1}{0}".format(10-maxind[0], list(ltn.keys())[maxind[1]]))
        if maxind in [x for x in hiddenShips for x in x]:
            bbb[maxind[0]][maxind[1]] = 2
            print("{1}{0} HIT".format(10-maxind[0], list(ltn.keys())[maxind[1]]))
        else:
            bbb[maxind[0]][maxind[1]] = 1
            print("{1}{0} MISS".format(10-maxind[0], list(ltn.keys())[maxind[1]]))
        shots+=1
        if shots==20: print(allRuns)
        shotCoords.append(maxind)
        for s in hiddenShips:
            if not False in [t in shotCoords for t in s]:
                liveShips.remove(len(s))
                hiddenShips.remove(s)
                print("SIZE {} SHIP SUNK".format(len(s)))
                for x,y in s: bbb[x][y] = 3


if __name__=="__main__":
    #board[7][8] = 2
    allRuns = []
    mplo = True
    if len(sys.argv) == 2:
        if sys.argv[1] == "1":
            mplo = False

    if mplo:
        shotcolor,shotnorm = colors.from_levels_and_colors([0,1,2,3,4],["Blue", "Red", "Lime", "Yellow"])

        numpyTen = renderMap(np.zeros((10,10)))


        matplotlib.rcParams['toolbar'] = 'None'
        fig, (boardax, ax, shotax) = plt.subplots(1,3,figsize=(18,6))

        #fig.canvas.mpl_connect('key_press_event', press)
        pcm = ax.pcolormesh(numpyTen,cmap = 'hot')
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        fig.tight_layout()

        shotpcm = shotax.pcolormesh(np.zeros((10,10)), cmap=shotcolor, norm=shotnorm, edgecolors="k", linewidths=1)
        shotax.axes.get_xaxis().set_visible(False)
        shotax.axes.get_yaxis().set_visible(False)
    
        boardax.axes.get_xaxis().set_visible(False)
        boardax.axes.get_yaxis().set_visible(False)


        fig.canvas.set_window_title('Probability heatmap')
    totaltime = time()
    inpt()
    print('Time taken = {} seconds'.format(time() - totaltime))
    input()