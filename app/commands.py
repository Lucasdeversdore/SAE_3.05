import click
from .app import app, db
from .models import *
from hashlib import sha256
# import des modèles

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    '''Creates the tables and populates them with data.'''

    # création de toutes les tables
    db.create_all()
