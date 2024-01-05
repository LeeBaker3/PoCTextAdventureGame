import unittest
from src.action_factory import ActionFactory
from src.actions.pick_up import PickUp
from src.player.player import Player
from src.locations.location import Location
from src.items.item import Item


class TestActionFactory(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        self.player_name = 'Bob'
        self.player = Player(self.player_name)

        self.item_id = '1'
        self.name = 'Rocket Fuel'
        self.description = '12% Imperial Stout'
        self.actions = {'Drink': 'Tastes wonderful'}
        self.item = Item(self.item_id, self.name,
                         self.description, self.actions)

        self.moves = {'1', 'Leave the scratch through the entrance'}
        self.item_ids = ['1']
        self.location = Location('1', 'Scratch', 'Serves delightful dark beers. You can see some peanuts, the entrance door, and some comfy old seats',
                                 self.item_ids, self.moves)

        self.actionFactory = ActionFactory()
        return super().setUpClass()

    def test_action_factory_create_pick_up(self) -> None:
        self.pick_up = self.actionFactory.create(
            'PickUp', self.player, self.location, self.item)
        self.assertIsInstance(self.pick_up, PickUp)
