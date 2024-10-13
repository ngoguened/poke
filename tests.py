"""Testing"""
import unittest
import server.model as model

class TestModel(unittest.TestCase):
    """Test the model"""

    def test_move(self):
        """test move class"""
        scratch_move = model.Move(name="scratch", damage=10, special_effects=[])
        assert scratch_move.name == "scratch" and scratch_move.damage == 10
    
    def test_template(self):
        """test template class"""
        scratch_move = model.Move(name="scratch", damage=10, special_effects=[])

        rattata_template = model.Template(name="rattata", health=40, move=scratch_move)
        assert rattata_template.name == "rattata" and rattata_template.health == 40 and rattata_template.move == scratch_move
    
    def test_card(self):
        """test card class and get_move()"""
        scratch_move = model.Move(name="scratch", damage=10, special_effects=[])

        rattata_template = model.Template(name="rattata", health=40, move=scratch_move)
        rattata_card = model.Card(template=rattata_template)
        assert rattata_card.template == rattata_template and rattata_card.health == 40
        assert rattata_card.get_move() == scratch_move

    def test_player(self):
        """test player class and set_active_card() and move()"""
        scratch_move = model.Move(name="scratch", damage=10, special_effects=[])
        rattata_template = model.Template(name="rattata", health=40, move=scratch_move)
        rattata_card = model.Card(template=rattata_template)
        player = model.Player(active_card=rattata_card, user=0)
        assert player.active_card == rattata_card and player.user == 0

        opponent_rattata_card = model.Card(template=rattata_template)
        player.move(opponent_card=opponent_rattata_card)
        assert opponent_rattata_card.health == 30

    def test_model(self):
        """Test model class and register() and move()"""
        scratch_move = model.Move(name="scratch", damage=10, special_effects=[])
        rattata_template = model.Template(name="rattata", health=40, move=scratch_move)
        m = model.Model(moves=[scratch_move],templates=[rattata_template])

        assert not m.players[0] and not m.players[1]
        m.register()
        assert (m.players[0] and not m.players[1]) or (not m.players[0] and m.players[1]), [m.players[0], m.players[1]]
        m.register()
        with self.assertRaises(Exception):
            m.register()

        # m.move(player=m.players[0])
        # assert m.players[1].active_card.health == 30

if __name__ == '__main__':
    unittest.main()
    print("All tests pass\n")
