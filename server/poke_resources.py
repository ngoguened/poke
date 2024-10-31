import json
import server.model as model

def read_moves_and_templates():
    moves = dict()
    with open("moves.json", encoding="UTF-8") as moves_file:
        for item in json.load(moves_file):
            move = model.Move(
                name=item["name"],
                damage=item["damage"],
                special_effects=item["special_effects"])
            moves[move.name] = move

    templates = dict()
    with open("templates.json", encoding="UTF-8") as templates_file:
        for item in json.load(templates_file):
            template = model.Template(
                name=item["name"],
                health=item["health"],
                move=moves[item["move"]])
            templates[template.name] = template

    return moves, templates
