import unittest
import logging
from src.action_factory import ActionFactory
from src.actions import move_location, pick_up
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
        self.items = {self.item.item_id, self.item}

        self.moves = {'1', 'Leave the scratch through the entrance'}
        self.item_ids = ['1']
        self.location = Location('1', 'Scratch', 'Serves delightful dark beers. You can see some peanuts, the entrance door, and some comfy old seats',
                                 self.item_ids, self.moves)

        self.locations = [self.location]

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel('DEBUG')
        self.formatter = logging.Formatter(
            "%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
        self.file_handler = logging.FileHandler('test_log.txt')
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        self.logger.info("Logger created\n.")

        self.actionFactory = ActionFactory()
        return super().setUpClass()

    def test_create_pick_up_action(self) -> None:
        self.pick_up = self.actionFactory.create(
            'PickUp', self.player, self.location, self.locations, self.item, self.items, self.logger, 'Pickup test item 1')
        self.assertIsInstance(self.pick_up, pick_up.PickUp)

    def test_create_move_action(self) -> None:
        self.move = self.actionFactory.create(
            'MoveLocation', self.player, self.location, self.locations, self.item, self.items, self.logger, 'Leave the scratch through the entrance')
        self.assertIsInstance(self.move, move_location.MoveLocation)
