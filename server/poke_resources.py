from google.protobuf.text_format import Parse
import grpc
import proto.resources_pb2 as resources
import proto.config_pb2
import server.model as model

def read_moves_and_templates():
    moves = dict()
    templates = dict()
    # Will try to find the data file from the docker's runfiles first. If not found, will try to find the unpackaged file.
    try:
        moves_and_templates_file = open("server/poke_servicer.runfiles/_main/server/moves_and_templates.textproto", encoding="ascii")
    except IOError:
        moves_and_templates_file = open("server/moves_and_templates.textproto", encoding="ascii")
    moves_and_templates_text_lines = [line for line in moves_and_templates_file.readlines()]
    moves_and_templates_text = ' '.join(moves_and_templates_text_lines)
    config = proto.config_pb2.Config()
    Parse(moves_and_templates_text, config)
    for m in config.moves:
        moves[m.name] = m
    for t in config.templates:
        templates[t.name] = t
    return moves, templates

if __name__ == "__main__":
    read_moves_and_templates()