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
from time import time
from numba import jit, cuda
from numba.typed import List
os.system("cls")

def allCoords(x,y,len,rotate):
    if rotate:
        return [(x,a) for a in range(y,y+len)]
    else:
        return [(a,y) for a in range(x,x+len)]

def press(event):
    print('press', event.key)
    stdout.flush()
    if event.key == 'x':
        ax.clear()
        ax.pcolormesh(renderMap(), cmap="Greys")
        fig.canvas.draw()

boardProb = [[0 for _ in range(10)] for _ in range(10)]

board = [[0 for _ in range(10)] for _ in range(10)]

#board[2][7] = 2
#board[4][4] = 1
#board[7][2] = 1

#board[7][7] = 2

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
def inpt():
    plt.show(block=False)
    ltn = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
    #Board
    #0: not shot, 1: shot missed, 2: shot hit, 3: sunk (treated as missed)
    bbb = np.zeros((10,10))
    shotCoords = []
    liveShips = [5,4,3,3,2]
    shots = 0
    #ax.pcolormesh(np.array(renderMap(bbb)),cmap="hot")
    #plt.draw()
    inp = input("load save? ")
    rs = readSave(inp)
    
    if rs != False:
        bbb,shotCoords,liveShips = rs
        
    while True:
        if liveShips == []:
            print("You win!\n{} rounds!".format(shots))
        print("Round " + str(shots))
        inp = input("Input: ")
        if inp.upper() == "GO" or inp.upper() == "":
#        print(inp[0])
            
            boardRendered = renderMap(bbb,liveShips)
            for x,y in shotCoords: boardRendered[x][y] = 0

            #boardRendered[10-int(inp[2])][ltn[inp[1].upper()]] = 0
            boardRendered = np.array(boardRendered)

            ax.pcolormesh(boardRendered, cmap="hot")
        
            #fig.canvas.draw()
            plt.draw()
            maxind = np.unravel_index(boardRendered.argmax(),boardRendered.shape)
            print("Recommended attack: {1}{0}".format(10-maxind[0], list(ltn.keys())[maxind[1]]))
            continue
        elif inp[0].upper() == "S":
            if len(inp) == 2:
                liveShips.remove(int(inp[1]))
            else: print("ERROR")
            continue
        elif inp[0].upper() == "H": bbb[10-int(inp[2:])][ltn[inp[1].upper()]] = 2
        elif inp[0].upper() == "M": bbb[10-int(inp[2:])][ltn[inp[1].upper()]] = 1
        elif inp[0].upper() == "R": bbb[10-int(inp[2:])][ltn[inp[1].upper()]] = 3
        elif inp == "q": return "{0}_{1}_{2}".format(''.join([str(int(x)) for x in bbb for x in x]),'-'.join([str(x[0])+str(x[1]) for x in shotCoords]),''.join(str(x) for x in liveShips))
        """
        BBB is converted to 1d string, each character representing place as number
        shotCoords is split by -, numbers are put next to eachother as 10 is not used by coord system
        liveships is string of numbers representing sizes
        """
        recentShot = (10-int(inp[2:]),ltn[inp[1].upper()])
        shotax.pcolormesh(bbb, cmap=shotcolor, norm=shotnorm, edgecolors="k", linewidths=1)
        plt.draw()
        if not recentShot in shotCoords:
            shotCoords.append((10-int(inp[2:]),ltn[inp[1].upper()]))
            shots+=1


if __name__=="__main__":
    #board[7][8] = 2
    shotcolor,shotnorm = colors.from_levels_and_colors([0,1,2,3,4],["Blue", "Red", "Lime", "Yellow"])

    numpyTen = renderMap(np.zeros((10,10)))


    matplotlib.rcParams['toolbar'] = 'None'
    fig, (ax, shotax) = plt.subplots(1,2,figsize=(13,6))

    #fig.canvas.mpl_connect('key_press_event', press)
    pcm = ax.pcolormesh(numpyTen,cmap = 'hot')
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    fig.tight_layout()

    shotpcm = shotax.pcolormesh(np.zeros((10,10)), cmap=shotcolor, norm=shotnorm, edgecolors="k", linewidths=1)
    shotax.axes.get_xaxis().set_visible(False)
    shotax.axes.get_yaxis().set_visible(False)

    fig.canvas.set_window_title('Probability heatmap')
    print(inpt())