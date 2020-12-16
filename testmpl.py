from sys import stdout

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
import random
#import cProfile
#import re
from time import time
import multiprocessing

if __name__=="__main__":
    matplotlib.rcParams['toolbar'] = 'None'
    fig, ax = plt.subplots()

    rarr = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    cmcol = colors.ListedColormap(["Blue", "Red", "Yellow"])
    ax.pcolormesh(rarr,cmap = cmcol, edgecolors="k",linewidths=1)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    fig.tight_layout()
    fig.canvas.set_window_title('Probability heatmap')
    plt.show()