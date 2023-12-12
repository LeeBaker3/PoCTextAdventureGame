import unittest
from tests.test_item_list import TestItemList
from tests.test_item import TestItem
from tests.test_location import TestLocation
from tests.test_player import TestPlayer

testList = [TestItemList, TestItem, TestLocation, TestPlayer]
testLoad = unittest.TestLoader()

TestList = []
for testCase in testList:
    testSuite = testLoad.loadTestsFromTestCase(testCase)
    TestList.append(testSuite)

newSuite = unittest.TestSuite(TestList)
runner = unittest.TextTestRunner()
runner.run(newSuite)
