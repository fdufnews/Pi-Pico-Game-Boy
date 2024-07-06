# main.py: Game selection menu by Vincent Mistler (YouMakeTech)
from machine import Pin, PWM, I2C, Timer
from PicoGameBoy import PicoGameBoy
import time
import random

BLACK = PicoGameBoy.color(0,0,0)
WHITE = PicoGameBoy.color(255,255,255)
LIGHT_GREY = PicoGameBoy.color(192,192,192)
RED = PicoGameBoy.color(255,0,0)
GREEN = PicoGameBoy.color(0,255,0)
BLUE = PicoGameBoy.color(0,0,255)
BACKGROUND = PicoGameBoy.color(0x09,0x6E,0x5F)
SIDES1 = PicoGameBoy.color(0x07,0x5E,0x4F)
SIDES2 = PicoGameBoy.color(0x06,0x4E,0x3F)


pgb = PicoGameBoy()

#if __name__ == "__main__":
# To avoid strange errors at startup
# I don't know why but it works!
time.sleep(0.2)


# list of games
GAMELIST=["Tetris","Game Of Life","Game Of Life 2","Hungry Rain", "Power off"]

current = 0
game_selected = -1

def power_off():
    pgb.goto_sleep()

draw_background = True

while True:
    if draw_background:
        pgb.load_image('menu_freckle.bin')
        pgb.rect(23,45,196,180,SIDES1,False)
        pgb.rect(24,46,194,178,SIDES2,False)
        draw_background = False
    pgb.rect(25,47,192,176,BACKGROUND,True)
    #pgb.hcenter_text("Pico GameBoy",0, GREEN)
    for row in range(0, len(GAMELIST)):
        if row == current:
            pgb.fill_rect(26, 48 + row*10, 191, 11, LIGHT_GREY)
            color = BLACK
        else:
            color = RED

        pgb.hcenter_text(GAMELIST[row], 50 + row*10,color)

    pgb.show()

    time.sleep(0.2)

    buttonPressed = False

    while buttonPressed == False:
        if (pgb.button_down() or pgb.button_right()) and current < len(GAMELIST) - 1:
            current += 1
            buttonPressed = True
        elif (pgb.button_up() or pgb.button_left()) and current > 0:
            current -= 1
            buttonPressed = True
        elif pgb.button_A() or pgb.button_B():
            buttonPressed = True
            game_selected = current

    # Make a sound
    pgb.sound(250)
    time.sleep(0.100)
    pgb.sound(0)

    # Start the selected game
    if game_selected >= 0:
        pgb.fill(0)
        pgb.show()
        # clears sprites created inside menu
        pgb.sprites_clear()

        if game_selected==0:
            from tetris import tetris
            game = tetris(pgb)
            game.begin()
        elif game_selected==1:
            from GameOfLife import GameOfLife
            game = GameOfLife(pgb)
            game.begin()
        elif game_selected==2:
            from GameOfLife2 import GameOfLife2
            game = GameOfLife2(pgb)
            game.begin()
        elif game_selected==3:
            from HungryRain import HungryRain
            game = HungryRain(pgb)
            game.begin()
        elif game_selected==len(GAMELIST)-1:
            power_off()
        # clears sprites created inside the application
        pgb.sprites_clear()
        draw_background = True
    game_selected=-1


