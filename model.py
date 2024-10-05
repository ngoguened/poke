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
    """Representation of active cards in the game. 
    Stores the template associated with a card and its local state."""
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

    def move(self, opponent_card:Card):
        """Logic to have an active card use their move."""
        m = self.active_card.get_move()
        opponent_card.health -= m.damage

class Model:
    """Represents complete state of a game."""
    def __init__(self, moves, templates):
        self.moves = moves # In the future this will read from a file.
        self.templates = templates # In the future this will read from a file.
        self.players = [None, None]

    def initialized(self) -> bool:
        """Check if there are 2 players."""
        return self.players[0] and self.players[1]

    def register(self) -> int:
        """Lets 2 players join the game."""
        player = None
        for i in range(0, 2):
            if not self.players[i]:

                scratch_move = Move(name="scratch", damage=10) # Constants to initialize the game with a card.
                rattata_template = Template(name="rattata", health=40, move=scratch_move)
                rattata_card = Card(template=rattata_template)

                player = Player(rattata_card, i)
                self.players[i] = player
                break
        if not player:
            raise ValueError("Two players are already in this game.")
        return player.user

    def move(self, player:Player):
        """Lets the player use a move against the opponent."""
        if not self.initialized():
            raise ValueError("Cannot make a move without 2 players.")
        opponent_user = int(not player.user)
        opponent:Player = self.players[opponent_user]
        player.move(opponent_card=opponent.active_card)
