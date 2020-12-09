from sys import stdout

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random
#import cProfile
#import re
from time import time
import multiprocessing

def press(event):
    if event.key == 'x'

if __name__=="__main__":
    matplotlib.rcParams['toolbar'] = 'None'
    fig, ax = plt.subplots()

    fig.canvas.mpl_connect('key_press_event', press)
    rarr = np.random.rand(10,10)
    ax.pcolormesh(rarr,cmap = 'RdYlGn')
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    fig.tight_layout()
    fig.canvas.set_window_title('Probability heatmap')
    plt.show()