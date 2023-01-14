import unittest
from test import support

class TestCase1(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testFeature1(self):
        return True

    def testFeature2(self):
        return True

if __name__ == '__main__':
    unittest.main()
