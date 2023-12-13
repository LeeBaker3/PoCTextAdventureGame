import unittest
from item_list import ItemList
from item import Item


class TestItemList(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
    """

    @classmethod
    def setUpClass(cls):
        print(f'\n Running Test Item List Test Cases')

    def setUp(self) -> None:
        """_summary_
        """
        self.maxLength = 3
        self.item_list = ItemList()
        self.item_list.max_list_length = self.maxLength

    def test_item_list_maxListLength(self) -> None:
        """_summary_
        """
        self.assertEqual(3, self.item_list.max_list_length)

    def test_item_list_append_item(self) -> None:
        """_summary_
        """
        self.item1 = Item(1, 'test', 'test')
        self.item_list.append(self.item1)
        self.assertEqual(1, len(self.item_list))

    def test_items_in_list(self) -> None:
        """_summary_
        """
        self.item1 = Item(1, 'test', 'test')
        self.item_list.append(self.item1)
        self.assertEqual('- test\n', self.item_list.items_in_list())

    def test_item_list_raise_append_exception(self) -> None:
        """_summary_
        """
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
