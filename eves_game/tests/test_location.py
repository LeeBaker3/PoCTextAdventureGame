import unittest
from src.locations import location


class TestLocation(unittest.TestCase):

    def setUp(self) -> None:
        self.moves = {'1', 'Leave the scratch through the entrance'}
        self.item_ids = ['1']
        self.testLocation = location.Location('1', 'Scratch', 'Serves delightful dark beers. You can see some peanuts, the entrance door, and some comfy old seats',
                                              self.item_ids, self.moves)

    def test_moves_length(self) -> None:
        """_summary_
        Test that the movesLength property is set to the correct value i.e.
        the number of moves available
        """
        self.assertEqual(self.testLocation.movesLength, len(self.moves))

    def test_items_length(self) -> None:
        """_summary_
        Test that the itemLength property is set to the correct value i.e.
        the number of items available
        """
        self.assertEqual(self.testLocation.itemsLength, len(self.item_ids))


if __name__ == '__main__':
    unittest.main()
