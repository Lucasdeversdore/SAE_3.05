import click
from .app import app
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
    