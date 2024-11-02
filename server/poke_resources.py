from google.protobuf.text_format import Parse
import grpc
# import proto.resources_pb2
import proto.config_pb2
import server.model as model

def read_moves_and_templates():
    moves = dict()
    with open("server/moves_and_templates.textproto") as moves_and_templates_file:
        moves_and_templates_text_lines = [line for line in moves_and_templates_file.readlines()]
        moves_and_templates_text = ' '.join(moves_and_templates_text_lines)
        config = proto.config_pb2.Config()
        Parse(moves_and_templates_text, config)

    return config.moves, config.templates

if __name__ == "__main__":
    read_moves_and_templates()