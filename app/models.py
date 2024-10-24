#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, Date, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import func
import time
from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import registry

mapper_registry = registry()
Base = mapper_registry.generate_base()


class Chimiste(Base):

    __tablename__ = "CHIMISTE"

    idChimiste = Column(Integer, primary_key = True, nullable = False)
    prenom = Column(Text)
    nom = Column(Text)
    email = Column(Text)
    mdp = Column(Text)
    chimisteCom = relationship("Commande", back_populates="commandeChim")
    chimisteFaire = relationship("Faire", back_populates="faireChim")


    def __init__(self, idChimiste, prenom, nom, email, mdp):
        self.idChimiste = idChimiste
        self.prenom = prenom
        self.nom = nom
        self.email = email
        self.mdp = mdp
        
    def __str__(self):
        return str(self.idChimiste) + self.prenom + self.nom + self.email + self.mdp
    

class Unite(Base):

    __tablename__ = "UNITE"

    nomUnite = Column(Text, primary_key = True)
    uniteProd = relationship("Produit", back_populates="produitUnite")


    def __init__(self, nomUnite):
        self.nomUnite = nomUnite

    def __str__(self):
        return self.nomUnite

class Produit(Base):

    __tablename__ = "PRODUIT"

    idProduit = Column(Integer, primary_key = True, nullable = False)
    nomProduit = Column(Text)
    nomUnite = Column(Text, ForeignKey("UNITE.nomUnite"))
    afficher = Column(Boolean)
    produitUnite = relationship("Unite", back_populates="uniteProd")
    produitStock = relationship("Est_Stocker", back_populates="stockerProduit")
    produitHist = relationship("Historique", back_populates="historiqueProd")
    produitCom = relationship("Commande", back_populates="commandeProd")
    produitFour = relationship("Fournisseur", back_populates="fournisseurProd")


    def __init__(self, idProduit, nomProduit, nomUnite):
        self.idProduit = idProduit
        self.nomProduit = nomProduit
        self.nomUnite = nomUnite
        self.afficher = True

    def __str__(self):
        return str(self.idProduit) + self.nomProduit + self.nomUnite + str(self.afficher)

class Commande(Base):

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


class Faire(Base):

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
    
class Lieu_Stockage(Base):
    
    __tablename__ = "LIEU_STOCKAGE"

    idLieu = Column(Integer, primary_key = True, nullable = False)
    nomLieu = Column(Text)
    lieuStock = relationship("Est_Stocker", back_populates="stockerLieu")


    def __init__(self, idLieu, nomLieu):
        self.idLieu = idLieu
        self.nomLieu = nomLieu
    
    def __str__(self):
        return str(self.idLieu) + self.nomLieu
    

class Est_Stocker(Base):

    __tablename__ = "EST_STOCKER"
    
    idProduit = Column(Integer, ForeignKey("PRODUIT.idProduit"), primary_key = True, nullable = False)
    idLieu = Column(Integer, ForeignKey("LIEU.idLieu"), primary_key = True, nullable = False)
    quantiteStocke = Column(Integer)
    stockerLieu = relationship("Lieu_Stockage", back_populates="lieuStock")
    stockerProduit = relationship("Produit", back_populates="produitStock")

    def __init__(self, idProduit, idLieu, quantiteStocke):
        self.idProduit = idProduit
        self.idLieu = idLieu
        self.quantiteStocke = quantiteStocke
    
    def __str__(self):
        return str(self.idProduit) + str(self.idLieu) + self.quantiteStocke

class Fournisseur(Base):

    __tablename__ = "FOURNISSEUR"

    idFou = Column(Integer, primary_key = True, nullable = False)
    nomFou = Column(Text)
    adresseFou = Column(Text)
    numTelFou = Column(Integer)
    fournisseurHist = relationship("Historique", back_populates="historiqueFour")
    fournisseurProd = relationship("Produit", back_populates="produitFour")



    def __init__(self, idFou, nomFou, adresseFou, numTelFou):

        self.idFou = idFou
        self.nomFou = nomFou
        self.adresseFouFou = adresseFou
        self.numTelFou = numTelFou
    
    def __str__(self):
        return str(self.idFou) + self.nomFou + self.adresseFou + str(self.numTelFou)


class Historique(Base):

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
