import unittest
from flask import app, request
from app.app import app
from app.form import LoginForm

class Testing(unittest.TestCase):

    def setUp(self):
        """ Démarrer un contexte de requête avant chaque test """
        self.app = app.test_client()
        self.ctx = app.test_request_context()
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