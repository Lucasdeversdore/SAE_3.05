// Fonction pour afficher le popup d'info produit
function handleButtonInfoClick(produit, lieu) {
    // Crée le fond du popup
    const popup_overlay_info = document.createElement("div");
    popup_overlay_info.id = "popup-overlay-info";

    // Contenu du popup
    const popup_content = document.createElement("div");

    // Titre du popup
    const h3 = document.createElement("h3");
    h3.textContent = produit.nomProduit;

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




