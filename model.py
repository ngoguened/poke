"""Model module. Part of the MVC architecture."""
import random

RANDOM_DAMAGE = "random_damage"

class Move:
    """Class that acts as a struct, storing inherent move information. 
    For now this is only the name, damage, and special_effects."""
    def __init__(self, name:str, damage:int, special_effects:list):
        self.name = name
        self.damage = damage
        self.special_effects = special_effects

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
        move = self.active_card.get_move()
        for s in move.special_effects:
            if s == RANDOM_DAMAGE:
                move.damage = 10*random.randint(0,2)
        opponent_card.health -= move.damage

class Model:
    """Represents complete state of a game."""
    def __init__(self, moves, templates):
        self.moves = moves # In the future this will read from a file.
        self.templates = templates # In the future this will read from a file.
        self.players:list[Player] = [None, None]
        self.turn = 0
        self.winner = None
        self.quit = False

    def initialized(self) -> bool:
        """Check if there are 2 players."""
        return self.players[0] and self.players[1]

    def register(self) -> int:
        """Lets 2 players join the game."""
        scratch_move = Move(name="weird scratch", damage=0, special_effects=[RANDOM_DAMAGE]) # Constants to initialize the game with a card.
        rattata_template = Template(name="rattata", health=40, move=scratch_move)
        if not self.players[0] and not self.players[1]:
            rattata_card = Card(template=rattata_template)
            player = Player(rattata_card, user=random.randint(0,1))
            self.players[player.user] = player
        elif not self.players[0]:
            rattata_card = Card(template=rattata_template)
            player = Player(rattata_card, 0)
            self.players[0] = player
        elif not self.players[1]:
            rattata_card = Card(template=rattata_template)
            player = Player(rattata_card, 1)
            self.players[1] = player
        else:
            raise ValueError("Two players are already in this game.")
        return player.user

    def move(self, player:Player):
        """Lets the player use a move against the opponent."""
        if not self.initialized():
            raise ValueError("Cannot make a move without 2 players.")
        opponent_user = (player.user+1) % 2
        opponent:Player = self.players[opponent_user]
        player.move(opponent_card=opponent.active_card)
        self.turn = opponent_user

    def check_winner(self) -> bool:
        """Check if one of the players has won the game. 
        For now this is only if the active card reaches 0 health."""
        if self.players[0].active_card.health <= 0:
            self.winner = 1
        elif self.players[1].active_card.health <= 0:
            self.winner = 0

        return self.winner is not None
    
    def playing(self) -> bool:
        if self.quit:
            return False
        return not self.check_winner()