class Model:
    def __init__(self, player_health:int, opponent_health:int, player_active_card_name:str, opponent_active_card_name:str, winner:int=False):
        self.player_health = player_health
        self.opponent_health = opponent_health
        self.player_active_card_name = player_active_card_name
        self.opponent_active_card_name = opponent_active_card_name
        self.winner = winner
        self.quit = False