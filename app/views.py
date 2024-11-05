from hashlib import sha256
from flask_login import login_required, login_user, logout_user
from wtforms import HiddenField, PasswordField, StringField
from .app import app
from flask_wtf import FlaskForm
from flask import redirect, render_template, url_for
from .models import Chimiste, get_sample, search_filter, search_famille_filter
from flask import request

class LoginForm ( FlaskForm ):
    email = StringField('email')
    password = PasswordField('Password')
    next = HiddenField()
    def get_authenticated_user(self):
        user = Chimiste.query.filter(Chimiste.email == self.email.data).first()
        if user is None:
            return "Email incorrect"
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.mdp else "Mot de passe incorrect"

@app.route("/")
@login_required
def home():
    #TODO log pour current_user, supprimer current_user de render templete
    #TODO donner une liste de produits à liste_produit dans render
    liste_produit = get_sample()
    return render_template("home.html", liste_produit=liste_produit, current_user=True) 

@app.route("/preparation/reservations")
@login_required
def preparation_reservation():
    #TODO log pour current_user, supprimer current_user de render templete
    #TODO remplir reservations avec la liste des reservations ordonné dans un ordre pré définie
    reservations = [] 
    return render_template("reservation-preparation.html", reservations=reservations, current_user=True)


@app.route("/connection")
def connecter():
    f = LoginForm()
    return render_template("connection.html", msg=None, form=f)

@app.route("/inscription")
def inscrire():
    return render_template("inscription.html")

@app.route("/search", methods=('GET',))
@login_required
def search():
    q = request.args.get("search")
    results = search_filter(q) + search_famille_filter(q)
    return render_template("home.html", liste_produit=results, current_user=True)


@app.route("/test/connection", methods=('GET', 'POST'))
def connection():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if type(user) != str:
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect(next)
    return render_template("connection.html", form=f, msg=user)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('connection'))