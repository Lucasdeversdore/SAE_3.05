from hashlib import sha256
from flask_login import login_required, login_user, logout_user
from wtforms import HiddenField, PasswordField, StringField
from .app import app
from flask_wtf import FlaskForm
from flask import redirect, render_template, url_for
from .models import Chimiste, get_sample, search_filter, search_famille_filter
from flask import request

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

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class InscriptionForm(FlaskForm):
    prenom = StringField('Prénom', validators=[DataRequired(), Length(min=2, max=50)])
    nom = StringField('Nom', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mdp = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    confirm_mdp = PasswordField('Confirmer mot de passe', 
                                validators=[DataRequired(), EqualTo('mdp', message='Les mots de passe doivent correspondre')])
    submit = SubmitField("S'inscrire")


@app.route("/")
@login_required
def home():
    liste_produit = get_sample()
    return render_template("home.html", liste_produit=liste_produit) 

@app.route("/preparation/reservations")
@login_required
def preparation_reservation():
    #TODO remplir reservations avec la liste des reservations ordonné dans un ordre pré définie
    reservations = [] 
    return render_template("reservation-preparation.html", reservations=reservations)


@app.route("/connection")
def connecter():
    f = LoginForm()
    return render_template("connection.html", msg=None, form=f)


from flask import Flask, render_template, redirect, url_for, flash
from .models import Chimiste, db

@app.route('/inscription', methods=['GET', 'POST'])
def inscrire():
    form = InscriptionForm()
    if form.validate_on_submit():
        # Récupérer les données du formulaire
        prenom = form.prenom.data
        nom = form.nom.data
        email = form.email.data
        mdp = form.mdp.data  # Hashage du mot de passe

        # Vérifier si l'email existe déjà dans la base
        chimiste_existant = Chimiste.query.filter_by(email=email).first()
        if chimiste_existant:
            flash('Cet email est déjà utilisé.', 'danger')
            return redirect(url_for('inscription'))
        
        # Créer un nouvel utilisateur Chimiste
        nouveau_chimiste = Chimiste(idChimiste=next_chimiste_id(), prenom=prenom, nom=nom, email=email, mdp=mdp)
        
        # Ajouter à la session et enregistrer dans la base de données
        db.session.add(nouveau_chimiste)
        db.session.commit()

        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('connexion'))

    return render_template('inscription.html', form=form)

@app.route("/search", methods=('GET',))
@login_required
def search():
    q = request.args.get("search")
    results = search_filter(q) + search_famille_filter(q)
    return render_template("home.html", liste_produit=results)


@app.route("/test/connection", methods=('GET', 'POST'))
def connection():
    user = None
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if type(user) != str:
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect(next)
    return render_template("connection.html", form=f, msg=user)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('connection'))
