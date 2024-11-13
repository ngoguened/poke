"""Testing"""
from locust import User, task, constant, HttpUser, events
from locust.stats import stats_history, stats_printer
from locust.env import Environment
import gevent
import random
import unittest
import poke_servicer as poke_servicer
import proto.poke_pb2 as poke_pb2

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
        assert len(servicer.moves_dict) == 2 and len(servicer.templates_dict) == 1 # Template only has ratatta for now and moves has scratch and weird_scratch.
        assert len(servicer.active_players) == 0 # No players yet.
    
    def testPokeServicerRegister(self):
        servicer = poke_servicer.PokeServicer()
        header = poke_pb2.RequestHeader(user_id="nick")
        request = poke_pb2.RegisterRequest(header=header, first_connect=True)
        servicer.Register(request, None)
        assert (servicer.active_players["nick"] == 0) != (servicer.active_players["nick"] == 1), servicer.active_players # One player can join the game.

        servicer.Register(request, None)
        assert (servicer.active_players["nick"] == 0) != (servicer.active_players["nick"] == 1), servicer.active_players # The same player cannot join twice.

        header = poke_pb2.RequestHeader(user_id="skye")
        request = poke_pb2.RegisterRequest(header=header, first_connect=True)
        servicer.Register(request, None)
        assert (servicer.active_players["skye"] == 0 and servicer.active_players["nick"] == 1) or (servicer.active_players["nick"] == 0 and servicer.active_players["skye"] == 1) # Two players can join the game.
        
        header = poke_pb2.RequestHeader(user_id="pablo")
        request = poke_pb2.RegisterRequest(header=header, first_connect=True)
        servicer.Register(request, None)
        assert servicer.active_models["pablo"] != servicer.active_models["nick"] and servicer.active_models["pablo"] != servicer.active_models["skye"] # A third player joins a different game.

        header = poke_pb2.RequestHeader(user_id="skye")
        request = poke_pb2.RegisterRequest(header=header, first_connect=False)
        servicer.Register(request, None)
        assert (servicer.active_players["skye"] == 0 and servicer.active_players["nick"] == 1) or (servicer.active_players["nick"] == 0 and servicer.active_players["skye"] == 1) # The same player can rejoin the game.

    def testPokeServicerCheckClientIsWinner(self):
        servicer = registerNickAndSkye()
        assert servicer.checkPlayerIsWinnerInModel(player_number=servicer.active_players["skye"], stored_model=servicer.active_models["nick"]) is None
        servicer.active_models["nick"].winner = 1
        assert servicer.checkPlayerIsWinnerInModel(player_number=servicer.active_players["skye"], stored_model=servicer.active_models["nick"]) != servicer.checkPlayerIsWinnerInModel(player_number=servicer.active_players["nick"], stored_model=servicer.active_models["nick"])

    def testPokeServicerGetModel(self):
        servicer = registerNickAndSkye()
        header = poke_pb2.RequestHeader(user_id="skye")
        request = poke_pb2.GetModelRequest(header=header)
        
        model_response = servicer.GetModel(request, None)
        skye_model = model_response.model
        
        assert skye_model.client_health == 40 and skye_model.opponent_health == 40, servicer.model.players[1].active_card.health
        assert not skye_model.winner

    def testPokeServicerCommand(self):
        servicer = registerNickAndSkye()
        if servicer.active_players["nick"] == 0:
            header_player1 = poke_pb2.RequestHeader(user_id="nick")
            player2 = "skye"
        else:
            header_player1 = poke_pb2.RequestHeader(user_id="skye")
            player2 = "nick"
        move = poke_pb2.MoveCommand()
        request = poke_pb2.CommandRequest(header=header_player1, move=move)
        command_reply:poke_pb2.CommandReply = servicer.Command(request, None)
        assert servicer.active_models["nick"].turn == servicer.active_players[player2]
        assert command_reply.diff.client_health == 0

    def testMultiServicer(self):
        servicer = registerNickAndSkye()
        
        assert "nick" in servicer.active_models and "skye" in servicer.active_models

        header = poke_pb2.RequestHeader(user_id="pablo")
        request = poke_pb2.RegisterRequest(header=header, first_connect=True)
        servicer.Register(request, None)

        header = poke_pb2.RequestHeader(user_id="steve")
        request = poke_pb2.RegisterRequest(header=header, first_connect=True)
        servicer.Register(request, None)

        assert all([name in servicer.active_models for name in ["skye","nick","pablo","steve"]]) and all([name in servicer.active_players for name in ["skye","nick","pablo","steve"]])
        assert servicer.active_models["nick"] == servicer.active_models["skye"] and servicer.active_models["pablo"] == servicer.active_models["steve"]

    def testUIDIsEjected(self):
        servicer = registerNickAndSkye()
        assert "nick" in servicer.active_players and "skye" in servicer.active_players and "nick" in servicer.active_models and "skye" in servicer.active_models
        header = poke_pb2.RequestHeader(user_id="nick")
        request = poke_pb2.CommandRequest(header=header, move=poke_pb2.MoveCommand())
        servicer.Command(request, None)
        header = poke_pb2.RequestHeader(user_id="skye")
        request = poke_pb2.CommandRequest(header=header, move=poke_pb2.MoveCommand())
        servicer.Command(request, None)
        assert "nick" in servicer.active_players and "skye" in servicer.active_players and "nick" in servicer.active_models and "skye" in servicer.active_models

        servicer.active_models["nick"].players[0].active_card.health = 0
        servicer.active_models["nick"].check_winner()
        header = poke_pb2.RequestHeader(user_id="nick")
        request = poke_pb2.CommandRequest(header=header, move=poke_pb2.MoveCommand())
        servicer.Command(request, None)
        header = poke_pb2.RequestHeader(user_id="skye")
        request = poke_pb2.CommandRequest(header=header, move=poke_pb2.MoveCommand())
        servicer.Command(request, None)
        assert "nick" not in servicer.active_players and "skye" not in servicer.active_players and "nick" not in servicer.active_models and "skye" not in servicer.active_models

    def testRobustRPC(self):
        servicer = registerNickAndSkye()
        for _ in range(50):
            header = poke_pb2.RequestHeader(user_id="nick")
            request = poke_pb2.CommandRequest(header=header, move=poke_pb2.MoveCommand())
            servicer.Command(request, None)
        assert servicer.active_models["nick"].players[0].active_card.health > 20 and servicer.active_models["nick"].players[1].active_card.health > 20

    # def testLoadBalancing(self):
    #     servicer = poke_servicer.PokeServicer()
    #     user_ids = []
    #     class MyUser(User):
    #         host = "https://docs.locust.io"

    #         @task
    #         def register(self):
    #             user_id=''.join([str(random.randint(0,9)) for _ in range(100)])
    #             user_ids.append(user_id)
    #             header = poke_pb2.RequestHeader(user_id=user_id)
    #             request = poke_pb2.RegisterRequest(header=header, first_connect=True)
    #             servicer.Register(request, None)
    #             print(f"registered as {user_id}")

            # def command(self):
            #     if user_ids:
            #         user_id = random.choice(user_ids)
            #         model = servicer.active_models[user_id]
            #         if model.initialized():
            #             model.players[0]
            #             header = poke_pb2.RequestHeader(user_id=user_id)
            #             request = poke_pb2.CommandRequest(header=header, move=poke_pb2.MoveCommand())
            #             servicer.Command(request, None)


        # env = Environment(user_classes=[MyUser], events=events)
        # runner = env.create_local_runner()
        # web_ui = env.create_web_ui("127.0.0.1", 8089)
        # gevent.spawn(stats_printer(env.stats))
        # gevent.spawn(stats_history, env.runner)
        # runner.start(1, spawn_rate=10)
        # gevent.spawn_later(30, runner.quit)
        # runner.greenlet.join()
        # web_ui.stop()

if __name__ == '__main__':
    unittest.main()
    print("All tests pass\n")
