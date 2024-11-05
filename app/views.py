from hashlib import sha256
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField
from .app import app
from flask import render_template
from .models import Chimiste, get_sample

#TODO Mettre un login required sur toutes les pages qui le nécessite

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
def home():
    #TODO log pour current_user, supprimer current_user de render templete
    #TODO donner une liste de produits à liste_produit dans render
    liste_produit = get_sample()
    return render_template("home.html", liste_produit=liste_produit, current_user=True) 

@app.route("/preparation/reservations")
def preparation_reservation():
    #TODO log pour current_user, supprimer current_user de render templete
    #TODO remplir reservations avec la liste des reservations ordonné dans un ordre pré définie
    reservations = [] 
    return render_template("reservation-preparation.html", reservations=reservations, current_user=True)


@app.route("/connection")
def connecter():
    return render_template("connection.html")


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