from .app import app
from flask import render_template
from .models import get_sample, search_filter, get_all_prod
from flask import request

#TODO Mettre un login required sur toutes les pages qui le nécessite

@app.route("/")
def home():
    #TODO log pour current_user, supprimer current_user de render templete
    #TODO donner une liste de produits à liste_produit dans render
    liste_produit = get_sample()
    return render_template("home.html", liste_produit=liste_produit, current_user=True) 

@app.route("/preparation/reservations")
def preparation_reservation():
    #TODO log pour current_user, supprimer current_user de render templete
    #TODO remplir reservations avec la liste des reservations ordonné dans un ordre pré définie
    reservations = [] 
    return render_template("reservation-preparation.html", reservations=reservations, current_user=True)


@app.route("/connection")
def connecter():
    return render_template("connection.html")

@app.route("/inscription")
def inscrire():
    return render_template("inscription.html")

@app.route("/search", methods=('GET',))
def search():
    q = request.args.get("search")
    erreur = ''
    results = search_filter(q)  
    return render_template("home.html", liste_produit=results, current_user=True)

