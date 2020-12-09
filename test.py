from __future__ import print_function
import sys
from time import sleep
import threading
import colorama
import random
from colorama import Style, Cursor
colorama.init()

pos = lambda y, x: Cursor.POS(x, y)

def writingThread():
    while True:
        sleep(1)
        sys.stdout.write(pos(random.randint(0,9),1))
        sys.stdout.flush()
sys.stdout.write("aaaaaaaaaa\n"*10)
wt = threading.Thread(target=writingThread)
wt.start()
input(">")