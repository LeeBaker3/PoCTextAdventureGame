import unittest
from player import Player
from item import Item


class TestPlayer(unittest.TestCase):

    def setUp(self) -> None:
        self.player = Player('Lee')
        return super().setUp()

    def test_player_name(self) -> None:
        self.assertEqual('Lee', self.player.player_name)

    def test_player_to_many_items(self) -> None:
        self.item1 = Item(1, 'test', 'test')
        self.item2 = Item(2, 'test', 'test')
        self.item3 = Item(3, 'test', 'test')
        self.item4 = Item(4, 'test', 'test')
        self.player.add_item(self.item1)
        self.player.add_item(self.item2)
        self.player.add_item(self.item3)
        self.player.add_item(self.item4)


if __name__ == '__main__':
    unittest.main()
