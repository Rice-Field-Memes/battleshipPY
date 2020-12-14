from sys import stdout
import os

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import random
from random import getrandbits
#import cProfile
#import re
import time
from time import time
import threading
import multiprocessing
from numba import jit, cuda
import colorama
colorama.init()
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
@jit(nopython=True)
def shipLoop(len,occupied):
    shouldRun = True
    while shouldRun:
        #sh_t = allCoords(int(10*random.random()),int(10*random.random()),len,not getrandbits(1))
        x,y = int(10*random.random()), int(10*random.random())
        sh_t = [(x,a) for a in range(y,y+len)] if not getrandbits(1) else [(a,y) for a in range(x,x+len)]
        shouldRun = True in [c in [x for x in occupied for x in x] or c[0]>9 or c[1]>9 for c in sh_t]
    return sh_t

@jit(nopython=True)
def monteHunt(n, bb, tr):
    # n: recursions, bb: board, 
    #st1 = time()
    #print("Process ID {} spawned!".format(tr))
    freqBoard = [[0 for _ in range(10)] for _ in range(10)]
    hitSpots = []
    occupied = []
    tempBoard = bb
    lenOrder = [5,4,3,3,2]
    tries = 0
    for i,a in enumerate(tempBoard):
        for e,s in enumerate(a):
            if s == 2: hitSpots.append((i,e))
            elif s == 1: occupied.append([(i,e)])

    for x in range(n):
        sr = True
        while sr:
            #Hitspots: Each tile that has a hit attack, all must be in tempOccupied, if any
            #Tempoccupied: List of all occupied coordinates, after each recursion is set to missed attacks

            #tempb = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
            tempOccupied = list(occupied)
            #if x == 0: print(tempOccupied)
            
            #Appending each individually is necessary, as each one needs the most recent occupied coordintes, cannot be done on one line
            tempOccupied.append(shipLoop(5,tempOccupied))
            tempOccupied.append(shipLoop(4,tempOccupied))
            tempOccupied.append(shipLoop(3,tempOccupied))
            tempOccupied.append(shipLoop(3,tempOccupied))
            tempOccupied.append(shipLoop(2,tempOccupied))

            tries+=1
            #List of if each hitSpot has a place in tempOccupied, should not be false in it
            #If it is all true, each hit spot has been taken, should stop looping
            #Will return false if false in list, meaning it is not all true
            sr = False in [elem in [x for x in tempOccupied for x in x] for elem in hitSpots]
        #print("e")
        #if x==0: print(occupied)
        for a,b in [e for e in tempOccupied for e in e]: freqBoard[a][b]+=1
#    q.put(freqBoard)
    #print("Avg. per run: " + str(tries/n))
    #print('Process took = {} seconds'.format(time() - st1))
    print("Average tries per recursion: {}".format(tries / n))
    return freqBoard

def npa(perc):
    pMax = max([x for x in perc for x in x])
    pMin = min([x for x in perc for x in x])
    bp = [[(y-pMin)/(pMax-pMin) for y in x] for x in perc]
    return np.array(bp)

def combineBoards(*args):
    retBoard = [[0 for _ in range(10)] for _ in range(10)]
#    print("EEEEEEEEEEEEEEEEE")
#    print(args)
    for a in range(10):
        for b in range(10):
            retBoard[a][b] = sum([x[a][b] for x in args[0]])
    return retBoard

def renderMap(board):
    st = time()
    
    resultTen = monteHunt(20000, board, 1)
    print('Time taken = {} seconds'.format(time() - st))
    return npa(resultTen)
def inpt():
    ltn = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
    bbb = np.zeros((10,10))
    shotCoords = []
    #ax.pcolormesh(np.array(renderMap(bbb)),cmap="hot")
    #plt.draw()
    while True:
        inp = input("Input: ")
        if inp == "q": exit()
        if inp[0].upper() == "H": bbb[10-int(inp[2])][ltn[inp[1].upper()]] = 2
        elif inp[0].upper() == "M": bbb[10-int(inp[2])][ltn[inp[1].upper()]] = 1
        else: continue
#        print(inp[0])
        shotCoords.append((10-int(inp[2]),ltn[inp[1].upper()]))
        boardRendered = renderMap(bbb)
        for x,y in shotCoords: boardRendered[x][y] = 0

        #boardRendered[10-int(inp[2])][ltn[inp[1].upper()]] = 0
        boardRendered = np.array(boardRendered)
        ax.pcolormesh(boardRendered, cmap="hot")
        
        #fig.canvas.draw()
        plt.draw()
        maxind = np.unravel_index(boardRendered.argmax(),boardRendered.shape)
        print("Recommended attack: {1}{0}".format(10-maxind[0], list(ltn.keys())[maxind[1]]))


if __name__=="__main__":
    #board[7][8] = 2
    numpyTen = renderMap(np.zeros((10,10)))

    matplotlib.rcParams['toolbar'] = 'None'
    fig, ax = plt.subplots()

    #fig.canvas.mpl_connect('key_press_event', press)

    pcm = ax.pcolormesh(numpyTen,cmap = 'hot')
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    fig.tight_layout()
    fig.canvas.set_window_title('Probability heatmap')
    x = threading.Thread(target=inpt, args=())
    x.start()
    plt.show()