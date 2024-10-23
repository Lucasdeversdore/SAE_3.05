create table CHIMISTE (
    PRIMARY KEY (idChimiste)
    idChimiste int NOT NULL,
    prenom VARCHAR(50),
    nom VARCHAR(50),
    email VARCHAR(50),
    mdp VARCHAR(50),
    estPreparateur boolean
);


create table COMMANDE (
    PRIMARY KEY (idCommande),
    idCommande int NOT NULL,
    dateCommande date,
    qteCommande int,
    idChimiste int NOT NULL,
    idProduit int NOT NULL
);

create table FAIRE (
    PRIMARY KEY(idCommande, idChimiste)
    idCommande int NOT NULL,
    idChimiste int NOT NULL,
    statutCommande VARCHAR(50)
);

create table PRODUIT (
    PRIMARY KEY(idProduit)
    idProduit int NOT NULL,
    nomProduit VARCHAR(50),
    fonctionProduit VARCHAR(50),
    nomUnite VARCHAR(50)
);

create table EST_STOCKER (
    PRIMARY KEY(idProduit, idLieu),
    idProduit int NOT NULL,
    idLieu int NOT NULL,
    quantiteStocke int
);

create table LIEU_STOCKAGE (
    PRIMARY KEY (idLieu),
    idLieu int NOT NULL,
    nomLieu VARCHAR(50),
    quantiteTotale int,
    quantiteDispo int
);

create table UNITE (
    PRIMARY KEY (nomUnite),
    nomUnite VARCHAR(50)
);

create table FOURNISSEUR (
    PRIMARY KEY (idFou),
    idFou int NOT NULL,
    nomFou VARCHAR(50),
    adresseFou  VARCHAR(50),
    numTelFou int (10)
);

create table HISTORIQUE (
    PRIMARY KEY (idAction),
    idAction int NOT NULL,
    nomAction VARCHAR(50),
    dateAction date,
    qteFourni int,
    idFou int NOT NULL,
    idProduit int NOT NULL
);