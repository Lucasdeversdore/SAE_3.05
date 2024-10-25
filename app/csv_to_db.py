import csv, sys
from models import add_prod


def csv_to_db(filename):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        try:
            demarer =False
            for row in reader:
                if demarer:
                    print(row)
                if row == ['Produits', 'Fournisseur', 'Quantité', 'Fonction', 'Lieu de stockage']:
                    demarer = True
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))


csv_to_db("/home/iut45/Etudiants/o22300799/Téléchargements/Produits de formulation Chimie Minérale.csv")