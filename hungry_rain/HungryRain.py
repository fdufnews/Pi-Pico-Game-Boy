# Hungry_Rain.py by K.G. Orphanides, version 1.5
# A tiny survival game for the Raspberry Pi Pico Game Boy
# Find food. Hide from the flood.
#
# 2024-07-5 fdufnews
# turn program into a class in order to call it from a menu
# create functions with basic bricks: title screen, gameover screen, init game, ....
# add possibility to restart game or leave after gameover
# is_shelted_by() function to test if dot is under a shelter

from PicoGameBoy import PicoGameBoy
import time
from random import randint, choice
import machine


#sprites
apple_green_bg_14x15=bytearray(b'\x06 \x06 \x06 \x06 \x06 \xb3\xc8\xb3\xc8\x06 \x06 \x06 \x06 \x06 \x06 \x06 \x06 \x06 \x06 \x06 \x06 \xb3\xc8\xb3\xc8\x8cjL\xc9\x14G\x06 \x06 \x06 \x06 \x06 \x06 \x06 \x06 \x06 \x06 \x9c\x07\x14\x85\x1c\x88\x1c\x88\x06 \x06 \x06 \x06 \x06 \x06 \xec\xab\xec\xab\xec\xab\x06 \x84H\x1c\xa7\xa4j\xac\xcb\xec\xab\xec\xab\x06 \x06 \x06 \xeci\xeb\xa5\xebc\xeb\xc6\xecI\xec\x8a\xec\x8a\xecI\xeb\xe6\xebc\xeb\xa5\xeci\x06 \xeci\xebc\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebc\xeci\xeb\xe6\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebC\xf3\xa4\xf3\xa4\xeb\x83\xebB\xeb\xc6\xebc\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebc\xf3\xa4\xf3\xa4\xf3\xa4\xebB\xebc\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xf3\x84\xf3\xa4\xf3\xa4\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebc\xebC\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x06 \xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x06 \x06 \xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x06 \x06 \x06 \xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x06 \x06 \x06 \x06 \x06 \xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x06 \x06 \x06 ')
apple_blue_bg_14x15=bytearray(b'\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\xb3\xc8\xb3\xc8\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\xb3\xc8\xb3\xc8\x8cjL\xc9\x14G\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x9c\x07\x14\x85\x1c\x88\x1c\x88\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\xec\xab\xec\xab\xec\xab\x00\x1b\x84H\x1c\xa7\xa4j\xac\xcb\xec\xab\xec\xab\x00\x1b\x00\x1b\x00\x1b\xeci\xeb\xa5\xebc\xeb\xc6\xecI\xec\x8a\xec\x8a\xecI\xeb\xe6\xebc\xeb\xa5\xeci\x00\x1b\xeci\xebc\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebc\xeci\xeb\xe6\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebC\xf3\xa4\xf3\xa4\xeb\x83\xebB\xeb\xc6\xebc\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebc\xf3\xa4\xf3\xa4\xf3\xa4\xebB\xebc\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xf3\x84\xf3\xa4\xf3\xa4\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebc\xebC\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x1b\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x1b\x00\x1b\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x1b\x00\x1b\x00\x1b\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x1b\x00\x1b\x00\x1b')
dot_14x14=bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x95)\x959\x94QtatqtyS\x81S\x893\x912\x99\x12\xa1\x11\x00\x00\x00\x00)\x95A\x94YtatqtyS\x81S\x912\x912\x99\x12\xa1\x11\xa8\xf1\x00\x00\x00\x00A\x94YtitqsyS\x81S\x912\x992\x99\x12\xa1\x11\xa8\xf1\xb0\xd1\x00\x00\x00\x00YtitqSyS\x81S\x912\x992\xa1\x12\xa1\x11\xa8\xf1\xb0\xd1\xb8\xd0\x00\x00\x00\x00itqs\x81S\x81S\x912\x992\xa1\x12\xa9\x11\xa8\xf1\xb0\xf0\xb8\xd0\xc0\xb0\x00\x00\x00\x00qsyS\x89S\x912\x992\xa1\x12\xa1\x11\xa8\xf1\xb0\xd0\xb8\xd0\xc0\xb0\xc0\x8f\x00\x00\x00\x00\x81S\x89S\x912\x99\x12\xa1\x12\xa9\x11\xa8\xf1\xb0\xd0\xb8\xb0\xc0\xb0\xc0\x8f\xc8o\x00\x00\x00\x00\x89S\x912\x992\xa1\x12\xa9\x11\xa8\xf1\xb0\xd0\xb8\xb0\xc0\xb0\xc0\x8f\xc8o\xd0N\x00\x00\x00\x00\x912\x992\xa1\x11\xa8\xf1\xa8\xf1\xb0\xd0\xb8\xd0\xc0\xaf\xc8\x8f\xc8O\xd0N\xd0\x0e\x00\x00\x00\x00\x99\x12\xa1\x12\xa8\xf1\xb0\xf1\xb8\xd0\xb8\xd0\xc0\xaf\xc8\x8f\xc8o\xd0.\xd0\x0e\xd8\r\x00\x00\x00\x00\xa1\x11\xa8\xf1\xb0\xf1\xb8\xd0\xb8\xb0\xc0\xaf\xc8\x8f\xc8o\xd0.\xd8\r\xd8\r\xd8\r\x00\x00\x00\x00\xa9\x11\xb0\xf1\xb8\xd0\xb8\xb0\xc0\x8f\xc8\x8f\xc8N\xd0.\xd8\r\xd8\r\xd8\r\xd8\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
apple_black_bg_14x15=bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb3\xc8\xb3\xc8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb3\xc8\xb3\xc8\x8cjL\xc9\x14G\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9c\x07\x14\x85\x1c\x88\x1c\x88\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xec\xab\xec\xab\xec\xab\x00\x00\x84H\x1c\xa7\xa4j\xac\xcb\xec\xab\xec\xab\x00\x00\x00\x00\x00\x00\xeci\xeb\xa5\xebc\xeb\xc6\xecI\xec\x8a\xec\x8a\xecI\xeb\xe6\xebc\xeb\xa5\xeci\x00\x00\xeci\xebc\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebc\xeci\xeb\xe6\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebC\xf3\xa4\xf3\xa4\xeb\x83\xebB\xeb\xc6\xebc\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebc\xf3\xa4\xf3\xa4\xf3\xa4\xebB\xebc\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xf3\x84\xf3\xa4\xf3\xa4\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebc\xebC\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x00\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x00\x00\x00\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x00\x00\x00\x00\x00\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x00\x00\x00\x00\x00')
shelter_stone_30x5=bytearray(b'k\xcfk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xcfk\xcfk\xefc.c.c.c.c.k\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xefk\xcfk\xcfk\xefc.c.c.k\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfc.c.c.k\xcfk\xefk\xcfk\xcfk\xefk\xcfk\xcfc.k\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfc.k\xcfk\xefk\xcfk\xcfk\xefk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xefk\xcf')

# define some colors
BACKGROUND_COLOR = PicoGameBoy.color(0,197,0)
WHITE = PicoGameBoy.color(255,255,255)
BLACK = PicoGameBoy.color(0,0,0)
BOX_COLOR = WHITE
FLOOD_COLOR = PicoGameBoy.color(0,0,220)
SHELTER_COLOR = BLACK

#what does dot look like?
DOT_WIDTH = 14
DOT_HEIGHT = 14
#define food
FOOD_WIDTH = 14
FOOD_HEIGHT = 15
#define shelter
SHELTER_WIDTH = 30  #width
SHELTER_HEIGHT = 5   #height
NUMBER_OF_SHELTER = 3

class HungryRain():
    def __init__(self,pgb):

        self._pgb = pgb
        self._pgb.add_sprite(apple_green_bg_14x15,14,15) # sprite 0
        self._pgb.add_sprite(apple_blue_bg_14x15,14,15) # sprite 1
        self._pgb.add_sprite(dot_14x14,14,14) # sprite 2
        self._pgb.add_sprite(apple_black_bg_14x15,14,15) # sprite 3
        self._pgb.add_sprite(shelter_stone_30x5,30,5) # sprite 4

    def init_game(self):
        #define dot's starting x and y cordinates
        self.x = 113
        self.y = 113
        #save last position for collisions
        self.last_x = 113
        self.last_y = 113

        self.food_available = False

        #initialise hunger timer and food meter
        self.reference_time = time.ticks_ms()
        self.food = 100

        #initialise flood
        self.antediluvian_time = time.ticks_ms()
        self.flood = False
        self.flood_y = 3
        self.flood_delay = 15000
        self.flood_duration = 10000

        self.shelters = [[0 for col in range(3)] for row in range(NUMBER_OF_SHELTER)]
        for i in range(NUMBER_OF_SHELTER):
            self.shelters[i][0] = choice([i for i in range(10,210) if i not in (self.x - SHELTER_WIDTH - 1, self.x + DOT_WIDTH + 1)]) #excluding positions that collide with dot
            self.shelters[i][1] = y = choice([i for i in range(10,240-DOT_HEIGHT-SHELTER_HEIGHT-1) if i not in (self.y - SHELTER_HEIGHT -1, self.y + DOT_HEIGHT+1)])
            self.shelters[i][2] = 233 - y

        self.run_game = True
        self.gameover = False

    # collision detection function - feed it the x, y, width and height of dot and the x, y, width and height of the thing to check collision against
    def collision(self,x1,y1,w1,h1,x2,y2,w2,h2):
        if x1+w1 < x2:
            return False
        if x2+w2 < x1:
            return False
        if y1+h1 < y2:
            return False
        if y2+h2 < y1:
            return False
        else:
            return True

    # test if dot is shelted by some object same arguments as collision
    def is_shelted_by(self,x1,y1,w1,h1,x2,y2,w2,h2,s):
        if y1 > y2:
            s |= {i for i in range(x2, x2+w2)}
        return s

    #instructions
    def intro(self):
        self._pgb.fill(BACKGROUND_COLOR)
        self._pgb.text("HUNGRY RAIN",80,25,WHITE)
        self._pgb.text("You are dot.",20,40,WHITE)
        self._pgb.sprite(2,20,50)
        self._pgb.text("Find food.",20,70,WHITE)
        self._pgb.sprite(3,20,80)
        self._pgb.text("Hide from the flood.",20,100,WHITE)
        self._pgb.fill_rect(20,110,12,12,FLOOD_COLOR)
        self._pgb.text("Shelter beneath the stones.",20,128,WHITE)
        self._pgb.sprite(4,20,140)
        self._pgb.text("Press any key to start",38,180,WHITE)
        self._pgb.show()
        while self._pgb.any_button()==False:
            pass
        if self._pgb.button_A() or self._pgb.button_B():
            antediluvian_time = time.ticks_ms() #so intro doesn't result in shorter flood delay on first round

    def game_over(self):
        time.sleep_ms(100) # let them see how they died
        self._pgb.fill_rect(10,40,220,100,BLACK)
        self._pgb.hcenter_text("GAME OVER",65,WHITE)
        self._pgb.hcenter_text("Press A to restart",90,WHITE)
        self._pgb.hcenter_text("Press B to quit",110,WHITE)
        self._pgb.show()
        if self._pgb.button_A():
            self.init_game()
        if self._pgb.button_B():
            self.run_game = False

    def begin(self):
        self.intro()
        self.init_game()
        # game loop
        while self.run_game:

            #gameover screen
            if self.gameover==True:
                self.game_over()
            elif self.gameover is not True:
                #run the hunger timer
                if time.ticks_ms() > self.reference_time + 1000:
                    self.reference_time = time.ticks_ms()
                    self.food = self.food - 1

                #run the flood timers
                if time.ticks_ms() > self.antediluvian_time + self.flood_delay:
                    self.flood = True

                if time.ticks_ms() > self.antediluvian_time + self.flood_delay + self.flood_duration:
                    self.flood = False
                    self.antediluvian_time = time.ticks_ms()

                #draw the game scene:
                #the background
                if self.flood:
                    self._pgb.fill(FLOOD_COLOR)
                else:
                    self._pgb.fill(BACKGROUND_COLOR)

                #the box
                self._pgb.rect(1, 1, 238, 238, BOX_COLOR)

                #shelters' protective shadows in a flood
                for i in range(NUMBER_OF_SHELTER):
                    self._pgb.fill_rect(self.shelters[i][0], self.shelters[i][1] + 5, SHELTER_WIDTH, self.shelters[i][2], BACKGROUND_COLOR)

                #the shelters
                for i in range(NUMBER_OF_SHELTER):
                    self._pgb.sprite(4, self.shelters[i][0], self.shelters[i][1])

                #draw dot
                self._pgb.sprite(2, self.x, self.y)

                #move dot
                if self._pgb.button_left():
                    self.last_x = self.x            #record last known position in case we need to call it upon hitting a solid object
                    self.x = self.x - 1
                if self._pgb.button_right():
                    self.last_x = self.x
                    self.x = self.x + 1
                if self._pgb.button_up():
                    self.last_y = self.y
                    self.y = self.y - 1
                if self._pgb.button_down():
                    self.last_y = self.y
                    self.y = self.y + 1

                #you're not allowed past the walls
                if self.x < 3:
                    self.x = self.last_x
                if self.x > 224:
                    self.x = self.last_x
                if self.y < 3:
                    self.y = self.last_y
                if self.y > 224:
                    self.y = self.last_y

                #check for collisions with shelters
                for i in range(NUMBER_OF_SHELTER):
                    if self.collision(self.x, self.y,DOT_WIDTH, DOT_HEIGHT, self.shelters[i][0], self.shelters[i][1], SHELTER_WIDTH, SHELTER_HEIGHT):
                        self.x = self.last_x
                        self.y = self.last_y

                # water is deadly
                if self.flood:
                    self.gameover = True
                    s=set()
                    for i in range(NUMBER_OF_SHELTER):
                        s = self.is_shelted_by(self.x, self.y,DOT_WIDTH, DOT_HEIGHT, self.shelters[i][0], self.shelters[i][1], SHELTER_WIDTH, SHELTER_HEIGHT, s)
                    self.gameover = not({i for i in range(self.x, self.x+DOT_WIDTH)} <= s)


                #food! (generate random position for food)
                if self.food_available==False:
                    foodSpawn_x = randint(15,215)
                    foodSpawn_y = randint(15,215)
                    self.food_available = True

                if self.food_available==True and self.flood==False:
                    self._pgb.sprite(0,foodSpawn_x,foodSpawn_y)

                elif self.food_available==True and self.flood==True:
                    #make sure we have the right background colour
                    for i in range(NUMBER_OF_SHELTER):
                        if self.collision(foodSpawn_x, foodSpawn_y, FOOD_WIDTH, FOOD_HEIGHT, self.shelters[i][0],self.shelters[i][1], SHELTER_WIDTH, self.shelters[i][2]):
                            self._pgb.sprite(0,foodSpawn_x,foodSpawn_y)
                        else:
                            self._pgb.sprite(1,foodSpawn_x,foodSpawn_y)

                #dot eats food
                if self.collision(self.x, self.y, DOT_WIDTH,DOT_HEIGHT, foodSpawn_x, foodSpawn_y, FOOD_WIDTH,FOOD_HEIGHT):
                    self._pgb.fill_rect(foodSpawn_x, foodSpawn_y, FOOD_WIDTH, FOOD_HEIGHT, BACKGROUND_COLOR)
                    self.food = self.food + 10 #get less hungry
                    self.food_available = False

                #die of starvation
                if self.food==0:
                    self.gameover = True

                #hunger
                self._pgb.text("Food:"+ str(self.food),170,5)

                #debug tools
                #self._pgb.text("position:"+ str(x) + "," + str(y),5,15)

                #flood countdown
                if self.flood:
                    self._pgb.text("Flood count: NOW",5,5)

                else:
                    flood_countdown = time.ticks_diff(self.antediluvian_time + self.flood_delay, time.ticks_ms())
                    self._pgb.text("Flood count:"+ str(round(flood_countdown/1000,1)),5,5)

                #transfer all this from the framebuffer to the screen
                self._pgb.show()

if __name__ == "__main__":
    from PicoGameBoy import PicoGameBoy
    pgb=PicoGameBoy()
    from HungryRain import HungryRain
    game = HungryRain(pgb)
    game.begin()

# Credits
# Apple and stone images modified from Kenney Game Assets (https://kenney.itch.io/)
# Pico Game Boy libraries by Vincent Mistler of YouMakeTech
# AABB collision detection code adapted from a function by Matthieu Mistler

# License
# The MIT License (MIT)
# Copyright (c) 2013-2017 Damien P. George, and others
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

