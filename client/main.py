import curses

import client.model as model
import client.view as view
import client.controller as controller

def main():
    window_screen = curses.initscr()
    m = model.Model(player_active_card_name="rattata", opponent_active_card_name="rattata", player_health=50, opponent_health=50,
                    winner=None)
    v = view.View(m, window_screen)
    c = controller.Controller(m, window_screen)

    #TODO: fix main to connect with server model.
    m.register()
    m.register()
    while m.playing():
        c.wait()
        v.refresh()

    while not m.quit:
        c.wait()
        v.refresh()

    curses.nocbreak()
    window_screen.keypad(False)
    curses.echo()
    curses.endwin()

if __name__ == "__main__":
    main()