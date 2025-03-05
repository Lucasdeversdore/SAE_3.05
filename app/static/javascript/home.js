// Popup info
function handleButtonInfoClick(produit, lieu) {
    // Crée le fond du popup
    let popup_overlay_info = document.getElementById("popup-overlay-info")
    if (!popup_overlay_info){
        popup_overlay_info = document.createElement("div");
        popup_overlay_info.id = "popup-overlay-info";
    }
    clearContent(popup_overlay_info);

    // Contenu du popup
    const popup_content = document.createElement("div");
    popup_content.classList.add("popup-content");

    // Titre du popup
    const h3 = document.createElement("h3");
    h3.textContent = `Informations sur le produit: ${produit.nomProduit}`;
    popup_content.appendChild(h3);

    // Informations du produit
    const pFonction = document.createElement("p");
    if (produit.fonctionProduit != null){
        
        pFonction.textContent = "Fonction: "+produit.fonctionProduit; 
    }
    else{
        pFonction.textContent = "Ce produit n'a pas de fonction assignée.";
    }
    popup_content.appendChild(pFonction);

    const pLieuStockage = document.createElement("p");
    pLieuStockage.textContent = "Lieu de stockage: "+lieu.nomLieu; 
    popup_content.appendChild(pLieuStockage);
    // Bouton OK pour fermer le popup

    const bOk = document.createElement("button");
    const spanOk = document.createElement("span");
    spanOk.textContent = "OK";
    bOk.id = "ok"; // Associez un ID pour le bouton
    bOk.className = "cssbuttons-io"
    bOk.addEventListener("click", handleButtonOKClick);
    bOk.appendChild(spanOk)

    const ligne_bouton = document.createElement("div");
    ligne_bouton.appendChild(bOk)
    ligne_bouton.id = "bouton_modif"

    popup_content.appendChild(ligne_bouton);

    
    popup_overlay_info.appendChild(popup_content);
    document.body.appendChild(popup_overlay_info); // Ajoute le popup au DOM
}

function handleButtonOKClick() {
    const popup = document.getElementById("popup-overlay-info");
    if (popup) {
        popup.remove(); 
    }
}

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


// Popup modifier produit
function handleButtonModifClick(produit, lieu, fournisseur, est_stocker, les_fournisseurs, les_fonctions, les_lieux) {
    let popup_overlay_modif = document.getElementById("popup-overlay-modif")
    if (!popup_overlay_modif){
        popup_overlay_modif = document.createElement("div");
        popup_overlay_modif.id = "popup-overlay-modif";
        popup_overlay_modif.classList.add("popup-overlay-modif");
    }
    clearContent(popup_overlay_modif);

    const popup_content = document.createElement("div");
    popup_content.classList.add("popup-content");

    const h3 = document.createElement("h3");
    h3.textContent = `Modification du produit: ${produit.nomProduit}`;

    popup_content.appendChild(h3);

    // ligne Nom du produit
    const pNom = document.createElement("p");
    pNom.textContent = "Nom du produit:";

    const inputNom = document.createElement("input");
    inputNom.type = "text";
    inputNom.name = "inputNom";
    inputNom.placeholder = "Nom du produit";
    inputNom.value = produit.nomProduit;

    const ligne_nom = document.createElement("div");
    ligne_nom.className = "inputGroup";
    ligne_nom.appendChild(pNom);
    ligne_nom.appendChild(inputNom);

    popup_content.appendChild(ligne_nom);

    // ligne Fournisseur
    const pFournisseur = document.createElement("p");
    pFournisseur.textContent = "Fournisseur :";

    const selectFournisseur = document.createElement("select");
    selectFournisseur.name = "selectFournisseur";
    selectFournisseur.className = "form-control"

    const optionFournisseur = document.createElement("option");
    optionFournisseur.value = fournisseur.nomFou
    optionFournisseur.innerHTML = fournisseur.nomFou;
    selectFournisseur.appendChild(optionFournisseur);
    for (let i = 0; i < les_fournisseurs.length; i++) {
        let option = document.createElement("option");
        option.value = les_fournisseurs[i].nomFou;
        option.innerHTML = les_fournisseurs[i].nomFou;
        selectFournisseur.appendChild(option);
    }

    const ligne_fournisseur = document.createElement("div");
    ligne_fournisseur.className = "selectGroup";
    ligne_fournisseur.appendChild(pFournisseur)
    ligne_fournisseur.appendChild(selectFournisseur)

    popup_content.appendChild(ligne_fournisseur);

    // ligne Quantité
    const pQuantite = document.createElement("p");
    pQuantite.textContent = `Quantité actuelle : ${est_stocker.quantiteStocke || 0} ${produit.nomUnite || ""} *`;
    pQuantite.className = "obligatoire";

    const textQuantite = document.createElement("input");
    textQuantite.type = "text";
    textQuantite.name = "textQuantite";
    textQuantite.placeholder = "Quantite";
    textQuantite.value = est_stocker.quantiteStocke || 0;

    const ligne_quantite = document.createElement("div");
    ligne_quantite.className = "inputGroup";
    ligne_quantite.appendChild(createDivObligatoire(pQuantite))
    ligne_quantite.appendChild(textQuantite)

    popup_content.appendChild(ligne_quantite);

    // Ligne seuil
    const pSeuil = document.createElement("p");
    pSeuil.textContent = `Seuil d'alerte actuel : ${produit.seuilProduit || 0} ${produit.nomUnite || ""} *`;
    pSeuil.className = "obligatoire";

    const textSeuil = document.createElement("input");
    textSeuil.type = "number";
    textSeuil.name = "textSeuil";
    textSeuil.placeholder = "Seuil d'alerte";
    textSeuil.value = produit.seuilProduit || 0;

    const ligne_seuil = document.createElement("div");
    ligne_seuil.className = "inputGroup";
    ligne_seuil.appendChild(createDivObligatoire(pSeuil))
    ligne_seuil.appendChild(textSeuil)

    popup_content.appendChild(ligne_seuil);

    // ligne Fonction du produit
    const pFonction = document.createElement("p");
    pFonction.textContent = "Fonction du produit :";

    const optionFonction = document.createElement("option");
    optionFonction.value = produit.fonctionProduit
    optionFonction.innerHTML = produit.fonctionProduit
    
    const optionFonctionVide = document.createElement("option");
    optionFonctionVide.value = "vide"
    optionFonctionVide.innerHTML = " "
    
    const selectFonction = document.createElement("select");
    selectFonction.name = "selectFonction";
    selectFonction.className = "form-control"
    selectFonction.appendChild(optionFonction);
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

    const ligne_fonction = document.createElement("div");
    ligne_fonction.className = "selectGroup";
    ligne_fonction.appendChild(pFonction)
    ligne_fonction.appendChild(selectFonction)

    popup_content.appendChild(ligne_fonction);

    // ligne Lieu de stockage
    const pLieuStock = document.createElement("p");
    pLieuStock.textContent = "Lieu de stockage : *";
    pLieuStock.className = "obligatoire";
    
    const selectLieuStock = document.createElement("select");  
    selectLieuStock.name = "selectLieuStock";
    selectLieuStock.className = "form-control";

    const optionLieuStock = document.createElement("option");
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

    const ligne_lieu_stock = document.createElement("div");
    ligne_lieu_stock.className = "selectGroup";
    ligne_lieu_stock.appendChild(createDivObligatoire(pLieuStock))
    ligne_lieu_stock.appendChild(selectLieuStock)

    popup_content.appendChild(ligne_lieu_stock)

    // boutton Annuler
    const bAnnuler = document.createElement("button");
    const spanOk = document.createElement("span");
    spanOk.textContent = "Annuler";
    bAnnuler.id = "okModif";
    bAnnuler.className = "cssbuttons-io"
    bAnnuler.onclick = () => handleButtonAnnulerClick(popup_overlay_modif)
    bAnnuler.appendChild(spanOk)

    // boutton Sauvegarder
    const bSauv = document.createElement("button");
    const spanSauv = document.createElement("span");
    spanSauv.textContent = "Sauvegarder";
    bSauv.id = "sauvModif";
    bSauv.className = "cssbuttons-io"
    bSauv.addEventListener("click", function () {
        if (!inputNom.value || !textQuantite.value || !selectLieuStock.value) {
            alert("Veuillez remplir tous les champs requis.");
            return;
        }
        console.log(selectFournisseur.value);
        console.log(selectFonction.value);
        console.log(selectLieuStock.value);

        console
        sauvegarderProduit(produit.idProduit, inputNom.value, selectFournisseur.value,
            textSeuil.value, textQuantite.value, selectFonction.value, selectLieuStock.value);
    });
    bSauv.appendChild(spanSauv)

    // ligne de bouton
    const ligne_bouton = document.createElement("div");
    ligne_bouton.appendChild(bSauv)
    ligne_bouton.appendChild(bAnnuler)
    ligne_bouton.id = "bouton_modif"

    popup_content.appendChild(ligne_bouton);

    popup_overlay_modif.appendChild(popup_content);
    document.body.appendChild(popup_overlay_modif);
}

function sauvegarderProduit(idProduit, nom, nom_fournisseur, seuil, quantite, fonction, lieu) {
    fetch(`/sauvegarder/${idProduit}?inputNom=${encodeURIComponent(nom)}&textFournisseur=${encodeURIComponent(nom_fournisseur)}&textQuantite=${encodeURIComponent(quantite)}&textSeuil=${encodeURIComponent(seuil)}&textFonction=${encodeURIComponent(fonction)}&textLieu=${encodeURIComponent(lieu)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // alert(data.message);
                window.location.reload();
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
                    handleButtonModifClick(data.produit, data.lieu, data.fournisseur, data.est_stocker, data.les_fournisseurs, data.les_fonctions, data.les_lieux, data.seuil);
                })
                .catch(error => console.error('Erreur lors de la récupération des données du produit:', error));
        });
    }
});


// Popup réserver
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

function handleButtonReservation(produit, stock, erreur) {
    // Crée le fond du popup
    let popup_overlay = document.getElementById("popup-overlay-resrev")
    if (!popup_overlay){
        popup_overlay = document.createElement("div");
        popup_overlay.id = "popup-overlay-resrev";
    }
    clearContent(popup_overlay);

    // Contenu du popup
    const popup_content = document.createElement("div");
    popup_content.classList.add("popup-content");

    // Titre du popup
    const h3 = document.createElement("h3");
    h3.textContent = `${produit.nomProduit}`;

    popup_content.appendChild(h3);

    // quantité en stock
    const perreur = document.createElement("p")
    perreur.textContent = erreur

    const pQte = document.createElement("p");
    pQte.textContent = "Quantité en stock : "+stock.quantiteStocke+produit.nomUnite
    
    const ligne_quantite = document.createElement("div");
    if (erreur){
        popup_content.appendChild(createDivObligatoire(perreur))
    }
    ligne_quantite.appendChild(pQte)

    popup_content.appendChild(ligne_quantite);

    // quantité reservé
    const pQteReserv = document.createElement("p")
    pQteReserv.textContent = "Quantite réservée : *"
    pQteReserv.className = "obligatoire";

    const inputQte = document.createElement("input")
    inputQte.id = "inputQte"
    inputQte.name = "inputQte"
    inputQte.type = "number"
    
    const ligne_quantite_reserve = document.createElement("div");
    ligne_quantite_reserve.className = "inputGroup";
    ligne_quantite_reserve.appendChild(createDivObligatoire(pQteReserv))
    ligne_quantite_reserve.appendChild(inputQte)

    popup_content.appendChild(ligne_quantite_reserve);


    // Bouton Annuler
    const bAnnuler = document.createElement("button");
    const spanAnnuler = document.createElement("span");
    spanAnnuler.textContent = "Annuler";
    bAnnuler.appendChild(spanAnnuler);
    bAnnuler.id = "annuler"; 
    bAnnuler.className = "cssbuttons-io";
    bAnnuler.onclick = () => handleButtonAnnulerClick(popup_overlay);


    // Bouton Reserver
    const bResrever = document.createElement("button");
    const spanReserver = document.createElement("span");
    spanReserver.textContent = "Reserver";
    bResrever.appendChild(spanReserver);
    bResrever.id = produit.idProduit; 
    bResrever.className = "cssbuttons-io";
    bResrever.addEventListener("click", function () {
        const quantite = inputQte.value;
        reserverProduit(produit.idProduit, quantite);
    });
    
    // ligne de bouton
    const ligne_bouton = document.createElement("div");
    ligne_bouton.appendChild(bResrever)
    ligne_bouton.appendChild(bAnnuler)
    ligne_bouton.id = "bouton_modif"

    popup_content.appendChild(ligne_bouton);

    popup_overlay.appendChild(popup_content);
    document.body.appendChild(popup_overlay); 
}

function reserverProduit(produitId, quantite) {
    fetch(`/reservation/${produitId}?inputQte=${quantite}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Redirigez ou mettez à jour l'interface si la réservation est réussie
                // alert(data.message);  // Affiche la confirmation
                window.location.reload();
            } else {
                // Affiche une alerte en cas d'erreur
                alert(data.message);
            }
        })
        .catch(error => console.error('Erreur:', error));
}


// Ppopup ajouter produit
function handleButtonAjoutProdClick(les_fournisseurs, les_lieux) {
    let popup_overlay_ajout = document.getElementById("popup-overlay-ajout")
    if (!popup_overlay_ajout){
        popup_overlay_ajout = document.createElement("div");
        popup_overlay_ajout.id = "popup-overlay-ajout";
    }
    clearContent(popup_overlay_ajout);

    const popup_content = document.createElement("div");
    popup_content.classList.add("popup-content");

    const h3 = document.createElement("h3");
    h3.textContent = `Ajout d'un produit`;

    popup_content.appendChild(h3);

    // ligne Nom du produit
    const pNom = document.createElement("p");
    pNom.textContent = "Nom du produit *";
    pNom.className = "obligatoire";

    const textNom = document.createElement("input");
    textNom.type = "text";
    textNom.name = "textNewNom";
    textNom.placeholder = "Nom du produit";

    const ligne_nom = document.createElement("div");
    ligne_nom.className = "inputGroup";
    ligne_nom.appendChild(createDivObligatoire(pNom))
    ligne_nom.appendChild(textNom)

    popup_content.appendChild(ligne_nom);

    // ligne Fournisseur

    const pFournisseur = document.createElement("p");
    pFournisseur.textContent = "Fournisseur :";

    const selectFournisseur = document.createElement("select");
    selectFournisseur.name = "textNewFournisseur";
    selectFournisseur.className = "form-control";

    const optionFournisseur = document.createElement("option");
    optionFournisseur.value = ""
    optionFournisseur.innerHTML = "";
    selectFournisseur.appendChild(optionFournisseur);
    for (let i = 0; i < les_fournisseurs.length; i++) {
        let option = document.createElement("option");
        option.value = les_fournisseurs[i].nomFou;
        option.innerHTML = les_fournisseurs[i].nomFou;
        selectFournisseur.appendChild(option);
    }

    const ligne_fournisseur = document.createElement("div");
    ligne_fournisseur.className = "selectGroup";
    ligne_fournisseur.appendChild(pFournisseur)
    ligne_fournisseur.appendChild(selectFournisseur)

    popup_content.appendChild(ligne_fournisseur);

    // ligne Unité
    const pUnite = document.createElement("p");
    pUnite.textContent = "Unité *"
    pUnite.className = "obligatoire";

    const textUnite = document.createElement("input");
    textUnite.type = "text";
    textUnite.name = "textNewUnite";
    textUnite.placeholder = "Unité";

    const ligne_unite = document.createElement("div");
    ligne_unite.className = "inputGroup";
    ligne_unite.appendChild(createDivObligatoire(pUnite))
    ligne_unite.appendChild(textUnite)

    popup_content.appendChild(ligne_unite);

    // ligne Quantité
    const pQuantite = document.createElement("p");
    pQuantite.textContent = "Quantité disponible *"
    pQuantite.className = "obligatoire";

    const textQuantite = document.createElement("input");
    textQuantite.type = "number";
    textQuantite.name = "textNewQuantite";
    textQuantite.placeholder = "Quantité";

    const ligne_quantite = document.createElement("div");
    ligne_quantite.className = "inputGroup";
    ligne_quantite.appendChild(createDivObligatoire(pQuantite))
    ligne_quantite.appendChild(textQuantite)

    popup_content.appendChild(ligne_quantite);

    // ligne Seuil

    const pSeuil = document.createElement("p");
    pSeuil.textContent = "Seuil d'alerte *"
    pSeuil.className = "obligatoire";

    const textSeuil = document.createElement("input");
    textSeuil.type = "number";
    textSeuil.name = "textNewSeuil";
    textSeuil.placeholder = "Seuil d'alerte";

    const ligne_seuil = document.createElement("div");
    ligne_seuil.className = "inputGroup";
    ligne_seuil.appendChild(createDivObligatoire(pSeuil))
    ligne_seuil.appendChild(textSeuil)

    popup_content.appendChild(ligne_seuil);
    
    // ligne Fonction du produit
    const pFonction = document.createElement("p");
    pFonction.textContent = "Fonction du produit:";

    const textFonction = document.createElement("input");
    textFonction.type = "text";
    textFonction.name = "textNewFonction";
    textFonction.placeholder = "Fonction du produit";

    const ligne_fonction = document.createElement("div");
    ligne_fonction.className = "inputGroup";
    ligne_fonction.appendChild(pFonction)
    ligne_fonction.appendChild(textFonction)

    popup_content.appendChild(ligne_fonction);
    
    // ligne Lieu de stockage
    const pLieuStock = document.createElement("p");
    pLieuStock.textContent = "Lieu de stockage : *";
    pLieuStock.className = "obligatoire";
    
    const selectLieuStock = document.createElement("select");  
    selectLieuStock.name = "textNewLieu";
    selectLieuStock.className = "form-control";

    const optionLieuStock = document.createElement("option");
    optionLieuStock.value = "";
    optionLieuStock.innerHTML = "";
    selectLieuStock.appendChild(optionLieuStock);
    for (let i = 0; i < les_lieux.length; i++) {
        if (les_lieux[i].nomLieu !== null) {
            // Vérifie si l'option existe déjà dans le select
            let existeDeja = Array.from(selectFournisseur.options).some(option => option.value === les_lieux[i].nomLieu);
            
            if (!existeDeja) {
                let option = document.createElement("option");
                option.value = les_lieux[i].nomLieu;
                option.innerHTML = les_lieux[i].nomLieu;
                selectLieuStock.appendChild(option);
            }
        }
    }

    const ligne_lieu_stock = document.createElement("div");
    ligne_lieu_stock.className = "selectGroup";
    ligne_lieu_stock.appendChild(createDivObligatoire(pLieuStock))
    ligne_lieu_stock.appendChild(selectLieuStock)

    popup_content.appendChild(ligne_lieu_stock)


    // ligne csv
    const divBCsv = document.createElement("div");
    divBCsv.id = "div_csv";
    
    // Créer l'élément image
    const imgCsv = document.createElement("img");
    imgCsv.src = "/static/images/ajouter_prod.png";
    imgCsv.alt = "i";
    
    // Créer le bouton
    const bCsv = document.createElement("button");
    bCsv.className = "bouton-ajouter";
    bCsv.id = "ajouter_csv";
    
    // Ajouter l'image et le texte dans le bouton
    bCsv.appendChild(imgCsv);
    bCsv.appendChild(document.createTextNode(" Ajouter un csv"));
    
    // Ajouter un événement au bouton
    bCsv.onclick = function () {
        document.getElementById('fileInput').click();
    };
    
    
    const divTCsv = document.createElement("div");
    const textCsv1 = document.createElement("p");
    textCsv1.textContent = "Première ligne du fichier csv :"
    divTCsv.appendChild(textCsv1)
    const textCsv2 = document.createElement("p");
    textCsv2.textContent = "Produits,Fournisseur,Quantité,Fonction,Lieu de stockage,Seuil"
    divTCsv.appendChild(textCsv2)

    divBCsv.appendChild(divTCsv)
    divBCsv.appendChild(bCsv)
    popup_content.appendChild(divBCsv)
    


    // boutton Annuler
    const bAnnuler = document.createElement("button");
    const spanOk = document.createElement("span");
    spanOk.textContent = "Annuler";
    bAnnuler.id = "AnnulerAjout";
    bAnnuler.className = "cssbuttons-io"
    bAnnuler.onclick = () => handleButtonAnnulerClick(popup_overlay_ajout);
    bAnnuler.appendChild(spanOk)

    // boutton Sauvegarder
    const bSauv = document.createElement("button");
    const spanSauv = document.createElement("span");
    spanSauv.textContent = "Sauvegarder";
    bSauv.id = "sauvAjout";
    bSauv.className = "cssbuttons-io"
    bSauv.addEventListener("click", function () {
        if (!textNom.value || !textQuantite.value || !selectLieuStock.value || !textUnite.value || !textSeuil.value) {
            alert("Veuillez remplir tous les champs requis.");
            return;
        }
        sauvegarderAjoutProduit(textNom.value, 
            selectFournisseur.value, textUnite.value, textQuantite.value, textSeuil.value,
            textFonction.value, selectLieuStock.value)
        
    });
    bSauv.appendChild(spanSauv)

    // ligne de bouton
    const ligne_bouton = document.createElement("div");
    ligne_bouton.appendChild(bSauv)
    ligne_bouton.appendChild(bAnnuler)
    ligne_bouton.id = "bouton_modif"

    popup_content.appendChild(ligne_bouton);

    popup_overlay_ajout.appendChild(popup_content);
    document.body.appendChild(popup_overlay_ajout);
}

document.addEventListener('DOMContentLoaded', function() {
    const button = document.querySelector('.ajouter');
    button.addEventListener('click', function() {
        fetch(`/ajouter`)
            .then(response => response.json())
            .then(data => {
                    handleButtonAjoutProdClick(data.les_fournisseurs, data.les_lieux);
            })
            .catch(error => console.error('Erreur lors de la récupération des données du produit:', error));
    });
});

function sauvegarderAjoutProduit(nom, nom_fournisseur, unite, quantite, seuil, fonction, lieu) {
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
            textSeuil: seuil,
            textFonction: fonction,
            textLieu: lieu
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // alert(data.message);  // Message de succès
            window.location.reload();
        } else {
            alert(data.message);  // Message d'erreur si ajout échoue
        }
    })
    .catch(error => console.error('Erreur:', error));
}

// Ajout csv
document.getElementById('fileInput').onchange = ajoutCSV;

function ajoutCSV(event) {  // 'event' doit être en minuscule
    let file = event.target.files[0]; // 'event' contient l'objet d'événement

    if (file) {
        let fileName = file.name; // Nom du fichier
        let fileType = file.type; // Récupère le type du fichier
        if (fileName.endsWith(".csv") || fileType === "text/csv") {
            let chemin = `./${fileName}`;

            // Envoi du fichier via fetch
            let formData = new FormData();
            formData.append("file", file);

            fetch("/ajout_csv", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => alert(data.message))
            .catch(error => alert("Erreur lors de l'envoi, renvoyer le fichier"));
        }
        else{
            alert("Veulliez choisir un fichier csv")
        }
    }
}



// Ppopup ajouter lieu
function handleButtonAjoutLieuClick() {
    let popup_overlay_ajouter_lieu = document.getElementById("popup-overlay-lieu")
    if (!popup_overlay_ajouter_lieu){
        popup_overlay_ajouter_lieu = document.createElement("div");
        popup_overlay_ajouter_lieu.id = "popup-overlay-lieu";
    }
    clearContent(popup_overlay_ajouter_lieu);

    const popup_content = document.createElement("div");
    popup_content.classList.add("popup-content");

    const h3 = document.createElement("h3");
    h3.textContent = `Ajout d'un lieu`;

    popup_content.appendChild(h3);

    // ligne nom du lieu
    const pNom = document.createElement("p");
    pNom.textContent = "Nom du lieu *";
    pNom.className = "obligatoire";

    const textNom = document.createElement("input");
    textNom.type = "text";
    textNom.name = "textNomLieu";
    textNom.placeholder = "Nom du lieu";

    const ligne_nom_lieu = document.createElement("div");
    ligne_nom_lieu.className = "inputGroup";
    ligne_nom_lieu.appendChild(createDivObligatoire(pNom))
    ligne_nom_lieu.appendChild(textNom)

    popup_content.appendChild(ligne_nom_lieu);

    // bouton annuler
    const bAnnuler = document.createElement("button");
    const spanAnnuler = document.createElement("span");
    spanAnnuler.textContent = "Annuler";
    bAnnuler.id = "AnnulerLieu";
    bAnnuler.className = "cssbuttons-io"
    bAnnuler.onclick = () => handleButtonAnnulerClick(popup_overlay_ajouter_lieu);
    bAnnuler.appendChild(spanAnnuler)

    // bouton sauvegarder
    const bSauv = document.createElement("button");
    const spanSauv = document.createElement("span");
    spanSauv.textContent = "Sauvegarder";
    bSauv.id = "sauvLieu";
    bSauv.className = "cssbuttons-io"
    bSauv.addEventListener("click", function () {
        if (!textNom.value) {
            alert("Veuillez remplir le champ requis.");
            return;
        }
        sauvegarderAjoutLieu(textNom.value);
    });
    bSauv.appendChild(spanSauv)

    // ligne de bouton
    const ligne_bouton = document.createElement("div");
    ligne_bouton.appendChild(bSauv)
    ligne_bouton.appendChild(bAnnuler)
    ligne_bouton.id = "bouton_modif"

    popup_content.appendChild(ligne_bouton);

    popup_overlay_ajouter_lieu.appendChild(popup_content);
    document.body.appendChild(popup_overlay_ajouter_lieu);
}

function sauvegarderAjoutLieu(nom) {
    fetch('/ajoutLieu/sauvegarder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nomLieu: nom
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // alert(data.message);
            window.location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Erreur:', error));
}


// Ppopup ajouter fournisseur
function handleButtonAjoutFournisseurClick() {
    let popup_overlay = document.getElementById("popup-overlay-fournisseur")
    if (!popup_overlay){
        popup_overlay = document.createElement("div");
        popup_overlay.id = "popup-overlay-fournisseur";
    }
    clearContent(popup_overlay);

    const popup_content = document.createElement("div");
    popup_content.classList.add("popup-content");

    const h3 = document.createElement("h3");
    h3.textContent = `Ajout d'un fournisseur`;

    popup_content.appendChild(h3);

    // ligne nom du fournisseur
    const pNom = document.createElement("p");
    pNom.textContent = "Nom du fournisseur *";
    pNom.className = "obligatoire";

    const textNom = document.createElement("input");
    textNom.type = "text";
    textNom.name = "textNomFournisseur";
    textNom.placeholder = "Nom du fournisseur";

    const ligne_nom_fournisseur = document.createElement("div");
    ligne_nom_fournisseur.className = "inputGroup";
    ligne_nom_fournisseur.appendChild(createDivObligatoire(pNom))
    ligne_nom_fournisseur.appendChild(textNom)

    popup_content.appendChild(ligne_nom_fournisseur);

    // ligne adresse
    const pAdresse = document.createElement("p");
    pAdresse.textContent = "Adresse";

    const textAdresse = document.createElement("input");
    textAdresse.type = "text";
    textAdresse.name = "textAdresseFournisseur";
    textAdresse.placeholder = "Adresse du fournisseur";

    const ligne_adresse = document.createElement("div");
    ligne_adresse.className = "inputGroup";
    ligne_adresse.appendChild(pAdresse)
    ligne_adresse.appendChild(textAdresse)

    popup_content.appendChild(ligne_adresse);

    // ligne numero de telephone
    const pTelephone = document.createElement("p");
    pTelephone.textContent = "Numéro de téléphone";

    const textTelephone = document.createElement("input");
    textTelephone.type = "text";
    textTelephone.name = "textTelephoneFournisseur";
    textTelephone.placeholder = "Numéro de teléphone du fournisseur";

    const ligne_numero = document.createElement("div");
    ligne_numero.className = "inputGroup";
    ligne_numero.appendChild(pTelephone);
    ligne_numero.appendChild(textTelephone);

    popup_content.appendChild(ligne_numero);

    // boutton Annuler
    const bAnnuler = document.createElement("button");
    const spanOk = document.createElement("span");
    spanOk.textContent = "Annuler";    
    bAnnuler.id = "AnnulerFournisseur";
    bAnnuler.className = "cssbuttons-io";
    bAnnuler.onclick = () => handleButtonAnnulerClick(popup_overlay);
    bAnnuler.appendChild(spanOk)

    // boutton Sauvegarder
    const bSauv = document.createElement("button");
    const spanSauv = document.createElement("span");
    spanSauv.textContent = "Sauvegarder";
    bSauv.id = "sauvFournisseur";
    bSauv.className = "cssbuttons-io"
    bSauv.addEventListener("click", function () {
        if (!textNom.value) {
            alert("Veuillez rensigner le nom du fournisseur.");
            return;
        }
        sauvegarderAjoutFournisseur(textNom.value, textAdresse.value, textTelephone.value);
    });
    bSauv.appendChild(spanSauv)

    // ligne de bouton
    const ligne_bouton = document.createElement("div");
    ligne_bouton.appendChild(bSauv)
    ligne_bouton.appendChild(bAnnuler)
    ligne_bouton.id = "bouton_modif"

    popup_content.appendChild(ligne_bouton);

    popup_overlay.appendChild(popup_content);
    document.body.appendChild(popup_overlay);
}

function sauvegarderAjoutFournisseur(nom, adresse, telephone) {
    fetch('/ajoutFournisseur/sauvegarder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nomFournisseur: nom,
            adresseFournisseur: adresse,
            telephoneFournisseur: telephone
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // alert(data.message);
            window.location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Erreur:', error));
}


// Listener boutons ajout produit, lieu, fournisseur et seuil
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('ajouter_prod').addEventListener('click', handleButtonAjoutProdClick);
    document.getElementById('ajouter_lieu').addEventListener('click', handleButtonAjoutLieuClick);
    document.getElementById('ajouter_fournisseur').addEventListener('click', handleButtonAjoutFournisseurClick);
    document.getElementById("search_seuil").addEventListener("click", function() {
        fetch('/generate_pdf', { method: 'POST' })
        .then(response => response.blob())
        .then(blob => {
            let url = window.URL.createObjectURL(blob);
            let a = document.createElement("a");
            a.href = url;
            a.download = "produits_seuil.pdf";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        })
        .catch(error => console.error("Erreur :", error));
    });
});


// Popup cacher un produit
function handleButtonCacherProduit(produit, nomProduit) {
    // Crée le fond du popup
    let popup_overlay_cacher = document.getElementById("popup-overlay-cacher")
    if (!popup_overlay_cacher){
        popup_overlay_cacher = document.createElement("div");
        popup_overlay_cacher.id = "popup-overlay-cacher";
    }
    clearContent(popup_overlay_cacher);

    // Contenu du popup
    const popup_content = document.createElement("div");
    popup_content.classList.add("popup-content");

    // Titre du popup
    const h3 = document.createElement("h3");
    h3.textContent = `Souhaitez vous cacher: ${nomProduit} ?`;
    popup_content.appendChild(h3);

    // Bouton Non pour fermer le popup
    const bNon = document.createElement("button");
    const spanNon = document.createElement("span");
    spanNon.textContent = "Non";
    bNon.className = "cssbuttons-io"
    bNon.onclick = () => handleButtonAnnulerClick(popup_overlay_cacher);
    bNon.appendChild(spanNon)
    
    // Bouton Oui 
    const bOui = document.createElement("button");
    const spanOui = document.createElement("span");
    spanOui.textContent = "Oui";
    bOui.className = "cssbuttons-io"
    bOui.data = produit
    bOui.addEventListener("click", function (){
        cacherProduit(produit)
    });
    bOui.appendChild(spanOui)

    // ligne de bouton
    const ligne_bouton = document.createElement("div");
    ligne_bouton.appendChild(bOui)
    ligne_bouton.appendChild(bNon)
    ligne_bouton.id = "bouton_modif"

    popup_content.appendChild(ligne_bouton);

    popup_overlay_cacher.appendChild(popup_content);
    document.body.appendChild(popup_overlay_cacher); 

}

function cacherProduit(idProduit) {
    fetch(`/cacher/${idProduit}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // alert(data.message);
                window.location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Erreur:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    const les_buttons = document.getElementsByClassName('supp_produit');
    for (let button of les_buttons) {
        const produitId = button.getAttribute('data-produit');
        button.addEventListener('click', function() {
            fetch(`/pop_up_cacher/${produitId}`)
                .then(response => response.json())
                .then(data => {
                    handleButtonCacherProduit(data.id_produit, data.nomProduit);

                })
                .catch(error => console.error('Erreur lors de la récupération des données du produit:', error));
        });
    }
});


// Popup de montrer un produit
function handleButtonMontrerProduit(produit, nomProduit) {
    let popup_overlay_montrer = document.getElementById("popup-overlay-montrer")
    if (!popup_overlay_montrer){
        popup_overlay_montrer = document.createElement("div");
        popup_overlay_montrer.id = "popup-overlay-montrer";
    }
    clearContent(popup_overlay_montrer);

    // Contenu du popup
    const popup_content = document.createElement("div");
    popup_content.classList.add("popup-content");
    

    // Titre du popup
    const h3 = document.createElement("h3");
    h3.textContent = `Souhaitez vous montrer: ${nomProduit} ?`;
    popup_content.appendChild(h3);

    // Bouton Non pour fermer le popup
    const bNon = document.createElement("button");
    const spanNon = document.createElement("span");
    spanNon.textContent = "Non";
    bNon.className = "cssbuttons-io"
    bNon.onclick = () => handleButtonAnnulerClick(popup_overlay_montrer);
    bNon.appendChild(spanNon)


    // Bouton Oui 
    const bOui = document.createElement("button");
    const spanOui = document.createElement("span");
    spanOui.textContent = "Oui";
    bOui.className = "cssbuttons-io"
    bOui.data = produit
    bOui.addEventListener("click", function (){
        montrerProduit(produit)
    });
    bOui.appendChild(spanOui)

    // ligne de bouton
    const ligne_bouton = document.createElement("div");
    ligne_bouton.appendChild(bOui)
    ligne_bouton.appendChild(bNon)
    ligne_bouton.id = "bouton_modif"

    popup_content.appendChild(ligne_bouton);

    popup_overlay_montrer.appendChild(popup_content);
    document.body.appendChild(popup_overlay_montrer); 

}

function montrerProduit(idProduit) {
    fetch(`/montrer/${idProduit}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // alert(data.message);
                window.location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Erreur:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    const les_buttons = document.getElementsByClassName('remettre_produit');
    for (let button of les_buttons) {
        const produitId = button.getAttribute('data-produit');
        button.addEventListener('click', function() {
            fetch(`/pop_up_montrer/${produitId}`)
                .then(response => response.json())
                .then(data => {
                    handleButtonMontrerProduit(data.id_produit, data.nomProduit);

                })
                .catch(error => console.error('Erreur lors de la récupération des données du produit:', error));
        });
    }
});
