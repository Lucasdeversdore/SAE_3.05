import click
from .app import app
from .csv_to_db import csv_to_db

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    '''Creates the tables and populates them with data.'''
    with app.app_context():
        csv_to_db(filename)
    
