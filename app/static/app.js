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

function clearContent(element){
    while(element.firstChild){
        element.removeChild(element.firstChild);
    }
}
