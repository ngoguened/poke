"""View module. Part of the MVC architecture."""

import client.model as model

class View:
    def __init__(self, m:model, window_screen):
        self.model = m
        self.window_screen = window_screen

    def refresh(self):
        if self.model.winner is not None:
            self.window_screen.addstr(f"Player {self.model.winner+1} wins!")
        else:
            self.window_screen.addstr(f"[{self.model.player_active_card_name} {self.model.player_health}]  [{self.model.opponent_active_card_name} {self.model.opponent_health}]")