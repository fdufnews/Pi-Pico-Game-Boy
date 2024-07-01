# GameOfLife.py by Matthieu Mistler
# John Conway's Game of Life for the Raspberry Pi Pico Game Boy

# 2024 06 26 fdufnews
# added cell age to the rules
# cell's age is displayed as a color

from PicoGameBoy import PicoGameBoy
import random
from time import sleep
pgb = PicoGameBoy()

# Predefined colors
BLACK = PicoGameBoy.color(0,0,0)
WHITE = PicoGameBoy.color(255,255,255)
RED = PicoGameBoy.color(255,0,0)
GREEN = PicoGameBoy.color(0,255,0)
BLUE = PicoGameBoy.color(0,0,255)

colors = [PicoGameBoy.color(0,0,0),
PicoGameBoy.color(0,63,0),
PicoGameBoy.color(0,127,0),
PicoGameBoy.color(0,191,0),
PicoGameBoy.color(127,191,15),
PicoGameBoy.color(160,191,63),
PicoGameBoy.color(191,160,15),
PicoGameBoy.color(191,63,0),
PicoGameBoy.color(127,63,48),
PicoGameBoy.color(127,63,127),
PicoGameBoy.color(127,48,191),
PicoGameBoy.color(63,63,191),
PicoGameBoy.color(31,63,255),
PicoGameBoy.color(0,63,127),
PicoGameBoy.color(0,31,127),
PicoGameBoy.color(0,15,63)
]
MASK_R = 0xF800
MASK_G = 0x07F0
MASK_B = 0x001F

# Game parameters
WIDTH = pgb.width        # screen width in pixels
HEIGHT = pgb.height      # screen height in pixels
CELL_SIZE = 8            # width and height of cells in pixels
POPULATION_PERCENT = 12  # Initial population size as function of total surface in %
BACKGROUND_COLOR = 0
UNPOPULATED = 0
NEW_BORN = 1

# Board initialisation
BOARD_SIZE_X = int(WIDTH/CELL_SIZE)
BOARD_SIZE_Y = int(HEIGHT/CELL_SIZE)
BOARD_SURFACE = BOARD_SIZE_X * BOARD_SIZE_Y

BLACK = PicoGameBoy.color(0,0,0)
WHITE = PicoGameBoy.color(255,255,255)
GREEN = PicoGameBoy.color(0,255,0)
RED = PicoGameBoy.color(255,0,0)
BLUE = PicoGameBoy.color(0,0,255)
GREY = PicoGameBoy.color(127,127,127)
DARK_GREY = PicoGameBoy.color(63,63,63)

board=[]
for i in range(0,BOARD_SIZE_Y):
    line = []
    for j in range(0,BOARD_SIZE_X):
        line.append(0)
    board.append(line)

# Initial number of cells 
NUMBER_OF_CELLS = int((POPULATION_PERCENT)/100 * BOARD_SURFACE);

# clear the board
def clear_board():
    global board
    for i in range(BOARD_SIZE_Y):
        for j in range(BOARD_SIZE_X):
            board[i][j] = UNPOPULATED


# Create the initial population
def populate_board():
    global board
    for i in range(0,NUMBER_OF_CELLS):
        # Randomly place cells on the board
        board[random.randint(0,BOARD_SIZE_Y-1)][random.randint(0,BOARD_SIZE_X-1)] = NEW_BORN

clear_board()
populate_board()

x,y,lx,ly = pgb.center_text('Game Of Life', WHITE)
pgb.show()
sleep(2)
pgb.text('A or B to reset board', x- lx//4, y+16, GREEN)
pgb.show()
sleep(3)

# run the animation
while True:
    # Test A key if pressed Reset
    if pgb.button_A() or pgb.button_B():
        clear_board()
        populate_board()

    # Update the screen
    pgb.fill(BACKGROUND_COLOR)
    for i in range(0,BOARD_SIZE_Y):
        for j in range(0,BOARD_SIZE_X):
            if board[i][j]!=0:
                pgb.fill_rect(j*CELL_SIZE,i*CELL_SIZE,CELL_SIZE,CELL_SIZE,colors[board[i][j]])
    pgb.show()
#    while True:
#        pass
    # count number of neighbors for each position
    for i in range(0,BOARD_SIZE_Y):
        for j in range(0,BOARD_SIZE_X):
            number_neighbors = 0
            
            if i>1 and j>1 and board[i-1][j-1]!=0:
                number_neighbors+=1
            if i>1 and board[i-1][j]!=0:
                number_neighbors+=1
            if i>1 and j<BOARD_SIZE_X-1 and board[i-1][j+1]!=0:
                number_neighbors+=1
            if i<BOARD_SIZE_Y-1 and j>1 and board[i+1][j-1]!=0:
                number_neighbors+=1
            if i<BOARD_SIZE_Y-1 and board[i+1][j]!=0:
                number_neighbors+=1
            if i<BOARD_SIZE_Y-1 and j<BOARD_SIZE_Y-1 and board[i+1][j+1]!=0:
                number_neighbors+=1
            if j>1 and board[i][j-1]!=0:
                number_neighbors+=1
            if j<BOARD_SIZE_X-1 and board[i][j+1]!=0:
                number_neighbors+=1
            
            # The game's rules
            if board[i][j]!=0:
                # There is a living cell at row #i col #j
                # It survives only if it surrounded by 2 or 3 neighbors
                if number_neighbors<2 or number_neighbors>3:
                    board[i][j] = 0
                else:
                    board[i][j]+=1
                    if board[i][j]>15:
                        board[i][j]=0
            else:
                # row #i col #j is empty
                # Create a new cell at (i,j) if it is surrounded by exactly 3 neighbors
                if number_neighbors == 3 :
                    board[i][j] = NEW_BORN
