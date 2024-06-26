import unittest
from src.items.item import Item, LoadItems


class TestLoadItems(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
    """

    def setUp(self) -> None:
        self.items_dict = {}
        self.xml_file_name = 'items_test_file.xml'
        self.xml_file_path = 'eves_game/tests/'
        self.loadItems = LoadItems(
            self.items_dict, self.xml_file_path + self.xml_file_name)
        self.loadItems.load()

        self.item1 = Item('1', 'Test Item 1', 'This is a test item 1', {
                          'Pick Up': {'action_description': 'This is a test action1', 'action_id': '0', 'holding': 'No'},
                          'Put Down': {'action_description': 'This is a test action3', 'action_id': '3', 'holding': 'Yes'}})

        self.item2 = Item('2', 'Test Item 2', 'This is a test item 2', {
                          'Pick Up': {'action_description': 'This is a test action2', 'action_id': '1', 'holding': 'No'}})

        return super().setUp()

    def test_add_two_items(self) -> None:
        self.test_item_dict = self.loadItems.items
        self.test_item1 = self.test_item_dict['1']
        self.test_item2 = self.test_item_dict['2']
        self.assertEqual(len(self.test_item_dict), 2)
        self.assertEqual(vars(self.test_item1), vars(self.item1))
        self.assertEqual(vars(self.test_item2), vars(self.item2))
