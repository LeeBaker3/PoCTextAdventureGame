import unittest
from locations import location


class TestLocation(unittest.TestCase):

    def setUp(self) -> None:
        self.moves = {'1', 'Leave the scratch through the entrance'}
        self.item_ids = ['1']
        self.testLocation = location.Location('1', 'Scratch', 'Serves delightful dark beers. You can see some peanuts, the entrance door, and some comfy old seats',
                                              self.item_ids, self.moves)

    def testMovesLength(self) -> None:
        self.assertEqual(self.testLocation.itemsLength, len(self.item_ids))

    def testItemsLength(self) -> None:
        self.assertEqual(self.testLocation.movesLength, len(self.moves))
