from sys import stdout

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random
#import cProfile
#import re
from time import time
import threading
import multiprocessing

def allCoords(x,y,len,rotate):
    if rotate == 0:
        return [(x,a+1) for a in range(y-len,y)][::-1]
    elif rotate == 1:
        return [(a+1,y) for a in range(x-len,x)][::-1]
    elif rotate == 2:
        return [(x,a) for a in range(y,y+len)]
    elif rotate == 3:
        return [(a,y) for a in range(x,x+len)]

def press(event):
    print('press', event.key)
    stdout.flush()
    if event.key == 'x':
        #board[7][7] = 2
#        cmesh.cmap = "Grays"
        ax.clear()
        #im.set_data(renderMap())
        ax.pcolormesh(renderMap(), cmap="RdYlGn")
#        print(pcm)
#        pcm.cmap = plt.get_cmap("Greys")
        fig.canvas.draw()
#        plt.show()

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
def monteHunt(n, bb, tr, q):
    st1 = time()
    print("Process ID {} spawned!".format(tr))
    freqBoard = [[0 for _ in range(10)] for _ in range(10)]
    hitSpots = []
    tempBoard = bb
    tries = 0
    for i,a in enumerate(tempBoard):
        for e,s in enumerate(a):
            if s == 2: hitSpots.append((i,e))
    for x in range(n):
        while True:
            tempb = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
            #Carrier loop
            while True:
                tries+=1
                ca_t = allCoords(int(10*random.random()),int(10*random.random()),5,int(2*random.random())+2)
                try:
                    if not all([tempb[c[0]][c[1]]==0 and tempBoard[c[0]][c[1]]!=1 for c in ca_t]): continue
                except:
                    continue
                for x,y in ca_t: tempb[x][y]=1
                break
            #Battleship loop
            while True:
                tries+=1
                ba_t = allCoords(int(10*random.random()),int(10*random.random()),4,int(2*random.random())+2)
                try:
                    if not all([tempb[c[0]][c[1]]==0 and tempBoard[c[0]][c[1]]!=1 for c in ba_t]): continue
                except:
                    continue
                for x,y in ba_t: tempb[x][y]=1
                break
            #Cruiser loop
            while True:
                tries+=1
                cr_t = allCoords(int(10*random.random()),int(10*random.random()),3,int(2*random.random())+2)
                try:
                    if not all([tempb[c[0]][c[1]]==0 and tempBoard[c[0]][c[1]]!=1 for c in cr_t]): continue
                except:
                    continue
                for x,y in cr_t: tempb[x][y]=1
                break
            #Submarine loop
            while True:
                tries+=1
                su_t = allCoords(int(10*random.random()),int(10*random.random()),3,int(2*random.random())+2)
                try:
                    if not all([tempb[c[0]][c[1]]==0 and tempBoard[c[0]][c[1]]!=1 for c in su_t]): continue
                except:
                    continue
                for x,y in su_t: tempb[x][y]=1
                break
            #Destroyer loop
            while True:
                tries+=1
                de_t = allCoords(int(10*random.random()),int(10*random.random()),2,int(2*random.random())+2)
                try:
                    if not all([tempb[c[0]][c[1]]==0 and tempBoard[c[0]][c[1]]!=1 for c in de_t]): continue
                except:
                    continue
                for x,y in de_t: tempb[x][y]=1
                break
            if not all([tempb[x][y]==1 for x,y in hitSpots]): continue
            break
        for i,e in enumerate(freqBoard): freqBoard[i] = [x + y for x, y in zip(e, tempb[i])]
    q.put(freqBoard)
    print("Avg. per run: " + str(tries/n))
#    print('Process ID {} took = {} seconds'.format(tr, time() - st1))

    return

def npa(perc):
    pMax = max([x for x in perc for x in x])
    pMin = min([x for x in perc for x in x])
    bp = [[(y-pMin)/(pMax-pMin) for y in x] for x in perc]
    return np.array(bp)

def combineBoards(*args):
    retBoard = [[0 for _ in range(10)] for _ in range(10)]
    for a in range(10):
        for b in range(10):
            retBoard[a][b] = sum([x[a][b] for x in args])
    return retBoard

def renderMap(board):
    st = time()
    m = multiprocessing.Manager()
    q = m.Queue()
    pool = multiprocessing.Pool()
    print('Time taken = {} seconds'.format(time() - st))
    tr = range(10)
    pool.starmap(monteHunt, [(2000, board, i, q) for i in range(8)])
    print('Time taken = {} seconds'.format(time() - st))
    resultTen = q.get()
    pool.close()
    return npa(resultTen)
def inpt():
    ltn = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
    bbb = [[0 for _ in range(10)] for _ in range(10)]
    while True:
        inp = input("Input: ")
        if inp[0].upper() == "H": bbb[10-int(inp[2])][ltn[inp[1]]] = 2
        elif inp[0].upper() == "M": bbb[10-int(inp[2])][ltn[inp[1]]] = 1
        print(inp[0])
        ax.clear()
        print("f")
        ax.pcolormesh(renderMap(bbb), cmap="RdYlGn")
        print("g")
        plt.draw()
        print("h")


if __name__=="__main__":
    #board[7][8] = 2
    numpyTen = renderMap([[0 for _ in range(10)] for _ in range(10)])

    matplotlib.rcParams['toolbar'] = 'None'
    fig, ax = plt.subplots()

    #fig.canvas.mpl_connect('key_press_event', press)

    pcm = ax.pcolormesh(numpyTen,cmap = 'RdYlGn')
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    fig.tight_layout()
    fig.canvas.set_window_title('Probability heatmap')
    x = threading.Thread(target=inpt, args=())
    x.start()
    plt.show()