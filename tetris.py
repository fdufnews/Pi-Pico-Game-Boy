# tetris.py by Vincent Mistler for YouMakeTech
# Tetris game for the Raspberry Pi Pico Game Boy

# fdufnews 2024 06 26
# modified title_screen so it is more reactive and text flashes slowly
# some cosmetic changes to game_over_screen
# corrected last_button="LEFT" in game loop
# added a test in test of keypress to suppress unwanted double clicks

from PicoGameBoy import PicoGameBoy
from micropython import const
import time
from random import randint

BLOCK_SIZE = const(12) # Size of a single tetromino block in pixels
GRID_OFFSET = const(2)
GRID_ROWS  = const(20)
GRID_COLS  = const(10)


# image definitions 12x12 pixels
tetris_wall=bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf7\x9e\xf7\x9e\xf7\x9emX\x00\x00\x00\x00\xf7\x9e\xf7\x9e\xf7\x9emX\x00\x00\x00\x00\xf7\x9e\xf7\x9e\xf7\x9emX\x00\x00\x00\x00\xf7\x9e\xf7\x9e\xf7\x9emX\x00\x00\x00\x00mXmXmX3\x91\x00\x00\x00\x00mXmXmX3\x91\x00\x00\x00\x00mX3\x913\x913\x91\x00\x00\x00\x00mX3\x913\x913\x91\x00\x00\x00\x00mX3\x913\x913\x91\x00\x00\x00\x00mX3\x913\x913\x91\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00mX\x00\x00\x00\x00\xf7\x9e\xf7\x9e\xf7\x9emX\x00\x00\x00\x00\xf7\x9e\xf7\x9e\xf7\x9emX\x00\x00\x00\x00\xf7\x9e\xf7\x9e\xf7\x9emX\x00\x00\x00\x00\xf7\x9e\xf7\x9e\xf7\x9e3\x91\x00\x00\x00\x00mXmXmX3\x91\x00\x00\x00\x00mXmXmX3\x91\x00\x00\x00\x00mX3\x913\x913\x91\x00\x00\x00\x00mX3\x913\x913\x91\x00\x00\x00\x00mX3\x913\x913\x91\x00\x00\x00\x00mX3\x913\x91')
bottom_border=bytearray(b'\xeeP\xf6\x90\xf6\x90\xf6\x90\xf6\x90\xf6\x90\xf6\x90\xf6\x90\xf6\x90\xf6\x90\xf6\x90\xeeP\xf6p\xfe\xb1\xfe\xb1\xfe\xb1\xfe\xb1\xfe\xb1\xfe\xb1\xfe\xb1\xfe\xb1\xfe\xb1\xfe\xb1\xf6p\xdd\x0f\xe5P\xe5P\xe5P\xe5P\xe5P\xe5P\xe5P\xe5P\xe5P\xe5P\xdd\x0fI\x84I\x84I\x84I\x84I\x84I\x84I\x84I\x84I\x84I\x84I\x84I\x84@\xc3H\xc4H\xc4H\xc4H\xc4H\xc4H\xc4H\xc4H\xc4H\xc4H\xc4@\xc3\xd3\r\xdb.\xdb.\xdb.\xdb.\xdb.\xdb.\xdb.\xdb.\xdb.\xdb.\xd3\r\xe4\xef\xed0\xed0\xed0\xed0\xed0\xed0\xed0\xed0\xed0\xed0\xe4\xef\xe5P\xf5p\xf5p\xf5p\xf5p\xf5p\xf5p\xf5p\xf5p\xf5p\xf5p\xe5P\xf6p\xfe\xb1\xfe\xb1\xfe\xb1\xfe\xb1\xfe\xb1\xfe\xb1\xfe\xb1\xfe\xb1\xfe\xb1\xfe\xb1\xf6p\xe5P\xf5p\xf5p\xf5p\xf5p\xf5p\xf5p\xf5p\xf5p\xf5p\xf5p\xe5P\xdc\xef\xe5\x0f\xe5\x0f\xe5\x0f\xe5\x0f\xe5\x0f\xe5\x0f\xe5\x0f\xe5\x0f\xe5\x0f\xe5\x0f\xdc\xefI\x84I\xa4I\xa4I\xa4I\xa4I\xa4I\xa4I\xa4I\xa4I\xa4I\xa4I\x84')
corner=bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00mX\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffmX\x00\x00\x00\x00mXmX\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffmXmX\x00\x00\x00\x00mXmXmX\xff\xff\xff\xff\xff\xff\xff\xffmXmXmX\x00\x00\x00\x00mXmXmXmX\xff\xff\xff\xffmXmXmXmX\x00\x00\x00\x00mXmXmXmX3\x913\x91mXmXmXmX\x00\x00\x00\x00mXmXmX3\x913\x913\x913\x91mXmXmX\x00\x00\x00\x00mXmX3\x913\x913\x913\x913\x913\x91mXmX\x00\x00\x00\x00mX3\x913\x913\x913\x913\x913\x913\x913\x91mX\x00\x00\x00\x003\x913\x913\x913\x913\x913\x913\x913\x913\x913\x91\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
left_border=bytearray(b'\x00\x00\xe3\x0e\xe3\x0e\xedP\xe3\x0e\xe3\x0e\xe3\x0e\x00\x00\x00\x00\xedP\xedP\xedP\x00\x00\xedP\xedP\xfe\xd1\xedP\xedP\xe3\x0e\x00\x00\x00\x00\xedP\xfe\xd1\xfe\xd1\x00\x00\xedP\xedP\xfe\xd1\xedP\xedP\xe3\x0e\x00\x00\x00\x00\xedP\xfe\xd1\xfe\xd1\x00\x00\xedP\xedP\xfe\xd1\xedP\xedP\xe3\x0e\x00\x00\x00\x00\xedP\xfe\xd1\xfe\xd1\x00\x00\xe3\x0e\xe3\x0e\xedP\xe3\x0e\xe3\x0e\x00\x00\x00\x00\x00\x00\xedP\xfe\xd1\xfe\xd1\x00\x00\xe3\x0e\xe3\x0e\xedP\xe3\x0e\xe3\x0e\x00\x00\x00\x00\x00\x00\xedP\xfe\xd1\xfe\xd1\x00\x00\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xedP\x00\x00\x00\x00\xedP\xfe\xd1\xfe\xd1\x00\x00\xedP\xedP\xfe\xd1\xedP\xedP\xe3\x0e\x00\x00\x00\x00\xedP\xfe\xd1\xfe\xd1\x00\x00\xedP\xedP\xfe\xd1\xedP\xedP\xe3\x0e\x00\x00\x00\x00\xedP\xfe\xd1\xfe\xd1\x00\x00\xe3\x0e\xe3\x0e\xedP\xe3\x0e\xe3\x0e\x00\x00\x00\x00\x00\x00\xedP\xfe\xd1\xfe\xd1\x00\x00\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xedP\x00\x00\x00\x00\xedP\xfe\xd1\xfe\xd1\x00\x00\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xedP\x00\x00\x00\x00\xedP\xfe\xd1\xfe\xd1')
right_border=bytearray(b'\xedP\xedP\xedP\x00\x00\x00\x00\xe3\x0e\xe3\x0e\xe3\x0e\xedP\xe3\x0e\xe3\x0e\x00\x00\xfe\xd1\xfe\xd1\xedP\x00\x00\x00\x00\xe3\x0e\xedP\xedP\xfe\xd1\xedP\xedP\x00\x00\xfe\xd1\xfe\xd1\xedP\x00\x00\x00\x00\xe3\x0e\xedP\xedP\xfe\xd1\xedP\xedP\x00\x00\xfe\xd1\xfe\xd1\xedP\x00\x00\x00\x00\xe3\x0e\xedP\xedP\xfe\xd1\xedP\xedP\x00\x00\xfe\xd1\xfe\xd1\xedP\x00\x00\x00\x00\x00\x00\xe3\x0e\xe3\x0e\xedP\xe3\x0e\xe3\x0e\x00\x00\xfe\xd1\xfe\xd1\xedP\x00\x00\x00\x00\x00\x00\xe3\x0e\xe3\x0e\xedP\xe3\x0e\xe3\x0e\x00\x00\xfe\xd1\xfe\xd1\xedP\x00\x00\x00\x00\xedP\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\x00\x00\xfe\xd1\xfe\xd1\xedP\x00\x00\x00\x00\xe3\x0e\xedP\xedP\xfe\xd1\xedP\xedP\x00\x00\xfe\xd1\xfe\xd1\xedP\x00\x00\x00\x00\xe3\x0e\xedP\xedP\xfe\xd1\xedP\xedP\x00\x00\xfe\xd1\xfe\xd1\xedP\x00\x00\x00\x00\x00\x00\xe3\x0e\xe3\x0e\xedP\xe3\x0e\xe3\x0e\x00\x00\xfe\xd1\xfe\xd1\xedP\x00\x00\x00\x00\xedP\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\x00\x00\xfe\xd1\xfe\xd1\xedP\x00\x00\x00\x00\xedP\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\x00\x00')
top_border=bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xe3\x0e\xe3\x0e\xe3\x0e\xe3\x0e\xe3\x0e\xe3\x0e\xe3\x0e\xe3\x0e\xe3\x0e\xe3\x0e\xe3\x0e\xe3\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xedP\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1\xfe\xd1')



# shape of the 7 tetrominos
# [0][1]
# [2][3]
# [4][5]
# [6][7]
# e.g. [3,4,5,7] is:
#    [ ]
# [ ][ ]
#    [ ]
tetrominos = [[1,3,5,7],
              [2,4,5,7],
              [3,5,4,6],
              [3,5,4,7],
              [2,3,5,7],
              [3,5,7,6],
              [2,3,4,5]]

# Game Boy Color Tetrominos colors
# Color scheme
BLACK = PicoGameBoy.color(0,0,0)
WHITE = PicoGameBoy.color(255,255,255)
GREY = PicoGameBoy.color(127,127,127)
DARK_GREY = PicoGameBoy.color(63,63,63)
GRID_BACKGROUND_COLOR = PicoGameBoy.color(255,211,132)
BACKGROUND_COLOR = PicoGameBoy.color(99,154,132)
BACKGROUND_COLOR2 = PicoGameBoy.color(57,89,41)
TEXT_COLOR = BLACK
TEXT_BACKGROUND_COLOR = WHITE

class tetris():

    def __init__(self, pgb):
        self._pgb = pgb
        self._pgb.add_sprite(tetris_wall,12,12) #0
        self._pgb.add_sprite(bottom_border,12,12) #1
        self._pgb.add_sprite(corner,12,12) #2
        self._pgb.add_sprite(left_border,12,12) #3
        self._pgb.add_sprite(right_border,12,12) #4
        self._pgb.add_sprite(top_border,12,12) #5
        self._lines = 0
        self._level = 0
        self._score = 0
        self._last_button="NONE"
        self._has_rotated=False
        self._now = time.ticks_ms()
        self._n = randint(0, 6)
        self._next_n = randint(0, 6)
        self._x=[0,0,0,0]
        self._y=[0,0,0,0]
        self._prev_x=[0,0,0,0]
        self._prev_y=[0,0,0,0]
        self._field = [[-1 for col in range(GRID_COLS)] for row in range(GRID_ROWS)]
        self._tetrominos_colors =[PicoGameBoy.color(239,146,132),
                     PicoGameBoy.color(222,146,239),
                     PicoGameBoy.color(239,170,132),
                     PicoGameBoy.color(165,211,132),
                     PicoGameBoy.color(99,219,222),
                     PicoGameBoy.color(231,97,115),
                     PicoGameBoy.color(0,0,0)]

        for i in range(0,4):
            self._x[i]=(tetrominos[self._n][i]) % 2;
            self._y[i]=int(tetrominos[self._n][i] / 2);

            self._x[i]+=int(GRID_COLS/2)

    def collision(self, x, y):
        for i in range(4):
            # check collision against the border
            if self._x[i]<0 or self._x[i]>=GRID_COLS or self._y[i]>=GRID_ROWS:
                return True
            # check collision against another triomino
            if self._field[self._y[i]][self._x[i]]>=0:
                return True

        return False

    def title_screen(self):
        # title screen
        txtstate = True
        self._now = time.ticks_ms()
        self._pgb.load_image("tetris_title.bin")
        self._pgb.show()
        color = self._pgb.pixel(120,120)
        while self._pgb.any_button()==False:
            if time.ticks_diff(time.ticks_ms(), self._now) > 500:
                self._now = time.ticks_ms()
                if txtstate:
                    x,y,lx,ly= self._pgb.center_text("PRESS ANY BUTTON",WHITE)
                else:
                    self._pgb.rect(x, y, lx, ly, color, True)
                self._pgb.show()
                txtstate = not txtstate

    def game_over_screen(self):
        x = 45
        y = 90
        lx = 150
        ly = 60
        self._pgb.fill_rect(x,y,lx,ly,DARK_GREY)
        self._pgb.rect(x,y,lx,ly,GREY)
        self._pgb.rect(x+1,y+1,lx-2,ly-2,WHITE)
        self._pgb.rect(x+2,y+2,lx-4,ly-4,GREY)
        x,y,lx,ly= self._pgb.center_text("GAME OVER",WHITE)
        self._pgb.show()
        if self._pgb.any_button():
            while self._pgb.any_button():
                time.sleep(0.200)
        self._pgb.hcenter_text("PRESS ANY BUTTON",y + 10, WHITE)
        self._pgb.show()
        while not self._pgb.any_button():
            time.sleep(0.200)

    def draw_background(self):
        self._pgb.fill(BACKGROUND_COLOR)

        for i in range(0,int(240/BLOCK_SIZE),2):
            for j in range(0,int(240/BLOCK_SIZE),2):
                self._pgb.fill_rect(j*BLOCK_SIZE,i*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE,BACKGROUND_COLOR2)
                self._pgb.fill_rect((j+1)*BLOCK_SIZE,(i+1)*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE,BACKGROUND_COLOR2)

        self._pgb.fill_rect(GRID_OFFSET*BLOCK_SIZE,0,
                      GRID_COLS*BLOCK_SIZE,GRID_ROWS*BLOCK_SIZE,
                      GRID_BACKGROUND_COLOR)

        # add walls
        for i in range(GRID_ROWS):
            self._pgb.sprite(0,(GRID_OFFSET-1)*BLOCK_SIZE,i*BLOCK_SIZE)
            self._pgb.sprite(0,(GRID_OFFSET+GRID_COLS)*BLOCK_SIZE,i*BLOCK_SIZE)

        # draw text (LINES)
        self._pgb.fill_rect((GRID_OFFSET+GRID_COLS+1)*BLOCK_SIZE+1,16*BLOCK_SIZE,
                      BLOCK_SIZE*7,BLOCK_SIZE*2,
                      TEXT_BACKGROUND_COLOR)
        self._pgb.text("LINES",(GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE+1,16*BLOCK_SIZE+1,TEXT_COLOR)
        self._pgb.text("%8s" % self._lines,(GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE+1,17*BLOCK_SIZE+1,TEXT_COLOR)

        # draw text (LEVEL)
        self._pgb.fill_rect((GRID_OFFSET+GRID_COLS+1)*BLOCK_SIZE+1,13*BLOCK_SIZE,
                      BLOCK_SIZE*7,BLOCK_SIZE*2,
                      TEXT_BACKGROUND_COLOR)
        self._pgb.text("LEVEL",(GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE+1,13*BLOCK_SIZE+1,TEXT_COLOR)
        self._pgb.text("%8s" % self._level,(GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE+1,14*BLOCK_SIZE+1,TEXT_COLOR)

        # draw text (SCORE)
        self._pgb.fill_rect((GRID_OFFSET+GRID_COLS+1)*BLOCK_SIZE+1,10*BLOCK_SIZE,
                      BLOCK_SIZE*7,BLOCK_SIZE*2,
                      TEXT_BACKGROUND_COLOR)
        self._pgb.text("SCORE",(GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE+1,10*BLOCK_SIZE+1,TEXT_COLOR)
        self._pgb.text("%8s" % self._score,(GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE+1,11*BLOCK_SIZE+1,TEXT_COLOR)

        # next tetromino box
        self._pgb.fill_rect((GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE,2*BLOCK_SIZE,
                      BLOCK_SIZE*6 ,BLOCK_SIZE*7,TEXT_BACKGROUND_COLOR)

        self._pgb.sprite(2,(GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE,2*BLOCK_SIZE) #upper left corner
        self._pgb.sprite(5,(GRID_OFFSET+GRID_COLS+3)*BLOCK_SIZE,2*BLOCK_SIZE) #top border
        self._pgb.sprite(5,(GRID_OFFSET+GRID_COLS+4)*BLOCK_SIZE,2*BLOCK_SIZE) #
        self._pgb.sprite(5,(GRID_OFFSET+GRID_COLS+5)*BLOCK_SIZE,2*BLOCK_SIZE) #
        self._pgb.sprite(5,(GRID_OFFSET+GRID_COLS+6)*BLOCK_SIZE,2*BLOCK_SIZE) #
        self._pgb.sprite(2,(GRID_OFFSET+GRID_COLS+7)*BLOCK_SIZE,2*BLOCK_SIZE) #upper right corner

        self._pgb.sprite(2,(GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE,8*BLOCK_SIZE) #lower left corner
        self._pgb.sprite(1,(GRID_OFFSET+GRID_COLS+3)*BLOCK_SIZE,8*BLOCK_SIZE) #lower border
        self._pgb.sprite(1,(GRID_OFFSET+GRID_COLS+4)*BLOCK_SIZE,8*BLOCK_SIZE) #
        self._pgb.sprite(1,(GRID_OFFSET+GRID_COLS+5)*BLOCK_SIZE,8*BLOCK_SIZE) #
        self._pgb.sprite(1,(GRID_OFFSET+GRID_COLS+6)*BLOCK_SIZE,8*BLOCK_SIZE) #
        self._pgb.sprite(2,(GRID_OFFSET+GRID_COLS+7)*BLOCK_SIZE,8*BLOCK_SIZE) #lower right corner

        for k in range(3,8):
            self._pgb.sprite(3,(GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE,k*BLOCK_SIZE) #left border
            self._pgb.sprite(4,(GRID_OFFSET+GRID_COLS+7)*BLOCK_SIZE,k*BLOCK_SIZE) #right border

        for i in range(4):
            self.draw_block((GRID_OFFSET+GRID_COLS+2)+tetrominos[self._next_n][i] % 2,
                       3+int(tetrominos[self._next_n][i] / 2), self._next_n)

    def draw_block(self, j,i,n):
        # draw a tetris block of type n at the ith row and jth column
        # of the grid

        x = (GRID_OFFSET+j)*BLOCK_SIZE
        y = i*BLOCK_SIZE

        self._pgb.fill_rect(x,y,BLOCK_SIZE,BLOCK_SIZE,self._tetrominos_colors[n]) # main color
        self._pgb.rect(x,y,BLOCK_SIZE,BLOCK_SIZE,BLACK) # black border
        self._pgb.line(x+3,y+3,x+5,y+3,WHITE)
        self._pgb.line(x+3,y+3,x+3,y+5,WHITE)

    #####################################################################
    def begin(self):
        # show title screen and wait for a button
        self.title_screen()
        loop = True
        # game loop
        while loop:
            dx=0
            dy=1
            rotate=False
            delay=500

            if self._pgb.button_A() or self._pgb.button_B():
                if self._last_button!="UP":
                    rotate=True
                self._last_button="UP"
            elif self._pgb.button_left():
                if self._last_button!="LEFT":
                    self._last_button="LEFT"
                    dx=-1
                else:
                    self._last_button="NONE"
            elif self._pgb.button_right():
                if self._last_button!="RIGHT":
                    self._last_button="RIGHT"
                    dx=1
                else:
                    self._last_button="NONE"
            elif self._pgb.button_down():
                self._last_button="DOWN"
                delay=0
            else:
                self._last_button="NONE"

            # save current position to restore it
            # in case the requested move generates a collision
            for i in range(4):
                self._prev_x[i] = self._x[i]
                self._prev_y[i] = self._y[i]

            # move left & right
            for i in range(4):
                self._x[i]+=dx

            if self.collision(self._x, self._y):
                # collision detected => impossible move
                # => restore previous position
                for i in range(4):
                    self._x[i] = self._prev_x[i]
                    self._y[i] = self._prev_y[i]

            # rotate
            if rotate:
                # center of rotation
                x0 = self._x[1]
                y0 = self._y[1]
                for i in range(4):
                    x_=self._y[i]-y0
                    y_=self._x[i]-x0
                    self._x[i]=x0-x_
                    self._y[i]=y0+y_

                if self.collision(self._x, self._y):
                    # collision detected => impossible move
                    # => restore previous position
                    for i in range(4):
                        self._x[i] = self._prev_x[i]
                        self._y[i] = self._prev_y[i]
                else:
                    self._has_rotated=True

            # move down
            ticks_ms = time.ticks_ms()
            if time.ticks_diff(ticks_ms, self._now) > delay:
                print(str(time.ticks_diff(ticks_ms, self._now)))
                self._now = ticks_ms

                if self._has_rotated:
                    freq=180
                elif delay>0:
                    freq=140
                else:
                    freq=0
                self._pgb.sound(freq)
                self._has_rotated = False

                for i in range(4):
                    self._prev_x[i]=self._x[i]
                    self._prev_y[i]=self._y[i]
                    self._y[i]+=dy

                if self.collision(self._x,self._y):
                    # collision detected

                    # collision at the top of the screen?
                    # => game over
                    for i in range(4):
                        if self._prev_y[i]<=1:
                            self._pgb.sound(0)
                            self.game_over_screen()
                            loop = False
                            break

                    # => Store the last good position in the field
                    for i in range(4):
                        self._field[self._prev_y[i]][self._prev_x[i]]=self._n

                    # => choose randomly the next trinomino
                    self._n = self._next_n
                    self._next_n = randint(0, 6)
                    for i in range(4):
                        self._x[i]=(tetrominos[self._n][i]) % 2;
                        self._y[i]=int(tetrominos[self._n][i] / 2);

                        self._x[i]+=int(GRID_COLS/2)
            if not loop:
                break
            # check lines
            k=GRID_ROWS-1
            for i in range(GRID_ROWS-1,0,-1):
                count=0
                for j in range(GRID_COLS):
                    if self._field[i][j]>=0:
                        count+=1
                    self._field[k][j]=self._field[i][j]
                if count<GRID_COLS:
                    k-=1
                else:
                    # ith line complete
                    self._lines+=1
                    self._score+=40

                    # make the line blink white <-> black

                    for l in range(3):
                        self._pgb.sound(1100)
                        self._pgb.fill_rect(GRID_OFFSET*BLOCK_SIZE,i*BLOCK_SIZE,
                                      GRID_COLS*BLOCK_SIZE,BLOCK_SIZE,WHITE)
                        self._pgb.show()
                        time.sleep(0.050)
                        self._pgb.sound(2000)
                        self._pgb.fill_rect(GRID_OFFSET*BLOCK_SIZE,i*BLOCK_SIZE,
                                      GRID_COLS*BLOCK_SIZE,BLOCK_SIZE,BLACK)
                        self._pgb.show()
                        time.sleep(0.050)
                    self._pgb.sound(0)

            #####################################################################
            # update screen 

            # background
            self.draw_background()

            # draw all the previous blocks
            for i in range(GRID_ROWS):
                for j in range(GRID_COLS):
                    if self._field[i][j]>=0:
                        # non empty
                        self.draw_block(j,i,self._field[i][j])

            # draw the current block
            for i in range(4):
                self.draw_block(self._x[i],self._y[i],self._n)

            # transfer the frame buffer to the actual screen over the SPI bus
            self._pgb.show()

            self._pgb.sound(0)

if __name__ == "__main__":
    from PicoGameBoy import PicoGameBoy
    pgb=PicoGameBoy()
    from tetris import tetris
    game = tetris(pgb)
    game.begin()

