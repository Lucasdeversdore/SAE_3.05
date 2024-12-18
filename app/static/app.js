// Fonction pour afficher le popup d'info produit
function handleButtonInfoClick(produit, lieu) {
    // Crée le fond du popup
    const popup_overlay_info = document.createElement("div");
    popup_overlay_info.id = "popup-overlay-info";
    popup_overlay_info.style.position = "fixed";
    popup_overlay_info.style.top = "0";
    popup_overlay_info.style.left = "0";
    popup_overlay_info.style.width = "100%";
    popup_overlay_info.style.height = "100%";
    popup_overlay_info.style.backgroundColor = "rgba(0, 0, 0, 0.7)";
    popup_overlay_info.style.display = "flex";
    popup_overlay_info.style.justifyContent = "center";
    popup_overlay_info.style.alignItems = "center";
    popup_overlay_info.style.zIndex = "1000"; 

    // Contenu du popup
    const popup_content = document.createElement("div");
    popup_content.style.backgroundColor = "#fff";
    popup_content.style.padding = "20px";
    popup_content.style.borderRadius = "5px";
    popup_content.style.width = "300px";
    popup_content.style.textAlign = "center";

    // Titre du popup
    const h3 = document.createElement("h3");
    h3.textContent = `Informations sur le produit: ${produit.nomProduit}`;

    // Informations du produit
    const pFonction = document.createElement("p");
    if (produit.fonctionProduit != null){
        
        pFonction.textContent = "Fonction: "+produit.fonctionProduit; 
    }
    else{
        pFonction.textContent = "Ce produit n'a pas de fonction assignée.";
    }
    const pLieuStockage = document.createElement("p");
    pLieuStockage.textContent = "Lieu de stockage: "+lieu.nomLieu; 

    // Bouton OK pour fermer le popup
    const bOk = document.createElement("button");
    bOk.textContent = "OK";
    bOk.id = "ok"; // Associez un ID pour le bouton
    bOk.addEventListener("click", handleButtonOKClick);

    // Assemble les éléments dans le popup
    popup_content.appendChild(h3);
    popup_content.appendChild(pFonction);
    popup_content.appendChild(pLieuStockage);
    popup_content.appendChild(bOk);
    popup_overlay_info.appendChild(popup_content);
    document.body.appendChild(popup_overlay_info); // Ajoute le popup au DOM
}

// Fonction pour masquer le popup
function handleButtonOKClick() {
    const popup = document.getElementById("popup-overlay-info");
    if (popup) {
        popup.remove(); 
    }
}

// Ajoute un gestionnaire d'événements aux boutons 'info_prod'
document.addEventListener('DOMContentLoaded', function() {
    const les_buttons = document.getElementsByClassName('info_prod');

    for (let button of les_buttons) {
        const produitId = button.getAttribute('data-produit');

        button.addEventListener('click', function() {
            // Effectuer la requête fetch au clic pour récupérer les données du produit
            fetch(`/get/produit/${produitId}`)
                .then(response => response.json())
                .then(data => {
                    handleButtonInfoClick(data.produit, data.lieu);
                })
                .catch(error => console.error('Erreur lors de la récupération des données du produit:', error));
        });
    }
});



// Fonction pour afficher le popup de modifications de produit

function handleButtonModifClick(produit, lieu, fournisseur, est_stocker, les_fournisseurs, les_fonctions, les_lieux) {
    const popup_overlay_modif = document.createElement("div");
    popup_overlay_modif.id = "popup-overlay-modif";
    popup_overlay_modif.classList.add("popup-overlay-modif");  // Ajoute une classe CSS

    const popup_content = document.createElement("div");
    popup_content.classList.add("popup-content");  // Ajoute une classe CSS

    const h3 = document.createElement("h3");
    h3.textContent = `Modification du produit: ${produit.nomProduit}`;

    const pNom = document.createElement("p");
    pNom.textContent = "Nom du produit : *";
    const textNom = document.createElement("input");
    textNom.type = "text";
    textNom.name = "textNom";
    textNom.value = produit.nomProduit;
    textNom.className = "form-control"

    const ligne_nom = document.createElement("div");
    ligne_nom.appendChild(pNom)
    ligne_nom.appendChild(textNom)

    const pFournisseur = document.createElement("p");
    pFournisseur.textContent = "Fournisseur :";
    const selectFournisseur = document.createElement("select");
    const optionFournisseur = document.createElement("option");
    selectFournisseur.name = "selectFournisseur";

    optionFournisseur.value = fournisseur.nomFou
    optionFournisseur.innerHTML = fournisseur.nomFou;
    selectFournisseur.appendChild(optionFournisseur);


    for (let i = 0; i < les_fournisseurs.length; i++) {
        let option = document.createElement("option");
        option.value = les_fournisseurs[i].nomFou;
        option.innerHTML = les_fournisseurs[i].nomFou;
        selectFournisseur.appendChild(option);
    }

    selectFournisseur.className = "form-control"

    const ligne_fournisseur = document.createElement("div");
    ligne_fournisseur.appendChild(pFournisseur)
    ligne_fournisseur.appendChild(selectFournisseur)

    const pQuantite = document.createElement("p");
    pQuantite.textContent = `Quantité actuelle (${est_stocker.quantiteStocke || 0} ${produit.nomUnite || null}) : *`;
    const textQuantite = document.createElement("input");
    textQuantite.type = "text";
    textQuantite.name = "textQuantite";
    textQuantite.value = est_stocker.quantiteStocke || 0;
    textQuantite.className = "form-control"

    const ligne_quantite = document.createElement("div");
    ligne_quantite.appendChild(pQuantite)
    ligne_quantite.appendChild(textQuantite)

    const pFonction = document.createElement("p");
    pFonction.textContent = "Fonction du produit :";
    const selectFonction = document.createElement("select");
    const optionFonction = document.createElement("option");
    selectFonction.name = "selectFonction";
    
    optionFonction.value = produit.fonctionProduit
    optionFonction.innerHTML = produit.fonctionProduit
    selectFonction.appendChild(optionFonction);

    const optionFonctionVide = document.createElement("option");
    optionFonctionVide.value = "vide"
    optionFonctionVide.innerHTML = " "
    selectFonction.appendChild(optionFonctionVide);

    for (let i = 0; i < les_fonctions.length; i++) {
        if (les_fonctions[i].fonctionProduit !== null && les_fonctions[i].fonctionProduit !== '-') {
            // Vérifie si l'option existe déjà dans le select
            let existeDeja = Array.from(selectFonction.options).some(option => option.value === les_fonctions[i].fonctionProduit);
            
            if (!existeDeja) {
                let option = document.createElement("option");
                option.value = les_fonctions[i].fonctionProduit;
                option.innerHTML = les_fonctions[i].fonctionProduit;
                selectFonction.appendChild(option);
            }
        }
    }

    selectFonction.className = "form-control"

    const ligne_fonction = document.createElement("div");
    ligne_fonction.appendChild(pFonction)
    ligne_fonction.appendChild(selectFonction)

    const pLieuStock = document.createElement("p");
    pLieuStock.textContent = "Lieu de stockage : *";

    const selectLieuStock = document.createElement("select");  
    const optionLieuStock = document.createElement("option");
    selectLieuStock.name = "selectLieuStock";

    optionLieuStock.value = lieu.nomLieu;
    optionLieuStock.innerHTML = lieu.nomLieu;
    selectLieuStock.appendChild(optionLieuStock);

    

    for (let i = 0; i < les_lieux.length; i++) {
        if (les_lieux[i].nomLieu !== null) {
            // Vérifie si l'option existe déjà dans le select
            let existeDeja = Array.from(selectFonction.options).some(option => option.value === les_lieux[i].nomLieu);
            
            if (!existeDeja) {
                let option = document.createElement("option");
                option.value = les_lieux[i].nomLieu;
                option.innerHTML = les_lieux[i].nomLieu;
                selectLieuStock.appendChild(option);
            }
        }
    }

    selectLieuStock.className = "form-control"

    const ligne_lieu_stock = document.createElement("div");
    ligne_lieu_stock.appendChild(pLieuStock)
    ligne_lieu_stock.appendChild(selectLieuStock)
    
    const bOk = document.createElement("button");
    bOk.textContent = "Annuler";
    bOk.id = "okModif";
    bOk.className = "btn btn-dark"
    bOk.addEventListener("click", handleButtonOKModifClick);


    const bSauv = document.createElement("button");
    bSauv.textContent = "Sauvegarder";
    bSauv.id = "sauvModif";
    bSauv.className = "btn btn-dark"
    bSauv.addEventListener("click", function () {
        if (!textNom.value || !textQuantite.value || !selectLieuStock.value) {
            alert("Veuillez remplir tous les champs requis.");
            return;
        }
        console.log(selectFournisseur.value);
        console.log(selectFonction.value);
        console.log(selectLieuStock.value);

        console
        sauvegarderProduit(produit.idProduit, textNom.value, selectFournisseur.value,
            textQuantite.value, selectFonction.value, selectLieuStock.value);
    });

    const ligne_bouton = document.createElement("div");
    ligne_bouton.appendChild(bOk)
    ligne_bouton.appendChild(bSauv)
    ligne_bouton.id = "bouton_modif"

    popup_content.appendChild(h3);
    popup_content.appendChild(ligne_nom)
    popup_content.appendChild(ligne_fournisseur)
    popup_content.appendChild(ligne_quantite)
    popup_content.appendChild(ligne_fonction)
    popup_content.appendChild(ligne_lieu_stock)
    popup_content.appendChild(ligne_bouton);
    popup_overlay_modif.appendChild(popup_content);
    document.body.appendChild(popup_overlay_modif);
}


function handleButtonOKModifClick() {
    const popup = document.getElementById("popup-overlay-modif");
    if (popup) {
        popup.remove();
    }
}

function sauvegarderProduit(idProduit, nom, nom_fournisseur, quantite, fonction, lieu) {
    fetch(`/sauvegarder/${idProduit}?textNom=${encodeURIComponent(nom)}&textFournisseur=${encodeURIComponent(nom_fournisseur)}&textQuantite=${encodeURIComponent(quantite)}&textFonction=${encodeURIComponent(fonction)}&textLieu=${encodeURIComponent(lieu)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                window.location.href = '/';
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Erreur:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    const les_buttons = document.getElementsByClassName('Modifier');
    for (let button of les_buttons) {
        const produitId = button.getAttribute('data-produit');
        button.addEventListener('click', function() {
            fetch(`/modifier/${produitId}`)
                .then(response => response.json())
                .then(data => {
                    handleButtonModifClick(data.produit, data.lieu, data.fournisseur, data.est_stocker, data.les_fournisseurs, data.les_fonctions, data.les_lieux);
                })
                .catch(error => console.error('Erreur lors de la récupération des données du produit:', error));
        });
    }
});

// Fonction pour afficher la popup de ajouter produit
function handleButtonAjoutProdfClick() {
    const popup_overlay_modif = document.createElement("div");
    popup_overlay_modif.id = "popup-overlay-Ajout";
    popup_overlay_modif.style.position = "fixed";
    popup_overlay_modif.style.top = "0";
    popup_overlay_modif.style.left = "0";
    popup_overlay_modif.style.width = "100%";
    popup_overlay_modif.style.height = "100%";
    popup_overlay_modif.style.backgroundColor = "rgba(0, 0, 0, 0.7)";
    popup_overlay_modif.style.display = "flex";
    popup_overlay_modif.style.justifyContent = "center";
    popup_overlay_modif.style.alignItems = "center";
    popup_overlay_modif.style.zIndex = "1000";

    const popup_content = document.createElement("div");
    popup_content.style.backgroundColor = "#fff";
    popup_content.style.padding = "20px";
    popup_content.style.borderRadius = "5px";
    popup_content.style.width = "300px";
    popup_content.style.textAlign = "center";

    const h3 = document.createElement("h3");
    h3.textContent = `Ajout d'un produit`;

    const pNom = document.createElement("p");
    pNom.textContent = "Nom du produit *";
    const textNom = document.createElement("input");
    textNom.type = "text";
    textNom.name = "textNewNom";

    const pFournisseur = document.createElement("p");
    pFournisseur.textContent = "Fournisseur";
    const selectFournisseur = document.createElement("input");
    selectFournisseur.type = "text";
    selectFournisseur.name = "textNewFournisseur";

    const pUnite = document.createElement("p");
    pUnite.textContent = "Unité *"
    const textUnite = document.createElement("input");
    textUnite.type = "text";
    textUnite.name = "textNewUnite";

    const pQuantite = document.createElement("p");
    pQuantite.textContent = "Quantiter disponible *"
    const textQuantite = document.createElement("input");
    textQuantite.type = "number";
    textQuantite.name = "textNewQuantite";
    

    const pFonction = document.createElement("p");
    pFonction.textContent = "Fonction du produit:";
    const textFonction = document.createElement("input");
    textFonction.type = "text";
    textFonction.name = "textNewFonction";
    

    const pLieuStock = document.createElement("p");
    pLieuStock.textContent = "Lieu de stockage *";
    const selectLieuStock = document.createElement("input");
    selectLieuStock.type = "text";
    selectLieuStock.name = "textNewLieu";

    const bAnnuler = document.createElement("button");
    bAnnuler.textContent = "Annuler";
    bAnnuler.id = "AnnulerAjout";
    bAnnuler.addEventListener("click", handleButtonAnnulerAjoutClick);

    const bSauv = document.createElement("button");
    bSauv.textContent = "Sauvegarder";
    bSauv.id = "sauvAjout";
    bSauv.addEventListener("click", function () {
        if (!textNom.value || !textQuantite.value || !selectLieuStock.value || !textUnite.value) {
            alert("Veuillez remplir tous les champs requis.");
            return;
        }
        sauvegarderAjoutProduit(textNom.value, 
            selectFournisseur.value, textUnite.value, textQuantite.value, 
            textFonction.value, selectLieuStock.value)
        
    });
    
    
    

    popup_content.appendChild(h3);
    popup_content.appendChild(pNom);
    popup_content.appendChild(textNom);
    popup_content.appendChild(pFournisseur);
    popup_content.appendChild(selectFournisseur);
    popup_content.appendChild(pUnite);
    popup_content.appendChild(textUnite);
    popup_content.appendChild(pQuantite);
    popup_content.appendChild(textQuantite);
    popup_content.appendChild(pFonction);
    popup_content.appendChild(textFonction);
    popup_content.appendChild(pLieuStock);
    popup_content.appendChild(selectLieuStock);
    popup_content.appendChild(bAnnuler);
    popup_content.appendChild(bSauv);
    popup_overlay_modif.appendChild(popup_content);
    document.body.appendChild(popup_overlay_modif);
}


function handleButtonAnnulerAjoutClick() {
    const popup = document.getElementById("popup-overlay-Ajout");
    if (popup) {
        popup.remove();
    }
}

function sauvegarderAjoutProduit(nom, nom_fournisseur, unite, quantite, fonction, lieu) {
    fetch('/ajout/sauvegarder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            textNom: nom,
            textFournisseur: nom_fournisseur,
            textUnite: unite,
            textQuantite: quantite,
            textFonction: fonction,
            textLieu: lieu
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);  // Message de succès
            window.location.href = '/';  // Redirection si ajout réussi
        } else {
            alert(data.message);  // Message d'erreur si ajout échoue
        }
    })
    .catch(error => console.error('Erreur:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    const le_button = document.getElementById('ajouter_prod');
    le_button.addEventListener('click', handleButtonAjoutProdfClick);
});





// Fonction pour afficher la popup de reservation
function handleButtonReservation(produit, stock, erreur) {
    // Crée le fond du popup
    const popup_overlay = document.createElement("div");
    popup_overlay.id = "popup-overlay-resrev";
    popup_overlay.style.position = "fixed";
    popup_overlay.style.top = "0";
    popup_overlay.style.left = "0";
    popup_overlay.style.width = "100%";
    popup_overlay.style.height = "100%";
    popup_overlay.style.backgroundColor = "rgba(0, 0, 0, 0.7)";
    popup_overlay.style.display = "flex";
    popup_overlay.style.justifyContent = "center";
    popup_overlay.style.alignItems = "center";
    popup_overlay.style.zIndex = "1000"; 

    // Contenu du popup
    const popup_content = document.createElement("div");
    popup_content.style.backgroundColor = "#fff";
    popup_content.style.padding = "20px";
    popup_content.style.borderRadius = "5px";
    popup_content.style.width = "300px";
    popup_content.style.textAlign = "center";

    // Titre du popup
    const h3 = document.createElement("h3");
    h3.textContent = `${produit.nomProduit}`;

    const perreur = document.createElement("p")
    perreur.textContent = erreur
    const pQte = document.createElement("p");
    pQte.textContent = "Quantite en stock : "+stock.quantiteStocke+produit.nomUnite
    
    const pQteReserv = document.createElement("p")
    pQteReserv.textContent = "Quantite réservée :"


    const inputQte = document.createElement("input")
    inputQte.id = "inputQte"
    inputQte.name = "inputQte"
    inputQte.type = "number"
    

    // Bouton Annuler pour fermer le popup
    const bAnnuler = document.createElement("button");
    bAnnuler.textContent = "Annuler";
    bAnnuler.id = "annuler"; 
    bAnnuler.addEventListener("click", handleButtonAnnulerClick);

    const bResrever = document.createElement("button");
    bResrever.textContent = "Réserver";
    bResrever.id = produit.idProduit; 
    bResrever.addEventListener("click", function () {
        const quantite = inputQte.value;
        reserverProduit(produit.idProduit, quantite);
    });
    
    

    // Assemble les éléments dans le popup
    popup_content.appendChild(h3);
    if (erreur){
        popup_content.appendChild(perreur)
    }
    popup_content.appendChild(pQte);
    popup_content.appendChild(pQteReserv);
    popup_content.appendChild(inputQte);
    popup_content.appendChild(bResrever);
    popup_content.appendChild(bAnnuler);
    popup_overlay.appendChild(popup_content);
    document.body.appendChild(popup_overlay); 
}

// Fonction pour masquer le popup
function handleButtonAnnulerClick() {
    const popup = document.getElementById("popup-overlay-resrev");
    if (popup) {
        popup.remove(); 
    }
}



// Ajoute un gestionnaire d'événements aux boutons 'info_prod'
document.addEventListener('DOMContentLoaded', function() {
    const les_buttons = document.getElementsByClassName('Reserver');

    for (let button of les_buttons) {
        const produitId = button.getAttribute('data-produit');

        button.addEventListener('click', function() {
            // Effectuer la requête fetch au clic pour récupérer les données du produit
            fetch(`/reserver/${produitId}`)
                .then(response => response.json())
                .then(data => {
                    handleButtonReservation(data.produit, data.stock);
                })
                .catch(error => console.error('Erreur lors de la récupération des données du produit:', error));
        });
    }
}); 

function reserverProduit(produitId, quantite) {
    fetch(`/reservation/${produitId}?inputQte=${quantite}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Redirigez ou mettez à jour l'interface si la réservation est réussie
                alert(data.message);  // Affiche la confirmation
                window.location.href = '/';  
            } else {
                // Affiche une alerte en cas d'erreur
                alert(data.message);
            }
        })
        .catch(error => console.error('Erreur:', error));
}

// Ajoute un gestionnaire d'événements aux boutons 'Etat'
document.addEventListener('DOMContentLoaded', function() {
    const les_buttons = document.getElementsByClassName('Etat');
    console.log(les_buttons.length);

    for (let button of les_buttons) {
        const idCommande = button.getAttribute('idCommande');
        const idChimiste = button.getAttribute('idChimiste');
        const etat = button.getAttribute('etat');

        if (etat != "termine"){
            button.addEventListener('click', function() {
                handleButtonEtatCommande(idCommande, idChimiste, etat);
            });
        }
    }
}); 

function handleButtonEtatCommande(idCommande, idChimiste, etat) {
    // Crée le fond du popup
    const popup_overlay = document.createElement("div");
    popup_overlay.id = "popup-overlay-resrev";
    popup_overlay.style.position = "fixed";
    popup_overlay.style.top = "0";
    popup_overlay.style.left = "0";
    popup_overlay.style.width = "100%";
    popup_overlay.style.height = "100%";
    popup_overlay.style.backgroundColor = "rgba(0, 0, 0, 0.7)";
    popup_overlay.style.display = "flex";
    popup_overlay.style.justifyContent = "center";
    popup_overlay.style.alignItems = "center";
    popup_overlay.style.zIndex = "1000"; 

    // Contenu du popup
    const popup_content = document.createElement("div");
    popup_content.style.backgroundColor = "#fff";
    popup_content.style.padding = "20px";
    popup_content.style.borderRadius = "5px";
    popup_content.style.width = "300px";
    popup_content.style.textAlign = "center";

    // Titre du popup
    const h3 = document.createElement("h3");
    if (etat == "non-commence"){
        h3.textContent = "Voulez vous occupez de cette commande ?";
    }
    else if (etat == "en-cours"){
        h3.textContent = "Voulez vous terminez cette commande ?";
    }
    else{
        h3.textContent = "Commande terminé";
    }

    // Bouton Annuler pour fermer le popup
    const bAnnuler = document.createElement("button");
    bAnnuler.textContent = "Non";
    bAnnuler.addEventListener("click", handleButtonAnnulerClick);

    const bResrever = document.createElement("button");
    bResrever.textContent = "Oui";
    bResrever.addEventListener("click", function() {
        window.location.href = `/etat/commande/${idCommande}/${idChimiste}`;
    });
    
    

    // Assemble les éléments dans le popup
    popup_content.appendChild(h3);
    popup_content.appendChild(bResrever);
    popup_content.appendChild(bAnnuler);
    popup_overlay.appendChild(popup_content);
    document.body.appendChild(popup_overlay); 
}

document.addEventListener('DOMContentLoaded', function() {
    const les_buttons = document.getElementsByClassName('delete_reservation');
    for (let button of les_buttons) {
        const idCommande = button.getAttribute('idCommande');
        const idChimiste = button.getAttribute('idChimiste');
        button.addEventListener('click', function() {
            handleButtonDeleteReservation(idCommande, idChimiste);
        });
    }
}); 

function handleButtonDeleteReservation(idCommande, idChimiste) {
    // Crée le fond du popup
    const popup_overlay = document.createElement("div");
    popup_overlay.id = "popup-overlay-resrev";
    popup_overlay.style.position = "fixed";
    popup_overlay.style.top = "0";
    popup_overlay.style.left = "0";
    popup_overlay.style.width = "100%";
    popup_overlay.style.height = "100%";
    popup_overlay.style.backgroundColor = "rgba(0, 0, 0, 0.7)";
    popup_overlay.style.display = "flex";
    popup_overlay.style.justifyContent = "center";
    popup_overlay.style.alignItems = "center";
    popup_overlay.style.zIndex = "1000"; 

    // Contenu du popup
    const popup_content = document.createElement("div");
    popup_content.style.backgroundColor = "#fff";
    popup_content.style.padding = "20px";
    popup_content.style.borderRadius = "5px";
    popup_content.style.width = "300px";
    popup_content.style.textAlign = "center";

    // Titre du popup
    const h3 = document.createElement("h3");
    h3.textContent = "Voulez vous supprimer cette commande ?";

    // Bouton Annuler pour fermer le popup
    const bAnnuler = document.createElement("button");
    bAnnuler.textContent = "Non";
    bAnnuler.addEventListener("click", handleButtonAnnulerClick);

    const bResrever = document.createElement("button");
    bResrever.textContent = "Oui";
    bResrever.addEventListener("click", function() {
        window.location.href = `/supprimer/reservation/${idCommande}/${idChimiste}`;
    });

    // Assemble les éléments dans le popup
    popup_content.appendChild(h3);
    popup_content.appendChild(bResrever);
    popup_content.appendChild(bAnnuler);
    popup_overlay.appendChild(popup_content);
    document.body.appendChild(popup_overlay); 
}
