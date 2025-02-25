import unittest
from flask import app, request
from app.app import app
from app.form import InscriptionForm, LoginForm

class Testing(unittest.TestCase):

    def setUp(self):
        """ Démarrer un contexte de requête avant chaque test """
        # Configure l'application avant de créer un client
        app.config['WTF_CSRF_ENABLED'] = False  # Désactive CSRF pour les tests
        app.config['SECRET_KEY'] = 'mysecretkey'  # Nécessaire pour les formulaires Flask
        self.app = app.test_client()  # Crée le client de test
        self.ctx = app.test_request_context()  # Démarre un contexte de requête pour les tests
        self.ctx.push()
        

    def tearDown(self):
        """ Nettoyer le contexte de requête après chaque test """
        self.ctx.pop()

    def test_login_form_valid_user(self):
        """ Teste si un utilisateur valide peut s'authentifier """
        user_email = "email.dev@gmail.com"
        user_password = "A1#45678"
        
        form = LoginForm(data={"email": user_email, "mdp": user_password})
        authenticated_user = form.get_authenticated_user()
        
        self.assertIsNot(authenticated_user, False)
        self.assertEqual(authenticated_user.email, user_email)

    def test_login_form_invalid_email(self):
        """ Teste l'authentification avec un email incorrect """
        form = LoginForm(data={"email": "wrong@example.com", "mdp": "password123"})
        user = form.get_authenticated_user()

        self.assertFalse(user)
        self.assertIn("Email incorrect", form.email.errors)

    def test_login_form_invalid_password(self):
        """ Teste l'authentification avec un mot de passe incorrect """
        valid_email = "email.dev@gmail.com"
        form = LoginForm(data={"email": valid_email, "mdp": "wrongpassword"})
        user = form.get_authenticated_user()

        self.assertFalse(user)
        self.assertIn("Mot de passe incorrect", form.mdp.errors)

    def test_inscription_valid_form(self):
        """ Teste un formulaire valide """
        form = InscriptionForm(data={
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean.dupont@example.com",
            "mdp": "A1#45678",
            "confirm_mdp": "A1#45678",
            "cgu": True
        })

        # Affiche les erreurs si la validation échoue
        if not form.validate():
            print(form.errors)  # Affiche les erreurs pour le débogage

        self.assertTrue(form.validate())  # Cela devrait maintenant passer


    def test_inscription_missing_fields(self):
        """ Teste avec des champs manquants """
        form = InscriptionForm(data={})
        self.assertFalse(form.validate())
        self.assertIn("This field is required.", form.prenom.errors)
        self.assertIn("This field is required.", form.nom.errors)
        self.assertIn("This field is required.", form.email.errors)
        self.assertIn("This field is required.", form.mdp.errors)
        self.assertIn("This field is required.", form.confirm_mdp.errors)
        self.assertIn("This field is required.", form.cgu.errors)

    def test_inscription_invalid_email(self):
        """ Teste avec un email invalide """
        form = InscriptionForm(data={
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "email-invalide",
            "mdp": "A1#45678",
            "confirm_mdp": "A1#45678",
            "cgu": True
        })
        self.assertFalse(form.validate())
        self.assertIn("Email incorrect", form.email.errors)

    def test_inscription_password_mismatch(self):
        """ Teste avec des mots de passe qui ne correspondent pas """
        form = InscriptionForm(data={
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean.dupont@example.com",
            "mdp": "A1#45678",
            "confirm_mdp": "differentPassword",
            "cgu": True
        })
        self.assertFalse(form.validate())
        self.assertIn("Les mots de passe doivent correspondre", form.confirm_mdp.errors)

    def test_inscription_missing_cgu(self):
        """ Teste si l'utilisateur ne coche pas les CGU """
        form = InscriptionForm(data={
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean.dupont@example.com",
            "mdp": "A1#45678",
            "confirm_mdp": "A1#45678",
            "cgu": False  # Non coché
        })
        self.assertFalse(form.validate())
        self.assertIn("This field is required.", form.cgu.errors)