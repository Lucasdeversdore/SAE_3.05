// Fonctions pour afficher le popup d'info produit
function handleButtonInfoClick(produit, lieu) {
    // Crée le fond du popup
    const popup_overlay = document.createElement("div");
    popup_overlay.id = "popup-overlay-info";
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
    popup_overlay.appendChild(popup_content);
    document.body.appendChild(popup_overlay); // Ajoute le popup au DOM
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

