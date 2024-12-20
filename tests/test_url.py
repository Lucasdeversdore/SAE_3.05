import os
import sys
import time
import unittest




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


    # tests redirection login required
    def test_home_redirect(self):
        response = self.client.get('/')
        assert response.status_code == 302
        assert b'/connection' in response.data  

    def test_home_page_1_redirect(self): 
        response = self.client.get('/1')
        assert response.status_code == 302
        assert b'/connection' in response.data

    def test_preparation_reservations_redirect(self):
        response = self.client.get('/preparation/reservations')
        assert response.status_code == 302
        assert b'/connection' in response.data

    def test_preparation_reservations_1_redirect(self):
        response = self.client.get('/preparation/reservations/1')
        assert response.status_code == 302
        assert b'/connection' in response.data


    def test_search_redirect(self):
        response = self.client.get('/search')
        assert response.status_code == 302
        assert b'/connection' in response.data

    def test_search_preparation(self):
        response = self.client.get('/search-preparation')
        assert response.status_code == 302
        assert b'/connection' in response.data

    def test_get_produit_redirect(self):
        response = self.client.get('/get/produit/0')
        assert response.status_code == 302
        assert b'/connection' in response.data

    def test_reserver_redirect(self):
        response = self.client.get('/reserver/0')
        assert response.status_code == 302
        assert b'/connection' in response.data

    def test_reservation_redirect(self):
        response = self.client.get('/reservation/0')
        assert response.status_code == 302
        assert b'/connection' in response.data

    def test_modif_produit_redirect(self):
        response = self.client.get('/modifier/0')
        assert response.status_code == 302
        assert b'/connection' in response.data

    def test_sauvegarder_modif_redirect(self):
        response = self.client.get('/sauvegarder/0')
        assert response.status_code == 302
        assert b'/connection' in response.data
    
    def test_searchByButton_redirect(self):
        response = self.client.get('/search/famille/0')
        assert response.status_code == 302
        assert b'/connection' in response.data

    def test_sauvegarder_ajout_redirect(self):
        response = self.client.get('/ajout/sauvegarder/')
        assert response.status_code == 302


    def test_sauvegarder_ajout_fournisseur_redirect(self):
        response = self.client.get('/ajoutFournisseur/sauvegarder')
        assert response.status_code == 302

    def test_etat_commande_redirect(self):
        response = self.client.get('/etat/commande/0/0')
        assert response.status_code == 302
        assert b'/connection' in response.data


    # test des chemins non login required sans connection

    def test_inscrire(self):
        response = self.client.get('/inscription')
        assert response.status_code == 200

    def test_cgu(self):
        response = self.client.get('/inscription-cgu')
        assert response.status_code == 200

    def test_inscrire(self):
        response = self.client.get('/inscription')
        assert response.status_code == 200
    
    def test_activation_token(self):
        with app.app_context():
            timer = time.time()
            new_c=Chimiste(999,"tr","tr","aeaaaa@fjfj.fr","mdp", False)
            token = new_c.get_token()
            response = self.client.get('/activation/'+token+'/'+str(timer))
            assert response.status_code == 302

    def test_connection(self):
        response = self.client.get('/connection')
        assert response.status_code == 200

    def test_logout(self):
        response = self.client.get('/logout/')
        assert response.status_code == 302

    def test_reset_pwd(self):
        response = self.client.get('/reset_pwd')
        assert response.status_code == 200


    def login_laborentain(self):
        user = Chimiste.query.filter(Chimiste.email == "email.dev@gmail.com").first()
        login_user(user)

    # tests des pages login required avec une connexion
    def test_home(self):
        with app.test_request_context():
            self.login_laborentain()
            response = self.client.get('/')
            assert response.status_code == 200  
    
    def test_home_page_1(self):
        with app.test_request_context(): 
            self.login_laborentain()
            response = self.client.get('/1')
            assert response.status_code == 302
        

    def test_preparation_reservations(self):
        with app.test_request_context(): 
            self.login_laborentain() 
            response = self.client.get('/preparation/reservations')
            assert response.status_code == 200

    def test_preparation_reservations_1(self):
        with app.test_request_context(): 
            self.login_laborentain() 
            response = self.client.get('/preparation/reservations/1')
            assert response.status_code == 302


    def test_search(self):
        with app.test_request_context(): 
            self.login_laborentain() 
            response = self.client.get('/search', query_string={'search': 'test'})
            assert response.status_code == 200
        

    def test_search_preparation(self):
        with app.test_request_context(): 
            self.login_laborentain()
            response = self.client.get('/search-preparation', query_string={'search': 'test'})
            assert response.status_code == 200
        

    def test_get_produit(self):
        with app.test_request_context(): 
            self.login_laborentain() 
            response = self.client.get('/get/produit/1')
            assert response.status_code == 200

    def test_reserver(self):
        with app.test_request_context(): 
            self.login_laborentain() 
            response = self.client.get('/reserver/1')
            assert response.status_code == 200


    def test_modif_produit(self):
        with app.test_request_context(): 
            self.login_laborentain() 
            response = self.client.get('/modifier/1')
            assert response.status_code == 200
        
    
    def test_searchByButton(self):
         with app.test_request_context(): 
            self.login_laborentain()
            response = self.client.get('/search/famille/1', query_string={'search': 'test'})
            
            assert response.status_code == 200

    def test_sauvegarder_ajout(self):
        with app.test_request_context(): 
            self.login_laborentain() 
            response = self.client.get('/ajout/sauvegarder/')
            assert response.status_code == 302


    def test_sauvegarder_ajout_fournisseur(self):
         with app.test_request_context(): 
            self.login_laborentain()
            response = self.client.get('/ajoutFournisseur/sauvegarder')
            assert response.status_code == 302



    def test_etat_commande(self):
        with app.app_context():
            commande = Commande(0, 1, 2, 1)
            db.session.add(commande)
            db.session.commit()
            faire = Faire(0,1)
            db.session.add(faire)
            db.session.commit()
        with app.test_request_context(): 
            self.login_laborentain() 
            
            response = self.client.get('/etat/commande/0/1')
            assert response.status_code == 302

    
    
    def test_not_found_page(self):
        response = self.client.get('/not-a-valid-url')
        assert response.status_code == 302
        assert b'/' in response.data

if __name__ == '__main__':
    unittest.main()