# main.py: Game selection menu
#2024 07 07 fdufnews
# moved menu management in a function in order to reuse it in submenu
# read/write settings from/to a configuration file.
#
#2024 07 08 fdufnews
# added change settings 

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
# BEWARE keep 'Settings' and 'Power off' at the end of the list

GAMELIST=['Tetris', 'Game Of Life', 'Game Of Life 2', 'Hungry Rain', 'Pico 2048', 'Settings', 'Power off']
SETTINGSLIST=['Sound off', 'Sound on', 'Backlight -',  'Backlight +', 'Cancel & Exit', 'Save & Exit']

def power_off():
    pgb.goto_sleep()

def manage_menu(menulist, background, default=0):
    nbItem = len(menulist)
    item_selected = None
    current = default

    try:
        pgb.load_image(background)
    except OSError:
        pgb.hcenter_text('Error in background filename',10, WHITE,)
        pgb.hcenter_text(background, 20, RED)
    pgb.rect(0,40,240,200,BACKGROUND,True)
    pgb.rect(23,45,196,180,SIDES1,False)
    pgb.rect(24,46,194,178,SIDES2,False)
    
    while pgb.any_button():
        time.sleep(0.1)

    while True:
        pgb.rect(25,47,192,176,BACKGROUND,True)
        for row in range(0, nbItem):
            if row == current:
                pgb.fill_rect(26, 48 + row*10, 191, 11, LIGHT_GREY)
                color = BLACK
            else:
                color = RED
            pgb.hcenter_text(menulist[row], 50 + row*10,color)
        pgb.show()
        if sound:
            time.sleep(0.05)
        else:
            time.sleep(0.15)
        buttonPressed = False
        while buttonPressed == False:
            if (pgb.button_down() or pgb.button_right()) and current < nbItem - 1:
                current += 1
                buttonPressed = True
            elif (pgb.button_up() or pgb.button_left()) and current > 0:
                current -= 1
                buttonPressed = True
            elif pgb.button_A() or pgb.button_B():
                buttonPressed = True
                item_selected = current

        # Make a sound
        if sound:
            pgb.sound(250)
            time.sleep(0.100)
            pgb.sound(0)
        if item_selected != None:
            break
    return item_selected

def change_conf():
    global settings, sound, backlight
    save_sound = sound
    save_backlight = backlight
    choice = 0
    change = False
    while choice != 4 and choice != 5:
        choice = manage_menu(SETTINGSLIST, 'bandeau_settings.bin', choice)
        if choice == 0:
            sound = False
        if choice == 1:
            sound = True
        if choice == 2:
            backlight = backlight - 10 if backlight>10 else 10
            pgb.backlight(backlight)
        if choice == 3:
            backlight = backlight + 10 if backlight<100 else 100
            pgb.backlight(backlight)
            change = True
        if choice == 4:
            sound = save_sound
            backlight = save_backlight
            pgb.backlight(backlight)
            change = False
        if choice == 5:
            settings['sound'] = sound
            settings['backlight'] = backlight
            change = True
    if change:
        pgb.set_settings_for('menu', settings,True)


#-----------------------------------------------
# Main loop
#-----------------------------------------------
game_selected = 0
settings = pgb.get_settings_for('menu')
sound = settings.get('sound',None)
backlight = settings.get('backlight',None)
background = settings.get('background', None)
saveSettings = False
if sound == None:
    sound = True
    settings['sound']=True
    saveSettings = True
if backlight == None:
    backlight = 50
    settings['backlight']=50
    saveSettings = True
if background == None:
    background = 'menu_cabin.bin'
    settings['background'] = 'menu_cabin.bin'
    saveSettings = True
if saveSettings :
    pgb.set_settings_for('menu', settings,True)

pgb.backlight(backlight)

while True:
    game_selected = manage_menu(GAMELIST, background)
    # Start the selected game
    if game_selected >= 0:
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
        elif game_selected==4:
            from Pico2048 import Pico2048
            game = Pico2048(pgb)
            game.begin()
        elif game_selected==len(GAMELIST)-2:
            change_conf()
        elif game_selected==len(GAMELIST)-1:
            power_off()
        # clears sprites created inside the application
        pgb.sprites_clear()
    game_selected=-1


