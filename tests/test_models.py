import unittest
import os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(os.path.abspath(ROOT))
import nomDB
from app.models import *
from app.app import app



class Testing(unittest.TestCase):
    """
    On utilsera une base de données test pour effectuer les tests
    """
    def test_chercher_produit(self):
        with app.app_context():
            
            self.assertEqual(search_filter(""), get_all_prod_qte())
            self.assertEqual(search_filter("make"), [])
            #self.assertEqual(search_filter("acide"), Produit.query.filter(Produit.nomProduit.contains("acide")).all())
            #self.assertEqual(search_filter("ACIDE"), Produit.query.filter(Produit.nomProduit.contains("acide")).all())

    def test_chercher_famille_produit(self):
        with app.app_context():
            self.assertEqual(search_famille_filter(""), get_all_prod_qte())
            self.assertEqual(search_famille_filter("make"), [])
            #self.assertEqual(search_famille_filter("ajuste"), Produit.query.filter(Produit.fonctionProduit == "ajusteur de pH").all())

    def test_reserver_qte_produit(self):
        with app.app_context():
            prod = Produit.query.filter(Produit.idProduit == 2).first()
            id_prod = prod.idProduit 
            
            qte1 = 10
            qte2 = 190 
            qte3 = 0
            qte4 = None
            id_chimiste1 = 1
            id_chimiste2 = 2
            
            r1 = reserver_prod(id_prod, qte1, id_chimiste1)
            commande1 = Commande.query.filter(Commande.idCommande == next_commande_id()-1).first()
            user1 = commande1.idChimiste

            r2 = reserver_prod(id_prod, qte2, id_chimiste2)
            commande2 = Commande.query.filter(Commande.idCommande == next_commande_id()-1).first()
            user2 = commande2.idChimiste

            r3 = reserver_prod(id_prod, qte3, id_chimiste1)
            r4 = reserver_prod(id_prod, qte4, id_chimiste1)


            self.assertEqual(r1, True)
            self.assertEqual(user1, id_chimiste1)

            self.assertEqual(r2, True)
            self.assertEqual(user2, id_chimiste2)
            
            self.assertEqual(r3, None)
            self.assertEqual(r4, None)
            
            
    

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
        nom1 = "abc"
        nom2 = "1abd"
        nom3 = ""
        nom4 = None
        nom_four1 = "abc"
        nom_four2 = "1abd"
        nom_four3 = ""
        nom_four4 = ""
        unite5 = "L"
        unite1 = "abc"
        unite2 = "1abd"
        unite3 = ""
        unite4 = None
        quantite1 = 5
        quantite2 = 0
        quantite3 = "5.6"
        quantite4 = "a"
        quantite5 = None
        fonction1 = "test"
        fonction2 = ""
        fonction3 = None
        lieu1 = "armoire"
        lieu2 = "lieu_test"
        lieu3 = None
        seuil = 1
        with app.app_context():
            id_four = Fournisseur.query.filter(Fournisseur.nomFou == "").first().idFou
            ajout_sauvegarde(nom1, nom_four1, unite1, quantite1, seuil, fonction1, lieu1)
            id_prod = next_prod_id()-1
            fournisseur = Fournisseur.query.filter_by(nomFou=nom_four1).first()
            prod1 = Produit.query.filter(Produit.idProduit == id_prod).first().to_dict()
            testprod1 = {
                'idProduit': id_prod,
                'nomProduit': nom1,
                'nomUnite': unite1,
                'seuilProduit': 1,
                'afficher': True,
                'fonctionProduit' : fonction1,
                'idFou': fournisseur.idFou
            }
            stock = Est_Stocker.query.filter(Est_Stocker.idProduit == id_prod).first()
            testqte1 = stock.quantiteStocke
            testlieu1 = Lieu_Stockage.query.filter(Lieu_Stockage.idLieu == stock.idLieu).first().nomLieu


            ajout_sauvegarde(nom2, nom_four2, unite2, quantite2, seuil, fonction2, lieu2)
            id_prod = next_prod_id()-1
            fournisseur = Fournisseur.query.filter_by(nomFou=nom_four2).first()
            prod2 = Produit.query.filter(Produit.idProduit == id_prod).first().to_dict()
            testprod2 = {
                'idProduit': id_prod,
                'nomProduit': nom2,
                'nomUnite': unite2,
                'seuilProduit': 1,
                'afficher': True,
                'fonctionProduit' : fonction2,
                'idFou': fournisseur.idFou
            }
            stock = Est_Stocker.query.filter(Est_Stocker.idProduit == id_prod).first()
            testqte2 = stock.quantiteStocke
            testlieu2 = Lieu_Stockage.query.filter(Lieu_Stockage.idLieu == stock.idLieu).first().nomLieu
            
            ajout_sauvegarde(nom2, nom_four3, unite3, quantite3, seuil, fonction3, lieu3)
            id_prod = next_prod_id()-1
            prod3 = Produit.query.filter(Produit.idProduit == id_prod).first().to_dict()
            testprod3 = {
                'idProduit': id_prod,
                'nomProduit': nom2,
                'nomUnite': unite3,
                'seuilProduit': 1,
                'afficher': True,
                'fonctionProduit' : fonction3,
                'idFou': id_four
            }
            stock = Est_Stocker.query.filter(Est_Stocker.idProduit == id_prod).first()
            testqte3 = stock.quantiteStocke
            testlieu3 = Lieu_Stockage.query.filter(Lieu_Stockage.idLieu == stock.idLieu).first().nomLieu

            ajout_sauvegarde(nom2, nom_four4, unite4, quantite4, seuil, fonction3, lieu3)
            id_prod = next_prod_id()-1
            prod4 = Produit.query.filter(Produit.idProduit == id_prod).first().to_dict()
            testprod4 = {
                'idProduit': id_prod,
                'nomProduit': nom2,
                'nomUnite': unite4,
                'seuilProduit': 1,
                'afficher': True,
                'fonctionProduit' : fonction3,
                'idFou': id_four
            }
            stock = Est_Stocker.query.filter(Est_Stocker.idProduit == id_prod).first()
            testqte4 = stock.quantiteStocke

            ajout_sauvegarde(nom2, nom_four4, unite5, quantite5, seuil, fonction3, lieu3)
            id_prod = next_prod_id()-1
            prod5 = Produit.query.filter(Produit.idProduit == id_prod).first().to_dict()
            testprod5 = {
                'idProduit': id_prod,
                'nomProduit': nom2,
                'nomUnite': unite5,
                'seuilProduit': 1,
                'afficher': True,
                'fonctionProduit' : fonction3,
                'idFou': id_four
            }
            stock = Est_Stocker.query.filter(Est_Stocker.idProduit == id_prod).first()
            testqte5 = stock.quantiteStocke

            id_prod_av=  next_prod_id()-1
            ajout_sauvegarde(nom3, nom_four4, unite5, quantite5, seuil, fonction3, lieu3)
            id_prod_6 = next_prod_id()-1

            ajout_sauvegarde(nom4, nom_four4, unite5, quantite5, seuil, fonction3, lieu3)
            id_prod_7 = next_prod_id()-1


            self.assertEqual(prod1,testprod1)
            self.assertEqual(quantite1, testqte1)
            self.assertEqual(lieu1, testlieu1)

            self.assertEqual(prod2,testprod2)
            self.assertEqual(quantite2, testqte2)
            self.assertEqual(lieu2, testlieu2)

            self.assertEqual(prod3,testprod3)
            self.assertEqual(float(quantite3), testqte3)
            self.assertEqual(lieu3, testlieu3)

            self.assertEqual(prod4,testprod4)
            self.assertEqual(0, testqte4)

            self.assertEqual(prod5,testprod5)
            self.assertEqual(0, testqte5)

            self.assertEqual(id_prod_av,id_prod_6)
            self.assertEqual(id_prod_av,id_prod_7)
            



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
        self.assertEqual(check_mdp(mdp1), (False, "mdp doit contenir au moins : 1 majuscule, 1 caractère spécial, 1 chiffre et doit faire au moins 8 caractères"))
        self.assertEqual(check_mdp(mdp2), (False, "mdp doit contenir au moins : 1 majuscule, 1 caractère spécial, 1 chiffre et doit faire au moins 8 caractères"))
        self.assertEqual(check_mdp(mdp3), (False, "mdp doit contenir au moins : 1 majuscule, 1 caractère spécial, 1 chiffre et doit faire au moins 8 caractères"))
        self.assertEqual(check_mdp(mdp4), (False, "mdp doit contenir au moins : 1 majuscule, 1 caractère spécial, 1 chiffre et doit faire au moins 8 caractères"))
        self.assertEqual(check_mdp(mdp5), (False, "mdp doit contenir au moins : 1 majuscule, 1 caractère spécial, 1 chiffre et doit faire au moins 8 caractères"))
        self.assertEqual(check_mdp(mdp6), (False, "mdp doit contenir au moins : 1 majuscule, 1 caractère spécial, 1 chiffre et doit faire au moins 8 caractères"))
        self.assertEqual(check_mdp(mdp7), (False, "mdp doit contenir au moins : 1 majuscule, 1 caractère spécial, 1 chiffre et doit faire au moins 8 caractères"))
        self.assertEqual(check_mdp(mdp10), (True,""))
        self.assertEqual(check_mdp(mdp11), (True,""))

    def test_convertir_quantite(self):
        with app.app_context():
            prod1 = Produit.query.filter(Produit.idProduit == 3).first()
            id_prod = prod1.idProduit 
            stock = Est_Stocker.query.filter(Est_Stocker.idProduit == prod1.idProduit).first()
            stock_base= stock.quantiteStocke
            
            stock.quantiteStocke = 2000
            convertir_quantite(id_prod)
            self.assertEqual(stock.quantiteStocke, 2)
            self.assertEqual(prod1.nomUnite, "kg")
            stock.quantiteStocke = 0.1
            convertir_quantite(id_prod)
            self.assertEqual(stock.quantiteStocke, 100)
            self.assertEqual(prod1.nomUnite, "g")
            stock.quantiteStocke = stock_base

            prod2 = Produit.query.filter(Produit.idProduit == 4).first()
            id_prod = prod2.idProduit 
            stock2 = Est_Stocker.query.filter(Est_Stocker.idProduit == prod2.idProduit).first()
            stock_base= stock2.quantiteStocke

            stock2.quantiteStocke = 2000
            convertir_quantite(id_prod)
            self.assertEqual(stock2.quantiteStocke, 2)
            self.assertEqual(prod2.nomUnite, "L")
            stock2.quantiteStocke = 0.1
            convertir_quantite(id_prod)
            self.assertEqual(stock2.quantiteStocke, 100)
            self.assertEqual(prod2.nomUnite, "mL")
            stock2.quantiteStocke = stock_base

    def test_modif_sauvegarde(self):
        with app.app_context():
       
            produit = Produit.query.get(1)
            add_fournisseur("NouveauFournisseur","","")
            add_lieu_stock("NouveauLieu")
            
            success = modif_sauvegarde(produit.idProduit, "NouveauNom", "NouveauFournisseur", 50,1, "NouvelleFonction", "NouveauLieu")

            # Vérifier que la mise à jour a bien eu lieu
            produit_modif = Produit.query.get(produit.idProduit)
            stock = Est_Stocker.query.filter(Est_Stocker.idProduit == produit_modif.idProduit).first()
            
            self.assertTrue(success)
            self.assertEqual(produit_modif.nomProduit, "NouveauNom")
            self.assertEqual(produit_modif.fonctionProduit, "NouvelleFonction")
            self.assertEqual(stock.quantiteStocke, 50)
            self.assertEqual(produit_modif.idFou, next_fou_id()-1)

    
    def test_get_id_lieu(self):
        with app.app_context():
            id = get_id_lieu("réserve")
            lieu = Lieu_Stockage.query.get(id)
            self.assertEqual(lieu.nomLieu, "réserve")

    def test_add_est_stocker(self):
        with app.app_context():
            add_est_stocker(2,2,150)
            stock1 = Est_Stocker.query.filter(Est_Stocker.idProduit == 2).first()
            self.assertEqual(stock1.quantiteStocke, 350) # 200 de base + 150 = 350

            add_prod("teststock", "L", 1, "teef", "Esperis")
            add_est_stocker(next_prod_id()-1, 1, 50)
            stock2 = Est_Stocker.query.filter(Est_Stocker.idProduit == next_prod_id()-1).first()
            self.assertEqual(stock2.quantiteStocke, 50)

    def test_get_sample_reservation(self):
        with app.app_context():
            reserver_prod(1,1,1)
            chimiste = Chimiste.query.get(1)
            prod = Produit.query.get(1)
            res = get_sample_reservation(3)
            #res = Commande.query.all()
            c1 = Commande.query.get(1) 
            li_commandes = [(c1, "non-commence", chimiste, prod)]
            self.assertEqual(res, li_commandes)

    def test_get_sample_reservation_chimiste(self):
        with app.app_context():
            reserver_prod(1,1,1)
            chimiste = Chimiste.query.get(1)
            prod = Produit.query.get(1)
            res = get_sample_reservation_chimiste(chimiste)
            #res = Commande.query.all()
            c1 = Commande.query.get(1) 
            li_commandes = [(c1, "non-commence", chimiste, prod)]
            self.assertEqual(res, li_commandes)


    def test_next_chimiste_id(self):
        with app.app_context():
           nb_chimiste = db.session.query(func.max(Chimiste.idChimiste)).scalar()
           self.assertEqual(nb_chimiste+1, next_chimiste_id()) 


    def test_load_user(self):
        with app.app_context():
            email = "email.dev@gmail.com"
            c = Chimiste.query.get(email)
            self.assertEqual(c, load_user(email))

    def test_ajout_lieu_sauvegarde(self):
        with app.app_context():
            nom = "new lieu"
            ajout_lieu_sauvegarde(nom)
            lieu = Lieu_Stockage.query.get(next_lieu_id()-1)
            self.assertEqual(lieu.nomLieu, nom)

    def test_ajout_fournisseur_sauvegarde(self):
        with app.app_context():
            nom = "new fournisseur"
            ajout_fournisseur_sauvegarde(nom)
            fou = Fournisseur.query.get(next_fou_id()-1)
            self.assertEqual(fou.nomFou, nom)

            self.assertEqual(ajout_fournisseur_sauvegarde(nom), False)

    
    def test_est_en_dessous_du_seuil(self):
        with app.app_context():
            add_prod("prod", "kg", 50, "fonction", "four")
            prod = Produit.query.get(next_prod_id()-1)

            add_prod("prod2", "kg", 50, "fonction", "four")
            add_est_stocker(next_prod_id()-1, 1, 10.0)
            prod2 = Produit.query.get(next_prod_id()-1)

            liste = est_en_dessous_du_seuil() 
            self.assertIn((prod, 0, "kg"), liste)
            self.assertIn((prod2, 10.0, "kg"), liste)

    def test_search_reserv_filter(self):
        with app.app_context():
            liste = search_reserv_filter("NouveauNom")
            prod = Produit.query.get(1)
            commande = Commande.query.get(1)
            chimiste = Chimiste.query.get(1)
            self.assertEqual(liste, [(commande, 'non-commence', chimiste, prod)])

    def test_search_chimiste_filter(self):
        with app.app_context():
            liste = search_chimiste_filter("etu")
            chimiste = Chimiste.query.get(3)
            self.assertEqual(liste, [])





if __name__ == "__main__":
    test = Testing()