import unittest
import logging
from src.actions.move_location import MoveLocation
from src.locations.location import Location, Move
from src.player.player import Player
from src.items.item import Item


class TestMove(unittest.TestCase):
    def setUp(self) -> None:

        # Setup Location 1
        self.location_moves = {}
        self.location_moves['2'] = Move(
            '2', 'Scratch exit to Patio', 'Leave the scratch through the entrance to the patio', '1')
        self.location_item_ids = ['1', '2']
        self.location_description = 'Serves delightful dark beers. You can see some peanuts, the entrance door, and some comfy old seats'
        self.location_id = '1'
        self_location_name = 'Scratch'
        self.location = Location(
            self.location_id, self_location_name, self.location_description, self.location_item_ids, self.location_moves)

        # Setup Location 2
        self.location_2_moves = {}
        self.location_2_moves['1'] = Move(
            '1', 'Enter Scratch from the Patio', 'Enter the scratch through the entrance', '1')
        self.location_2_item_ids = []
        self.location_2_description = 'Patio of the Scratch. You can see some delightful beers inside'
        self.location_2_id = '2'
        self_location_2_name = 'Patio'
        self.location_2 = Location(
            self.location_2_id, self_location_2_name, self.location_2_description, self.location_2_item_ids, self.location_2_moves)

        self.locations = {self.location_id: self.location,
                          self.location_2_id: self.location_2}

        self.current_location = self.locations['1']

        # Setup Player
        self.player_name = 'Bob'
        self.max_item_length = 2
        self.player = Player(self.player_name, self.max_item_length)

        # Setup Item
        self.item1 = Item('2', 'Test Item 2', 'This is a test item 2', {
                          'Pick Up': {'action_description': 'This is a test action2', 'holding': 'No'}})

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel('DEBUG')
        self.formatter = logging.Formatter(
            "%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
        self.file_handler = logging.FileHandler('test_log.txt')
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        self.logger.info("Logger created\n.")

        self.move = MoveLocation('Leave the scratch through the entrance to the patio', self.player, self.current_location, self.locations,
                                 self.item1, self.logger)
        return super().setUp()

    def test_move_action_successful(self) -> None:
        """
        Test that the Move object can successfully move locations.

        This test verifies that the Move object is able to move to a different location
        and that the expected messages and location ID are returned correctly.
        """
        self.test_msg = f"You have moved to {self.location_2_description}"
        self.success, self.action_return_msg = self.move.action()
        self.assertTrue(self.success)
        self.assertEqual(self.test_msg, self.action_return_msg)
        self.assertEqual('2', self.move.location.location_id)


if __name__ == '__main__':
    unittest.main()
