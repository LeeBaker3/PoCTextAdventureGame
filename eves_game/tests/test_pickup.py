from contextlib import AbstractContextManager
from typing import Any
import unittest
import logging
from src.actions.pick_up import PickUp
from src.locations.location import Location
from src.player.player import Player
from src.items.item import Item


class TestPickUp(unittest.TestCase):
    def setUp(self) -> None:

        # Setup Location
        self.location_moves = {'1': 'Leave the scratch through the entrance'}
        self.location_item_ids = ['1', '2']
        self.location_description = 'Serves delightful dark beers. You can see some peanuts, the entrance door, and some comfy old seats'
        self.location_id = '1'
        self_location_name = 'Scratch'
        self.location = Location(
            self.location_id, self_location_name, self.location_description, self.location_item_ids, self.location_item_ids)

        self.locations = {self.location_id: self.location}

        # Setup Player
        self.player_name = 'Bob'
        self.max_item_length = 2
        self.player = Player(self.player_name, self.max_item_length)

        # Setup Item
        self.item1 = Item('2', 'Test Item 2', 'This is a test item 2', {
                          'Pick Up': {'action_description': 'This is a test action2', 'holding': 'No'}})
        
        self.items{self.item1.item_id: self.item1}

        # Setup Logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel('DEBUG')
        self.formatter = logging.Formatter(
            "%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
        self.file_handler = logging.FileHandler('test_log.txt')
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        self.logger.info("Logger created\n.")

        self.pickUp = PickUp('Pickup test item 1', self.player, self.location, self.locations,
                             self.item1, self.items, self.logger)
        return super().setUp()

    def test_pickup_action_successful(self) -> None:
        """_summary_
        Test that the PickUp object can successfully adds Test Item 1 to the Player ItemList object
        and removes it from the Location object
        """

        self.test_msg = 'You have picked up Test Item 2'
        self.success, self.action_return_msg = self.pickUp.action()
        self.assertTrue(self.success)
        self.assertEqual(self.test_msg, self.action_return_msg)
        self.assertEqual(1, self.location.items_length)

    def test_action_maximum_number_of_items(self) -> None:
        """_summary_
        Test that when a player is already holding the maximum number of items. No more items
        can be picked up
        """
        self.player.max_item_length = 0
        self.test_msg = 'Sorry, you are already holding the maximum number of items'
        self.success, self.action_return_msg = self.pickUp.action()
        self.assertFalse(self.success)
        self.assertEqual(self.test_msg, self.action_return_msg)
        self.assertEqual(2, self.location.items_length)


if __name__ == '__main__':
    unittest.main()
