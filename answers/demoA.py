import numpy as np
from collections import deque
import pygame
from typing import Tuple
import math
import sys
import copy

class board:
    gridSize: Tuple[int, int]  # columns, rows == x,y
    data: np.ndarray
    generations: int

    def __init__(self, size, setup):
        self.gridSize = size
        self.data = setup(size)
        self.generations = 0


def initStart(size):
    sud = np.full(size, 0)
    sud[0, 0] = 1 # position 1
    sud[3, 1] = 2 # position 8
    sud[1, 3] = 3 # position 14
    sud[2, 3] = 4 # position 15
    return sud

def initBIG(size):
    sud = np.full(size, 0)
    sud[1, 0] = 6
    sud[4, 0] = 7
    sud[7, 0] = 8
    sud[6, 1] = 3
    sud[4, 2] = 6
    sud[5, 2] = 3
    sud[7, 2] = 9

    sud[2, 3] = 9
    sud[3, 3] = 2
    sud[4, 4] = 4
    sud[1, 5] = 2
    sud[3, 5] = 1
    sud[6, 5] = 8

    sud[1, 6] = 1
    sud[2, 6] = 6
    sud[5, 6] = 9
    sud[7, 6] = 7
    sud[8, 6] = 3
    sud[1, 7] = 7
    sud[5, 7] = 8
    sud[6, 7] = 2
    sud[7, 7] = 4
    sud[2, 8] = 4

    return sud

# this function changes a position into and x,y location
def postup(p): # grid is 0 indexed.
    return p % states, p // states

# this function should check that the position is on the grid
# and that it doesn't violate the rules of the game.
def valid(grid, position, num):
    if position >= states * states: #off the board
        return False

    x, y = postup(position)
    if num in grid[x, :]:
        return False
    elif num in grid[:, y]:
        return False
    elif num in grid[boxesDim * (x // boxesDim):   boxesDim * (x // boxesDim) + boxesDim,
                boxesDim * (y // boxesDim):boxesDim * (y // boxesDim) + boxesDim]:
        return False
    else:
        return True

def itSolver(grid):
    s = deque()
    position = 0

    movie = []
    s.append((copy.deepcopy(grid), position))

    while s and position < states * states:
        g, position = s.pop()
        x, y = postup(position)
        movie.append((copy.deepcopy(g), position))

        # we need to skip over given filled cells!
        while position < states*states and not g[x, y] == 0:
            position += 1
            x, y = postup(position)
        # position is the next place to fill


        for num in range(1, states+1):
            if valid(g, position, num): # on grid and follows rules
                g[x, y] = num
                s.append((copy.deepcopy(g), position+1))
                movie.append((copy.deepcopy(g), position+1))
    return movie

def draw_block(x, y, acolor):
    pygame.draw.rect(screen, acolor, [pad + (pad + sqSize) * x + (x//boxesDim)*pad,
                                      pad + (pad + sqSize) * y+ (y//boxesDim)*pad,
                                      sqSize, sqSize])


def draw(gr):
    cols = gr[0].shape[0]
    rows = gr[0].shape[1]
    for x in range(cols):
        for y in range(rows):
            state = gr[0][x][y]
            state_color = pygame.Color(0, 0, 0)
            state_color.hsva = [(360 // states) * state, 100, 50]
            if state == 0:
                state_color = pygame.Color(0, 0, 0)
            draw_block(x, y, state_color)


# given
def handleInputEvents():
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close...
            sys.exit(0)  # quit

states = 9
boxesDim = int(math.sqrt(states))

g = board((states, states), initBIG)
#g = board((states, states), initStart)
movie = itSolver(g.data)
print(movie)
print(len(movie))

# drawing parameters that determine the look of the grid when it's shown.
# These can be set, but defaults are probably fine
sqSize = 40  # size of the squares in pixels
pad = sqSize // 5  # the number of pixels between each square

# computed from parameters above and grid dimensions
s = (g.gridSize[0] * sqSize + (g.gridSize[0] + 1) * pad + (boxesDim - 1)*pad,
     g.gridSize[1] * sqSize + (g.gridSize[1] + 1) * pad + (boxesDim - 1)*pad)  # dimensions of pixels in window
screen = pygame.display.set_mode(s)  # initializes the display window
screen.fill((0,0,0))

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# words to display on the window
pygame.display.set_caption("CPSC203 Sudoku")

i = 0
# -------- Main Program Loop -----------
while True:
    # --- Main event loop
    handleInputEvents()

    # --- Draw the grid
    # this function loops over the data in the grid object
    # and draws appropriately colored rectangles.
    if i in range(len(movie)):
        draw(movie[i])
    else:
        draw(movie[-1])

    i += 1

    # --- Mysterious reorientation that every pygame application seems to employ
    pygame.display.flip()

    # --- Limit to 60 frames per second
    #clock.tick(2)
    clock.tick(160)

# Close the window and quit.
pygame.quit()
