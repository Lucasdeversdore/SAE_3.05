from hashlib import sha256
from flask_login import login_required, login_user, logout_user, current_user
from wtforms import HiddenField, PasswordField, StringField
from .app import app
from flask_wtf import FlaskForm
from flask import jsonify, redirect, render_template, url_for
from .models import Chimiste, Produit, Est_Stocker, Lieu_Stockage, Fournisseur, get_sample_prduit_qte, get_sample_reservation, next_chimiste_id, next_prod_id, search_filter, search_famille_filter, reserver_prod, modif_sauvegarde, ajout_sauvegarde
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

from flask_wtf import FlaskForm
from wtforms import SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo

class InscriptionForm(FlaskForm):
    from .models import check_mdp_validator
    prenom = StringField('Prénom', validators=[DataRequired(), Length(min=2, max=50)])
    nom = StringField('Nom', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mdp = PasswordField('Mot de passe', validators=[DataRequired(), check_mdp_validator])
    confirm_mdp = PasswordField('Confirmer mot de passe',
                                validators=[DataRequired(), EqualTo('mdp', message='Les mots de passe doivent correspondre')])
    submit = SubmitField("S'inscrire")


@app.route("/")
@login_required
def home():
    liste_produit_qte = get_sample_prduit_qte(141)
    return render_template("home.html", liste_produit_qte=liste_produit_qte)

@app.route("/preparation/reservations")
@login_required
def preparation_reservation():
    reservations_etats = get_sample_reservation()
    return render_template("reservation-preparation.html", reservations_etats=reservations_etats)


@app.route("/connection")
def connecter():
    f = LoginForm()
    return render_template("connection.html", msg=None, form=f)


from flask import Flask, render_template, redirect, url_for, flash
from .models import Chimiste, db, next_chimiste_id

@app.route('/inscription', methods=['GET', 'POST'])
def inscrire():
    form = InscriptionForm()
    if form.validate_on_submit():
        # Récupérer les données du formulaire
        prenom = form.prenom.data
        nom = form.nom.data
        email = form.email.data
        mdp = form.mdp.data
        
        m = sha256()
        m.update(mdp.encode())
        passwd = m.hexdigest()

        # Vérifier si l'email existe déjà dans la base
        chimiste_existant = Chimiste.query.filter_by(email=email).first()
        if chimiste_existant:
            flash('Cet email est déjà utilisé.', 'danger')
            return redirect(url_for('inscription'))
        
        # Créer un nouvel utilisateur Chimiste
        nouveau_chimiste = Chimiste(idChimiste=next_chimiste_id(), prenom=prenom, nom=nom, email=email, mdp=passwd)
        
        # Ajouter à la session et enregistrer dans la base de données
        db.session.add(nouveau_chimiste)
        db.session.commit()

        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('connection'))

    return render_template('inscription.html', form=form)

@app.route("/search", methods=('GET',))
@login_required
def search():
    q = request.args.get("search")
    results = search_filter(q) + search_famille_filter(q)
    return render_template("home.html", liste_produit_qte=results)


@app.route("/test/connection", methods=('GET', 'POST'))
def connection():
    user = None
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


@app.route('/get/produit/<int:id_produit>', methods=['GET'])
@login_required
def get_produit(id_produit):
    produit = Produit.query.get(id_produit).to_dict()
    est_stocker = Est_Stocker.query.filter(Est_Stocker.idProduit == id_produit).first()
    if est_stocker:
        id_lieu = est_stocker.idLieu
        lieu = Lieu_Stockage.query.filter(Lieu_Stockage.idLieu == id_lieu).first().to_dict()
    else:
        lieu = None
    return jsonify(produit=produit, lieu=lieu)


@app.route('/reserver/<int:id_produit>', methods=['GET'])
@login_required
def popup_reserver_produit(id_produit, erreur=None):
    produit=Produit.query.get(id_produit).to_dict()
    stock=Est_Stocker.query.filter(Est_Stocker.idProduit == id_produit).first().to_dict()
    return jsonify(produit=produit, stock=stock, erreur=erreur)
    
@app.route('/reservation/<int:id_produit>', methods=('GET',))
@login_required
def reserver_produit(id_produit):
    
    qte = request.args.get("inputQte")
    print(qte)
    if qte == "":
        qte = 0
    else:
        qte = int(qte)
    res = reserver_prod(id_produit, qte, current_user.idChimiste)
    if res:
        return jsonify(success=True, message="Réservation réussie !"), 200
    else:
        return jsonify(success=False, message="Quantité non valide"), 400   

@app.route('/modifier/<int:id_produit>', methods=['GET'])
def get_modif_produit(id_produit):
    
    les_four = Fournisseur.query.all()
    les_fournisseurs = []
    cpt = 0
    for fourn in les_four:
        cpt +=1
        if cpt != id_produit:
            les_fournisseurs.append(fourn.to_dict())
        cpt +=1

    les_fon = Produit.query.all()
    les_fonctions = []
    for fonc in les_fon:
        les_fonctions.append(fonc.to_dict())

    les_li = Lieu_Stockage.query.all()
    les_lieux = []
    for li in les_li:
        les_lieux.append(li.to_dict())
    
    produit = Produit.query.get(id_produit).to_dict()
    est_stocker = Est_Stocker.query.filter(Est_Stocker.idProduit == id_produit).first().to_dict()
    id_lieu = est_stocker["idLieu"]
    lieu = Lieu_Stockage.query.filter(Lieu_Stockage.idLieu == id_lieu).first().to_dict()

    id_fou = produit["idFou"]
    print(id_fou)
    if id_fou is None:
        fournisseur = ""
    else:
        fournisseur = Fournisseur.query.filter(Fournisseur.idFou == id_fou).first().to_dict()
    return jsonify(produit=produit, lieu=lieu, fournisseur=fournisseur, est_stocker=est_stocker, les_fournisseurs=les_fournisseurs, les_fonctions=les_fonctions, les_lieux=les_lieux)     

@app.route('/sauvegarder/<int:id_produit>',  methods=['GET'])
def sauvegarder_modif(id_produit):
   
    nom = request.args.get("textNom")
    four = request.args.get("textFournisseur")
    quantite = request.args.get("textQuantite")
    fonction = request.args.get("textFonction")
    lieu = request.args.get("textLieu")

    res = modif_sauvegarde(id_produit, nom, four, quantite, fonction, lieu)
    if res:
        return jsonify(success=True, message="Modification réussie !"), 200
    else:
        return jsonify(success=False, message="Quantité non valide"), 400
    

@app.route("/search/famille/<int:id_produit>", methods=('GET',))
@login_required
def searchByButton(id_produit):
    prod = Produit.query.get(id_produit)
    q = str(prod.fonctionProduit)
    results = search_famille_filter(q)
    print(results)
    return render_template("home.html", liste_produit_qte=results)




@app.route('/ajout/sauvegarder/', methods=['POST'])
def sauvegarder_ajout():
   
    data = request.get_json()
    nom = data.get("textNom")
    four = data.get("textFournisseur")
    unite = data.get("textUnite")
    quantite = data.get("textQuantite")
    fonction = data.get("textFonction")
    lieu = data.get("textLieu")

    res = ajout_sauvegarde(nom, four, unite, quantite, fonction, lieu)
    if res:
        print("test")
        return jsonify(success=True, message="Réservation réussie !"), 200
    else:
        print("test2")
        return jsonify(success=False, message="Quantité non valide"), 400