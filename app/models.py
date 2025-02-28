#!/usr/bin/python3
import base64
import time, os
from flask import url_for
from flask_login import UserMixin
from flask_mail import Message
from sqlalchemy import Column, Float, Integer, Text, Date, Boolean
from sqlalchemy.orm import relationship 
from sqlalchemy.sql.schema import ForeignKey
from .app import login_manager
from itsdangerous import URLSafeTimedSerializer as Serializer
from sqlalchemy import func
from .app import  mail, db, app
from wtforms import ValidationError
from fpdf import FPDF


class Chimiste(db.Model, UserMixin): # pragma: no cover

    __tablename__ = "CHIMISTE"

    idChimiste = Column(Integer, primary_key = True, nullable = False)
    prenom = Column(Text)
    nom = Column(Text)
    email = Column(Text)
    mdp = Column(Text)
    info = Column(Boolean)
    estPreparateur = Column(Boolean)
    chimisteCom = relationship("Commande", back_populates="commandeChim")
    chimisteFaire = relationship("Faire", back_populates="faireChim")


    def __init__(self, idChimiste, prenom, nom, email, mdp, estPreparateur=False):
        self.idChimiste = idChimiste
        self.prenom = prenom
        self.nom = nom
        self.email = email
        self.mdp = mdp
        self.info = True
        self.estPreparateur = estPreparateur
        
    def __str__(self):
        return str(self.idChimiste) + self.prenom + self.nom + self.email + self.mdp
    
    def get_id(self):
        return self.idChimiste
    
    def get_token(self):
        # Utilisez URLSafeTimedSerializer avec expires_in pour définir l'expiration du token
        serial = Serializer(app.config['SECRET_KEY']) 
        # Sérialisez les données de l'utilisateur dans un token
        token= serial.dumps({
            'idChimiste': self.idChimiste,
            'prenom': self.prenom,
            'nom': self.nom,
            'email': self.email,
            'mdp': self.mdp,
            'preparateur': self.estPreparateur
        })
        return token
    
    @staticmethod
    def verify_mdp_token(token, time_in_link):
        print("ds verif mdp " +time_in_link)
        if time_in_link != "pass" and time_in_link != "app.js":
            time_limit = 60*15 # 15 min
            if (time.time() - float(time_in_link)) > time_limit:
                return None
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)['idChimiste']
        except:
            return None
        return Chimiste.query.get(user_id)
    
    @staticmethod
    def verify_activation_token(token, time_in_link):
        time_limit = 15*60 # 15 min
        if (time.time() - float(time_in_link)) > time_limit:
            return None
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            idChimiste = serial.loads(token)['idChimiste']
            prenom =  serial.loads(token)['prenom']
            nom = serial.loads(token)['nom']
            email = serial.loads(token)['email'] 
            mdp = serial.loads(token)['mdp']
            estPreparateur=serial.loads(token)['preparateur']

            return Chimiste(idChimiste=idChimiste, prenom=prenom, nom=nom, email=email, mdp=mdp, estPreparateur=estPreparateur)
        except:
            return None
    
    def changer_nom(self, nom):
        self.nom = nom
        db.session.commit()

    def changer_prenom(self, prenom):
        self.prenom = prenom
        db.session.commit()

    def reception_notif(self):
        self.info = not self.info
        db.session.commit()


class Unite(db.Model): # pragma: no cover

    __tablename__ = "UNITE"

    nomUnite = Column(Text, primary_key = True)
    uniteProd = relationship("Produit", back_populates="produitUnite")


    def __init__(self, nomUnite):
        self.nomUnite = nomUnite

    def __str__(self):
        return self.nomUnite


class Produit(db.Model): # pragma: no cover

    __tablename__ = "PRODUIT"

    idProduit = Column(Integer, primary_key = True, nullable = False)
    nomProduit = Column(Text)
    nomUnite = Column(Text, ForeignKey("UNITE.nomUnite"))
    afficher = Column(Boolean)
    seuilProduit = Column(Integer)
    fonctionProduit = Column(Text)
    idFou = Column(Integer, ForeignKey("FOURNISSEUR.idFou"))
    produitUnite = relationship("Unite", back_populates="uniteProd")
    produitStock = relationship("Est_Stocker", back_populates="stockerProduit")
    produitHist = relationship("Historique", back_populates="historiqueProd")
    produitCom = relationship("Commande", back_populates="commandeProd")
    produitFour = relationship("Fournisseur", back_populates="fournisseurProd")


    def __init__(self, idProduit, nomProduit, nomUnite, seuilProduit, fonctionProduit, idfou):
        self.idProduit = idProduit

        self.nomProduit = nomProduit
        self.nomUnite = nomUnite
        self.seuilProduit = seuilProduit
        self.fonctionProduit = fonctionProduit
        self.idFou = idfou
        self.afficher = True
        if self.idProduit == 1:
            self.afficher = False

    def __str__(self):
        return str(self.idProduit) + self.nomProduit + str(self.nomUnite) + str(self.afficher) 
    
    def to_dict(self):
        return {
            'idProduit': self.idProduit,
            'nomProduit': self.nomProduit,
            'nomUnite': self.nomUnite,
            'seuilProduit' : self.seuilProduit,
            'afficher': self.afficher,
            'fonctionProduit' : self.fonctionProduit,
            'idFou':self.idFou
        }


class Commande(db.Model): # pragma: no cover

    __tablename__ = "COMMANDE"

    idCommande = Column(Integer, primary_key = True, nullable = False)
    dateCommande = Column(Date)
    qteCommande = Column(Integer)
    idChimiste = Column(Integer, ForeignKey("CHIMISTE.idChimiste"), nullable = False)
    idProduit = Column(Integer, ForeignKey("PRODUIT.idProduit"), nullable = False)
    commandeChim = relationship("Chimiste", back_populates="chimisteCom")
    commandeFaire = relationship("Faire", back_populates="faireCom")
    commandeProd = relationship("Produit", back_populates="produitCom")

    def __init__(self, idCommande, qteCommande, idChimiste, idProduit, dateCommande=func.current_date()):
        self.idCommande = idCommande
        self.dateCommande = dateCommande
        self.qteCommande = qteCommande
        self.idChimiste = idChimiste
        self.idProduit = idProduit
    
    def __str__(self):
        return str(self.idChimiste) + str(self.dateCommande) + str(self.qteCommande)  + str(self.idChimiste) + str(self.idProduit)
    
    def to_dict(self):
        return {
            'idCommande': self.idCommande,
            'qteCommande': self.qteCommande,
            'idChimiste': self.idChimiste,
            'idProduit': self.idProduit,
            'dateCommande' : self.dateCommande
        }


class Faire(db.Model): # pragma: no cover

    __tablename__ = "FAIRE"

    idCommande = Column(Integer, ForeignKey("COMMANDE.idCommande"), primary_key = True, nullable = False)
    idChimiste = Column(Integer, ForeignKey("CHIMISTE.idChimiste"), primary_key = True, nullable = False)
    statutCommande = Column(Text)
    faireCom = relationship("Commande", back_populates="commandeFaire")
    faireChim = relationship("Chimiste", back_populates="chimisteFaire")

    def __init__(self, idCommande, idChimiste, statutCommande = 'non-commence'):
        self.idCommande = idCommande
        self.idChimiste = idChimiste
        self.statutCommande = statutCommande
    
    def __str__(self):
        return str(self.idCommande) + str(self.idChimiste) + self.statutCommande


class Est_Stocker(db.Model): # pragma: no cover

    __tablename__ = "EST_STOCKER"
    
    idProduit = Column(Integer, ForeignKey("PRODUIT.idProduit"), primary_key = True, nullable = False)
    idLieu = Column(Integer, ForeignKey("LIEU_STOCKAGE.idLieu"), primary_key = True, nullable = False)
    quantiteStocke = Column(Float)
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


class Lieu_Stockage(db.Model): # pragma: no cover
    
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


class Fournisseur(db.Model): # pragma: no cover

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
        return str(self.idFou) + str(self.nomFou) + str(self.adresseFou) + str(self.numTelFou)

    def to_dict(self):
        return {
            'idFou': self.idFou,
            'nomFou': self.nomFou,
            'adresseFou': self.adresseFou,
            'numTelFou': self.numTelFou
        }


class Historique(db.Model): # pragma: no cover
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

def add_fournisseur(nom, addr, tel):
    if addr == "":
        addr = None
    if tel == "":
        tel = None
    existing_fou = Fournisseur.query.filter_by(nomFou=nom).first()
    if not existing_fou:
        id = next_fou_id()
        fou = Fournisseur(id, nom, addr, tel)
        db.session.add(fou)
        db.session.commit()
        return True
    return False


def get_id_fournisseur(nom):
    return Fournisseur.query.filter(Fournisseur.nomFou == nom).all()[0].idFou


def next_prod_id():
    max_id = db.session.query(func.max(Produit.idProduit)).scalar()
    next_id = (max_id or 0) + 1
    return next_id

def add_prod(nom, unite, seuil, fonctionProd, four):
    id = next_prod_id()
    add_unite(unite)
    if four:
        add_fournisseur(four, None, None)
        id_fou = get_id_fournisseur(four)
    else:
        four = Fournisseur.query.filter(Fournisseur.nomFou == "").first()
        if four:
            id_fou = four.idFou
        else:
            add_fournisseur("", "", "")
            id_fou = next_fou_id()-1
    if nom != "" and nom is not None:
        prod = Produit(id, nom, unite, seuil, fonctionProd, id_fou)
        db.session.add(prod)
        db.session.commit()
        return id


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
        
    else:
        existing_stock.quantiteStocke += quantiteStock
    db.session.commit()

def next_chimiste_id():
    max_id = db.session.query(func.max(Chimiste.idChimiste)).scalar()
    next_id = (max_id or 0) + 1
    return next_id


def get_all_prod():
    return Produit.query.all()

def get_all_prod_qte():
    liste_prod_qte = []
    liste_prod = Produit.query.all()
    for produit in liste_prod:
        est_stocker = Est_Stocker.query.filter(Est_Stocker.idProduit == produit.idProduit).first()
        if est_stocker is None:
            qte = 0
        else:
            qte = est_stocker.quantiteStocke
        liste_prod_qte.append((produit, qte))
    return liste_prod_qte


def get_all_chimiste():
    return Chimiste.query.all()

def get_pagination_produits(page=1, nb=15):
    # Pour les produits non caché
    liste_prod_qte = []
    liste_prod = Produit.query.filter(Produit.afficher == 1).all()
    liste_prod_cacher = Produit.query.filter(Produit.afficher == False).all()
    liste_prod = liste_prod + liste_prod_cacher
    liste_prod = liste_prod[(page-1)*nb:page*nb]
    for produit in liste_prod:
        est_stocker = Est_Stocker.query.filter(Est_Stocker.idProduit == produit.idProduit).first()
        if est_stocker is None:
            qte = 0
        else:
            qte = est_stocker.quantiteStocke
        liste_prod_qte.append((produit, qte))
    return liste_prod_qte


def get_nb_page_max_produits(nb):
    return len(Produit.query.all())//nb+1

def get_sample_reservation(nb=20):
    """Renvoie 20 reservations, ses états, chimistes et produits de la base de donnée"""
    liste_reserv_etat = []
    liste_reserv = Commande.query.limit(nb).all()
    for reservation in liste_reserv:
        faire = Faire.query.filter(Faire.idCommande == reservation.idCommande).first()
        chimiste = Chimiste.query.filter(Chimiste.idChimiste == reservation.idChimiste).first()
        produit = Produit.query.filter(Produit.idProduit == reservation.idProduit).first()
        if faire and chimiste and produit:
            etat = faire.statutCommande
            liste_reserv_etat.append((reservation, etat, chimiste, produit))
    return liste_reserv_etat

def get_pagination_reservations(page, nb, chimiste):
    liste_reserv_etat = []
    if not chimiste.estPreparateur:
        liste_reserv = Commande.query.filter(Commande.idChimiste == chimiste.idChimiste).all()
    else:
        liste_reserv = Commande.query.order_by(Commande.dateCommande).all()
    liste_reserv = liste_reserv[(page-1)*nb:page*nb]
    for reservation in liste_reserv:
        faire = Faire.query.filter(Faire.idCommande == reservation.idCommande).first()
        chimiste = Chimiste.query.filter(Chimiste.idChimiste == reservation.idChimiste).first()
        produit = Produit.query.filter(Produit.idProduit == reservation.idProduit).first()
        if faire and chimiste and produit:
            etat = faire.statutCommande
            liste_reserv_etat.append((reservation, etat, chimiste, produit))
    return liste_reserv_etat

def get_nb_page_max_reservations(nb, chimiste):
    if chimiste.estPreparateur:
        return len(Commande.query.all())//nb+1
    else:
        return len(Commande.query.filter(Commande.idChimiste == chimiste.idChimiste).all())//nb+1

def get_sample_reservation_chimiste(chimiste:Chimiste):
    """renvoi les Commandes avec leurs états du chimiste

    Args:
        chimiste (Chimiste): un Chimiste
    Return:
        list: liste des Commande avec leurs états du chimiste
    """
    liste_reserv_etat = []
    liste_reserv = Commande.query.filter(Commande.idChimiste == chimiste.idChimiste).all()
    for reservation in liste_reserv:
        faire = Faire.query.filter(Faire.idCommande == reservation.idCommande).first()
        chimiste = Chimiste.query.filter(Chimiste.idChimiste == reservation.idChimiste).first()
        produit = Produit.query.filter(Produit.idProduit == reservation.idProduit).first()
        if faire and chimiste and produit:
            etat = faire.statutCommande
            liste_reserv_etat.append((reservation, etat, chimiste, produit))
    return liste_reserv_etat

def search_filter(q):
    """renvoie une liste de produit_qte selon une requete q  

    Args:
        q (str): requete de l'utilisateur

    Returns:
        list: liste de produit_qte
    """
    results = get_all_prod()
    results2 = []
    for prod in results:
        if q.upper() in prod.nomProduit.upper():
            est_stocker = Est_Stocker.query.filter(Est_Stocker.idProduit == prod.idProduit).first()
            if est_stocker is None:
                qte = 0
            else:
                qte = est_stocker.quantiteStocke
            results2.append((prod,qte))
    results = results2
    return results


def search_famille_filter(q):
    results = get_all_prod()
    results2 = []
    for prod in results:
        if prod.fonctionProduit is None:
            prod.fonctionProduit = ""
        if q.upper() in prod.fonctionProduit.upper():
            est_stocker = Est_Stocker.query.filter(Est_Stocker.idProduit == prod.idProduit).first()
            if est_stocker is None:
                qte = 0
            else:
                qte = est_stocker.quantiteStocke
            results2.append((prod,qte))
    
    results = results2
    return results

def search_reserv_filter(q):
    """renvoie une liste des reservation selon une requete q  

    Args:
        q (str): requete de l'utilisateur

    Returns:
        list: liste de reservation
    """
    results = get_all_prod()
    results2 = []
    if q is None:
        return []
    for prod in results:
        if q.upper() in prod.nomProduit.upper():
            commandes = Commande.query.filter(Commande.idProduit == prod.idProduit)
            for commande in commandes:
                etat = Faire.query.filter(Faire.idCommande == commande.idCommande).first()
                etat= etat.statutCommande
                chimiste = Chimiste.query.filter(Chimiste.idChimiste == commande.idChimiste).first()
                prod = Produit.query.filter(Produit.idProduit == commande.idProduit).first()
                results2.append((commande,etat,chimiste,prod))
    results = results2
    return results

def search_chimiste_filter(q):
    results = get_all_chimiste()
    results2 = []
    if q is None:
        return []
    for chimiste in results:
        if q.upper() in chimiste.nom.upper() or q.upper() in chimiste.prenom.upper():
            commandes = Commande.query.filter(Commande.idChimiste == chimiste.idChimiste)
            for commande in commandes:
                etat = Faire.query.filter(Faire.idCommande == commande.idCommande).first()
                etat= etat.statutCommande
                chimiste = Chimiste.query.filter(Chimiste.idChimiste == commande.idChimiste).first()
                prod = Produit.query.filter(Produit.idProduit == commande.idProduit).first()
                results2.append((commande,etat,chimiste,prod))
    results = results2
    return results


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
        return (True, "")
    return (False, "mdp doit contenir au moins : 1 majuscule, 1 caractère spécial, 1 chiffre et doit faire au moins 8 caractères")

def verif_fourn_existe(fournisseur):
    les_fours = Fournisseur.query.all()

    for fourn in les_fours:
        if fourn.nomFou == fournisseur:
            return True
    return False



def modif_sauvegarde(idProduit, nom, nom_fournisseur, quantite, seuil, fonction, lieu):
    produit = Produit.query.get(idProduit)
    four = Fournisseur.query.filter(Fournisseur.nomFou == nom_fournisseur).first()
    produit.idFou = four.idFou
    produit.seuilProduit = seuil
    stock = Est_Stocker.query.filter(Est_Stocker.idProduit == idProduit).first()
    le_lieu = Lieu_Stockage.query.filter(Lieu_Stockage.nomLieu == lieu).first()
    stock.idLieu = le_lieu.idLieu
    
    if nom != "":
        produit.nomProduit = nom

        if verif_fourn_existe(nom_fournisseur) and four is not None:
            produit.idFou = four.idFou
        else:
            add_fournisseur(nom_fournisseur, None, None)
            res = Fournisseur.query.filter(Fournisseur.nomFou == nom_fournisseur).first()
            produit.idFou = res.idFou

    if quantite != "":
        stock.quantiteStocke = quantite
    
    if fonction != "":
       produit.fonctionProduit = fonction


    db.session.commit()
    print(stock)
    print("Commande mise à jour")
    return True


def cacher_le_produit(idProduit):
    produit = Produit.query.get(idProduit)
    produit.afficher = False
    db.session.commit()
    return True

def montrer_le_produit(idProduit):
    produit = Produit.query.get(idProduit)
    produit.afficher = 1
    db.session.commit()
    return True


def check_mdp_validator(form, field):
    """
    Validateur WTForms pour le champ mot de passe, utilisant la fonction `check_mdp`.

    Args:
        form (FlaskForm): L'instance du formulaire contenant le champ.
        field (Field): Le champ PasswordField à valider.

    Raises:
        ValidationError: Si le mot de passe est invalide selon les règles de `check_mdp`.

    Returns:
        None, lève une ValidationError si la validation échoue.
    """
    
    from .models import check_mdp
    from wtforms import ValidationError
    result = check_mdp(field.data)  # Appel de la fonction check_mdp
    if isinstance(result, bool):
        is_valid = result
        error_message = ""
    else:
        is_valid, error_message = result

    if not is_valid:  # Si le mot de passe n'est pas valide
        # Affiche le message d'erreur spécifique
        raise ValidationError(error_message)


def password_change_validator(form, field):
    # Champs à valider
    mdp = form.mdp.data
    old_mdp = form.old_mdp.data
    confirm_mdp = form.confirm_mdp.data
    if mdp:
        if field == form.old_mdp:
            if not old_mdp:
                raise ValidationError("L'ancien mot de passe est requis pour changer le mot de passe.")
        if field == form.confirm_mdp:
            if not confirm_mdp:
                raise ValidationError("Vous devez confirmer le nouveau mot de passe.")
        check_mdp_validator(form, field)


def send_mail_activation(user:Chimiste):
    token=user.get_token()
    time_in_link = time.time()

    encoded_time = base64.urlsafe_b64encode(str(time_in_link).encode()).decode()

    reset_url = url_for('activation_token', token=token, time_in_link=encoded_time, _external=True)
    
    msg = Message(
        'Activation de votre compte Stockage Chimie',
        recipients=[user.email],
        sender='noreply@codejana.com'
    )

    # Contenu de l'e-mail en HTML
    msg.html = f'''
                <!doctype html>
                <html>
                    <body>
                        <p>Pour activez votre compte Stockage Chimie, cliquez sur le lien ci-dessous :</p>
                        <p><a href="{reset_url}">Activez votre compte</a></p>
                        <p>Si vous n'avez pas demandé cette activation, ignorez simplement cet e-mail.</p>
                    </body>
                </html>
                '''
    mail.send(msg)
    print(msg)


def send_mail_mdp(user: Chimiste):
    token = user.get_token()
    time_in_link = time.time()

    encoded_time = base64.urlsafe_b64encode(str(time_in_link).encode()).decode()

    print("envoie mail " + str(time_in_link))
    reset_url = url_for('reset_token', token=token, time_in_link=encoded_time, _external=True)

    msg = Message(
        'Demande de réinitialisation de mot de passe',
        recipients=[user.email],
        sender='noreply@codejana.com'
    )

    # Contenu de l'e-mail en HTML
    msg.html = f'''
                <!doctype html>
                <html>
                    <body>
                        <p>Pour réinitialiser votre mot de passe, cliquez sur le lien ci-dessous :</p>
                        <p><a href="{reset_url}">Réinitialiser votre mot de passe</a></p>
                        <p>Si vous n'avez pas demandé cette réinitialisation, ignorez simplement cet e-mail.</p>
                    </body>
                </html>
                '''

    mail.send(msg)
    print(msg)


def send_mail_etat(user: Chimiste, commande: Commande):
    if user.info:
        produit = Produit.query.get(commande.idProduit)
        faire = Faire.query.filter(Faire.idCommande == commande.idCommande).first()

        msg = Message(
            'Avancement de votre commande de ' + produit.nomProduit,
            recipients=[user.email],
            sender='noreply@codejana.com'
        )

        # Vérifier le statut de la commande et construire le contenu du message
        if faire.statutCommande == 'en-cours':
            # Contenu de l'e-mail en texte brut
            msg.body = f'''Votre commande de {produit.nomProduit} du {commande.dateCommande} est en cours de préparation.'''
        else:
            msg.body = f'''Votre commande de {produit.nomProduit} du {commande.dateCommande} est terminée.'''

        mail.send(msg)


def send_mail_supp(user: Chimiste, commande:Commande):
    if user.info:
        produit = Produit.query.get(commande.idProduit)
        faire = Faire.query.filter(Faire.idCommande == commande.idCommande).first()

        msg = Message(
            'Avancement de votre commande de ' + produit.nomProduit,
            recipients=[user.email],
            sender='noreply@codejana.com'
        )

        # Vérifier le statut de la commande et construire le contenu du message
            # Contenu de l'e-mail en texte brut
        msg.body = f'''Votre commande de {produit.nomProduit} du {commande.dateCommande} a été supprimé par un laborentain.'''

        mail.send(msg)


def next_commande_id():
    max_id = db.session.query(func.max(Commande.idCommande)).scalar()
    next_id = (max_id or 0) + 1
    return next_id


def reserver_prod(id_produit, qte, user):
    """Fonction qui permet de réserver une quantité d'un produit

    Args:
        id_produit (int): l'id du produit
        qte (float): la quantité reservé
        user (int): l'id du chimiste qui a réservé
    """
    prod = Produit.query.get(id_produit)
    if prod:
        est_stocker =  Est_Stocker.query.filter(Est_Stocker.idProduit == id_produit).first()
        if est_stocker is None:
            qte_dispo = 0
        else:
            qte_dispo = est_stocker.quantiteStocke
        if qte is not None and qte <= qte_dispo and qte > 0:
            id = next_commande_id()
            commande = Commande(id, qte, user,id_produit)
            db.session.add(commande)
            faire = Faire(commande.idCommande, user)
            db.session.add(faire)
            qte_restante = qte_dispo-qte
            est_stocker.quantiteStocke = qte_restante
            convertir_quantite(id_produit)
            db.session.commit()
            return True
        
def save_modif_reserv(id_commande, qte, qte_base):
    """Fonction qui permet de modifier la quantité d'une réservation

    Args:
        id_commande (int): l'id de la commande
        qte (float): la quantité reservé modifié
        qte_base (float): la quantité reservé de base
    """
    commande = Commande.query.get(id_commande)
    prod = Produit.query.get(commande.idProduit)
    if prod:
        est_stocker =  Est_Stocker.query.filter(Est_Stocker.idProduit == commande.idProduit).first()
        if est_stocker is None:
            qte_dispo = qte_base
        else:
            qte_dispo = est_stocker.quantiteStocke + qte_base
        if qte is not None and qte <= qte_dispo and qte > 0:
            est_stocker.quantiteStocke = qte_dispo
            db.session.commit()

            qte_restante = qte_dispo-qte
            est_stocker.quantiteStocke = qte_restante
            db.session.add(est_stocker)
            commande.qteCommande = qte
            db.session.add(commande)
            convertir_quantite(commande.idProduit)
            db.session.commit()
            return True

def ajout_sauvegarde(nom, nom_fournisseur, unite, quantite, seuil, fonction, lieu):
    """Fonction qui permet d'ajouter un produit à la bd

    Args:
        nom (String): nom du produit
        nom_fournisseur (String): nom du fournisseur
        unite (String): nom de l'unite (L, g, mL ...)
        quantite (String, float): quantité deisponible du produit 
        fonction (String): famille du produit 
        lieu (String): nom du lieu de stockage

    Returns:
        bool: True si l'ajout du produit se passe bien
    """
    
    if add_prod(nom, unite, seuil, fonction, nom_fournisseur):
        prod = Produit.query.get(next_prod_id()-1)
        id_prod = prod.idProduit
        le_lieu = Lieu_Stockage.query.filter(Lieu_Stockage.nomLieu == lieu).first()
        if not le_lieu:
            add_lieu_stock(lieu)
            le_lieu = next_lieu_id()-1
        else:
            le_lieu = le_lieu.idLieu  
        try:
            quantite = float(quantite)
        except:
            quantite = 0
        stock = Est_Stocker(id_prod, le_lieu, quantite)
        db.session.add(stock)
        convertir_quantite(id_prod)
        db.session.commit()
        return True
    
def ajout_lieu_sauvegarde(nom_lieu):
    """Ajoute un lieu de stockage dans la base de données.

    Args:
        nom_lieu (String): Nom du lieu de stockage.

    Returns:
        bool: True si l'ajout se passe bien.
    """
    # Vérifie si le lieu existe déjà
    lieu_existant = Lieu_Stockage.query.filter_by(nomLieu=nom_lieu).first()
    if not lieu_existant:
        # Ajoute le lieu
        id_lieu = add_lieu_stock(nom_lieu)
        if id_lieu:
            add_lieu_stock(nom_lieu)
            return True  # Ajout réussi
        else:
            db.session.rollback()
            return False  # Échec lors de l'ajout
    else:
        return False  # Le lieu existe déjà

def ajout_fournisseur_sauvegarde(nom_fou, adresse_fou=None, num_tel_fou=None):
    """Ajoute un fournisseur dans la base de données.

    Args:
        nom_fou (String): Nom du fournisseur (obligatoire).
        adresse_fou (String, optional): Adresse du fournisseur.
        num_tel_fou (String, int, optional): Numéro de téléphone du fournisseur.

    Returns:
        bool: True si l'ajout se passe bien, False sinon.
    """
    # Vérifie si le fournisseur existe déjà
    fournisseur_existant = Fournisseur.query.filter_by(nomFou=nom_fou).first()
    if not fournisseur_existant:
        id_fou = add_fournisseur(nom_fou, adresse_fou, num_tel_fou)
        if id_fou:
            return True # Ajout réussi
        else: # pragma: no cover
            db.session.rollback()
            return False # Échec lors de l'ajout
    else:
        return False  # Le fournisseur existe déjà






def convertir_quantite(id_produit):
    """convertis les unités tous en adaptant la quantite,
    quand qte restante < 1 convertir sur l'unité inférieur, 
    quand qte restante > 999 convertir sur l'unité supérieur
    Args:
        id_produit (int): id d'un produit
    """
    stock = Est_Stocker.query.filter(Est_Stocker.idProduit == id_produit).first()
    quantite = float(stock.quantiteStocke)
    if quantite < 1 and quantite > 0:
        prod = Produit.query.get(id_produit)
        
        if prod:
            unite = prod.nomUnite
            match unite:
                case "L":
                    prod.nomUnite = "mL"
                    stock.quantiteStocke = quantite *10**3
                case "kg":
                    prod.nomUnite = "g"
                    stock.quantiteStocke = quantite *10**3
            db.session.commit()
    elif quantite > 999:
        prod = Produit.query.get(id_produit)
        if prod:
            
            unite = prod.nomUnite
            match unite:

                case "mL":
                    prod.nomUnite = "L"
                    stock.quantiteStocke = quantite *10**-3
                case "g":
                    prod.nomUnite = "kg"
                    stock.quantiteStocke = quantite *10**-3
            db.session.commit()

def update_etat(idCommande, idChimiste):
    faire = Faire.query.filter(Faire.idCommande == idCommande).first()
    if faire is not None:
        match faire.statutCommande:
            case 'non-commence':
                faire.idChimiste = idChimiste
                faire.statutCommande = 'en-cours'
            case 'en-cours':
                faire.statutCommande = 'termine'
        db.session.commit()

def delete_reservation(idCommande, idChimiste):
    commande = Commande.query.get(idCommande)
    if commande is not None:
        faire = Faire.query.filter(Faire.idCommande == idCommande).first()
        if faire is not None:
            if faire.statutCommande == 'non-commence' or (Chimiste.query.get(idChimiste).estPreparateur and faire.statutCommande == "en-cours"):
                produit = Produit.query.get(commande.idProduit)
                est_Stocker = Est_Stocker.query.filter(Est_Stocker.idProduit == produit.idProduit).first()
                est_Stocker.quantiteStocke += commande.qteCommande
                db.session.delete(faire)
                db.session.delete(commande)
                db.session.commit()

def est_en_dessous_du_seuil():
    """Renvoie une liste des produits qui sont en dessous de leur seuil

    Returns:
        list: liste des produits qui sont en dessous de leur seuil
    """
    liste_prod = Produit.query.all()
    liste_prod_seuil = []
    for prod in liste_prod:
        est_stocker = Est_Stocker.query.filter(Est_Stocker.idProduit == prod.idProduit).first()
        if est_stocker is None:
            qte = 0
        else:
            qte = est_stocker.quantiteStocke
        if qte < prod.seuilProduit:
            liste_prod_seuil.append((prod, qte, prod.nomUnite))
    return liste_prod_seuil

def get_unique_filename(base_name="produits_seuil.pdf", folder="app"): # pragma: no cover
    """Génère un nom de fichier unique en évitant les doublons"""
    base_path = os.path.join(os.getcwd(), folder)  # Chemin du dossier cible
    if not os.path.exists(base_path):
        os.makedirs(base_path)  # Crée le dossier s'il n'existe pas

    file_path = os.path.join(base_path, base_name)
    
    if not os.path.exists(file_path):
        return file_path  # Si le fichier n'existe pas encore, on le retourne

    # Sinon, on cherche un nom unique (produits_seuil(1).pdf, produits_seuil(2).pdf, ...)
    filename, ext = os.path.splitext(base_name)
    i = 1
    while os.path.exists(os.path.join(base_path, f"{filename}({i}){ext}")):
        i += 1
    
    return os.path.join(base_path, f"{filename}({i}){ext}")


def creer_pdf_produit_en_dessous_du_seuil():  # pragma: no cover
    """Crée un PDF listant les produits sous leur seuil avec un tableau structuré"""

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Produits en dessous de leur seuil", ln=True, align='C')

    pdf.ln(10)

    # En-tête du tableau
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(90, 10, "Nom du produit", border=1, align='C')
    pdf.cell(50, 10, "Quantité en stock", border=1, align='C')
    pdf.cell(50, 10, "Unité", border=1, align='C')
    pdf.ln()

    # Remplissage du tableau avec les données
    pdf.set_font("Arial", size=10)
    for prod in est_en_dessous_du_seuil():
        produit_nom = prod[0].nomProduit.encode('latin-1', 'replace').decode('latin-1')
        quantite = f"{prod[1]:.4f}".rstrip("0").rstrip(".")
        unite = prod[2] if prod[2] is not None else "N/A"

        pdf.cell(90, 10, produit_nom, border=1, align='L')
        pdf.cell(50, 10, quantite, border=1, align='C')
        pdf.cell(50, 10, unite, border=1, align='C')
        pdf.ln()

    # Générer un nom unique pour éviter d'écraser les fichiers existants
    pdf_path = get_unique_filename()
    pdf.output(pdf_path)

    return pdf_path
