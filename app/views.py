from hashlib import sha256
from flask_login import login_required, login_user, logout_user, current_user
from .app import app, db, mail
from flask import jsonify, redirect, render_template, url_for,flash, request, Flask
from .models import Chimiste, Produit, Est_Stocker, Lieu_Stockage, Fournisseur, get_sample_prduit_qte, get_sample_reservation, get_sample_reservation_chimiste, next_chimiste_id, next_prod_id, search_chimiste_filter, search_filter, search_famille_filter, reserver_prod, modif_sauvegarde, ajout_sauvegarde, get_pagination_produits, get_nb_page_max_produits, get_pagination_reservations, get_nb_page_max_reservations, search_reserv_filter
from .form import *
from flask_mail import Message

@app.route("/")
@login_required
def home():
    return home_page()

@app.route("/<int:id_page>", methods=['GET'])
@login_required
def home_page(id_page=1, nb=15):
    if id_page < 1:
        return redirect("/")
    id_page_max = get_nb_page_max_produits(nb)
    if id_page_max < id_page:
        return redirect(url_for('home_page', id_page=id_page_max))
    liste_produit_qte = get_pagination_produits(page=id_page, nb=nb)
    return render_template("home.html", liste_produit_qte=liste_produit_qte, actu_id_page=id_page)

# Route execptionnel pour ne pas afficher /1 comme adresse url
@app.route("/1")
@login_required
def home_page_1():
    return redirect("/")

@app.route("/preparation/reservations")
@login_required
def preparation_reservation():
    return preparation_reservation_page()

@app.route("/preparation/reservations/<int:id_page>")
@login_required
def preparation_reservation_page(id_page=1, nb=5):
    if id_page < 1:
        return redirect("/preparation/reservations")
    id_page_max = get_nb_page_max_reservations(nb, current_user)
    if id_page_max < id_page:
        return redirect(url_for('preparation_reservation_page', id_page=id_page_max))
    reservations_etats = get_pagination_reservations(page=id_page, nb=nb, chimiste=current_user)
    return render_template("reservation-preparation.html", reservations_etats=reservations_etats, actu_id_page=id_page)

# Même chose que pour "/1"
@app.route("/preparation/reservations/1")
@login_required
def preparation_reservation_page_1():
    return redirect("/preparation/reservations")






@app.route('/inscription', methods=['GET', 'POST'])
def inscrire():
    form = InscriptionForm()
    print("test")
    if form.validate_on_submit():
        print("form valide")
        # Récupérer les données du formulaire
        prenom = form.prenom.data
        nom = form.nom.data
        email = form.email.data
        mdp = form.mdp.data
        
        m = sha256()
        m.update(mdp.encode())
        passwd = m.hexdigest()
   
        print("mdp fait")
        # Vérifier si l'email existe déjà dans la base
        chimiste_existant = Chimiste.query.filter_by(email=email).first()
        if chimiste_existant:
            flash('Cet email est déjà utilisé.', 'danger')
            print('Cet email est déjà utilisé.')
            return redirect(url_for('inscrire'))
        nouveau_chimiste = Chimiste(idChimiste=next_chimiste_id(), prenom=prenom, nom=nom, email=email, mdp=passwd)
        send_mail_activation(nouveau_chimiste)
        return redirect(url_for('connection'))
    return render_template('inscription.html', form=form)

def send_mail_activation(user:Chimiste):
    token=user.get_token()
    reset_url = url_for('activation_token', token=token, _external=True)
    
    msg = Message(
        'Activation de votre compte Stockage Chimie',
        recipients=[user.email],
        sender='noreply@codejana.com'
    )

    # Contenu de l'e-mail en HTML
    msg.html = f'''
                <!doctype html>
                <html>
                    <body>
                        <p>Pour activez votre compte Stockage Chimie, cliquez sur le lien ci-dessous :</p>
                        <p><a href="{reset_url}">Activez votre compte</a></p>
                        <p>Si vous n'avez pas demandé cette activation, ignorez simplement cet e-mail.</p>
                    </body>
                </html>
                '''

    mail.send(msg)
    

@app.route('/activation/<token>', methods=['GET', 'POST'])
def activation_token(token):
    user=Chimiste.verify_activation_token(token)
    if user is None:
        flash('token invalide ou expiré. Veulliez réessayer.', 'warning')
        return redirect(url_for('inscrire'))
    
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('connection'))


@app.route("/inscription-cgu")
def cgu():
    return render_template("inscription-cgu.html")

@app.route("/search", methods=('GET',))
@login_required
def search():
    q = request.args.get("search")
    results = search_filter(q) + search_famille_filter(q)
    return render_template("home.html", liste_produit_qte=results, actu_id_page=None)

@app.route("/search-preparation")
@login_required
def search_preparation():
    q = request.args.get("search")
    results = search_reserv_filter(q) + search_chimiste_filter(q)
    return render_template("reservation-preparation.html", reservations_etats=results, actu_id_page=None)


@app.route("/connection", methods=('GET', 'POST'))
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


def send_mail_mdp(user: Chimiste):
    token = user.get_token()
    reset_url = url_for('reset_token', token=token, _external=True)

    msg = Message(
        'Demande de réinitialisation de mot de passe',
        recipients=[user.email],
        sender='noreply@codejana.com'
    )

    # Contenu de l'e-mail en HTML
    msg.html = f'''
                <!doctype html>
                <html>
                    <body>
                        <p>Pour réinitialiser votre mot de passe, cliquez sur le lien ci-dessous :</p>
                        <p><a href="{reset_url}">Réinitialiser votre mot de passe</a></p>
                        <p>Si vous n'avez pas demandé cette réinitialisation, ignorez simplement cet e-mail.</p>
                    </body>
                </html>
                '''

    mail.send(msg)

    
    

@app.route("/reset_pwd", methods=('GET', 'POST'))
def reset_pwd():
    form = ResetForm()
    if not form.is_submitted():
        form.next.data = request.args.get("next")
    elif form.validate_on_submit():
        email = form.email.data
         # Vérifier si l'email existe déjà dans la base
        chimiste_existant = Chimiste.query.filter_by(email=email).first()
        if chimiste_existant:
            send_mail_mdp(chimiste_existant)
            flash("Rgerdez vos mail pour réinitialiser votre mot de passe.")
            print("Rgerdez vos mail pour réinitialiser votre mot de passe.")
            return redirect(url_for('connection'))
    return render_template("reset_pwd.html", form=form)

@app.route('/reset_pwd/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user=Chimiste.verify_mdp_token(token)
    if user is None:
        flash('token invalide ou expiré. Veulliez réessayer.', 'warning')
        return redirect(url_for('reset_pwd'))
    form=ChangePasswordForm()
    
    if form.validate_on_submit():
        print("here")
        m = sha256()
        m.update(form.mdp.data.encode())
        passwd = m.hexdigest()
        user.mdp = passwd
        db.session.commit()
        flash("mot de passe changer.","success" )
        return redirect(url_for("connection"))
    return render_template('change_password.html', form=form, token=token)

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
        qte = float(qte)
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
    return render_template("home.html", liste_produit_qte=results, actu_id_page=None)

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

#@app.errorhandler(404)
#def internal_error(error):
#    return redirect(url_for('home'))
