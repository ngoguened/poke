import proto.poke_pb2 as poke_pb2

class Model:
    def __init__(self):
        # Model parameters controlled by the server.
        self.player_health = None
        self.opponent_health = None
        self.player_active_card_name = None
        self.opponent_active_card_name = None
        self.winner = None
        self.playing = None

        # Model parameters controlled by the client.
        self.quit = False
        self.user_id = None
    
    def changeClientInt(self, client_int:int, server_int:int) -> int:
        return client_int + server_int

    def changeClientStr(self, client_str:str, server_str:str) -> str:
        if server_str is not None:
            client_str = server_str
        return client_str

    def changeClientBool(self, client_bool:bool, server_bool:bool):
        if server_bool is not None:
            client_bool = server_bool
        return client_bool

    def addServerDifferenceToClient(self, diff:poke_pb2.Model):
        self.player_health = self.changeClientInt(self.player_health, diff.client_health)
        self.opponent_health = self.changeClientInt(self.opponent_health, diff.opponent_health)
        self.playing = self.changeClientBool(self.playing, diff.playing)
        self.winner = self.changeClientBool(self.winner, diff.winner)

    def overrideClientModel(self, server_model:poke_pb2.Model):
        self.player_health = server_model.client_health
        self.opponent_health = server_model.opponent_health
        self.playing = server_model.playing
        self.winner = server_model.winner