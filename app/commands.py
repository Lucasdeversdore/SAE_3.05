from hashlib import sha256
import click

from app.models import Chimiste, next_chimiste_id
from .app import app, db
from .csv_to_db import csv_to_db

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    '''Creates the tables and populates them with data.'''
    with app.app_context():
        csv_to_db(filename)


# TO DO vérifier le mot de passe
@app.cli.command()
@click.argument('email')
@click.argument('password')
@click.argument('prenom')
@click.argument('nom')
def newuser(email, password, nom, prenom):
    '''Adds a new user.'''
    m = sha256()
    m.update(password.encode())
    u = Chimiste(idChimiste=next_chimiste_id(), prenom=prenom, nom=nom, email = email, mdp = m.hexdigest(), estPreparateur=True)
    db.session.add(u)
    db.session.commit()