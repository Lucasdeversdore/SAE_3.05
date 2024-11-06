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

function handleButtonModifClick(produit, lieu, fournisseur, est_stocker) {
    const popup_overlay_modif = document.createElement("div");
    popup_overlay_modif.id = "popup-overlay-modif";
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
    h3.textContent = `Modification du produit: ${produit.nomProduit}`;

    const pNom = document.createElement("p");
    pNom.textContent = "Nom du produit:";
    const textNom = document.createElement("input");
    textNom.type = "text";
    textNom.name = "textNom";
    textNom.value = produit.nomProduit;

    const pFournisseur = document.createElement("p");
    pFournisseur.textContent = "Fournisseur:";
    const selectFournisseur = document.createElement("input");
    selectFournisseur.type = "text";
    selectFournisseur.name = "textFournisseur";
    selectFournisseur.value = fournisseur.nomFou;

    const pQuantite = document.createElement("p");
    pQuantite.textContent = `Quantité actuelle (${est_stocker.quantiteStocke || 0}):`;  // Définit 0 si la quantité est undefined
    const textQuantite = document.createElement("input");
    textQuantite.type = "text";
    textQuantite.name = "textQuantite";
    textQuantite.value = est_stocker.quantiteStocke || 0;

    const pFonction = document.createElement("p");
    pFonction.textContent = "Fonction du produit:";
    const textFonction = document.createElement("input");
    textFonction.type = "text";
    textFonction.name = "textFonction";
    textFonction.value = produit.fonctionProduit || "";

    const pLieuStock = document.createElement("p");
    pLieuStock.textContent = "Lieu de stockage:";
    const selectLieuStock = document.createElement("input");
    selectLieuStock.type = "text";
    selectLieuStock.name = "textLieu";
    selectLieuStock.value = lieu.nomLieu;

    const bOk = document.createElement("button");
    bOk.textContent = "Annuler";
    bOk.id = "okModif";
    bOk.addEventListener("click", handleButtonOKModifClick);

    const bSauv = document.createElement("button");
    bSauv.textContent = "Sauvegarder";
    bSauv.id = "sauvModif";
    bSauv.addEventListener("click", function () {
        if (!textNom.value || !textQuantite.value || !selectLieuStock.value) {
            alert("Veuillez remplir tous les champs requis.");
            return;
        }
        sauvegarderProduit(produit.idProduit, textNom.value, selectFournisseur.value,
            textQuantite.value, textFonction.value, selectLieuStock.value);
    });

    popup_content.appendChild(h3);
    popup_content.appendChild(pNom);
    popup_content.appendChild(textNom);
    popup_content.appendChild(pFournisseur);
    popup_content.appendChild(selectFournisseur);
    popup_content.appendChild(pQuantite);
    popup_content.appendChild(textQuantite);
    popup_content.appendChild(pFonction);
    popup_content.appendChild(textFonction);
    popup_content.appendChild(pLieuStock);
    popup_content.appendChild(selectLieuStock);
    popup_content.appendChild(bOk);
    popup_content.appendChild(bSauv);
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
                    handleButtonModifClick(data.produit, data.lieu, data.fournisseur, data.est_stocker);
                })
                .catch(error => console.error('Erreur lors de la récupération des données du produit:', error));
        });
    }
});


