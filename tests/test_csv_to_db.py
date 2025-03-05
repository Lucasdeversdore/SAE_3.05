import unittest
import os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(os.path.abspath(ROOT))
from app.csv_to_db import get_nombre_unite, get_unite

class Testing(unittest.TestCase):
    """
    On utilsera une base de données test pour effectuer les tests
    """
    def test_get_nombre_unite(self):
        self.assertEqual(get_nombre_unite(" 1250 g "), (1250, 'g'))
        self.assertEqual(get_nombre_unite("250g"), (250, 'g'))
        self.assertEqual(get_nombre_unite("250 g"), (250, 'g'))
        self.assertEqual(get_nombre_unite("3*250"), (750, None))
        self.assertEqual(get_nombre_unite("3*250g"), (750, 'g'))
        self.assertEqual(get_nombre_unite("3*250 g"), (750, 'g'))
        self.assertEqual(get_nombre_unite("3*250*2 g"), (1500, 'g'))
        self.assertEqual(get_nombre_unite(" "), (0, None))

    def test_get_unite(self):
        self.assertEqual(get_unite("G"), "g")
        self.assertEqual(get_unite("g"), "g")
        self.assertEqual(get_unite("KG"), "kg")
        self.assertEqual(get_unite("Kg"), "kg")
        self.assertEqual(get_unite("kG"), "kg")
        self.assertEqual(get_unite("kg"), "kg")
        self.assertEqual(get_unite("ML"), "mL")
        self.assertEqual(get_unite("Ml"), "mL")
        self.assertEqual(get_unite("mL"), "mL")
        self.assertEqual(get_unite("ml"), "mL")
        self.assertEqual(get_unite("L"), "L")
        self.assertEqual(get_unite("l"), "L")
        self.assertEqual(get_unite("test"), "test")

if __name__ == "__main__":
    test = Testing()
    print(get_nombre_unite("3*250"))