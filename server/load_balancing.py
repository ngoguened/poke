from locust import User, task, constant, HttpUser, events
from locust.stats import stats_history, stats_printer
from locust.env import Environment
import gevent
import random
import unittest

import poke_servicer as poke_servicer
import proto.poke_pb2 as poke_pb2

class TestModel(unittest.TestCase):
    def testLoadBalancing(self):
        servicer = poke_servicer.PokeServicer()
        user_ids = []
        class MyUser(User):
            host = "https://docs.locust.io"

            @task
            def register(self):
                user_id=''.join([str(random.randint(0,9)) for _ in range(100)])
                user_ids.append(user_id)
                header = poke_pb2.RequestHeader(user_id=user_id)
                request = poke_pb2.RegisterRequest(header=header, first_connect=True)
                servicer.Register(request, None)
                print(f"registered as {user_id}")

            @task
            def command(self):
                if user_ids:
                    user_id = random.choice(user_ids)
                    if user_id in servicer.active_models:
                        model = servicer.active_models[user_id]
                        header = poke_pb2.RequestHeader(user_id=user_id)
                        request = poke_pb2.CommandRequest(header=header, move=poke_pb2.MoveCommand())
                        servicer.Command(request, None)
                        print(f"{user_id} send a command")
                        if not model.playing():
                            print("the game ended.")
                            user_ids.pop(user_ids.index(user_id))


        env = Environment(user_classes=[MyUser], events=events)
        runner = env.create_local_runner()
        web_ui = env.create_web_ui("127.0.0.1", 8089)
        gevent.spawn(stats_printer(env.stats))
        gevent.spawn(stats_history, env.runner)
        runner.start(10, spawn_rate=10)
        gevent.spawn_later(30, runner.quit)
        runner.greenlet.join()
        web_ui.stop()

if __name__ == '__main__':
    unittest.main()
    print("All tests pass\n")
