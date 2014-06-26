import libtcodpy as libtcod
import shelve
import time
import random

BOARD_WIDTH = 30
BOARD_HEIGHT = 16
BOMB_NUM = 99

class Square:
    def __init__(self, x, y, clickable = True, bomb = False, flagged = False, number = 0, clicked = False, character = '#'):
        global board
        self.x = x
        self.y = y
        self.clickable = clickable  
        self.bomb = bomb       
        self.flagged = flagged
        self.number = number
        self.clicked = clicked
        self.character = character
                    
    def flag(self):    
        global flags
        if not self.flagged:
            self.flagged = True
            self.clickable = False
            self.character = 'O'
            flags -= 1
        else:
            self.flagged = False
            self.clickable = True
            self.character = '#'
            flags += 1
            
    def surrounding(self):
        global board
        surround_list = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if self.x + dx in range(BOARD_WIDTH) and self.y + dy in range(BOARD_HEIGHT) and not (dx == 0  and dy == 0):
                    surround_list.append(board[self.x + dx][self.y + dy])
        return surround_list
                    
    def compute_number(self):
        self.number = 0
        for item in self.surrounding():
            if item.bomb:
                self.number += 1
                        
    def click(self):
        self.clickable = False
        self.clicked = True
        
        if self.bomb:
            self.character = 'B'
            return 'boom'
        elif self.number == 0:
            self.character = ' '
        else:
            self.character = str(self.number)
        
        #if self.character == '0' and not (True in [item.clicked for item in self.surrounding()]):
            #for item in self.surrounding():
                #item.click()
        
        #if 0 in [item.number for item in self.surrounding()]:
            #for item in self.surrounding():
                #if item.character == '0' and (False in [subitem.clicked for subitem in item.surrounding()]):
                    #item.click() 

    def render(self):
        color = libtcod.white
        backcolor = libtcod.light_grey
        
        if self.character == '#':
            color = libtcod.white
            #backcolor = libtcod.blue
        elif self.character == ' ':
            color = libtcod.white
        elif self.character == 'O':
            color = libtcod.yellow
            #backcolor = libtcod.blue
        elif self.character == '1':
            color = libtcod.blue
        elif self.character == '2':
            color = libtcod.green
        elif self.character == '3':
            color = libtcod.red
        elif self.character == '4':
            color = libtcod.darker_blue
        elif self.character == '5':
            color = libtcod.dark_red
        elif self.character == '6':
            color = libtcod.cyan
        elif self.character == '7':
            color = libtcod.black
        elif self.character == '8':
            color = libtcod.yellow
        elif self.character == 'B':
            color = libtcod.black
            
        libtcod.console_set_default_background(con, backcolor)
        libtcod.console_set_default_foreground(con, color)
        libtcod.console_print_ex(con, self.x, self.y, backcolor, libtcod.RIGHT, self.character)
            
board = [[Square(x, y) 
    for y in range(BOARD_HEIGHT)]
        for x in range(BOARD_WIDTH)]
                    
for num in range(BOMB_NUM):
    tile = random.choice(random.choice(board))
    while tile.bomb:
        tile = random.choice(random.choice(board))
    tile.bomb = True
                    
for y in range(BOARD_HEIGHT):
    for x in range(BOARD_WIDTH):
        board[x][y].compute_number()
                    
libtcod.console_set_custom_font('arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(BOARD_WIDTH + 2, BOARD_HEIGHT + 4, "PySweeper", False)
con = libtcod.console_new(BOARD_WIDTH, BOARD_HEIGHT)
timer = libtcod.console_new(3, 1)
flagcon = libtcod.console_new(2, 1)
mouse = libtcod.Mouse()
key =  libtcod.Key()

libtcod.console_wait_for_keypress(True)

state = 'playing'
flags = BOMB_NUM
counter = 0
now = time.time()

while not libtcod.console_is_window_closed():
    if time.time() >= now + 1 and counter < 999:
        counter += 1
        now += 1
    
    libtcod.console_set_default_foreground(con, libtcod.white)
    libtcod.sys_check_for_event(libtcod.EVENT_MOUSE, key, mouse)
    libtcod.console_clear(con)
    libtcod.console_clear(timer)
    
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if board[x][y].clicked and board[x][y].number == 0:
                for item in board[x][y].surrounding():
                    if not item.clicked:
                        item.click()
            
            if (mouse.cx - 1, mouse.cy - 1) == (x, y):
                if mouse.lbutton_pressed and board[x][y].clickable:
                    state = board[x][y].click()
                
                elif mouse.rbutton_pressed:
                    board[x][y].flag()
            
            board[x][y].render()
                
    libtcod.console_print_ex(timer, 2, 0, libtcod.BKGND_NONE, libtcod.RIGHT, str(counter))
    libtcod.console_print_ex(flagcon, 1, 0, libtcod.BKGND_NONE, libtcod.RIGHT, str(flags))
    
    libtcod.console_blit(con, 0, 0, BOARD_WIDTH, BOARD_HEIGHT, 0, 1, 1)
    libtcod.console_blit(timer, 0, 0, 3, 1, 0, 5, BOARD_HEIGHT + 2)
    libtcod.console_blit(flagcon, 0, 0, 2, 1, 0, BOARD_WIDTH - 6, BOARD_HEIGHT + 2)
    libtcod.console_flush()
    
    if state == 'boom':
        break