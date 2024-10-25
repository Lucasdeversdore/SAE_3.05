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
    idFou int,
    CONSTRAINT PK_Produit PRIMARY KEY (idProduit),
    CONSTRAINT FK_Produit_Unite FOREIGN KEY (nomUnite) REFERENCES UNITE (nomUnite),
    CONSTRAINT FK_Produit_Fournisseur FOREIGN KEY (idFou) REFERENCES FOURNISSEUR (idFou)

);

CREATE TABLE UNITE (
    nomUnite VARCHAR(50),
    CONSTRAINT PK_Unite PRIMARY KEY (nomUnite)
);

