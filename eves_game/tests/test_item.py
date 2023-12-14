import unittest
from src.items.item import Item


class TestItem(unittest.TestCase):

    def setUp(self) -> None:
        self.item_id = '1'
        self.name = 'Rocket Fuel'
        self.description = '12% Imperial Stout'
        self.item = Item(self.item_id, self.name, self.description)

    def test_item_created(self) -> None:
        """_summary_
        Test that an Item object is created
        """
        self.assertEqual(self.item.item_id, self.item_id)
        self.assertEqual(self.item.item_name, self.name)
        self.assertEqual(self.item.item_description, self.description)


if __name__ == '__main__':
    unittest.main()
