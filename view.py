"""View module. Part of the MVC architecture."""

import curses
import model
import controller

class View:
    def __init__(self):
        self.window_screen = curses.initscr()

    def print_model(self):
        self.window_screen.addstr("[]  []")

    def exit(self):
        curses.nocbreak()
        self.window_screen.keypad(False)
        curses.echo()
        curses.endwin()

    def run(self, c:controller.Controller, m:model):
        self.window_screen.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.raw()
        while True:
            key_input = self.window_screen.getch()
            if key_input == 3: # CTRL+C
                self.exit()
                return
            else:
                c.parse_input(key_input, m)

            self.window_screen.erase()
            self.print_model()
            self.window_screen.refresh()
