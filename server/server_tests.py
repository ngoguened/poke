"""Testing"""
import unittest
import poke_servicer
import poke_pb2

def registerNickAndSkye():
    servicer = poke_servicer.PokeServicer()
    header = poke_pb2.RequestHeader(user_id="nick")
    request = poke_pb2.RegisterRequest(header=header, first_connect=True)
    servicer.Register(request, None)

    header = poke_pb2.RequestHeader(user_id="skye")
    request = poke_pb2.RegisterRequest(header=header, first_connect=True)
    servicer.Register(request, None)
    return servicer

class TestModel(unittest.TestCase):
    """Test the model"""
    def testPokeServicerInit(self):
        """Test the servicer."""
        servicer = poke_servicer.PokeServicer()
        assert len(servicer.model.moves) == 2 and len(servicer.model.templates) == 1 # Template only has ratatta for now and moves has scratch and weird_scratch.
        assert len(servicer.players) == 0 # No players yet.
    
    def testPokeServicerRegister(self):
        servicer = poke_servicer.PokeServicer()
        header = poke_pb2.RequestHeader(user_id="nick")
        request = poke_pb2.RegisterRequest(header=header, first_connect=True)
        servicer.Register(request, None)
        assert servicer.players["nick"] == 0 or servicer.players["nick"] == 1, servicer.players # One player can join the game.

        header = poke_pb2.RequestHeader(user_id="skye")
        request = poke_pb2.RegisterRequest(header=header, first_connect=True)
        servicer.Register(request, None)
        assert (servicer.players["skye"] == 0 and servicer.players["nick"] == 1) or (servicer.players["nick"] == 0 and servicer.players["skye"] == 1) # Two players can join the game.
        
        header = poke_pb2.RequestHeader(user_id="pablo")
        with self.assertRaises(Exception): # A third player cannot join the game.
            servicer.Register(request, None)
        
        header = poke_pb2.RequestHeader(user_id="skye")
        request = poke_pb2.RegisterRequest(header=header, first_connect=False)
        servicer.Register(request, None)
        assert (servicer.players["skye"] == 0 and servicer.players["nick"] == 1) or (servicer.players["nick"] == 0 and servicer.players["skye"] == 1) # The same player can rejoin the game.

    def testPokeServicerGetModel(self):
        servicer = registerNickAndSkye()
        header = poke_pb2.RequestHeader(user_id="skye")
        request = poke_pb2.GetModelRequest(header=header)
        
        skye_model = servicer.GetModel(request, None)
        assert skye_model.client_health == 40 and skye_model.opponent_health == 40

    def testPokeServicerCommand(self):
        servicer = registerNickAndSkye()
        if servicer.players["nick"] == 0:
            header_player1 = poke_pb2.RequestHeader(user_id="nick")
            player2 = "skye"
        else:
            header_player1 = poke_pb2.RequestHeader(user_id="skye")
            player2 = "nick"
        move = poke_pb2.Move()
        request = poke_pb2.CommandRequest(header=header_player1, move=move)
        servicer.Command(request, None)
        assert servicer.model.turn == servicer.players[player2]

if __name__ == '__main__':
    unittest.main()
    print("All tests pass\n")
