"""Model module. Part of the MVC architecture."""
class Move:
    """Class that acts as a struct, storing inherent move information. 
    For now this is only the name and the damage."""
    def __init__(self, name:str, damage:int):
        self.name = name
        self.damage = damage

class Template:
    """Class that acts as a struct, storing inherent card information. 
    For now this is only the health, move, and name."""
    def __init__(self, name:str, health:int, move:Move):
        self.name = name
        self.health = health
        self.move = move

class Card:
    """stores a card template and the state of the card, for now this is only the health, 
    but will include other card states like status and card class in the future."""
    def __init__(self, template:Template):
        self.template = template
        self.health = template.health

    def get_move(self) -> Move:
        """Getter for the move from the template. In the future there 
        can be more than one move in a template."""
        return self.template.move

class Player:
    """Has an active card, and can be player 0 or 1."""
    def __init__(self, active_card:Card, user:int):
        self.active_card = active_card
        self.user = user

    def set_active_card(self, card:Card):
        """Sets the active card to replace None instance."""
        self.active_card = card

    def move(self, opponent_card:Card):
        """Logic to have an active card use their move."""
        m = self.active_card.get_move()
        opponent_card.health -= m.damage

class Model:
    """Implements a move by a player, gets the state of the game, 
    and allows players to register into the game."""
    def __init__(self, moves, templates):
        self.moves = moves # In the future this will read from a file.
        self.templates = templates # In the future this will read from a file.
        self.players = [None, None]

    def register(self) -> int:
        """Lets 2 players join the game."""
        if not self.players[0]:
            self.players[0] = Player(None, 0)
            return 0
        elif not self.players[1]:
            self.players[1] = Player(None, 1)
            return 1
        else:
            raise ValueError("Two players are already in this game.")

    def move(self, player:Player):
        """Lets the player use a move aggainst the opponent."""
        opponent_user = int(not player.user)
        opponent:Player = self.players[opponent_user]
        player.move(opponent_card=opponent.active_card)
