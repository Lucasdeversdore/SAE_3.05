import unittest
from flask import app, request
from app.app import app
from app.form import ChangePasswordForm, InscriptionForm, LoginForm, ResetForm, SettingsForm

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

    # LoginForm
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

    # InscriptionForm
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

    # ResetForm
    def test_reset_form_valid_email(self):
        """ Teste la soumission d'un email valide pour réinitialiser le mot de passe """
        form = ResetForm(data={
            "email": "valid.email@example.com",
            "next": "/somepage" 
        })
        self.assertTrue(form.validate()) 
        self.assertEqual(form.email.data, "valid.email@example.com") 

    def test_reset_form_invalid_email(self):
        """ Teste la soumission avec un email invalide """
        form = ResetForm(data={
            "email": "invalid-email",
            "next": "/somepage"
        })
        self.assertFalse(form.validate())  
        self.assertIn("Email incorrect", form.email.errors) 

    def test_reset_form_missing_email(self):
        """ Teste la soumission sans email (champ manquant) """
        form = ResetForm(data={
            "email": "",  
            "next": "/somepage"
        })
        self.assertFalse(form.validate())  
        self.assertIn("This field is required.", form.email.errors)  

    def test_reset_form_missing_next(self):
        """ Teste la soumission avec un email valide mais sans le champ 'next' """
        form = ResetForm(data={
            "email": "valid.email@example.com",
            "next": "" 
        })
        self.assertTrue(form.validate())  
        self.assertEqual(form.next.data, "")  

    def test_reset_form_email_not_found(self):
        """ Teste si l'email n'est pas trouvé dans la base de données (logique d'application) """
        form = ResetForm(data={
            "email": "nonexistent.email@example.com",
            "next": "/somepage"
        })
        self.assertTrue(form.validate())  

    # ChangePasswordForm
    def test_change_password_valid(self):
        """ Teste la soumission d'un mot de passe valide et confirmé """
        form = ChangePasswordForm(data={
            "mdp": "A1#newPassword", 
            "confirm_mdp": "A1#newPassword" 
        })
        self.assertTrue(form.validate())  
        self.assertEqual(form.mdp.data, "A1#newPassword") 
        self.assertEqual(form.confirm_mdp.data, "A1#newPassword")  

    def test_change_password_invalid_password(self):
        """ Teste la soumission d'un mot de passe invalide (ne respectant pas le validateur) """
        form = ChangePasswordForm(data={
            "mdp": "weak", 
            "confirm_mdp": "weak"
        })
        self.assertFalse(form.validate())  
        self.assertIn("mdp doit contenir au moins : 1 majuscule, 1 caractère spécial, 1 chiffre et doit faire au moins 8 caractères", form.mdp.errors)  # Vérifie qu'une erreur liée au mot de passe est présente

    def test_change_password_mismatch(self):
        """ Teste la soumission lorsque les mots de passe ne correspondent pas """
        form = ChangePasswordForm(data={
            "mdp": "A1#newPassword",
            "confirm_mdp": "A1#differentPassword"
        })
        self.assertFalse(form.validate())  # Le formulaire ne devrait pas être valide
        self.assertIn("Les mots de passe doivent correspondre", form.confirm_mdp.errors)  # Vérifie l'erreur de non-correspondance

    def test_change_password_missing_password(self):
        """ Teste la soumission avec des mots de passe manquants """
        form = ChangePasswordForm(data={
            "mdp": "",  # Mot de passe vide
            "confirm_mdp": ""
        })
        self.assertFalse(form.validate())  # Le formulaire ne doit pas être valide
        self.assertIn("This field is required.", form.mdp.errors)  # Vérifie que l'erreur 'required' est présente pour 'mdp'
        self.assertIn("This field is required.", form.confirm_mdp.errors)  # Vérifie l'erreur pour 'confirm_mdp'

    def test_change_password_missing_confirmation(self):
        """ Teste la soumission avec un mot de passe et sans confirmation """
        form = ChangePasswordForm(data={
            "mdp": "A1#newPassword",
            "confirm_mdp": ""
        })
        self.assertFalse(form.validate())
        self.assertIn("This field is required.", form.confirm_mdp.errors)

    
    # SettingsForm
    def test_settings_form_valid(self):
        """ Teste la soumission d'un formulaire valide """
        form = SettingsForm(data={
            "prenom": "Jean",
            "nom": "Dupont",
            "old_mdp": "A1#oldPassword",
            "mdp": "A1#newPassword",
            "confirm_mdp": "A1#newPassword",
            "info": True  # L'option pour recevoir des notifications est cochée
        })
        
        self.assertTrue(form.validate())  # Le formulaire devrait être valide
        self.assertEqual(form.prenom.data, "Jean")  # Vérifie le prénom
        self.assertEqual(form.nom.data, "Dupont")  # Vérifie le nom
        self.assertEqual(form.mdp.data, "A1#newPassword")  # Vérifie le mot de passe
        self.assertTrue(form.info.data)  # Vérifie que l'option de notification est activée

    def test_settings_form_invalid_old_password(self):
        """ Teste la soumission avec un ancien mot de passe incorrect """
        form = SettingsForm(data={
            "prenom": "Jean",
            "nom": "Dupont",
            "old_mdp": "wrongOldPassword",
            "mdp": "A1#newPassword",
            "confirm_mdp": "A1#newPassword",
            "info": True
        })
        
        self.assertFalse(form.validate())
        self.assertIn("mdp doit contenir au moins : 1 majuscule, 1 caractère spécial, 1 chiffre et doit faire au moins 8 caractères", form.old_mdp.errors)

    def test_settings_form_password_mismatch(self):
        """ Teste la soumission lorsque les mots de passe ne correspondent pas """
        form = SettingsForm(data={
            "prenom": "Jean",
            "nom": "Dupont",
            "old_mdp": "A1#oldPassword",
            "mdp": "A1#newPassword",
            "confirm_mdp": "A1#differentPassword",
            "info": True
        })
        
        self.assertFalse(form.validate())
        self.assertIn("Les mots de passe doivent correspondre", form.confirm_mdp.errors)  # Vérifie l'erreur de non-correspondance


    def test_settings_form_toggle_info(self):
        """ Teste si l'utilisateur peut choisir de recevoir ou non des notifications """
        form = SettingsForm(data={
            "prenom": "Jean",
            "nom": "Dupont",
            "old_mdp": "A1#oldPassword",
            "mdp": "A1#newPassword",
            "confirm_mdp": "A1#newPassword",
            "info": False
        })
        
        self.assertTrue(form.validate())
        self.assertFalse(form.info.data)