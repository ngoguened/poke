"""View module. Part of the MVC architecture."""

import model

class View:
    def __init__(self, m:model, window_screen):
        self.model = m
        self.window_screen = window_screen

    def refresh(self):
        player_1:model.Player = self.model.players[0]
        player_2:model.Player = self.model.players[1]
        if self.model.check_winner():
            self.window_screen.addstr(f"Player {self.model.winner+1} wins!")
        else:
            self.window_screen.addstr(f"[{player_1.active_card.template.name} {player_1.active_card.health}]  [{player_2.active_card.template.name} {player_2.active_card.health}]")