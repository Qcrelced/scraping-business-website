import unittest
from modules.util import regex_tel


class MyTestCase(unittest.TestCase):

    def test_regex_tel(self):
        test = regex_tel('tel:+00-1-23-45-67-89')  # html href
        self.assertEqual(test, '01 23 45 67 89')


if __name__ == '__main__':
    unittest.main()
