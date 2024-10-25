"""Controller module. Part of the MVC architecture."""

import curses
import client_model as model

class Controller:
    def __init__(self, m:model.Model, window_screen):
        self.model = m
        self.window_screen = window_screen
    
    def wait(self):
        self.window_screen.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.raw()
        key_input = self.window_screen.getch()
        if key_input == 3: # CTRL+C
            self.model.quit = True
            return
        else:
            if key_input == ord(' '):
                return "move"

        self.window_screen.erase()
        self.window_screen.refresh()

        self.window_screen.keypad(False)
