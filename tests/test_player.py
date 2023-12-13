import unittest
from src.player.player import Player
from src.items.item import Item


class TestPlayer(unittest.TestCase):

    def setUp(self) -> None:
        self.player = Player('Lee')
        return super().setUp()

    def test_player_name(self) -> None:
        """_summary_
        Test that the player_name property is correctly set
        """
        self.assertEqual('Lee', self.player.player_name)

    def test_player_max_item_length_default(self) -> None:
        """_summary_
        Test that the player max_item_length property default
        is set to 3
        """
        self.assertEqual(3, self.player.max_item_length)

    def test_player_max_item_length_change(self) -> None:
        """_summary_
        Test that the player max_item_length property can be
        changed from the default value.
        """
        self.player.max_item_length = 5
        self.assertEqual(5, self.player.max_item_length)

    def test_player_to_many_items(self) -> None:
        """_summary_
        Test that the number of Item objects a player can add does not exceed
        the maxLength property and that an Exception is raised if an attempt
        is made to exceed maxLength property value.
        """
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
