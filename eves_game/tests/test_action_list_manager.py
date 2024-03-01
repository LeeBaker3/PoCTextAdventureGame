import unittest
import logging
from src.action_list_manager import ActionListManager, ActionReference
from src.player.player import Player
from src.locations.location import Location, Move
from src.items.item import Item


class TestActionListManager(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        self.player_name = 'Bob'
        self.player = Player(self.player_name)

        self.item_id = '3'
        self.name = 'Rocket Fuel'
        self.description = '12% Imperial Stout'
        self.actions = {'Drink': {
            'action_description': 'Sip thr 12% Imperial Stout. It tastes wonderful', 'action_id': '3', 'holding': 'Yes'}}
        self.item1 = Item(self.item_id, self.name,
                          self.description, self.actions)

        _ = self.player.add_item(self.item1)

        self.item4 = Item('4', '$10 Note', 'Some lovely Money',
                          {'Pick Up':
                           {'action_description': 'You pick up a $10 note', 'action_id': '4', 'holding': 'No'}})

        self.moves = {}
        self.moves['1'] = Move(
            '1', 'Move', 'Leave the scratch through the entrance', '2')
        self.item_ids = ['3', '4']
        self.location1 = Location('1', 'Scratch', 'Serves delightful dark beers. You can see some peanuts, the entrance door, and some comfy old seats',
                                  self.item_ids, self.moves)

        self.locations = [self.location1]

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel('DEBUG')
        self.formatter = logging.Formatter(
            "%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
        self.file_handler = logging.FileHandler('test_log.txt')
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        self.logger.info("Logger created\n.")

        self.item2 = Item('1', 'Test Item 1', 'This is a test item 1', {
                          'Put Down': {'action_description': 'This is a test action1', 'action_id': '0', 'holding': 'Yes'}})

        self.item3 = Item('2', 'Test Item 2', 'This is a test item 2', {
                          'Pick Up': {'action_description': 'This is a test action2', 'action_id': '1', 'holding': 'No'}})

        self.items = {}
        self.items[self.item1.item_id] = self.item1
        self.items[self.item2.item_id] = self.item2
        self.items[self.item3.item_id] = self.item3
        self.items[self.item4.item_id] = self.item4

        self.locations = {}
        self.locations[self.location1.location_id] = self.location1

        self.action_list_manager = ActionListManager(
            self.location1, self.player, self.items, self.locations, self.logger)

        self.action_reference1 = ActionReference(
            '3', 'Drink', 'Sip thr 12% Imperial Stout. It tastes wonderful', 'player')
        self.action_reference2 = ActionReference(
            '0', 'Put Down', 'This is a test action1', 'player')
        self.action_reference3 = ActionReference(
            '1', 'Pickup', 'This is a test action2', 'location')
        self.action_reference4 = ActionReference(
            '4', 'Pick Up', 'You pick up a $10 note', 'location')
        self.action_reference5 = ActionReference(
            '1', 'Move', 'Leave the scratch through the entrance', 'move_location')

        return super().setUpClass()

    def test_create_action_list_manager(self) -> None:
        """
        Test case for creating an ActionListManager.

        It asserts that the ActionListManager is initialized correctly with the expected attributes.

        Returns:
            None
        """
        self.assertTrue(len(self.action_list_manager.items), 3)
        self.assertTrue(vars(self.logger), vars(
            self.action_list_manager.logger))
        self.assertTrue(vars(self.player), vars(
            self.action_list_manager.player))
        self.assertTrue(vars(self.location1), vars(
            self.action_list_manager.location))

    def test_location_items_actions(self) -> None:
        """
        Test case for the _location_items_actions method of the ActionListManager class.
        """
        self.action_list_manager._location_actions()
        self.assertEqual(vars(self.action_reference4), vars(
            self.action_list_manager.action_reference_list[0]))

    def test_location_move_actions(self) -> None:
        """
        Test case for the _location_move_actions method of the ActionListManager class.
        """
        self.action_list_manager._location_move_actions()
        self.assertEqual(vars(self.action_reference5), vars(
            self.action_list_manager.action_reference_list[0]))

    def test_get_list_of_item_actions(self) -> None:
        """
        Test case for the get_list_of_item_actions method of the ActionListManager class.
        """
        self.action_list_manager.create_action_reference_list()
        self.assertEqual(self.action_list_manager.get_list_of_location_action_descriptions(), [
            'You pick up a $10 note'])

    def test_get_list_of_move_actions(self) -> None:
        """
        Test case for the get_list_of_move_actions method of the ActionListManager class.
        """
        self.action_list_manager.create_action_reference_list()
        self.assertEqual(self.action_list_manager.get_list_of_move_action_descriptions(), [
                         'Leave the scratch through the entrance'])

    def test_get_action_type_for_action_description(self) -> None:
        """
        Test case for the get_action_type_for_action_description method of the ActionListManager class.
        """
        self.action_list_manager.create_action_reference_list()
        self.assertEqual(self.action_list_manager.get_action_type_for_action_description(
            'You pick up a $10 note'), 'location')
        self.assertEqual(self.action_list_manager.get_action_type_for_action_description(
            'Leave the scratch through the entrance'), 'move_location')
        self.assertEqual(self.action_list_manager.get_action_type_for_action_description(
            'Sip thr 12% Imperial Stout. It tastes wonderful'), 'player')
