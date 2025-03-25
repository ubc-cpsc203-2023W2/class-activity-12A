import numpy as np
from collections import deque
import pygame
import math
import sys
import copy

# How many states to use?
# Note that current code supports only 4 or 9 (see exampleBoard).
STATES = 4

def exampleBoard(size):
    sud = np.full(size, 0)
    if(size == (4,4)):
        sud[0, 0] = 1 # position 1
        sud[3, 1] = 2 # position 8
        sud[1, 3] = 3 # position 14
        sud[2, 3] = 4 # position 15

    elif(size == (9,9)):
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
        
    else:
        # We do not have an example initialization for this size.
        assert False
        
    return sud

# this function changes a position into and x,y location
def postup(p): # board is 0 indexed.
    return p % STATES, p // STATES

# this function should check that the position is on the board
# and that it doesn't violate the rules of the game.
def valid(board, position, num):
    if position >= STATES * STATES: #off the board
        return False

    x, y = postup(position)
    if num in board[x, :]:
        return False
    elif num in board[:, y]:
        return False
    elif num in board[boxesDim * (x // boxesDim):   boxesDim * (x // boxesDim) + boxesDim,
                boxesDim * (y // boxesDim):boxesDim * (y // boxesDim) + boxesDim]:
        return False
    else:
        return True

def sudokuSolver(board):
    s = deque()
    position = 0
    s.append((copy.deepcopy(board), position))

    # We will also keep a list of all the states that we visit in the order that we
    # visited them.  It provides both a record of how we searched the graph 
    # (in other words, our search tree) and we can make a pretty movie from it
    # using PyGame.  (The algorithm would still find the solution without keeping this tree.)
    search_tree = []

    while s and position < STATES * STATES:
        g, position = s.pop()
        x, y = postup(position)
        search_tree.append((copy.deepcopy(g), position))

        # we need to skip over given filled cells!
        while position < STATES*STATES and not g[x, y] == 0:
            position += 1
            x, y = postup(position)
        # position is the next place to fill

        for num in range(1, STATES+1):
            if valid(g, position, num): # on board and follows rules
                g[x, y] = num
                s.append((copy.deepcopy(g), position+1))
                search_tree.append((copy.deepcopy(g), position+1))
    return search_tree

def drawBlock(x, y, state, acolor):
    colour_box = pygame.Rect([pad + (pad + sqSize) * x + (x//boxesDim)*pad,
                                      pad + (pad + sqSize) * y+ (y//boxesDim)*pad,
                                      sqSize, sqSize])
    pygame.draw.rect(screen, acolor, colour_box)
    
    # Draw number on blocks
    if state == 0:
        text_state = ''
    else:
        text_state = str(state)
    
    text = font.render(text_state, True, white, black)
    textRect = text.get_rect()
    text.set_alpha(150)

    # set the center of the rectangular object.
    textRect.center = colour_box.center
    
    # Draw text
    screen.blit(text,textRect)

def draw(gr):
    cols = gr[0].shape[0]
    rows = gr[0].shape[1]
    for x in range(cols):
        for y in range(rows):
            state = gr[0][x][y]
            state_color = pygame.Color(0, 0, 0)
            state_color.hsva = [(360 // STATES) * state, 100, 50]
            if state == 0:
                state_color = pygame.Color(0, 0, 0)
            drawBlock(x, y, state, state_color)


# given
def handleInputEvents():
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close...
            sys.exit(0)  # quit

board = exampleBoard((STATES, STATES))
boxesDim = int(math.sqrt(STATES))
search_tree = sudokuSolver(board)
print(search_tree)
print(len(search_tree))

# drawing parameters that determine the look of the board when it's shown.
# These can be set, but defaults are probably fine
sqSize = 40  # size of the squares in pixels
pad = sqSize // 5  # the number of pixels between each square

# computed from parameters above and board dimensions
s = (STATES * sqSize + (STATES + 1) * pad + (boxesDim - 1)*pad,
     STATES * sqSize + (STATES + 1) * pad + (boxesDim - 1)*pad)  # dimensions of pixels in window
screen = pygame.display.set_mode(s)  # initializes the display window
screen.fill((0,0,0))

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# words to display on the window
pygame.display.set_caption("CPSC203 Sudoku")

# -------- Main Program Loop -----------

# Initialize pygame and fonts
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 24)
white = (255, 255, 255)
black = (0, 0, 0)
frame = 0

while True:
    # --- Main event loop
    handleInputEvents()

    # --- Draw the board
    # this function loops over the data in the board object
    # and draws appropriately colored rectangles.
    if frame in range(len(search_tree)):
        draw(search_tree[frame])
    else:
        draw(search_tree[-1])

    frame += 1

    # --- Mysterious reorientation that every pygame application seems to employ
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(2)
    #clock.tick(160)

# Close the window and quit.
pygame.quit()
