from .app import app
from flask import render_template

#TODO Mettre un login required sur toutes les pages qui le nécessite

@app.route("/")
def home():
    #TODO log pour current_user, supprimer current_user de render templete
    #TODO donner une liste de produits à liste_produit dans render
    liste_produit=[]
    return render_template("home.html", liste_produit=liste_produit, current_user=True) 

@app.route("/preparation/reservations")
def preparation_reservation():
    #TODO remplir reservations avec la liste des reservations ordonné dans un ordre pré définie
    reservations = [] 
    return render_template("reservation-preparation.html", reservations=reservations)