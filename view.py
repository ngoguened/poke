"""View module. Part of the MVC architecture."""

import curses
import model
import controller

class View:
    def __init__(self):
        self.window_screen = curses.initscr()

    def print_model(self, m:model.Model):
        player_1:model.Player = m.players[0]
        player_2:model.Player = m.players[1]
        if m.check_winner():
            self.window_screen.addstr(f"Player {m.winner+1} wins!")
        else:
            self.window_screen.addstr(f"[{player_1.active_card.template.name} {player_1.active_card.health}]  [{player_2.active_card.template.name} {player_2.active_card.health}]")

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
        self.print_model(m=m)
        while True:
            key_input = self.window_screen.getch()
            if key_input == 3: # CTRL+C
                self.exit()
                return
            else:
                c.parse_input(key_input, m)
            self.window_screen.erase()
            self.print_model(m=m)
            self.window_screen.refresh()
