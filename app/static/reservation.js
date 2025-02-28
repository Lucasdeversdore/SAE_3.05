// Delete réservation
document.addEventListener('DOMContentLoaded', function() {
    const les_buttons = document.getElementsByClassName('delete_reservation');
    for (let button of les_buttons) {
        const idCommande = button.getAttribute('idCommande');
        button.addEventListener('click', function() {
            handleButtonDeleteReservation(idCommande);
        });
    }
}); 

function handleButtonDeleteReservation(idCommande) {
    // Crée le fond du popup
    const popup_overlay = document.createElement("div");
    popup_overlay.id = "popup-overlay-resrev";

    // Contenu du popup
    const popup_content = document.createElement("div");
    popup_content.classList.add("popup-content");

    // Titre du popup
    const h3 = document.createElement("h3");
    h3.textContent = "Voulez vous supprimer cette commande ?";
    popup_content.appendChild(h3);

    // Bouton Annuler pour fermer le popup
    const bAnnuler = document.createElement("button");
    const spanAnnuler = document.createElement("span");
    spanAnnuler.textContent = "Non";
    bAnnuler.className = "cssbuttons-io";
    bAnnuler.addEventListener("click", handleButtonAnnulerClick);
    bAnnuler.appendChild(spanAnnuler)

    // Bouton Reserver
    const bReserver = document.createElement("button");
    const spanReserver = document.createElement("span");
    spanReserver.textContent = "Oui";
    bReserver.appendChild(spanReserver)
    bReserver.className = "cssbuttons-io"
    bReserver.addEventListener("click", function() {
        window.location.href = `/supprimer/reservation/${idCommande}`;
    });

    // ligne de bouton
    const ligne_bouton = document.createElement("div");
    ligne_bouton.appendChild(bReserver)
    ligne_bouton.appendChild(bAnnuler)
    ligne_bouton.id = "bouton_modif"

    popup_content.appendChild(ligne_bouton);
    popup_overlay.appendChild(popup_content);
    document.body.appendChild(popup_overlay); 
}




// Ajoute un gestionnaire d'événements aux boutons 'Etat'
document.addEventListener('DOMContentLoaded', function() {
    const les_buttons = document.getElementsByClassName('Etat');

    for (let button of les_buttons) {
        const idCommande = button.getAttribute('idCommande');
        const etat = button.getAttribute('etat');

        if (etat != "termine"){
            button.addEventListener('click', function() {
                handleButtonEtatCommande(idCommande, etat);
            });
        }
    }
}); 

function handleButtonEtatCommande(idCommande, etat) {
    // Crée le fond du popup
    const popup_overlay = document.createElement("div");
    popup_overlay.id = "popup-overlay-resrev";

    // Contenu du popup
    const popup_content = document.createElement("div");
    popup_content.classList.add("popup-content");

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
    popup_content.appendChild(h3);

    // Bouton Annuler pour fermer le popup
    const bAnnuler = document.createElement("button");
    const spanAnnuler = document.createElement("span");
    spanAnnuler.textContent = "Non";
    bAnnuler.className = "cssbuttons-io";
    bAnnuler.addEventListener("click", handleButtonAnnulerClick);
    bAnnuler.appendChild(spanAnnuler)

    // Bouton Reserver
    const bReserver = document.createElement("button");
    const spanReserver = document.createElement("span");
    spanReserver.textContent = "Oui";
    bReserver.appendChild(spanReserver)
    bReserver.className = "cssbuttons-io"
    bReserver.addEventListener("click", function() {
        window.location.href = `/etat/commande/${idCommande}`;
    });
    
    // ligne de bouton
    const ligne_bouton = document.createElement("div");
    ligne_bouton.appendChild(bReserver)
    ligne_bouton.appendChild(bAnnuler)
    ligne_bouton.id = "bouton_modif"

    popup_content.appendChild(ligne_bouton);

    popup_overlay.appendChild(popup_content);
    document.body.appendChild(popup_overlay); 
}




// Popup modifier la quantité d'une réservation
function handleButtonModifReservation(commande, produit, stock, erreur) {
    // Crée le fond du popup
    const popup_overlay = document.createElement("div");
    popup_overlay.id = "popup-overlay-resrev";

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
    let quantite = stock.quantiteStocke + commande.qteCommande
    pQte.textContent = "Quantité en stock : "+ quantite +produit.nomUnite
    
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
    inputQte.value = commande.qteCommande
    
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
    bAnnuler.addEventListener("click", handleButtonAnnulerClick);


    // Bouton modifier
    const bModifier = document.createElement("button");
    const spanReserver = document.createElement("span");
    spanReserver.textContent = "Modifier";
    bModifier.appendChild(spanReserver);
    bModifier.id = produit.idProduit; 
    bModifier.className = "cssbuttons-io";
    bModifier.addEventListener("click", function () {
        const quantite = inputQte.value;
        ModifierQteProduit(commande.idCommande, quantite);
    });
    
    // ligne de bouton
    const ligne_bouton = document.createElement("div");
    ligne_bouton.appendChild(bAnnuler)
    ligne_bouton.appendChild(bModifier)
    ligne_bouton.id = "bouton_modif"

    popup_content.appendChild(ligne_bouton);

    popup_overlay.appendChild(popup_content);
    document.body.appendChild(popup_overlay); 
}

function handleButtonAnnulerClick() {
    const popup = document.getElementById("popup-overlay-resrev");
    if (popup) {
        popup.remove(); 
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const les_buttons = document.getElementsByClassName('modif_reserv');

    for (let button of les_buttons) {
        const commandeId = button.getAttribute('data-commande');
        console.log(commandeId)
        button.addEventListener('click', function() {
            // Effectuer la requête fetch au clic pour récupérer les données du produit
            fetch(`/commande/${commandeId}`)
                .then(response => response.json())
                .then(data => {
                    handleButtonModifReservation(data.commande, data.produit, data.stock);
                })
                .catch(error => console.error('Erreur lors de la récupération des données du produit:', error));
        });
    }
}); 

function ModifierQteProduit(CommandeId, quantite) {
    console.log(CommandeId)
    fetch(`/commande/modif/${CommandeId}?inputQte=${quantite}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Redirigez ou mettez à jour l'interface si la réservation est réussie
                // alert(data.message);  // Affiche la confirmation
                window.location.reload();
                // window.location.href = '/preparation/reservations';  
            } else {
                // Affiche une alerte en cas d'erreur
                alert(data.message);
            }
        })
        .catch(error => console.error('Erreur:', error));
}
