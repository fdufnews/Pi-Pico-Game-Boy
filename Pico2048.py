# Pico2048.py migrated by Kobi Tyrkel
# A simple 2048 game migrated 
# for the Rapsberry Pi Pico RetroGaming Console
#
# 2024 07 09 fdufnews
# converted to a class to call it from a global menu
# put sprites in files instead of including them in a .py to save space in memory
#
# 2024 07 10 fdufnews
# added score


from PicoGameBoy import PicoGameBoy
from P2048.Logic import Logic
from P2048.Resources import Resources
import time

X_OFFSET = 20
Y_OFFSET = 20
CELL_WIDTH = 50
CELL_HEIGHT = 50

WHITE = PicoGameBoy.color(0xFF, 0xFF, 0xFF)
BLACK = PicoGameBoy.color(0x0, 0x0, 0x0)
RED = PicoGameBoy.color(0xFF, 0x0, 0x0)
GREEN = PicoGameBoy.color(0x0, 0x0, 0xFF)
EMPTY_CELL = PicoGameBoy.color(0x9F, 0x9F, 0x9F)

class Pico2048:

    def __init__(self, pgb):
    
        self._pgb = pgb
        self._l = Logic()
        
        self.sprites = []
        self.sprites.append(pgb.add_rect_sprite(EMPTY_CELL, 40, 16)) # sprite 0
        a=[]
        for i in range(1,12):
            a.append(bytearray([0] * 40 * 16 * 2))
            filename = 'P2048/'+ str(1 << i) + '.bin'
            file = open(filename,'rb')
            file.readinto(a[i-1])
            self.sprites.append(pgb.add_sprite(a[i-1], 40, 16)) # sprite 1 to 11

        #background color of the cells
        self.cellColors = [ EMPTY_CELL,
        PicoGameBoy.color(0xf8, 0xe4, 0x5c),
        PicoGameBoy.color(0x57, 0xe3, 0x89),
        PicoGameBoy.color(0xff, 0xa3, 0x48),
        PicoGameBoy.color(0x62, 0xa0, 0xea),
        PicoGameBoy.color(0xbf, 0x80, 0xb7),
        PicoGameBoy.color(0xb5, 0x83, 0x5a),
        PicoGameBoy.color(0xed, 0x33, 0x3b),
        PicoGameBoy.color(0xde, 0xbb, 0x65),
        PicoGameBoy.color(0x11, 0xa8, 0x21),
        PicoGameBoy.color(0xc6, 0x46, 0x00),
        PicoGameBoy.color(0, 0, 0)
        ]

    # draw a tile at position x,y 
    def draw_cell(self, x,y, num):
        X = CELL_WIDTH * x + X_OFFSET
        Y = CELL_HEIGHT * y + Y_OFFSET
#        self._pgb.rect(X, Y, CELL_WIDTH, CELL_HEIGHT, BLACK, False)
#        self._pgb.rect(X + 1, Y + 1, CELL_WIDTH - 2, CELL_HEIGHT - 2, self.cellColors[num], True)
#        self._pgb.sprite(num, X + 5, Y + 17)
        self._pgb.rect(X + 1, Y + 1, CELL_WIDTH - 2, CELL_HEIGHT - 2, BLACK, False)
        self._pgb.rect(X + 2, Y + 2, CELL_WIDTH - 4, CELL_HEIGHT - 4, self.cellColors[num], True)
        self._pgb.sprite(num, X + 5, Y + 17)

    def animate_moves(self, moves):
        for mat in moves:
            self._pgb.fill(0)
            for i in range(4):
                for j in range(4):
                    for s_i in range(0, 12):
                        if mat[i][j] == 2 ** s_i:
                            self.draw_cell(i, j, s_i)
                            break;
            self._pgb.rect(X_OFFSET + 2, 0, 240 - 2 * X_OFFSET - 4, Y_OFFSET - 1, EMPTY_CELL, True)
            self._pgb.text('Score {}'.format(self._l.score), X_OFFSET + 10, 6, WHITE)
            self._pgb.show()
            time.sleep_ms(10)

    def play_tune(self, tune):
        for el in tune:
            self._pgb.sound(el[0])
            time.sleep_ms(int(800/el[1]) - 50)
            self._pgb.sound(0)
            time.sleep_ms(50)

    def game_over(self):
        self._l.moves.append(self._l.mat_copy(self._l.mat))
        end_game_tune = True
        toggle_end_message = False
        while True:
            toggle_end_message = not toggle_end_message
            self.animate_moves(self._l.moves)
            if toggle_end_message:
                self._pgb.rect(40, 95, 160, 40, WHITE, True)
                self._pgb.rect(40, 95, 160, 40, BLACK, False)
                if self._l.get_current_state() == Logic.WON:
                    self._pgb.center_text("YOU WIN!", GREEN)
                    if end_game_tune:
                        end_game_tune = False
                        self.play_tune(Resources.WIN_TUNE)
                else:
                    self._pgb.center_text("YOU LOSE", RED)
                    if end_game_tune:
                        end_game_tune = False
                        self.play_tune(Resources.GAME_OVER_TUNE)
            self._pgb.show()
            count_down = 10
            while count_down > 0:
                count_down -= 1
                time.sleep_ms(100)
                if self._pgb.any_button():
                    break;
            if self._pgb.any_button():
                break;

    def leave_game(self):
        self._l.moves.append(self._l.mat_copy(self._l.mat))
        toggle_message = False
        while True:
            toggle_message = not toggle_message
            self.animate_moves(self._l.moves)
            if toggle_message:
                self._pgb.rect(40, 95, 160, 40, WHITE, True)
                self._pgb.rect(40, 95, 160, 40, BLACK, False)
                self._pgb.center_text("CLICK A TO LEAVE", GREEN)
            self._pgb.show()
            count_down = 10
            while count_down > 0:
                count_down -= 1
                time.sleep_ms(100)
                if self._pgb.any_button():
                    if self._pgb.button_A():
                        return True
                    return False

    def begin(self):
        # Pico 2048 main
        # Game settings

        if self._l.get_current_state() != Logic.GAME_NOT_OVER:
            self._l.reset_game()

        clicked = False

        # game loop
        while True:
            if self._pgb.button_down():
                clicked = True
                self._l.move(Logic.DOWN)

            if self._pgb.button_up():
                clicked = True
                self._l.move(Logic.UP)

            if self._pgb.button_right():
                clicked = True
                self._l.move(Logic.RIGHT)

            if self._pgb.button_left():
                clicked = True
                self._l.move(Logic.LEFT)

            if self._pgb.button_A():
                clicked = True
                if self.leave_game():
                    break

            if (len(self._l.moves) > 0):
                self.animate_moves(self._l.moves)
                self._l.moves = []

            # wait for a clicked key to be released
            while (clicked):
                time.sleep_ms(100)
                if not self._pgb.any_button():
                    clicked = False

            if self._l.get_current_state() != Logic.GAME_NOT_OVER:
                self.game_over()
                break

if __name__ == "__main__":
    from PicoGameBoy import PicoGameBoy
    pgb = PicoGameBoy()
    from Pico2048 import Pico2048
    game = Pico2048(pgb)
    game.begin()

