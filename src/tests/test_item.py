import unittest
from item import Item


class TestItem(unittest.TestCase):

    def setUp(self) -> None:
        self.id = '1'
        self.name = 'Rocket Fuel'
        self.description = '12% Imperial Stout'
        self.item = Item(self.id, self.name, self.description)

    def testItemCreated(self) -> None:

        self.assertEqual(self.item.item_id, self.id)
        self.assertEqual(self.item.item_name, self.name)
        self.assertEqual(self.item.item_description, self.description)


if __name__ == '__main__':
    unittest.main()
