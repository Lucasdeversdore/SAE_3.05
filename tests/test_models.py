import unittest
import os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(os.path.abspath(ROOT))
import nomDB
from app.app import app
from app.models import *
from app.app import app


class Testing(unittest.TestCase):
    """
    On utilsera une base de données test pour effectuer les tests
    """
    def test_chercher_produit(self):
        with app.app_context():
            self.assertEqual(search_filter(""), get_all_prod())
            self.assertEqual(search_filter("make"), [])
            self.assertEqual(search_filter("acide"), Produit.query.filter(Produit.nomProduit.contains("acide")).all())
            self.assertEqual(search_filter("ACIDE"), Produit.query.filter(Produit.nomProduit.contains("acide")).all())

    def test_chercher_famille_produit(self):
        with app.app_context():
            self.assertEqual(search_famille_filter(""), get_all_prod())
            self.assertEqual(search_famille_filter("make"), [])
            self.assertEqual(search_famille_filter("ajuste"), Produit.query.filter(Produit.fonctionProduit == "ajusteur de pH").all())

    def test_reserver_qte_produit(self):
        #TODO Terminer le test
        pass
    def test_modifier_qte_produit(self):
        #TODO Terminer le test
        pass
    def test_delete_reservation(self):
        #TODO Terminer le test
        pass
    def test_get_res_produit(self):
        #TODO Terminer le test
        pass
    def test_get_res_etudiant(self):
        #TODO Terminer le test
        pass
    def test_edit_produit(self):
        #TODO Terminer le test
        pass
    def test_add_produit(self):
        #TODO Terminer le test
        pass
    def test_delete_produit(self):
        #TODO Terminer le test
        pass
    def test_inscription(self):
        #TODO Terminer le test
        pass
    def test_check_mdp(self):
        mdp1 = ""
        mdp2 = "abcdefer"
        mdp3 = "Abd"
        mdp4 = "A/45"
        mdp5 = "Abdgfh45"
        mdp6 = "A*jkfsksjjbfsb"
        mdp7 = "klfneefn45*\\"
        mdp10 = "AERTS4/M"
        mdp11 = "ADjf45@f"
        self.assertEqual(check_mdp(mdp1), False)
        self.assertEqual(check_mdp(mdp2), False)
        self.assertEqual(check_mdp(mdp3), False)
        self.assertEqual(check_mdp(mdp4), False)
        self.assertEqual(check_mdp(mdp5), False)
        self.assertEqual(check_mdp(mdp6), False)
        self.assertEqual(check_mdp(mdp7), False)
        self.assertEqual(check_mdp(mdp10), True)
        self.assertEqual(check_mdp(mdp11), True)



if __name__ == "__main__":
    test = Testing()
    test.recherche