from concurrent.futures import ThreadPoolExecutor
import grpc
import logging

import server.poke_resources as poke_resources
import proto.poke_pb2_grpc as poke_pb2_grpc
import proto.poke_pb2 as poke_pb2
import server.model as model


class PokeServicer(poke_pb2_grpc.PokeServicer):
    def __init__(self):
        moves_dict, templates_dict = poke_resources.read_moves_and_templates()
        self.model = model.Model(
            moves=list(moves_dict.values()),
            templates=list(templates_dict.values()))
        self.players = dict()
        
    def checkClientIsWinner(self, player_number) -> bool:
        return self.model.winner == player_number if self.model.check_winner() else None

    def createClientModel(self, user_id) -> poke_pb2.Model:
        player_number = self.players[user_id]
        if self.model.players[0] is None or self.model.players[1] is None:
            opponent_health = None
        else:
            opponent_health = self.model.players[(player_number+1)%2].active_card.health
        return poke_pb2.Model(client_health=self.model.players[player_number].active_card.health,
                                                    opponent_health=opponent_health,
                                                    winner=self.checkClientIsWinner(player_number),
                                                    playing=self.model.playing())
    
    def createDifferenceModel(self, user_id, client_snapshot:poke_pb2.Model) -> poke_pb2.Model:
        player_number = self.players[user_id]
        if not self.model.playing() or client_snapshot is None:
            return poke_pb2.Model(winner=self.checkClientIsWinner(player_number))
        return poke_pb2.Model(client_health=self.model.players[player_number].active_card.health-client_snapshot.client_health,
                                                    opponent_health=self.model.players[(player_number+1)%2].active_card.health-client_snapshot.opponent_health,
                                                    winner=self.checkClientIsWinner(player_number),
                                                    playing=self.model.playing())

    def GetModel(self, request:poke_pb2.GetModelRequest, context):
        return poke_pb2.GetModelReply(model=self.createClientModel(request.header.user_id))
    
    def Command(self, request:poke_pb2.CommandRequest, context):
        client_snapshot = self.createClientModel(request.header.user_id)
        if not self.model.playing():
            return poke_pb2.CommandReply(diff=self.createDifferenceModel(request.header.user_id, client_snapshot))
        if hasattr(request, "move"):
            player_number = self.players[request.header.user_id]
            player = self.model.players[player_number]
            self.model.move(player)
            return poke_pb2.CommandReply(diff=self.createDifferenceModel(request.header.user_id, client_snapshot))
        else:
            raise TypeError("Command is of unknown type.")
    
    def Register(self, request:poke_pb2.RegisterRequest, context):
        if request.header.user_id in self.players:
            return poke_pb2.RegisterReply()
        elif len(self.players) < 2:
            player_number = self.model.register()
            self.players[request.header.user_id] = player_number
            return poke_pb2.RegisterReply()
        else:
            raise ValueError("Two players are already in this game.")

    
    def Wait(self, request:poke_pb2.WaitRequest, context):
        client_snapshot = self.createClientModel(request.header.user_id)
        if self.model.turn == request.header.user_id:
            return poke_pb2.WaitReply(diff=self.createDifferenceModel(request.header.user_id, client_snapshot))
        self.model.wait(player_number=self.players[request.header.user_id])
        return poke_pb2.WaitReply(diff=self.createDifferenceModel(request.header.user_id, client_snapshot))

def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    poke_pb2_grpc.add_PokeServicer_to_server(PokeServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()