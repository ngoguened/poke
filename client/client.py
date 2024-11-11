import curses
import grpc
import logging
import sys

import client_model as model_client
import view
import controller
import proto.poke_pb2_grpc as poke_pb2_grpc
import proto.poke_pb2 as poke_pb2

def main():
    # Initialize client model
    m = model_client.Model()
    if len(sys.argv) == 2:
        m.user_id=str(sys.argv[1])
    else:
        m.user_id = "k"

    # Create connection with the server

    with grpc.insecure_channel('0.0.0.0:50052', options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = poke_pb2_grpc.PokeStub(channel)

    # Register for the first time.
        request_header = poke_pb2.RequestHeader(user_id=m.user_id)
        register_request = poke_pb2.RegisterRequest(header=request_header, first_connect=True)
        stub.Register(register_request)
        
    # Wait for both players to join.
        wait_request = poke_pb2.WaitRequest(header=request_header, wait_type=poke_pb2.WaitRequest.WaitType.TWOPLAYERS)
        stub.Wait(wait_request)

    # Request the server model.
        request_header = poke_pb2.RequestHeader(user_id=m.user_id)
        model_request = poke_pb2.GetModelRequest(header=request_header)
        model_reply:poke_pb2.GetModelReply = stub.GetModel(model_request)
        server_model = model_reply.model

    # Copy server model to client model.
        m.overrideClientModel(server_model)

    # Initialize user elements.
        window_screen = curses.initscr()
        v = view.View(m, window_screen)
        c = controller.Controller(m, window_screen)

        while m.playing:
            v.refresh()
            wait_request = poke_pb2.WaitRequest(header=request_header, wait_type=poke_pb2.WaitRequest.WaitType.MOVE)
            wait_response:poke_pb2.WaitReply = stub.Wait(wait_request)
            m.addServerDifferenceToClient(wait_response.diff)
            v.refresh()
            if not m.playing:
                break
            controller_input = c.wait()
            if controller_input == "move":
                request_header = poke_pb2.RequestHeader(user_id=m.user_id)
                move = poke_pb2.MoveCommand()
                command_request = poke_pb2.CommandRequest(header=request_header, move=move)
                command_reply:poke_pb2.CommandReply = stub.Command(command_request)
                m.addServerDifferenceToClient(command_reply.diff)
            v.refresh()
            
    while not m.quit:
        c.wait()
        v.refresh()

    curses.nocbreak()
    window_screen.keypad(False)
    curses.echo()
    curses.endwin()

if __name__ == "__main__":
    logging.basicConfig()
    main()