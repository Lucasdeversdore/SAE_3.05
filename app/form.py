from hashlib import sha256
from flask_wtf import FlaskForm
from wtforms import SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms import HiddenField, PasswordField, StringField
from app.models import Chimiste

class LoginForm ( FlaskForm ):
    email = StringField('email')
    password = PasswordField('Password')
    next = HiddenField()
    def get_authenticated_user(self):
        user = Chimiste.query.filter(Chimiste.email == self.email.data).first()
        if user is None:
            return "Email incorrect"
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.mdp else "Mot de passe incorrect"
    


class InscriptionForm(FlaskForm):
    from .models import check_mdp_validator
    prenom = StringField('Prénom', validators=[DataRequired(), Length(min=2, max=50)])
    nom = StringField('Nom', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mdp = PasswordField('Mot de passe', validators=[DataRequired(), check_mdp_validator])
    confirm_mdp = PasswordField('Confirmer mot de passe',
                                validators=[DataRequired(), EqualTo('mdp', message='Les mots de passe doivent correspondre')])
    submit = SubmitField("S'inscrire")