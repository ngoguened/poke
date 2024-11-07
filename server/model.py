"""Model module. Part of the MVC architecture."""
import random
import threading

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
    class WaitPredicate:
        """Callable class to evaluate if it's the client's turn."""
        def __init__(self, model, player_number):
            self.model = model
            self.player_number = player_number
        
        def __call__(self):
            print(f"expecting {self.player_number} got {self.model.turn}")
            return self.model.turn == self.player_number and self.model.players[0] is not None and self.model.players[1] is not None

    def __init__(self, moves, templates):
        self.moves = moves # In the future this will read from a file.
        self.templates = templates # In the future this will read from a file.
        self.players:list[Player] = [None, None]
        self.turn = 0
        self.winner = None
        self.quit = False
        self.lock = threading.Lock()
        self.conditions = [threading.Condition(self.lock), threading.Condition(self.lock)]

    def initialized(self) -> bool:
        """Check if there are 2 players."""
        return self.players[0] and self.players[1]

    def register(self) -> int:
        """Lets 2 players join the game."""
        scratch_move = Move(name="weird scratch", damage=0, special_effects=[RANDOM_DAMAGE]) # Constants to initialize the game with a card.
        rattata_template = Template(name="rattata", health=40, move=scratch_move)
        self.lock.acquire()
        if not self.players[0] and not self.players[1]:
            rattata_card = Card(template=rattata_template)
            player = Player(rattata_card, user=random.randint(0,1))
            self.players[player.user] = player
        elif not self.players[0]:
            rattata_card = Card(template=rattata_template)
            player = Player(rattata_card, 0)
            self.players[0] = player
            self.conditions[1].notify()
        elif not self.players[1]:
            rattata_card = Card(template=rattata_template)
            player = Player(rattata_card, 1)
            self.players[1] = player
            self.conditions[0].notify()
        else:
            raise ValueError("Two players are already in this game.")
        self.lock.release()
        return player.user

    def wait(self, player_number:int):
        print("before wait acquire")
        self.lock.acquire()
        print("after wait acquire")
        wait_for_player_turn = self.WaitPredicate(model=self, player_number=player_number)
        self.conditions[player_number].wait_for(wait_for_player_turn)
        self.lock.release()
        print("after wait release")


    def move(self, player:Player):
        """Lets the player use a move against the opponent."""
        if not self.initialized():
            raise ValueError("Cannot make a move without 2 players.")
        opponent_user = (player.user+1) % 2
        opponent:Player = self.players[opponent_user]
        print("before move acquire")
        self.lock.acquire()
        print("after move acquire")
        player.move(opponent_card=opponent.active_card)
        # self.check_winner()
        self.turn = opponent_user
        self.conditions[opponent_user].notify()
        self.lock.release()
        print("after move release")


    def check_winner(self) -> bool:
        """Check if one of the players has won the game. 
        For now this is only if the active card reaches 0 health."""
        self.lock.acquire()
        if self.players[0] is None or self.players[1] is None:
            self.winner = None
        elif self.players[0].active_card.health <= 0:
            self.winner = 1
        elif self.players[1].active_card.health <= 0:
            self.winner = 0
        self.lock.release()
        return self.winner is not None
    
    def playing(self) -> bool:
        if self.quit:
            return False
        self.check_winner()
        return self.winner is None