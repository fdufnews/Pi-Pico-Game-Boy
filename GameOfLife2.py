# GameOfLife.py by Matthieu Mistler
# John Conway's Game of Life for the Raspberry Pi Pico Game Boy

# 2024 06 26 fdufnews
# added cell age to the rules
# cell's age is displayed as a color
#
# 2024-07-4 fdufnews
# turned program into a class in order to call it from a menu
# added population count, title screen, game over screen
# added A and B key management to reinitialize or exit game
# made functions to clear and populate board

from PicoGameBoy import PicoGameBoy
import random
from time import sleep

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

BACKGROUND_COLOR = 0
UNPOPULATED = 0
NEW_BORN = 1


BLACK = PicoGameBoy.color(0,0,0)
WHITE = PicoGameBoy.color(255,255,255)
GREEN = PicoGameBoy.color(0,255,0)
RED = PicoGameBoy.color(255,0,0)
BLUE = PicoGameBoy.color(0,0,255)
GREY = PicoGameBoy.color(127,127,127)
DARK_GREY = PicoGameBoy.color(63,63,63)

class GameOfLife2():
    def __init__(self, pgb):
        self._pgb = pgb
        self.board=[]

        # Game parameters
        WIDTH = self._pgb.width        # screen width in pixels
        HEIGHT = self._pgb.height      # screen height in pixels
        self.CELL_SIZE = 8            # width and height of cells in pixels
        # Board initialisation
        self.BOARD_SIZE_X = int(WIDTH/self.CELL_SIZE)
        self.BOARD_SIZE_Y = int(HEIGHT/self.CELL_SIZE)
        BOARD_SURFACE = self.BOARD_SIZE_X * self.BOARD_SIZE_Y
        POPULATION_PERCENT = 12  # Initial population size as function of total surface in %
        # Initial number of cells
        self.NUMBER_OF_CELLS = int((POPULATION_PERCENT)/100 * BOARD_SURFACE);

        for i in range(0,self.BOARD_SIZE_Y):
            line = []
            for j in range(0,self.BOARD_SIZE_X):
                line.append(0)
            self.board.append(line)

    # clear the board
    def clear_board(self):
        for i in range(self.BOARD_SIZE_Y):
            for j in range(self.BOARD_SIZE_X):
                self.board[i][j] = UNPOPULATED

    # Create the initial population
    def populate_board(self):
        for i in range(0,self.NUMBER_OF_CELLS):
            # Randomly place cells on the board
            self.board[random.randint(0,self.BOARD_SIZE_Y-1)][random.randint(0,self.BOARD_SIZE_X-1)] = NEW_BORN

    def title_screen(self):
        self._pgb.fill(BACKGROUND_COLOR)
        x,y,lx,ly = self._pgb.center_text('Game Of Life', WHITE)
        self._pgb.show()
        sleep(2)
        self._pgb.text('A to reset board', x- lx//4, y+16, GREEN)
        self._pgb.text('B to quit', x- lx//4, y+28, GREEN)
        self._pgb.show()
        sleep(3)

    def game_over(self):
        x,y,lx,ly = self._pgb.center_text('All cells are dead', WHITE)
        self._pgb.text('Reset population', x+8, y+16, GREEN)
        self._pgb.show()
        sleep(2)

    def begin(self):
        self.title_screen()
        self.clear_board()
        self.populate_board()
        pop = 1
        # run the animation
        while True:
            # Test A key if pressed Reset or population == 0
            if self._pgb.button_A() or pop==0:
                if pop==0:
                    self.game_over()
                self.clear_board()
                self.populate_board()
            # Test B key if pressed Quit
            if self._pgb.button_B():
                break

            # Update the screen
            self._pgb.fill(BACKGROUND_COLOR)
            for i in range(0,self.BOARD_SIZE_Y):
                for j in range(0,self.BOARD_SIZE_X):
                    if self.board[i][j]!=0:
                        self._pgb.fill_rect(j*self.CELL_SIZE,i*self.CELL_SIZE,self.CELL_SIZE,self.CELL_SIZE,colors[self.board[i][j]])
            self._pgb.show()
            # count number of neighbors for each position
            pop = 0
            for i in range(0,self.BOARD_SIZE_Y):
                for j in range(0,self.BOARD_SIZE_X):
                    pop += 1 if self.board[i][j]!=0 else 0
                    number_neighbors = 0

                    if i>1 and j>1 and self.board[i-1][j-1]!=0:
                        number_neighbors+=1
                    if i>1 and self.board[i-1][j]!=0:
                        number_neighbors+=1
                    if i>1 and j<self.BOARD_SIZE_X-1 and self.board[i-1][j+1]!=0:
                        number_neighbors+=1
                    if i<self.BOARD_SIZE_Y-1 and j>1 and self.board[i+1][j-1]!=0:
                        number_neighbors+=1
                    if i<self.BOARD_SIZE_Y-1 and self.board[i+1][j]!=0:
                        number_neighbors+=1
                    if i<self.BOARD_SIZE_Y-1 and j<self.BOARD_SIZE_Y-1 and self.board[i+1][j+1]!=0:
                        number_neighbors+=1
                    if j>1 and self.board[i][j-1]!=0:
                        number_neighbors+=1
                    if j<self.BOARD_SIZE_X-1 and self.board[i][j+1]!=0:
                        number_neighbors+=1

                    # The game's rules
                    if self.board[i][j]!=0:
                        # There is a living cell at row #i col #j
                        # It survives only if it surrounded by 2 or 3 neighbors
                        if number_neighbors<2 or number_neighbors>3:
                            self.board[i][j] = 0
                        else:
                            self.board[i][j]+=1
                            if self.board[i][j]>15:
                                self.board[i][j]=0
                    else:
                        # row #i col #j is empty
                        # Create a new cell at (i,j) if it is surrounded by exactly 3 neighbors
                        if number_neighbors == 3 :
                            self.board[i][j] = NEW_BORN

if __name__ == "__main__":
    from PicoGameBoy import PicoGameBoy
    pgb=PicoGameBoy()
    from GameOfLife2 import GameOfLife2
    game = GameOfLife2(pgb)
    game.begin()

