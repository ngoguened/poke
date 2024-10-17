from concurrent.futures import ThreadPoolExecutor
import grpc

import poke_resources
import poke_pb2_grpc
import poke_pb2
import model


class PokeServicer(poke_pb2_grpc.PokeServicer):
    def __init__(self):
        moves_dict, templates_dict = poke_resources.read_moves_and_templates()
        self.model = model.Model(
            moves=list(moves_dict.values()),
            templates=list(templates_dict.values()))
        self.players = dict()
        
    def createClientModel(self, user_id) -> poke_pb2.Model:
        player_number = self.players[user_id]
        return poke_pb2.Model(client_health=self.model.players[player_number].active_card.health,
                                          opponent_health=self.model.players[(player_number+1)%2].active_card.health)

    def GetModel(self, request:poke_pb2.GetModelRequest, context):
        return self.createClientModel(request.header.user_id)
    
    def Command(self, request:poke_pb2.CommandRequest, context):

        if hasattr(request, "move"):
            player_number = self.players[request.header.user_id]
            player = self.model.players[player_number]
            self.model.move(player)
            return self.createClientModel(request.header.user_id)
        else:
            raise TypeError("Command is of unknown type.")
    
    def Register(self, request:poke_pb2.RegisterRequest, context):
        if request.first_connect:
            player_number = self.model.register()
            self.players[request.header.user_id] = player_number
        else:
            if request.header.user_id not in self.players:
                raise ValueError("Two players are already in this game.")

    
    def Wait(self, request:poke_pb2.WaitRequest, context):
        return self.createClientModel(request.header.user_id)

def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    poke_pb2_grpc.add_PokeServicer_to_server(PokeServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()