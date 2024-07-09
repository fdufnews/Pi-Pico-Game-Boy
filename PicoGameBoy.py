# PicoGameBoy.py by Vincent Mistler for YouMakeTech
# A class to easily write games for the Raspberry Pi Pico Game Boy

#
# 2024 06 26 fdufnews
# added support for other hardware by making an import of hardware conf
# added center_text returning the rect that embed displayed text
# added center text on a specified line
# added rotate screen
# added constraints on x and y value in test code
#
# 2024 07 05 fdufnews
# added sprites_clear()
#
# 2024 07 07 fdufnews
# added management of settings
# get_settings: read a configuration file
# get_settings_for, set_settings_for: get/set settings for a specified subset of the settings file


from machine import Pin, PWM, deepsleep
from framebuf import FrameBuffer, RGB565
from st7789 import ST7789
from time import sleep
#uncomment one of the following
#import PicoGameBoy_hardware as Hard
import gamePad_hardware as Hard
import json

class PicoGameBoy(ST7789):
    def __init__(self):
        self.__up = Pin(Hard.UP, Pin.IN, Pin.PULL_UP)
        self.__down = Pin(Hard.DOWN, Pin.IN, Pin.PULL_UP)
        self.__left = Pin(Hard.LEFT, Pin.IN, Pin.PULL_UP)
        self.__right = Pin(Hard.RIGHT, Pin.IN, Pin.PULL_UP)
        self.__button_A = Pin(Hard.A, Pin.IN, Pin.PULL_UP)
        self.__button_B = Pin(Hard.B, Pin.IN, Pin.PULL_UP)
        self.__buzzer = PWM(Pin(Hard.BUZZER))
        super().__init__(width=240, height=240, id_=Hard.ID, sck=Hard.SCK, mosi=Hard.MOSI,
                         dc=Hard.DC, rst=Hard.RST, cs=Hard.CS, bl=Hard.BKLIT, baudrate=Hard.BAUDRATE)

        self.rotate(Hard.ROTATE)
        self.__fb=[] # Array of FrameBuffer objects for sprites
        self.__w=[]
        self.__h=[]
        self._settings={}
        self.get_settings()

    # get_settings(file)
    # read the json file and populate the settings dictionnary
    # return True if successfull or false if file is missing
    def get_settings(self, filename='PicoGameBoy.json'):
        try:
            self.filename = filename
            file = open(filename, 'r')
        except OSError:
            print(filename, ' file is missing')
            self._settings = {}
            return False
        else:
            self._settings = json.load(file)
            file.close()
            return True

    # get_settings_for(key)
    # return the dictionnary associated with key
    # if key is missing in the dictionnary return an empty one
    def get_settings_for(self, key):
        return self._settings.get(key,{})

    # set_settings_for(key, setting, saveToFile)
    # update/create the dictionnary associated with key with setting
    # if saveToFile is True the settings file is updated
    def set_settings_for(self, key, setting, saveToFile):
        self._settings[key] = setting
        if saveToFile:
            file = open(self.filename, 'w')
            json.dump(self._settings, file)
            file.close()

    # center_text(s,color) displays a text in the middle of 
    # the screen with the specified color
    # return text frame position and size
    def center_text(self, s, color = 1):
        x = int(self.width/2)- int(len(s)/2 * 8)
        y = int(self.height/2) - 8
        self.text(s, x, y, color)
        return(x, y,len(s) * 8, 8)

    # hcenter_text(s,y, color) displays a text in the middle of 
    # a specified line with the specified color
    # return text frame position and size
    def hcenter_text(self, s, y, color = 1):
        x = int(self.width/2)- int(len(s)/2 * 8)
        self.text(s, x, y, color)
        return(x, y,len(s) * 8, 8)

    # top_right_corner_text(s,color) displays a text in the right corner of 
    # the screen with the specified color
    def top_right_corner_text(self, s, color = 1):
        x = self.width - int(len(s) * 8)
        y = 0
        self.text(s, x, y, color)

    # add_sprite(buffer,w,h) creates a new sprite from framebuffer
    # with a width of w and a height of h
    # The first sprite is #0 and can be displayed by sprite(0,x,y)
    def add_sprite(self, buffer, w, h):
        fb = FrameBuffer(buffer, w, h, RGB565)
        self.__fb.append(fb)
        self.__w.append(w)
        self.__h.append(h)

    # add_rect_sprite(color,w,h) creates a new rectangular sprite
    # with the specified color, width and height
    def add_rect_sprite(self, color, w, h):
        buffer = bytearray(w * h * 2) # 2 bytes per pixel
        # fill the buffer with the specified color
        lsb = (color & 0b0000000011111111)
        msb = (color & 0b1111111100000000) >> 8
        for i in range(0,w*h*2,2):
            buffer[i] = lsb
            buffer[i+1] = msb
        fb = FrameBuffer(buffer, w, h, RGB565)
        self.__fb.append(fb)
        self.__w.append(w)
        self.__h.append(h)

    # sprite(n,x,y) displays the nth sprite at coordinates (x,y)
    # the sprite must be created first by method add_sprite
    def sprite(self, n, x, y):
        self.blit(self.__fb[n], x, y)

    # sprite_width(n) returns the width of the nth sprite in pixels
    def sprite_width(self,n):
        return self.__w[n]

    # sprite_height(n) returns the height of the nth sprite in pixels
    def sprite_height(self,n):
        return self.__h[n]

    # clear all sprites
    def sprites_clear(self):
        self.__fb.clear() # Array of FrameBuffer objects for sprites
        self.__w.clear()
        self.__h.clear()

    # button_up() returns True when the player presses the up button
    def button_up(self):
        return self.__up.value()==0

    # button_down() returns True when the player presses the down button
    def button_down(self):
        return self.__down.value()==0

    # button_left() returns True when the player presses the left button
    def button_left(self):
        return self.__left.value()==0

    # button_right() returns True when the player presses the right button
    def button_right(self):
        return self.__right.value()==0

    # button_A() returns True when the player presses the A button
    def button_A(self):
        return self.__button_A.value()==0

    # button_B() returns True when the player presses the B button
    def button_B(self):
        return self.__button_B.value()==0

    # any_button() returns True if any button is pressed
    def any_button(self):
        button_pressed=False
        if self.button_up():
            button_pressed = True
        if self.button_down():
            button_pressed = True
        if self.button_left():
            button_pressed = True
        if self.button_right():
            button_pressed = True
        if self.button_A():
            button_pressed = True
        if self.button_B():
            button_pressed = True
        return button_pressed

    # sound(freq) makes a sound at the selected frequency in Hz
    # call sound(0) to stop playing the sound
    def sound(self, freq, duty_u16 = 2000):
        if freq>0:
            self.__buzzer.freq(freq)
            self.__buzzer.duty_u16(duty_u16)
        else:
            self.__buzzer.duty_u16(0)

    def goto_sleep(self):
        pass

if __name__ == "__main__":
    pgb=PicoGameBoy()

    # Colors (RGB)
    # Note that color is a static method and can be called
    # without creating an object (PicoGameBoy.color instead of pgb.color)
    BLACK=PicoGameBoy.color(0,0,0)
    WHITE=PicoGameBoy.color(255,255,255)
    RED=PicoGameBoy.color(255,0,0)
    GREEN=PicoGameBoy.color(0,255,0)
    BLUE=PicoGameBoy.color(0,0,255)

    # PicoGameBoy inherits all methods from the FrameBuffer class
    # see https://docs.micropython.org/en/latest/library/framebuf.html

    pgb.fill(BLACK)

    # The Raspberry Pi Pico GameBoy uses a framebuffer
    # The framebuffer is only transfered to the actual screen and become visible
    # when calling show()
    pgb.show()

    # Drawing primitive shapes
    # The screen resolution is 240x240 pixels but Python like many programming 
    # languages starts counting from zero, not one.
    # The top left corner is (0,0) and bottom right is (239,239)
    pgb.pixel(0,0,WHITE)
    pgb.pixel(239,239,BLUE)
    pgb.show()
    sleep(1)

    pgb.line(0,239,239,0,RED)
    pgb.show()

    pgb.rect(10,10,220,220,WHITE)
    pgb.show()
    sleep(1)

    pgb.fill_rect(10,10,220,220,WHITE)
    pgb.show()
    sleep(1)

    # text
    pgb.fill(BLACK)
    pgb.text('Hello from Pi Pico GameBoy!',0,0,GREEN)
    pgb.show()
    sleep(1)

    pgb.center_text('GAME OVER',WHITE)
    pgb.show()
    sleep(1)

    # sprites
    x = 120
    y = 120
    pgb.fill(BLACK)
    pgb.add_rect_sprite(GREEN,12,12) # Create sprite #0
    while True:
        pgb.sprite(0,x,y)
        pgb.show()
        while not pgb.any_button():
            sleep(0.020)
        if pgb.button_right():
            x=x+1
        elif pgb.button_left():
            x=x-1
        elif pgb.button_up():
            y=y-1
        elif pgb.button_down():
            y=y+1
        if x<0 :
            x = 0
        if x>239-12:
            x = 239-12
        if y<0 :
            y = 0
        if y>239-12:
            y = 239-12

