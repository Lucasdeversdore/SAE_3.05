DROP TABLE IF EXISTS FAIRE;

DROP TABLE IF EXISTS EST_STOCKER;

DROP TABLE IF EXISTS COMMANDE;

DROP TABLE IF EXISTS LIEU_STOCKAGE;

DROP TABLE IF EXISTS HISTORIQUE;

DROP TABLE IF EXISTS FOURNISSEUR;

DROP TABLE IF EXISTS CHIMISTE;

DROP TABLE IF EXISTS PRODUIT;

DROP TABLE IF EXISTS UNITE;

CREATE TABLE FAIRE (
    idCommande int NOT NULL,
    idChimiste int NOT NULL,
    statutCommande VARCHAR(50),
    CONSTRAINT PK_Faire PRIMARY KEY (idCommande, idChimiste),
    CONSTRAINT FK_Faire_Chimiste FOREIGN KEY (idChimiste) REFERENCES CHIMISTE (idChimiste),
    CONSTRAINT FK_Faire_Commande FOREIGN KEY (idCommande) REFERENCES COMMANDE (idCommande)
);

CREATE TABLE EST_STOCKER (
    idProduit int NOT NULL,
    idLieu int NOT NULL,
    quantiteStocke int,
    CONSTRAINT PK_Est_Stocker PRIMARY KEY (idProduit, idLieu),
    CONSTRAINT FK_Est_Stocker_Produit FOREIGN KEY (idProduit) REFERENCES PRODUIT (idProduit),
    CONSTRAINT FK_Est_Stocker_Lieu FOREIGN KEY (idLieu) REFERENCES LIEU_STOCKAGE (idLieu)
);

CREATE TABLE COMMANDE (
    idCommande int NOT NULL,
    dateCommande date,
    qteCommande int,
    idChimiste int NOT NULL,
    idProduit int NOT NULL,
    CONSTRAINT PK_Commande PRIMARY KEY (idCommande),
    CONSTRAINT FK_Commande_Produit FOREIGN KEY (idProduit) REFERENCES PRODUIT (idProduit),
    CONSTRAINT FK_Commande_Chimiste FOREIGN KEY (idChimiste) REFERENCES CHIMISTE (idChimiste)
);

CREATE TABLE LIEU_STOCKAGE (
    idLieu int NOT NULL,
    nomLieu VARCHAR(50),
    CONSTRAINT PK_Lieu_Stockage PRIMARY KEY (idLieu)
);

CREATE TABLE HISTORIQUE (
    idAction int NOT NULL,
    nomAction VARCHAR(50),
    dateAction date,
    qteFourni int,
    idFou int NOT NULL,
    idProduit int NOT NULL,
    CONSTRAINT PK_Historique PRIMARY KEY (idAction),
    CONSTRAINT FK_Historique_Produit FOREIGN KEY (idProduit) REFERENCES PRODUIT (idProduit),
    CONSTRAINT FK_Historique_Fournisseur FOREIGN KEY (idFou) REFERENCES FOURNISSEUR (idFou)
);

CREATE TABLE FOURNISSEUR (
    idFou int NOT NULL,
    nomFou VARCHAR(50) UNIQUE,
    adresseFou VARCHAR(50),
    numTelFou int (10),
    CONSTRAINT PK_Fournisseur PRIMARY KEY (idFou)
);

CREATE TABLE CHIMISTE (
    idChimiste int NOT NULL,
    prenom VARCHAR(50),
    nom VARCHAR(50),
    email VARCHAR(50),
    mdp VARCHAR(50),
    estPreparateur boolean default false,
    CONSTRAINT PK_Chimiste PRIMARY KEY (idChimiste)
);

CREATE TABLE PRODUIT (
    idProduit int NOT NULL,
    nomProduit VARCHAR(50),
    nomUnite VARCHAR(50),
    afficher boolean default true,
    fonctionProduit VARCHAR(100),
    idFou int,
    CONSTRAINT PK_Produit PRIMARY KEY (idProduit),
    CONSTRAINT FK_Produit_Unite FOREIGN KEY (nomUnite) REFERENCES UNITE (nomUnite),
    CONSTRAINT FK_Produit_Fournisseur FOREIGN KEY (idFou) REFERENCES FOURNISSEUR (idFou)

);

CREATE TABLE UNITE (
    nomUnite VARCHAR(50),
    CONSTRAINT PK_Unite PRIMARY KEY (nomUnite)
);


CREATE TRIGGER insert_bon_mdp
BEFORE INSERT ON CHIMISTE
WHEN NOT (NEW.mdp GLOB '*[A-Z]*' AND NEW.mdp GLOB '*[0-9]*' AND NEW.mdp GLOB '*[!@#$%^&*()_+=<>?]*')
BEGIN
  SELECT RAISE(FAIL, 'Le mot de passe doit inclure : une lettre majuscule, un nombre et un caractere special');
END;



CREATE TRIGGER update_bon_mdp
BEFORE UPDATE ON CHIMISTE
WHEN NOT (NEW.mdp GLOB '*[A-Z]*' AND NEW.mdp GLOB '*[0-9]*' AND NEW.mdp GLOB '*[!@#$%^&*()_+=<>?]*')
BEGIN
  SELECT RAISE(FAIL, 'Le mot de passe doit inclure : une lettre majuscule, un nombre et un caractere special');
END;

CREATE TRIGGER verif_qte_commande
BEFORE INSERT ON COMMANDE
WHEN NOT (NEW.qteCommande) < (SELECT quantiteStocke from EST_STOCKER where NEW.idProduit = idProduit)
BEGIN
    SELECT RAISE(FAIL, 'La quantite commandee doit être inférieur à la quantité stocké');
END;

insert into EST_STOCKER values(1, 1, 10);
insert into COMMANDE values(1, "18/11/2004", 11, 1, 1);