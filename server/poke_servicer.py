from concurrent.futures import ThreadPoolExecutor
import grpc
import logging

import server.poke_resources as poke_resources
import proto.poke_pb2_grpc as poke_pb2_grpc
import proto.poke_pb2 as poke_pb2
import server.model as model


class PokeServicer(poke_pb2_grpc.PokeServicer):
    ''' A servicer that stores active models, active players, a model waiting for a second player,
    (if there are an odd number of players using the service) and provides rpc responses to the
    client requesting the model, requesting to issue a command, registering into a game, and 
    waiting for their turn.
    '''
    def __init__(self):
        self.moves_dict, self.templates_dict = poke_resources.read_moves_and_templates()
        self.active_models = dict()
        self.active_players = dict()

        self.waiting_model = None

    def checkPlayerIsWinnerInModel(self, player_number, stored_model:model.Model) -> bool:
        '''Given a model and the client's player number for that model, return True
        if the player won, False if they lost, and None if the game is not over.'''
        return stored_model.winner == player_number if stored_model.check_winner() else None

    def createClientModel(self, user_id) -> poke_pb2.Model:
        '''Instantiates a new client model based on the data from the server model.'''
        player_number = self.active_players[user_id]
        if user_id in self.active_models:
            stored_model:model.Model = self.active_models[user_id]
        else:
            stored_model:model.Model = self.waiting_model
        if stored_model.players[0] is None or stored_model.players[1] is None:
            opponent_health = None
        else:
            opponent_health = stored_model.players[(player_number+1)%2].active_card.health
        return poke_pb2.Model(client_health=stored_model.players[player_number].active_card.health,
                              opponent_health=opponent_health,
                              winner=self.checkPlayerIsWinnerInModel(player_number, stored_model),
                              playing=stored_model.playing())

    def createDifferenceModel(self, user_id, client_snapshot:poke_pb2.Model) -> poke_pb2.Model:
        '''Creates a client model representing the delta before and after a move was made.'''
        player_number = self.active_players[user_id]
        stored_model:model.Model = self.active_models[user_id]
        if not stored_model.playing() or client_snapshot is None:
            return poke_pb2.Model(
                winner=self.checkPlayerIsWinnerInModel(player_number, stored_model)
                )
        return poke_pb2.Model(
            client_health=stored_model.players[player_number].active_card.health-client_snapshot.client_health,
            opponent_health=stored_model.players[(player_number+1)%2].active_card.health-client_snapshot.opponent_health,
            winner=self.checkPlayerIsWinnerInModel(player_number, stored_model),
            playing=stored_model.playing())

    def GetModel(self, request:poke_pb2.GetModelRequest, context):
        '''Fulfils a client's request for a client model.'''
        return poke_pb2.GetModelReply(model=self.createClientModel(request.header.user_id))

    def Command(self, request:poke_pb2.CommandRequest, context):
        '''Fulfils a client's request to issue a command.'''
        client_snapshot = self.createClientModel(request.header.user_id)
        stored_model:model.Model = self.active_models[request.header.user_id]

        if not stored_model.playing():
            return poke_pb2.CommandReply(
                diff=self.createDifferenceModel(request.header.user_id, client_snapshot)
                )
        if hasattr(request, "move"):
            player_number = self.active_players[request.header.user_id]
            player = stored_model.players[player_number]
            stored_model.move(player)
            return poke_pb2.CommandReply(
                diff=self.createDifferenceModel(request.header.user_id, client_snapshot)
                )
        else:
            raise TypeError("Command is of unknown type.")

    def Register(self, request:poke_pb2.RegisterRequest, context):
        '''Fulfils a client's request to register'''
        if (request.header.user_id in self.active_models or
            request.header.user_id in self.active_players):
            return poke_pb2.RegisterReply()

        if self.waiting_model is None:
            # Acquire lock here?
            self.waiting_model = model.Model(
                                    moves=list(self.moves_dict.values()),
                                    templates=list(self.templates_dict.values())
                                    )
            self.active_models[request.header.user_id] = self.waiting_model
            self.active_players[request.header.user_id] = self.waiting_model.register()
            # Release lock here?
            return poke_pb2.RegisterReply()
        # Acquire lock here?
        self.active_models[request.header.user_id] = self.waiting_model
        self.active_players[request.header.user_id] = self.waiting_model.register()
        self.waiting_model = None
        # Release lock here?
        return poke_pb2.RegisterReply()

    def Wait(self, request:poke_pb2.WaitRequest, context):
        '''Fulfils a client's request to wait until it is their turn'''
        client_snapshot = self.createClientModel(request.header.user_id)
        if request.header.user_id in self.active_models:
            stored_model:model.Model = self.active_models[request.header.user_id]
        else:
            stored_model:model.Model = self.waiting_model
        if stored_model.turn == self.active_players[request.header.user_id]:
            return poke_pb2.WaitReply(
                diff=self.createDifferenceModel(request.header.user_id, client_snapshot)
                )
        stored_model.wait(player_number=self.active_players[request.header.user_id])
        return poke_pb2.WaitReply(
            diff=self.createDifferenceModel(request.header.user_id, client_snapshot)
            )

def serve():
    '''The main service loop'''
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    poke_pb2_grpc.add_PokeServicer_to_server(PokeServicer(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    '''Starts the service'''
    logging.basicConfig()
    serve()
