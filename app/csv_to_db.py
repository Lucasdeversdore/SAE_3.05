import csv, sys
from .models import add_prod, add_lieu_stock, add_est_stocker, get_id_lieu, get_id_prod, next_prod_id

def get_nombre_unite(quantite):
    nb = ""
    quantite = quantite.strip()
    if quantite == "":
        return (0, None)
    for i in range(len(quantite)):
        try:
            a = int(quantite[i])
            nb += quantite[i]
        except:
            if quantite[i] == "*":
                res = get_nombre_unite(quantite[i+1:])
                return (int(nb)*res[0], res[1])
            else:
                return (int(nb), quantite[i:].strip())
    return (int(quantite), None)


def get_unite(unite):
    if unite is not None:
        if unite.upper() == "G":
            return "g"
        elif unite.upper() == "KG":
            return "kg"
        elif unite.upper() == "ML":
            return "mL"
        elif unite.upper() == "L":
            return "L"
        else:
            return unite


def csv_to_db(filename):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        try:
            demarer =False
            for row in reader:
                if demarer:
                    nom_prod = row[0]
                    if row[1]=="" or row[1]=="-" or row[1]=="\"":
                        nom_fou = None
                    else:
                        nom_fou = row[1]
                    qte_unite = get_nombre_unite(row[2])
                    qte = qte_unite[0]
                    unite = get_unite(qte_unite[1])
                    if row[3] == "":
                        prod_fonction = None
                    else: 
                        prod_fonction = row[3]
                    lieu = row[4]
                    add_prod(nom_prod, unite, prod_fonction, nom_fou)
                    add_lieu_stock(lieu)
                    id_prod = next_prod_id() -1
                    id_lieu= get_id_lieu(lieu)
                    add_est_stocker(id_prod, id_lieu, qte)
                if row == ['Produits', 'Fournisseur', 'Quantité', 'Fonction', 'Lieu de stockage']:
                    demarer = True
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))



    