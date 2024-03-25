import numpy as np
from collections import deque
import copy

sud = np.full((4,4),0)
sud[0,0] = 3
sud[3,1] = 2
sud[1,3] = 1
sud[2,3] = 4

def postup(p):

    # use clever math to change a position number into x,y coordinates
    return 

def valid(grid,position,num):

    # check to see if position is on the board...

    x,y = postup(position)
    if num in # your code here, check a row
        return False
    elif num in # your code here, check a column
        return False
    elif num in  # your code here, check a box
        return False
    else:
        return True


def itSolver(grid):

    # initialize a deque to use as a stack
    # initialize a position and its x,y rep

    # place initial grid and position in stack (use a copy of the grid!!

    # while there is something in the stack and the position < 16

        #pop a grid and position and set the x,y

        # advance over filled locations, if necessary


        print("________________________")
        print(position)
        print("________________________")
        print(g)
        print()

        # try out all the possible neighbors and for each...
            # if the neighbor is valid, set the grid position
            # put a copy of the grid and its position on the stack


itSolver(sud)

