import unittest
from tests.test_item_list import ItemList
from tests.test_item import TestItem
from tests.test_location import TestLocation
from tests.test_player import TestPlayer

testList = [ItemList, TestItem, TestLocation, TestPlayer]
# testList = [ItemList]
# testList = []
testLoad = unittest.TestLoader()

TestList = []
for testCase in testList:
    testSuite = testLoad.loadTestsFromTestCase(testCase)
    TestList.append(testSuite)

newSuite = unittest.TestSuite(TestList)
runner = unittest.TextTestRunner()
runner.run(newSuite)
