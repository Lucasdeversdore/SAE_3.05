#!/usr/bin/python3
from flask_login import UserMixin
from sqlalchemy import Column, Integer, Text, Date, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from .app import login_manager
from sqlalchemy import func
from .app import  db



class Chimiste(db.Model, UserMixin):

    __tablename__ = "CHIMISTE"

    idChimiste = Column(Integer, primary_key = True, nullable = False)
    prenom = Column(Text)
    nom = Column(Text)
    email = Column(Text)
    mdp = Column(Text)
    estPreparateur = Column(Boolean)
    chimisteCom = relationship("Commande", back_populates="commandeChim")
    chimisteFaire = relationship("Faire", back_populates="faireChim")


    def __init__(self, idChimiste, prenom, nom, email, mdp,  estPreparateur=False):
        self.idChimiste = idChimiste
        self.prenom = prenom
        self.nom = nom
        self.email = email
        self.mdp = mdp
        self.estPreparateur = estPreparateur
        
    def __str__(self):
        return str(self.idChimiste) + self.prenom + self.nom + self.email + self.mdp
    
    def get_id(self):
        return self.idChimiste

class Unite(db.Model):

    __tablename__ = "UNITE"

    nomUnite = Column(Text, primary_key = True)
    uniteProd = relationship("Produit", back_populates="produitUnite")


    def __init__(self, nomUnite):
        self.nomUnite = nomUnite

    def __str__(self):
        return self.nomUnite

class Produit(db.Model):

    __tablename__ = "PRODUIT"

    idProduit = Column(Integer, primary_key = True, nullable = False)
    nomProduit = Column(Text)
    nomUnite = Column(Text, ForeignKey("UNITE.nomUnite"))
    afficher = Column(Boolean)
    fonctionProduit = Column(Text)
    idFou = Column(Integer, ForeignKey("FOURNISSEUR.idFou"))
    produitUnite = relationship("Unite", back_populates="uniteProd")
    produitStock = relationship("Est_Stocker", back_populates="stockerProduit")
    produitHist = relationship("Historique", back_populates="historiqueProd")
    produitCom = relationship("Commande", back_populates="commandeProd")
    produitFour = relationship("Fournisseur", back_populates="fournisseurProd")


    def __init__(self, idProduit, nomProduit, nomUnite, fonctionProduit, idfou):
        self.idProduit = idProduit
        self.nomProduit = nomProduit
        self.nomUnite = nomUnite
        self.fonctionProduit = fonctionProduit
        self.idFou = idfou
        self.afficher = True

    def __str__(self):
        return str(self.idProduit) + self.nomProduit + str(self.nomUnite) + str(self.afficher) 
    
    def to_dict(self):
        return {
            'idProduit': self.idProduit,
            'nomProduit': self.nomProduit,
            'nomUnite': self.nomUnite,
            'afficher': self.afficher,
            'fonctionProduit' : self.fonctionProduit,
            'idFou':self.idFou
        }

class Commande(db.Model):

    __tablename__ = "COMMANDE"

    idCommande = Column(Integer, primary_key = True, nullable = False)
    dateCommande = Column(Date)
    qteCommande = Column(Integer)
    idChimiste = Column(Integer, ForeignKey("CHIMISTE.idChimiste"), nullable = False)
    idProduit = Column(Integer, ForeignKey("PRODUIT.idProduit"), nullable = False)
    commandeChim = relationship("Chimiste", back_populates="chimisteCom")
    commandeFaire = relationship("Faire", back_populates="faireCom")
    commandeProd = relationship("Produit", back_populates="produitCom")

    def __init__(self, idCommande, dateCommande, qteCommande, idChimiste, idProduit):
        self.idCommande = idCommande
        self.dateCommande = dateCommande
        self.qteCommande = qteCommande
        self.idChimiste = idChimiste
        self.idProduit = idProduit        
    
    def __str__(self):
        return str(self.idChimiste) + str(self.dateCommande) + str(self.qteCommande)  + str(self.idChimiste) + str(self.idProduit)


class Faire(db.Model):

    __tablename__ = "FAIRE"

    idCommande = Column(Integer, ForeignKey("COMMANDE.idCommande"), primary_key = True, nullable = False)
    idChimiste = Column(Integer, ForeignKey("CHIMISTE.idChimiste"), primary_key = True, nullable = False)
    statutCommande = Column(Text)
    faireCom = relationship("Commande", back_populates="commandeFaire")
    faireChim = relationship("Chimiste", back_populates="chimisteFaire")

    def __init__(self, idCommande, idChimiste, statutCommande):
        self.idCommande = idCommande
        self.idChimiste = idChimiste
        self.statutCommande = statutCommande
    
    def __str__(self):
        return str(self.idCommande) + str(self.idChimiste) + self.statutCommande


class Est_Stocker(db.Model):

    __tablename__ = "EST_STOCKER"
    
    idProduit = Column(Integer, ForeignKey("PRODUIT.idProduit"), primary_key = True, nullable = False)
    idLieu = Column(Integer, ForeignKey("LIEU_STOCKAGE.idLieu"), primary_key = True, nullable = False)
    quantiteStocke = Column(Integer)
    stockerLieu = relationship("Lieu_Stockage", back_populates="lieuStock")
    stockerProduit = relationship("Produit", back_populates="produitStock")

    def __init__(self, idProduit, idLieu, quantiteStocke):
        self.idProduit = idProduit
        self.idLieu = idLieu
        self.quantiteStocke = quantiteStocke
    
    def __str__(self):
        return str(self.idProduit) + " "+ str(self.idLieu) +" "+ str(self.quantiteStocke)
    
    def to_dict(self):
        return {
            'idProduit': self.idProduit,
            'idLieu': self.idLieu,
            'quantiteStocke': self.quantiteStocke
        }


class Lieu_Stockage(db.Model):
    
    __tablename__ = "LIEU_STOCKAGE"

    idLieu = Column(Integer, primary_key = True, nullable = False)
    nomLieu = Column(Text)
    lieuStock = relationship("Est_Stocker", back_populates="stockerLieu")


    def __init__(self, idLieu, nomLieu):
        self.idLieu = idLieu
        self.nomLieu = nomLieu
    
    def __str__(self):
        return str(self.idLieu) + self.nomLieu
    
    def to_dict(self):
        return {
            'idLieu': self.idLieu,
            'nomLieu': self.nomLieu
        }


class Fournisseur(db.Model):

    __tablename__ = "FOURNISSEUR"

    idFou = Column(Integer, primary_key = True, nullable = False)
    nomFou = Column(Text, unique=True)
    adresseFou = Column(Text)
    numTelFou = Column(Integer)
    fournisseurHist = relationship("Historique", back_populates="historiqueFour")
    fournisseurProd = relationship("Produit", back_populates="produitFour")



    def __init__(self, idFou, nomFou, adresseFou, numTelFou):

        self.idFou = idFou
        self.nomFou = nomFou
        self.adresseFou = adresseFou
        self.numTelFou = numTelFou
    
    def __str__(self):
        return str(self.idFou) + self.nomFou + self.adresseFou + str(self.numTelFou)

    def to_dict(self):
        return {
            'idFou': self.idFou,
            'nomFou': self.nomFou,
            'adresseFou': self.adresseFou,
            'numTelFou': self.numTelFou
        }
    
class Historique(db.Model):
    __tablename__ = "HISRORIQUE"

    idAction = Column(Integer, primary_key = True, nullable = False)
    nomAction = Column(Text)
    dateAction = Column(Date)
    qteFourni = Column(Integer)
    idFou = Column(Integer, ForeignKey("FOURNISSEUR.idFou"), nullable = False)
    idProduit = Column(Integer, ForeignKey("PRODUIT.idProduit"), nullable = False)
    historiqueProd = relationship("Produit", back_populates="produitHist")
    historiqueFour = relationship("Fournisseur", back_populates="fournisseurHist")


    def __init__(self, idAction, nomAction, dateAction, qteFourni, idFou, idProduit):
        self.idAction = idAction
        self.nomAction = nomAction
        self.dateAction = dateAction
        self.qteFourni = qteFourni
        self.idFou = idFou
        self.idProduit = idProduit
    
    def __str__(self):
        return str(self.idAction) + self.nomAction + str(self.dateAction) + str(self.qteFourni) + str(self.idFou) + str(self.idProduit)


@login_manager.user_loader
def load_user(email):
    return Chimiste.query.get(email)

def add_unite(nom):
    existing_unite = Unite.query.filter_by(nomUnite=nom).first()
    if not existing_unite and nom is not None:
        unit = Unite(nom)
        db.session.add(unit)
        db.session.commit()
   

def next_fou_id():
    max_id = db.session.query(func.max(Fournisseur.idFou)).scalar()
    next_id = (max_id or 0) + 1
    return next_id

def add_fournisseur(nom):
    existing_fou = Fournisseur.query.filter_by(nomFou=nom).first()
    if not existing_fou:
        id = next_fou_id()
        fou = Fournisseur(id, nom, None, None)
        db.session.add(fou)
        db.session.commit()


def get_id_fournisseur(nom):
    return Fournisseur.query.filter(Fournisseur.nomFou == nom).all()[0].idFou


def next_prod_id():
    max_id = db.session.query(func.max(Produit.idProduit)).scalar()
    next_id = (max_id or 0) + 1
    return next_id

def add_prod(nom, unite, fonctionProd, four):
    id = next_prod_id()
    add_unite(unite)
    add_fournisseur(four)
    id_fou = get_id_fournisseur(four)
    prod = Produit(id, nom, unite, fonctionProd, id_fou)
    db.session.add(prod)
    db.session.commit()
    return id

def get_id_prod(nom_prod):
    return Produit.query.filter(Produit.nomProduit == nom_prod).all()[0].idProduit


def next_lieu_id():
    max_id = db.session.query(func.max(Lieu_Stockage.idLieu)).scalar()
    next_id = (max_id or 0) + 1
    return next_id

def add_lieu_stock(nom_lieu):
    existing_lieu = Lieu_Stockage.query.filter_by(nomLieu=nom_lieu).first()
    if not existing_lieu:
        id = next_lieu_id()
        lieu = Lieu_Stockage(id, nom_lieu)
        db.session.add(lieu)
        db.session.commit()
        return id

def get_id_lieu(nom):
    return Lieu_Stockage.query.filter(Lieu_Stockage.nomLieu == nom).all()[0].idLieu

def add_est_stocker(idProduit, idLieu, quantiteStock):
    existing_stock = Est_Stocker.query.filter((Est_Stocker.idLieu == idLieu) & (Est_Stocker.idProduit == idProduit)).first()

    if existing_stock is None:
        objet = Est_Stocker(idProduit, idLieu, quantiteStock)
        db.session.add(objet)
        db.session.commit()
    else:
        if quantiteStock is not None:
            if existing_stock.quantiteStocke is None:
                existing_stock.quantiteStocke = quantiteStock
            else:
                existing_stock.quantiteStocke += quantiteStock

def next_chimiste_id():
    max_id = db.session.query(func.max(Chimiste.idChimiste)).scalar()
    next_id = (max_id or 0) + 1
    return next_id


def get_all_prod():
    return Produit.query.all()

def get_sample_prduit(nb=20):
    """Renvoie 20 produits de la base de donnée"""
    return Produit.query.limit(nb).all()

def get_sample_reservation(nb=20):
    """Renvoie 20 reservations de la base de donnée"""
    return Commande.query.limit(nb).all()


def search_filter(q):
    """renvoie une liste de produit selon une requete q  

    Args:
        q (str): requete de l'utilisateur

    Returns:
        list: liste de produit
    """
    results = get_all_prod()
    results2 = []
    for prod in results:
        if q.upper() in prod.nomProduit.upper():
            results2.append(prod)
    results = results2  
    return results


def search_famille_filter(q):
    results = get_all_prod()
    results2 = []
    for prod in results:
        if prod.fonctionProduit is None:
            prod.fonctionProduit = ""
        if q.upper() in prod.fonctionProduit.upper():
            results2.append(prod)
    
    results = results2
    return results

def edit_qte_commande(id_commande, new_qte):
    
    if new_qte >= 0:
        # Recherche de la commande et du statut de commande
        commande = Commande.query.get(id_commande)
        

        if not commande:
            print("Commande introuvable")
        

        # Vérifier le statut de la commande dans la table Faire
        statut = db.session.query(Faire).filter_by(idCommande=id_commande).first()
        
        if statut and statut.statutCommande == "Pas Commence":
            # Mise à jour de la quantité de la commande si le statut est correct
            commande.qteCommande = new_qte
            db.session.commit()
            print("Quantité de commande mise à jour avec succès.")
        else:
            print("Mise à jour refusée : le statut de commande ne permet pas la modification.")
    print("Erreur : qte inferieur à 0")

def check_mdp(mdp):
    """Fonction qui vérifie que le mot de passe contient au moins 8 craractères, 1 majuscule, 1 lettre, 1 caractère spécial

    Args:
        mdp (str): mdp a vérifier
    Return 
        bool True si le mot de passe est correct, false sinon
    """
    def contient_maj(mdp):
        for c in mdp:
            if c.isupper():
                return True
        return False

    def contient_special(mdp):
        special_characters = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        for c in mdp:
            if c in special_characters:
                return True
        return False
    
    def contient_chiffre(mdp):
        for c in mdp:
            if c in "0123456789":
                return True
        return False

    if len(mdp) >= 8 and contient_maj(mdp) and contient_special(mdp) and contient_chiffre(mdp):
        return True
    return False

def verif_fourn_existe(fournisseur):
    les_fours = Fournisseur.query.all()

    for fourn in les_fours:
        if fourn.nomFou == fournisseur:
            return True
    return False

def verif_lieu_existe(lieu):
    les_lieux = Lieu_Stockage.query.all()

    for endroit in les_lieux:
        if endroit.nomLieu == lieu:
            return True
    return False


def modif_sauvegarde(idProduit, nom, nom_fournisseur, quantite, fonction, lieu):
    produit = Produit.query.get(idProduit)
    four = Fournisseur.query.get(produit.idFou)
    stock = Est_Stocker.query.filter(Est_Stocker.idProduit == idProduit).first()
    le_lieu = Lieu_Stockage.query.get(stock.idLieu)

    if nom != "":
        produit.nomProduit = nom
    
    
    if nom_fournisseur != four.nomFou:
        if nom_fournisseur == "":
            produit.idFou = "null"
        elif verif_fourn_existe(nom_fournisseur):
            produit.idFou = four.idFou
        else:
            add_fournisseur(nom_fournisseur)
            res = Fournisseur.query.filter(Fournisseur.nomFou == nom_fournisseur).first()
            produit.idFou = res.idFou

    if quantite != "":
        stock.quantiteStock = quantite
    
    if fonction != "":
       produit.fonctionProduit = fonction

    if  lieu != le_lieu.nomLieu:

        if verif_lieu_existe(lieu):
            stock.idLieu = le_lieu.idLieu
        else:
            add_lieu_stock(lieu)
            res = Lieu_Stockage.query.filter(Lieu_Stockage.nomLieu == lieu).first()
            stock.idLieu = res.idLieu
    
    db.session.commit()
    print("Commande mise à jour")
    return True