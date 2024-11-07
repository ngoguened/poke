"""View module. Part of the MVC architecture."""

import client_model as model

class View:
    def __init__(self, m:model.Model, window_screen):
        self.model = m
        self.window_screen = window_screen

    def refresh(self):
        self.window_screen.clear()
        if not self.model.playing:
            self.window_screen.addstr(f"You {'Win' if self.model.winner else 'Lose'}!")
        else:
            self.window_screen.addstr(f"[{self.model.player_active_card_name} {self.model.player_health}]  [{self.model.opponent_active_card_name} {self.model.opponent_health}]")
        self.window_screen.refresh()
        