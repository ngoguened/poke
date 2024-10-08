"""Controller module. Part of the MVC architecture."""

import model

class Controller:
    def parse_input(self, key:int, m:model.Model):
        if key == ord(' '):
            m.move(m.players[0])