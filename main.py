import curses

import model
import view
import controller

def main():
    window_screen = curses.initscr()
    m = model.Model(moves=[],templates=[])
    v = view.View(m, window_screen)
    c = controller.Controller(m, window_screen)

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