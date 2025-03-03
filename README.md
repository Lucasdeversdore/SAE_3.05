# SAE_3.05 Sujet 9 - Chimie
## Présentation

[Manuel utilisateur étudiant](#manuel-utilisateur-étudiant) // 
[Manuel utilisateur préparateur](#manuel-utilisateur-préparateur)



Un étudiant doit pouvoir rechercher un produit et savoir s' il est disponible ou non.
Si il est disponible il doit pouvoir voir la quantité restante, le ou les lieux de stockage du produit et il doit pouvoir réserver une certaine quantité.
Si le produit n’est pas disponible, il faut afficher les produits de la même famille que le produit recherché.
L'étudiant doit pouvoir faire une recherche de famille de produit qui affiche tous les produits par famille.
La préparatrice doit pouvoir gérer les stocks, c'est-à-dire  ajouter/supprimer un produit et mettre à jour les stocks.
Quand un étudiant réserve un produit la quantité réservée est déduite de la base de donnée.
Faire une interface conviviale.



Vous retrouverez le projet sur ce dépôt distant

https://github.com/Lucasdeversdore/SAE_3.05

## Composition du Groupe

- #### Devers-Doré Lucas
-  Dantec Malo
-  Kerguen Tony
-  Mignan Baptiste
-  Gangneux Pierre


# Manuel utilisateur étudiant

#### Le manuel utilisateur de notre application web offre un guide complet pour naviguer et utiliser toutes les fonctionnalités disponibles. Il commence par l’inscription, la connexion, et la gestion des comptes, puis explique comment interagir avec la liste des produits, gérer les réservations. Chaque section est conçue pour vous permettre d’exploiter au mieux les capacités de l’application, assurant une expérience utilisateur fluide et intuitive.

### 1 - S'inscrire
La page d’inscription permet de créer un compte pour accéder à l’application.

#### Étapes pour s'inscrire : 
Accédez à la page d’inscription via le lien "Créer un compte".
Remplissez les champs suivants :

    Adresse email : Fournissez une adresse email universitaire valide.
    Nom : Entrez votre nom.
    Prénom : Entrez votre prénom.
    Mot de passe : Créez un mot de passe sécurisé (minimum 8 caractères, 1 majuscule, 1 caractère spécial).

Cochez la case pour accepter les Conditions Générales d'Utilisation (CGU). Un lien est disponible pour lire les CGU.
Cliquez sur le bouton S'inscrire.

Une fois l’inscription réussie, vous serez redirigé vers la page de connexion. Vous devrez activer votre compte avec un lien envoyé par mail avant de passer à l'étape suivante.

### 2 - Se connecter

La page de connexion permet d'accéder à votre compte utilisateur.

#### Étapes pour se connecter :

    Accédez à la page de connexion via le lien "Se connecter".
    Remplissez les champs suivants :
        Adresse email : Entrez l’email utilisé lors de l’inscription.
        Mot de passe : Saisissez le mot de passe associé à votre compte.
    Facultatif :
        Rester connecté : Cochez cette case si vous souhaitez rester connecté, même après la fermeture de votre navigateur.
        Si vous n’avez pas encore de compte, cliquez sur "Créer un compte" pour accéder à la page d'inscription.
    Cliquez sur le bouton Se connecter.

#### En cas de mot de passe oublié :

    Cliquez sur le lien "Mot de passe oublié".
    Suivez les étapes pour recevoir un email de réinitialisation.

### 3 - Liste des produits

La page de liste des produits permet de consulter et d’interagir avec les produits disponibles ou indisponibles dans l’application. Elle offre également des options de navigation vers d’autres pages, telles que la page de réservations et la page de connexion via la déconnexion.

Fonctionnalités Principales :

#### 3.1. Affichage de la Liste des Produits

    Tous les produits, qu’ils soient disponibles ou non, sont affichés dans une liste.
    Utilisez la barre de recherche pour :
        Rechercher un produit par son nom.
        Filtrer les produits par famille.
    Cliquez sur les boutons "Précédent" et "Suivant" pour parcourir les pages et afficher davantage de produits.

#### 3.2. Interagir avec un Produit

Chaque produit de la liste propose trois actions principales :

    Réserver
        Si le produit est disponible :
            Cliquez sur le bouton "Réserver".
            Une pop-up s’ouvre avec :
                La quantité disponible.
                Un champ pour entrer la quantité à réserver.
                Boutons "Réserver" pour confirmer ou "Annuler" pour annuler la réservation.
            Une fois confirmé :
                Le produit est ajouté à votre liste de réservations.
                Le stock est mis à jour en décrémentant la quantité réservée.
        Si le produit est indisponible :
            Le bouton "Réserver" n’apparaît pas.

    Information Produit
        Cliquez sur le bouton "Information Produit".
        Une pop-up affiche les détails suivants :
            Le nom du produit.
            Sa fonction.
            Son lieu de réserve.
        Cliquez sur "Ok" pour fermer la pop-up.

    Produits de la Même Famille
        Cliquez sur ce bouton pour afficher une nouvelle liste contenant les produits appartenant à la même famille.


### 4 - Liste des réservations

La page de liste des réservations permet de consulter et de gérer les produits réservés. Elle offre également des options de navigation vers la liste des produits et la page de connexion via la déconnexion.

#### 4.1. Affichage de la Liste des Réservations

La liste des réservations présente les détails des produits réservés, triés par date de réservation (du plus récent au moins récent). Chaque réservation affiche :

    Nom du produit : Identifie le produit réservé.
    Quantité réservée : La quantité réservée par l’utilisateur.
    Prénom et Nom : Le prénom et le nom de la personne ayant effectué la réservation.
    Date de réservation : La date à laquelle la réservation a été effectuée.
    État de la réservation :
        Non commencé.
        En cours.
        Terminé.

#### 4.2. Supprimer une Réservation

    Si l’état de la réservation est Non commencé :
        Cliquez sur le bouton Supprimer à côté de la réservation.
        La réservation sera immédiatement supprimée de la liste.

### 4.3. Modifier la quantité d'une réservation
    Appuyez sur la touche "modifier réservation", une pop-up s'ouvre et la quantité que vous avez 
    réservé est affiché dans le champ "Quantite réservée". Pour modifier cette quantité changez 
    la valeur de ce champ et appuyez sur "Modifier".

### 4.4. Recherche et Navigation

    Barre de recherche :
        Filtrez la liste en recherchant un produit par son nom.
    Boutons Précédent/Suivant :
        Utilisez ces boutons pour naviguer entre les pages et afficher plus de réservations.


# Manuel utilisateur préparateur

### 1 - S'inscrire

Le préparateur doit soumettre une demande à un administrateur pour s’inscrire. Il utilise ensuite le même système de connexion que les étudiants. Une fois son compte créé et approuvé, il peut accéder à toutes les fonctionnalités associées à son rôle.

### 2 - Se connecter

La page de connexion permet d'accéder à votre compte utilisateur.

Étapes pour se connecter :

    Accédez à la page de connexion via le lien "Se connecter".
    Remplissez les champs suivants :
        Adresse email : Entrez l’email utilisé lors de l’inscription.
        Mot de passe : Saisissez le mot de passe associé à votre compte.
    Facultatif :
        Rester connecté : Cochez cette case si vous souhaitez rester connecté, même après la fermeture de votre navigateur.
        Si vous n’avez pas encore de compte, cliquez sur "Créer un compte" pour accéder à la page d'inscription.
    Cliquez sur le bouton Se connecter.

En cas de mot de passe oublié :

    Cliquez sur le lien "Mot de passe oublié".
    Suivez les étapes pour recevoir un email de réinitialisation.

### 3 - Gérer les stocks

La page de gestion des stocks permet de naviguer entre plusieurs sections telles que "Gérer les réservations" et la page de connexion via la déconnexion.

#### 3.1. Ajouter un Produit

    Fonctionnalités Principales :
        Cliquez sur "Ajouter un produit" pour ouvrir une pop-up.
        Champs Obligatoires :
            Nom du produit.
            Unité.
            Quantité disponible.
            Lieu de stockage.
        Champs Non Obligatoires :
            Fournisseur.
            Fonction du produit.
        Actions :
            "Sauvegarder" pour ajouter le produit.
            "Annuler" pour annuler l’action.
        Alternative :
            Ajouter un fichier CSV en appuyant sur le bouton "Ajouter un csv"
            Ce fichier devra respecter cette organisation :
            Produits,Fournisseur,Quantité,Fonction,Lieu de stockage,Seuil

#### 3.2. Ajouter un Fournisseur

    Fonctionnalités Principales :
        Cliquez sur "Ajouter un fournisseur" pour ouvrir une pop-up.
        Champs Obligatoires :
            Nom du fournisseur.
        Champs Non Obligatoires :
            Adresse.
            Numéro de téléphone.
        Actions :
            "Sauvegarder" pour ajouter le fournisseur.
            "Annuler" pour annuler l’action.

#### 3.3. Ajouter un Lieu

    Fonctionnalités Principales :
        Cliquez sur "Ajouter un lieu" pour ouvrir une pop-up.
        Champs Obligatoires :
            Nom du lieu.
        Actions :
            "Sauvegarder" pour ajouter le lieu.
            "Annuler" pour annuler l’action.

#### 3.4 À commander

    Fonctionnalités principales :
        Cliquez sur "À commander" pour télécharger un fichier contenant la liste des produits ayant une quantité inférieure au seuil d'alerte.

#### 3.5. Gestion des Produits

    Barre de Recherche :
        Utilisez la barre de recherche pour trier la liste des produits par famille ou par nom de produit.

    Actions pour chaque produit :
        Information Produit
            Cliquez sur le bouton "Information Produit".
            Une pop-up affiche les détails suivants :
                Le nom du produit.
                Sa fonction.
                Son lieu de réserve.
            Cliquez sur "Ok" pour fermer la pop-up.
        Modifier Produit :
            Ouvrez la pop-up pour modifier les informations du produit.
            Champs Modifiables :
                Fournisseur et lieu de stockage (avec listes déroulantes).
            Actions :
                "Sauvegarder" pour sauvegarder les modifications.
                "Annuler" pour annuler les modifications.
        Produits de la Même Famille : 
            Affiche une liste des produits appartenant à la même famille.
        Suppression :
            Cacher le produit pour les étudiants, mais il reste visible pour le préparateur.

    Navigation :
        "Précédent" et "Suivant" pour afficher davantage de produits.

### 4 - Gérer les réservations
La page de gestion des réservations permet de consulter et de gérer les produits réservés par les étudiants. Elle offre également des options de navigation vers la liste des produits et la page de connexion via la déconnexion.

#### 4.1. Affichage de la Liste des Réservations

La liste des réservations présente les détails des produits réservés, triés par date de réservation (du plus récent au moins récent). Chaque réservation affiche :

    Nom du produit : Identifie le produit réservé.
    Quantité réservée : La quantité réservée par l’utilisateur.
    Prénom et Nom : Le prénom et le nom de la personne ayant effectué la réservation.
    Date de réservation : La date à laquelle la réservation a été effectuée.
    État de la réservation :
        Non commencé.
        En cours.
        Terminé.

#### 4.2. Supprimer une Réservation

    Si l’état de la réservation est Non commencé :
        Cliquez sur le bouton Supprimer à côté de la réservation.
        La réservation sera immédiatement supprimée de la liste.

#### 4.3. Changer l'état d'une Réservation

    Cliquez sur l'état actuel d'une réservation afin de le modifier dans l'ordre suivant : non commencé, en cours, terminé.

#### 4.4. Recherche et Navigation

    Barre de recherche :
        Filtrez la liste en recherchant un produit par son nom.
    Boutons Précédent/Suivant :
        Utilisez ces boutons pour naviguer entre les pages et afficher plus de réservations.







## Liens des documentations

- [Google Doc](https://docs.google.com/document/d/1Tj_LncErI6cz8Z9aLuyxrCyK7A-Zf0-V-t2XJHSf2D4/edit?tab=t.0)
- [Maquettes](https://www.figma.com/design/3zRVa4q9qhufaVrlDgFbux/Untitled?node-id=0-315&node-type=frame&t=TaOi67KtuTTnPceL-0)

