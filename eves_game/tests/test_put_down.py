from contextlib import AbstractContextManager
from typing import Any
import unittest
import logging
from src.actions.pick_up import PickUp
from src.actions.put_down import PutDown
from src.locations.location import Location
from src.player.player import Player
from src.items.item import Item


class TestPutDown(unittest.TestCase):

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
        self.item1 = Item('1', 'Test Item 1', 'This is a test item 1', {
                          'Pick Up': {'action_description': 'This is a test action1', 'holding': 'No'},
                          'Put Down': {'action_description': 'This is a test action3', 'holding': 'Yes'}})

        self.items = {self.item1.item_id: self.item1}

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
        self.success, self.action_return_msg = self.pickUp.action()

        self.putDown = PutDown('Put down test item 1', self.player, self.location, self.locations,
                               self.item1, self.items, self.logger)
        return super().setUp()

    def test_put_down_action(self) -> None:
        """_summary_
        Test that the PutDown object can successfully remove Test Item 2 from the Player ItemList object
        and adds it to the Location object
        """

        self.test_msg = 'You have put down Test Item 1'
        self.assertEqual(1, self.location.items_length)
        self.assertEqual(1, len(self.player.player_items))
        self.success, self.action_return_msg = self.putDown.action()
        self.assertTrue(self.success)
        self.assertEqual(self.test_msg, self.action_return_msg)
        self.assertEqual(2, self.location.items_length)
        self.assertEqual(0, len(self.player.player_items))

    def test_return_game_state(self) -> None:
        """_summary_
        Test that the PickUp object returns the correct game state after the action is executed
        """
        self.success, self.action_return_msg = self.putDown.action()
        self.assertTrue(self.success)

        player_state = self.putDown.return_game_state()[0]
        self.assertEqual(self.player, player_state)

        location_state = self.putDown.return_game_state()[1]
        self.assertEqual(self.location, location_state)

        locations_state = self.putDown.return_game_state()[2]
        self.assertEqual(self.locations, locations_state)

        item_state = self.putDown.return_game_state()[3]
        self.assertEqual(self.item1, item_state)

        items_state = self.putDown.return_game_state()[4]
        self.assertEqual(self.items, items_state)
