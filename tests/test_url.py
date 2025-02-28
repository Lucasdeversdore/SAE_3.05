import base64
import os
import sys
import time
import unittest

from app.views import logout
from app.models import Chimiste, Produit




ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(os.path.abspath(ROOT))

from app.app import app, db
from flask_login import login_user
from app.models import Chimiste, Commande, Faire
from flask import request


class Testing(unittest.TestCase):
    def setUp(self):
        """Set up a test client and other test configurations."""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def login_laborentain(self):
        user = Chimiste.query.filter(Chimiste.email == "email.dev@gmail.com").first()
        login_user(user)

    def login_eleve(self):
        user = Chimiste.query.filter(Chimiste.email == "etudiant@gmail.com").first()
        login_user(user)
    
    def logout(self):
        logout()


    def test_inscrire(self):
        response = self.client.get('/inscription')
        self.assertEqual(response.status_code, 200)

    def test_cgu(self):
        response = self.client.get('/inscription-cgu')
        self.assertEqual(response.status_code, 200)
    
    def test_activation_token(self):
        with app.app_context():
            timer = time.time()
            new_c=Chimiste(999,"tr","tr","aeaaaa@fjfj.fr","mdp", False)
            token = new_c.get_token()
            encoded_time = base64.urlsafe_b64encode(str(timer).encode()).decode()
            response = self.client.get('/activation/'+token+'/'+str(encoded_time))
            self.assertEqual(response.status_code, 302)

    def test_connection(self):
        response = self.client.get('/connection')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

    def test_reset_pwd(self):
        response = self.client.get('/reset_pwd')
        self.assertEqual(response.status_code, 200)

    def test_reset_token(self):
        with app.test_request_context():
            # Simule la génération d'un vrai token pour le test
            user = Chimiste.query.first()  # Prends un utilisateur existant
            token = user.get_token()  # Génère un token de réinitialisation
            timestamp = str(int(time.time())).encode()  # Convertir en bytes
            time_in_link = base64.urlsafe_b64encode(timestamp).decode()  # Encodage base64
    
            # Fait une requête avec un token et une timestamp valide
            response = self.client.get(f'/reset_pwd/{token}/{time_in_link}', follow_redirects=True)
    
            # Vérifie que la page charge correctement (redirection vers le formulaire)
            self.assertEqual(response.status_code, 200)


    def test_home(self):
        with app.test_request_context():
            self.login_laborentain()
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.logout()

            self.login_eleve()
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.logout()

            response = self.client.get('/')
            self.assertEqual(response.status_code, 302)
            self.assertIn("/connection?next=%2F", response.headers["Location"])


    def test_home_page(self):
        with app.test_request_context():
            self.login_laborentain()
            response = self.client.get('/1')
            self.assertEqual(response.status_code, 302)
            self.logout()

            self.login_eleve()
            response = self.client.get('/1')
            self.assertEqual(response.status_code, 302)
            self.logout()

            response = self.client.get('/1')
            self.assertEqual(response.status_code, 302)
            self.assertIn("/connection?next=%2F", response.headers["Location"])


    def test_preparation_reservations(self):
        with app.test_request_context():
            self.login_laborentain()
            response = self.client.get('/preparation/reservations')
            self.assertEqual(response.status_code, 200)
            self.logout()

            self.login_eleve()
            response = self.client.get('/preparation/reservations')
            self.assertEqual(response.status_code, 200)
            self.logout()

            response = self.client.get('/preparation/reservations', follow_redirects=False)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/connection?next=%2Fpreparation%2Freservations", response.headers["Location"])


    def test_preparation_reservations_page(self):
        with app.test_request_context():
            self.login_laborentain()
            response = self.client.get('/preparation/reservations/1')
            self.assertEqual(response.status_code, 302)
            self.logout()

            self.login_eleve()
            response = self.client.get('/preparation/reservations/1')
            self.assertEqual(response.status_code, 302)
            self.logout()

            response = self.client.get('/preparation/reservations/1', follow_redirects=False)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/connection?next=%2Fpreparation%2Freservations", response.headers["Location"])


    def test_search(self):
        with app.test_request_context():
            self.login_laborentain()
            response = self.client.get('/search', query_string={'search': 'test'})
            self.assertEqual(response.status_code, 200)
            self.logout()

            self.login_eleve()
            response = self.client.get('/search', query_string={'search': 'test'})
            self.assertEqual(response.status_code, 200)
            self.logout()

            response = self.client.get('/search', query_string={'search': 'test'})
            self.assertEqual(response.status_code, 302)

    def test_modif_produit(self):
        with app.test_request_context():
            self.login_laborentain()
            response = self.client.get('/modifier/1')
            self.assertEqual(response.status_code, 200)
            self.logout()

            self.login_eleve()
            response = self.client.get('/modifier/1', follow_redirects=False)
            self.assertEqual(response.status_code, 302) 
            self.assertIn("/", response.headers["Location"])
            self.logout()

            response = self.client.get('/modifier/1', follow_redirects=False)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/connection?next=%2Fmodifier%2F1", response.headers["Location"])

    
    def test_settings(self):
        with app.test_request_context():
            self.login_laborentain()
            response = self.client.get("/settings")
            self.assertEqual(response.status_code, 200)
            self.logout()

            self.login_eleve()
            response = self.client.get("/settings")
            self.assertEqual(response.status_code, 200)
            self.logout()

            response = self.client.get("/settings", follow_redirects=False)
            self.assertEqual(response.status_code, 302)  
            self.assertIn("/connection?next=%2Fsettings", response.headers["Location"])  # Vérifie la bonne URL de redirection


    def test_reserver_produit(self):
        with app.test_request_context():
            self.login_laborentain()
            response = self.client.get("/reservation/1?inputQte=1.0")
            self.assertEqual(response.status_code, 200)
            self.logout()

            self.login_eleve()
            response = self.client.get("/reservation/1?inputQte=1.0")
            self.assertEqual(response.status_code, 200)
            self.logout()

            response = self.client.get("/reservation/1?inputQte=1.0", follow_redirects=False)
            self.assertEqual(response.status_code, 302)  
            self.assertIn("/connection?next=%2Freservation%2F1%3FinputQte%3D1.0", response.headers["Location"])  # Vérifie la bonne URL de redirection


    def test_search_preparation(self):
        with app.test_request_context():
            response = self.client.get('/search-preparation', follow_redirects=False)
            self.assertEqual(response.status_code, 302)  # Redirection
            self.assertIn(b'/connection', response.headers["Location"].encode())

            self.login_laborentain()
            response = self.client.get('/search-preparation', query_string={'q': 'test'})
            self.assertEqual(response.status_code, 200)  # Accès autorisé
            self.logout()

            self.login_eleve()
            response = self.client.get('/search-preparation',  query_string={'q': 'test'})
            self.assertEqual(response.status_code, 200)  # Accès autorisé
            self.logout()
    

    def test_get_produit(self):
        with app.test_request_context():
            response = self.client.get('/get/produit/1', follow_redirects=False)
            self.assertEqual(response.status_code, 302)  # Redirection
            self.assertIn(b'/connection', response.headers["Location"].encode())

            self.login_laborentain()
            response = self.client.get('/get/produit/1')
            self.assertEqual(response.status_code, 200)  # Accès autorisé
            self.logout()

            self.login_eleve()
            response = self.client.get('/get/produit/1')
            self.assertEqual(response.status_code, 200)  # Accès autorisé
            self.logout()

    def test_popup_reserver_produit(self):
        with app.test_request_context():
            response = self.client.get('/reserver/1', follow_redirects=False)
            self.assertEqual(response.status_code, 302)  # Redirection
            self.assertIn(b'/connection', response.headers["Location"].encode())

            self.login_laborentain()
            response = self.client.get('/reserver/1')
            self.assertEqual(response.status_code, 200)  # Accès autorisé
            self.logout()

            self.login_eleve()
            response = self.client.get('/reserver/1')
            self.assertEqual(response.status_code, 200)  # Accès autorisé
            self.logout()

    def test_popup_modifier_commande(self):
        with app.test_request_context():
            response = self.client.get('/commande/1', follow_redirects=False)
            self.assertEqual(response.status_code, 302)  # Redirection
            self.assertIn(b'/connection', response.headers["Location"].encode())

            self.login_laborentain()
            response = self.client.get('/commande/1')
            self.assertEqual(response.status_code, 200)  # Accès autorisé
            self.logout()

            self.login_eleve()
            response = self.client.get('/commande/1')
            self.assertEqual(response.status_code, 200)  # Accès autorisé
            self.logout()

    def test_modifier_reserv(self):
        with app.test_request_context():
            response = self.client.get('/commande/modif/1?inputQte=1', follow_redirects=False)
            self.assertEqual(response.status_code, 302)  # Redirection
            self.assertIn(b'/connection', response.headers["Location"].encode())  # Vérifie la redirection vers la page de connexion

            self.login_laborentain() 
            response = self.client.get('/commande/modif/1?inputQte=1')
            self.assertEqual(response.status_code, 200)  # Accès autorisé
            self.logout()

            self.login_eleve() 
            response = self.client.get('/commande/modif/1?inputQte=1')
            self.assertEqual(response.status_code, 200)  # Accès autorisé
            self.logout()



    def test_get_modif_produit(self):
        with app.test_request_context():
            response = self.client.get('/modifier/1', follow_redirects=False)
            self.assertEqual(response.status_code, 302)  # Redirection
            self.assertIn(b'/connection', response.headers["Location"].encode())

            self.login_laborentain()  
            response = self.client.get('/modifier/1')
            self.assertEqual(response.status_code, 200)  # Accès autorisé
            self.logout()

            self.login_eleve()
            response = self.client.get('/modifier/1')
            self.assertEqual(response.status_code, 302)  # Redirection
            assert b'/' in response.headers["Location"].encode()
            self.logout()

    def test_sauvegarder_modif(self):
        with app.test_request_context():
            response = self.client.get('/modifier/1', follow_redirects=False)
            self.assertEqual(response.status_code, 302)  # Redirection
            self.assertIn(b'/connection', response.headers["Location"].encode())

            self.login_laborentain()
            response = self.client.get('/modifier/1')
            self.assertEqual(response.status_code, 200)  # Accès autorisé
            self.logout()

            self.login_eleve()
            response = self.client.get('/modifier/1')
            self.assertEqual(response.status_code, 302)  # Redirection
            assert b'/' in response.headers["Location"].encode()
            self.logout()
   

    def test_searchByButton(self):
        with app.test_request_context():
            response = self.client.get('/search/famille/1', follow_redirects=False)
            self.assertEqual(response.status_code, 302)  # Redirection
            self.assertIn(b'/connection', response.headers["Location"].encode())

            self.login_laborentain()
            response = self.client.get('/search/famille/1')
            self.assertEqual(response.status_code, 200)  # Accès autorisé
            self.logout()

            self.login_eleve()
            response = self.client.get('/search/famille/1')
            self.assertEqual(response.status_code, 200)  # Accès autorisé
            self.logout()

    def test_sauvegarder_ajout(self):
        with app.test_request_context():
            response = self.client.post('/ajout/sauvegarder/', json={
                'textNom': 'ProduitTest',
                'textFournisseur': 'FournisseurTest',
                'textUnite': 'kg',
                'textQuantite': 100,
                'textSeuil':1,
                'textFonction': 'Test',
                'textLieu': 'LieuTest'
            }, follow_redirects=False)
            self.assertEqual(response.status_code, 302)  # Redirection
            self.assertIn(b'/connection', response.headers["Location"].encode())  # Vérifie la redirection vers la page de connexion

            self.login_laborentain()
            response = self.client.post('/ajout/sauvegarder/', json={
                'textNom': 'ProduitTest',
                'textFournisseur': 'FournisseurTest',
                'textUnite': 'kg',
                'textQuantite': 100,
                'textSeuil':1,
                'textFonction': 'Test',
                'textLieu': 'LieuTest'
            })
            self.assertEqual(response.status_code, 200)  # Accès autorisé
            self.logout()

            self.login_eleve()
            response = self.client.post('/ajout/sauvegarder/', json={
                'textNom': 'ProduitTest',
                'textFournisseur': 'FournisseurTest',
                'textUnite': 'kg',
                'textQuantite': 100,
                'textSeuil':1,
                'textFonction': 'Test',
                'textLieu': 'LieuTest'
            })
            self.assertEqual(response.status_code, 200)  # Accès autorisé
            self.logout()


    def test_etat_commande(self):
        with app.test_request_context():
            response = self.client.get('/etat/commande/1', follow_redirects=False)
            self.assertEqual(response.status_code, 302)  # Redirection
            self.assertIn(b'/connection', response.headers["Location"].encode())

            self.login_laborentain()
            response = self.client.get('/etat/commande/1')
            self.assertEqual(response.status_code, 302)  
            assert b'/preparation/reservations' in response.headers["Location"].encode()
            self.logout()

            self.login_eleve()
            response = self.client.get('/etat/commande/1')
            self.assertEqual(response.status_code, 302)  
            assert b'/preparation/reservations' in response.headers["Location"].encode()
            self.logout()

    
    def test_suppr_reservation(self):
        with app.test_request_context():
            response = self.client.get('/supprimer/reservation/1', follow_redirects=False)
            self.assertEqual(response.status_code, 302)  # Redirection
            self.assertIn(b'/connection', response.headers["Location"].encode())

            self.login_laborentain()
            response = self.client.get('/supprimer/reservation/1')
            self.assertEqual(response.status_code, 302)  
            assert b'/preparation/reservations' in response.headers["Location"].encode()
            self.logout()

            self.login_eleve()
            response = self.client.get('/supprimer/reservation/2')
            self.assertEqual(response.status_code, 302)
            assert b'/preparation/reservations' in response.headers["Location"].encode()
            self.logout()

    
    def test_pop_up_cacher(self):
        with app.test_request_context():
            response = self.client.get('/pop_up_cacher/1', follow_redirects=False)
            self.assertEqual(response.status_code, 302)  # Redirection
            self.assertIn(b'/connection', response.headers["Location"].encode())

            self.login_laborentain()
            response = self.client.get('/pop_up_cacher/1')
            self.assertEqual(response.status_code, 200)  
            self.logout()

            self.login_eleve()
            response = self.client.get('/pop_up_cacher/1')
            self.assertEqual(response.status_code, 302)  
            assert b'/' in response.headers["Location"].encode()
            self.logout()


    def test_cacher(self):
        with app.test_request_context():
            response = self.client.get('/cacher/1', follow_redirects=False)
            self.assertEqual(response.status_code, 302)  # Redirection
            self.assertIn(b'/connection', response.headers["Location"].encode())

            self.login_laborentain()
            response = self.client.get('/cacher/1')
            self.assertEqual(response.status_code, 200)  
            self.logout()

            self.login_eleve()
            response = self.client.get('/cacher/1')
            self.assertEqual(response.status_code, 302)  
            assert b'/' in response.headers["Location"].encode()
            self.logout()

    
    def test_montrer(self):
        with app.test_request_context():
            response = self.client.get('/montrer/1', follow_redirects=False)
            self.assertEqual(response.status_code, 302)  # Redirection
            self.assertIn(b'/connection', response.headers["Location"].encode())

            self.login_laborentain()
            response = self.client.get('/montrer/1')
            self.assertEqual(response.status_code, 200)  
            self.logout()

            self.login_eleve()
            response = self.client.get('/montrer/1')
            self.assertEqual(response.status_code, 302)  
            assert b'/' in response.headers["Location"].encode()
            self.logout()


    def test_pop_up_montrer(self):
        with app.test_request_context():
            response = self.client.get('/pop_up_montrer/1', follow_redirects=False)
            self.assertEqual(response.status_code, 302)  # Redirection
            self.assertIn(b'/connection', response.headers["Location"].encode())

            self.login_laborentain()
            response = self.client.get('/pop_up_montrer/1')
            self.assertEqual(response.status_code, 200)  
            self.logout()

            self.login_eleve()
            response = self.client.get('/pop_up_montrer/1')
            self.assertEqual(response.status_code, 302)  
            assert b'/' in response.headers["Location"].encode()
            self.logout()

    def test_generate_pdf(self):
        with app.test_request_context():
            response = self.client.get('/generate_pdf', follow_redirects=False)
            self.assertEqual(response.status_code, 302)  # Redirection
            self.assertIn(b'/', response.headers["Location"].encode())

            self.login_laborentain()
            response = self.client.get('/generate_pdf')
            self.assertEqual(response.status_code, 302)
            self.assertIn(b'/', response.headers["Location"].encode())  
            self.logout()

            self.login_eleve()
            response = self.client.get('/generate_pdf')
            self.assertEqual(response.status_code, 302)  
            self.assertIn(b'/', response.headers["Location"].encode())
            self.logout()


    def test_ajout_csv(self):
        with app.test_request_context():
            response = self.client.get('/ajout_csv')
            self.assertEqual(response.status_code, 302)  # Redirection
            self.assertIn(b'/', response.headers["Location"].encode())

            self.login_laborentain()
            response = self.client.get('/ajout_csv')
            self.assertEqual(response.status_code, 302)
            self.assertIn(b'/', response.headers["Location"].encode())  
            self.logout()

            self.login_eleve()
            response = self.client.get('/ajout_csv')
            self.assertEqual(response.status_code, 302)  
            self.assertIn(b'/', response.headers["Location"].encode())
            self.logout()
            

    
    def test_not_found_page(self):
        response = self.client.get('/not-a-valid-url')
        self.assertEqual(response.status_code, 302)
        assert b'/' in response.data


    
if __name__ == '__main__':
    unittest.main()