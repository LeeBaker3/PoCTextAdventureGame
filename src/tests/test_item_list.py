import unittest
from item_list import ItemList
from item import Item


class TestItemList(unittest.TestCase):

    def setUp(self) -> None:
        self.maxLength = 3
        self.item_list = ItemList()
        self.item_list.max_list_length = self.maxLength

    def tearDown(self) -> None:
        return super().tearDown()

    def test_item_list_maxListLength(self) -> None:
        self.assertEqual(3, self.item_list.max_list_length)

    def test_item_list_append_item(self) -> None:
        self.item1 = Item(1, 'test', 'test')
        self.item_list.append(self.item1)
        self.assertEqual(1, len(self.item_list))

    def test_items_in_list(self) -> None:
        self.item1 = Item(1, 'test', 'test')
        self.item_list.append(self.item1)
        self.assertEqual('- test\n', self.item_list.items_in_list())

    def test_item_list_raise_append_exception(self) -> None:
        self.item1 = Item(1, 'test', 'test')
        self.item2 = Item(2, 'test', 'test')
        self.item3 = Item(3, 'test', 'test')
        self.item4 = Item(4, 'test', 'test')
        self.item_list.append(self.item1)
        self.item_list.append(self.item2)
        self.item_list.append(self.item3)

        with self.assertRaises(Exception) as cm:
            self.item_list.append(self.item4)

        self.assertEqual(str(cm.exception),
                         f"Can't have more than {self.maxLength} items")


if __name__ == '__main__':
    unittest.main()
