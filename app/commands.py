from hashlib import sha256
import click

from app.models import Chimiste, next_chimiste_id, check_mdp
from .app import app, db
from .csv_to_db import csv_to_db

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    '''Creates the tables and populates them with data.'''
    with app.app_context():
        csv_to_db(filename)
    
@app.cli.command()
@click.argument('id_commande')
@click.argument('new_qte')
def edit_commande(id_commande, new_qte):
    from .models import edit_qte_commande
    edit_qte_commande(id_commande, new_qte)

@app.cli.command()
@click.argument('email')
@click.argument('password')
@click.argument('prenom')
@click.argument('nom')
def newuser(email, password, nom, prenom):
    '''Adds a new user.'''
    if check_mdp(password):
        m = sha256()
        m.update(password.encode())
        u = Chimiste(idChimiste=next_chimiste_id(), prenom=prenom, nom=nom, email = email, mdp = m.hexdigest(), estPreparateur=True)
        db.session.add(u)
        db.session.commit()
    else:
        print("le mot de passe doit contenir au moins 8 craractères, 1 majuscule, 1 lettre, 1 caractère spécial")