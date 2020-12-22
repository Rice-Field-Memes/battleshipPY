from sys import stdout
import os

import numpy as np
import random
from random import getrandbits
import cProfile
#import re
from time import time,sleep


def shipLoop(len,occupied):
    shouldRun = True
    xocc = [x for x in occupied for x in x]
    while shouldRun:
        #sh_t = allCoords(int(10*random.random()),int(10*random.random()),len,not getrandbits(1))
        x,y = int(10*random.random()), int(10*random.random())
        sh_t = [(x,a) for a in range(y,y+len)] if not getrandbits(1) else [(a,y) for a in range(x,x+len)]
        shouldRun = True in [c in xocc or c[0]>9 or c[1]>9 for c in sh_t]
    return sh_t

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
    #print('Process took = {} seconds'.format(time() - st1))
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
    resultTen,tpn = monteHunt(20000, board, liveShips)
    print('Time taken = {} seconds'.format(time() - st))
    print("Average tries per recursion: {}".format(tpn))
    return npa(resultTen)

f = np.zeros((10,10))

f[4][4] = 1
f[7][6] = 1
f[1][2] = 2
f[5][5] = 2
f[1][1] = 1

renderMap(f)