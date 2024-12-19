function createDivTextCache() {
    const divTextCache2 = document.createElement("div");
    divTextCache2.className = "hover-text";
    divTextCache2.textContent = "champ obligatoire";
    return divTextCache2;
}

function createDivObligatoire(elem) {
    const divQuantite = document.createElement("div");
    divQuantite.className = "containerObligatoire";
    divQuantite.appendChild(elem);
    divQuantite.appendChild(createDivTextCache());
    return divQuantite;
}


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
    popup_overlay_modif.classList.add("popup-overlay-modif");

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
    pQuantite.textContent = `Quantité actuelle (${est_stocker.quantiteStocke || 0} ${produit.nomUnite || null}) : *`;
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
    bAnnuler.addEventListener("click", handleButtonOKModifClick);
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
            textQuantite.value, selectFonction.value, selectLieuStock.value);
    });
    bSauv.appendChild(spanSauv)

    // ligne de bouton
    const ligne_bouton = document.createElement("div");
    ligne_bouton.appendChild(bAnnuler)
    ligne_bouton.appendChild(bSauv)
    ligne_bouton.id = "bouton_modif"

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
    fetch(`/sauvegarder/${idProduit}?inputNom=${encodeURIComponent(nom)}&textFournisseur=${encodeURIComponent(nom_fournisseur)}&textQuantite=${encodeURIComponent(quantite)}&textFonction=${encodeURIComponent(fonction)}&textLieu=${encodeURIComponent(lieu)}`)
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
    const popup_overlay_ajout = document.createElement("div");
    popup_overlay_ajout.id = "popup-overlay-ajout";

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
    pFournisseur.textContent = "Fournisseur";
    
    const selectFournisseur = document.createElement("input");
    selectFournisseur.type = "text";
    selectFournisseur.name = "textNewFournisseur";
    selectFournisseur.placeholder = "Fournisseur";

    const ligne_fournisseur = document.createElement("div");
    ligne_fournisseur.className = "inputGroup";
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
    pQuantite.textContent = "Quantiter('ER' MDRRRRRR) disponible *"
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
    pLieuStock.textContent = "Lieu de stockage *";
    pLieuStock.className = "obligatoire";

    const selectLieuStock = document.createElement("input");
    selectLieuStock.type = "text";
    selectLieuStock.name = "textNewLieu";
    selectLieuStock.placeholder = "Lieu de stockage";

    const ligne_lieu_stock = document.createElement("div");
    ligne_lieu_stock.className = "inputGroup";
    ligne_lieu_stock.appendChild(createDivObligatoire(pLieuStock))
    ligne_lieu_stock.appendChild(selectLieuStock)

    popup_content.appendChild(ligne_lieu_stock);

    // boutton Annuler
    const bAnnuler = document.createElement("button");
    const spanOk = document.createElement("span");
    spanOk.textContent = "Annuler";
    bAnnuler.id = "AnnulerAjout";
    bAnnuler.className = "cssbuttons-io"
    bAnnuler.addEventListener("click", handleButtonAnnulerAjoutClick);
    bAnnuler.appendChild(spanOk)

    // boutton Sauvegarder
    const bSauv = document.createElement("button");
    const spanSauv = document.createElement("span");
    spanSauv.textContent = "Sauvegarder";
    bSauv.id = "sauvAjout";
    bSauv.className = "cssbuttons-io"
    bSauv.addEventListener("click", function () {
        if (!textNom.value || !textQuantite.value || !selectLieuStock.value || !textUnite.value) {
            alert("Veuillez remplir tous les champs requis.");
            return;
        }
        sauvegarderAjoutProduit(textNom.value, 
            selectFournisseur.value, textUnite.value, textQuantite.value, 
            textFonction.value, selectLieuStock.value)
        
    });
    bSauv.appendChild(spanSauv)

    // ligne de bouton
    const ligne_bouton = document.createElement("div");
    ligne_bouton.appendChild(bAnnuler)
    ligne_bouton.appendChild(bSauv)
    ligne_bouton.id = "bouton_modif"

    popup_content.appendChild(ligne_bouton);

    popup_overlay_ajout.appendChild(popup_content);
    document.body.appendChild(popup_overlay_ajout);
}


function handleButtonAnnulerAjoutClick() {
    const popup = document.getElementById("popup-overlay-ajout");
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

// function handleButtonAjoutFonctionClick() {
//     const popup_overlay = document.createElement("div");
//     popup_overlay.id = "popup-overlay-Fonction";
//     popup_overlay.style.position = "fixed";
//     popup_overlay.style.top = "0";
//     popup_overlay.style.left = "0";
//     popup_overlay.style.width = "100%";
//     popup_overlay.style.height = "100%";
//     popup_overlay.style.backgroundColor = "rgba(0, 0, 0, 0.7)";
//     popup_overlay.style.display = "flex";
//     popup_overlay.style.justifyContent = "center";
//     popup_overlay.style.alignItems = "center";
//     popup_overlay.style.zIndex = "1000";

//     const popup_content = document.createElement("div");
//     popup_content.style.backgroundColor = "#fff";
//     popup_content.style.padding = "20px";
//     popup_content.style.borderRadius = "5px";
//     popup_content.style.width = "300px";
//     popup_content.style.textAlign = "center";

//     const h3 = document.createElement("h3");
//     h3.textContent = `Ajout d'une fonction`;

//     const pNom = document.createElement("p");
//     pNom.textContent = "Nom de la fonction *";
//     const textNom = document.createElement("input");
//     textNom.type = "text";
//     textNom.name = "textNomFonction";

//     const bAnnuler = document.createElement("button");
//     bAnnuler.textContent = "Annuler";
//     bAnnuler.id = "AnnulerFonction";
//     bAnnuler.addEventListener("click", function () {
//         const popup = document.getElementById("popup-overlay-Fonction");
//         if (popup) popup.remove();
//     });

//     const bSauv = document.createElement("button");
//     bSauv.textContent = "Sauvegarder";
//     bSauv.id = "sauvFonction";
//     bSauv.addEventListener("click", function () {
//         if (!textNom.value) {
//             alert("Veuillez remplir le champ requis.");
//             return;
//         }
//         sauvegarderAjoutFonction(textNom.value);
//     });

    
//     popup_content.appendChild(h3);
//     popup_content.appendChild(pNom);
//     popup_content.appendChild(textNom);
//     popup_content.appendChild(bAnnuler);
//     popup_content.appendChild(bSauv);
//     popup_overlay.appendChild(popup_content);
//     document.body.appendChild(popup_overlay);
// }

// function sauvegarderAjoutFonction(nom) {
//     fetch('/ajoutFonction/sauvegarder', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({
//             nomFonction: nom
//         })
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.success) {
//             alert(data.message);
//             window.location.href = '/'; 
//         } else {
//             alert(data.message);
//         }
//     })
//     .catch(error => console.error('Erreur:', error));
// }

function handleButtonAjoutLieuClick() {
    const popup_overlay = document.createElement("div");
    popup_overlay.id = "popup-overlay-Lieu";
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

    const popup_content = document.createElement("div");
    popup_content.style.backgroundColor = "#fff";
    popup_content.style.padding = "20px";
    popup_content.style.borderRadius = "5px";
    popup_content.style.width = "300px";
    popup_content.style.textAlign = "center";

    const h3 = document.createElement("h3");
    h3.textContent = `Ajout d'un lieu`;

    const pNom = document.createElement("p");
    pNom.textContent = "Nom du lieu *";
    const textNom = document.createElement("input");
    textNom.type = "text";
    textNom.name = "textNomLieu";

    const bAnnuler = document.createElement("button");
    bAnnuler.textContent = "Annuler";
    bAnnuler.id = "AnnulerLieu";
    bAnnuler.addEventListener("click", function () {
        const popup = document.getElementById("popup-overlay-Lieu");
        if (popup) popup.remove();
    });

    const bSauv = document.createElement("button");
    bSauv.textContent = "Sauvegarder";
    bSauv.id = "sauvLieu";
    bSauv.addEventListener("click", function () {
        if (!textNom.value) {
            alert("Veuillez remplir le champ requis.");
            return;
        }
        sauvegarderAjoutLieu(textNom.value);
    });

    popup_content.appendChild(h3);
    popup_content.appendChild(pNom);
    popup_content.appendChild(textNom);
    popup_content.appendChild(bAnnuler);
    popup_content.appendChild(bSauv);
    popup_overlay.appendChild(popup_content);
    document.body.appendChild(popup_overlay);
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
            alert(data.message);
            window.location.href = '/'; 
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Erreur:', error));
}

function handleButtonAjoutFournisseurClick() {
    const popup_overlay = document.createElement("div");
    popup_overlay.id = "popup-overlay-Fournisseur";
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

    const popup_content = document.createElement("div");
    popup_content.style.backgroundColor = "#fff";
    popup_content.style.padding = "20px";
    popup_content.style.borderRadius = "5px";
    popup_content.style.width = "300px";
    popup_content.style.textAlign = "center";

    const h3 = document.createElement("h3");
    h3.textContent = `Ajout d'un fournisseur`;

    const pNom = document.createElement("p");
    pNom.textContent = "Nom du fournisseur *";
    const textNom = document.createElement("input");
    textNom.type = "text";
    textNom.name = "textNomFournisseur";

    const pAdresse = document.createElement("p");
    pAdresse.textContent = "Adresse";
    const textAdresse = document.createElement("input");
    textAdresse.type = "text";
    textAdresse.name = "textAdresseFournisseur";

    const pTelephone = document.createElement("p");
    pTelephone.textContent = "Numéro de téléphone";
    const textTelephone = document.createElement("input");
    textTelephone.type = "text";
    textTelephone.name = "textTelephoneFournisseur";

    const bAnnuler = document.createElement("button");
    bAnnuler.textContent = "Annuler";
    bAnnuler.id = "AnnulerFournisseur";
    bAnnuler.addEventListener("click", function () {
        const popup = document.getElementById("popup-overlay-Fournisseur");
        if (popup) popup.remove();
    });

    const bSauv = document.createElement("button");
    bSauv.textContent = "Sauvegarder";
    bSauv.id = "sauvFournisseur";
    bSauv.addEventListener("click", function () {
        if (!textNom.value) {
            alert("Veuillez rensigner le nom du fournisseur.");
            return;
        }
        sauvegarderAjoutFournisseur(textNom.value, textAdresse.value, textTelephone.value);
    });

    popup_content.appendChild(h3);
    popup_content.appendChild(pNom);
    popup_content.appendChild(textNom);
    popup_content.appendChild(pAdresse);
    popup_content.appendChild(textAdresse);
    popup_content.appendChild(pTelephone);
    popup_content.appendChild(textTelephone);
    popup_content.appendChild(bAnnuler);
    popup_content.appendChild(bSauv);
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
            alert(data.message);
            window.location.href = '/'; 
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Erreur:', error));
}



document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('ajouter_prod').addEventListener('click', handleButtonAjoutProdfClick);
    // document.getElementById('ajouter_fonction').addEventListener('click', handleButtonAjoutFonctionClick);
    document.getElementById('ajouter_lieu').addEventListener('click', handleButtonAjoutLieuClick);
    document.getElementById('ajouter_fournisseur').addEventListener('click', handleButtonAjoutFournisseurClick);
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
