import unittest

import test.__init__
from csv_to_bd import get_nombre_unite

class Testing(unittest.TestCase):
    """
    On utilsera une base de données test pour effectuer les tests
    """
    def test_get_nombre_unite(self):
        self.assertTrue(get_nombre_unite(" 1250 g "), (1250, 'g'))
        self.assertTrue(get_nombre_unite(), (250, 'g'))
        self.assertTrue(get_nombre_unite(), (250, 'g'))
        self.assertTrue(get_nombre_unite(), (750, None))
        self.assertTrue(get_nombre_unite(), (750, 'g'))
        self.assertTrue(get_nombre_unite(), (750, 'g'))
        self.assertTrue(get_nombre_unite(), (1500, 'g'))
        self.assertTrue(get_nombre_unite(), (0, None))

if __name__ == "__main__":
    test = Testing()