import unittest
from item_list import ItemList
from item import Item


class TestItemList(unittest.TestCase):

    def setUp(self) -> None:
        self.maxLength = 3
        self.item_list = ItemList()
        self.item_list.maxListLength = self.maxLength

    def test_item_list_maxListLength(self) -> None:
        self.assertEqual(3, self.item_list.maxListLength)

    def test_item_list_append_item(self) -> None:
        item1 = Item(1, 'test', 'test')
        self.item_list.append(item1)
        self.assertEqual(1, len(self.item_list))

    def test_item_list_raise_append_exception(self) -> None:
        item1 = Item(1, 'test', 'test')
        item2 = Item(2, 'test', 'test')
        item3 = Item(3, 'test', 'test')
        item4 = Item(4, 'test', 'test')
        self.item_list.append(item1)
        self.item_list.append(item2)
        self.item_list.append(item3)

        with self.assertRaises(Exception) as cm:
            self.item_list.append(item4)

        self.assertEqual(str(cm.exception), f"Can't have more than {
                         self.maxLength} items")
