"""Controller module. Part of the MVC architecture."""

import curses

import client.model as model

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
                self.model.move(self.model.players[self.model.turn]) #TODO: Fix with RPC call.
        self.window_screen.erase()
        self.window_screen.refresh()

        self.window_screen.keypad(False)
