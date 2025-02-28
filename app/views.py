from hashlib import sha256
import base64
import os
import time
from app.csv_to_db import csv_to_db
from .app import UPLOAD_FOLDER, app, db, mail, cache
from flask_login import login_required, login_user, logout_user, current_user
from flask import jsonify, redirect, render_template, send_file, url_for, request, Flask, render_template, redirect, url_for, flash
from flask_mail import Message
from .models import (
    Chimiste,
    Commande,
    Faire,
    Produit,
    Est_Stocker,
    Lieu_Stockage,
    Fournisseur,
    next_chimiste_id,
    save_modif_reserv,
    search_filter,
    search_famille_filter,
    search_chimiste_filter,
    search_reserv_filter,
    reserver_prod,
    modif_sauvegarde,
    ajout_sauvegarde,
    get_pagination_produits,
    get_nb_page_max_produits,
    get_pagination_reservations,
    get_nb_page_max_reservations,
    send_mail_activation,
    send_mail_etat,
    send_mail_mdp,
    send_mail_supp,
    update_etat,
    delete_reservation,
    ajout_fournisseur_sauvegarde,
    ajout_lieu_sauvegarde,
    cacher_le_produit,
    montrer_le_produit,
    creer_pdf_produit_en_dessous_du_seuil

)

from .form import *

@app.route("/")
@login_required
def home():
    return home_page()


@app.route("/<int:id_page>", methods=['GET'])
@login_required
def home_page(id_page=1, nb=15):
    print(1)
    if id_page < 1:
        return redirect("/")
    id_page_max = get_nb_page_max_produits(nb)
    if id_page_max < id_page:
        return redirect(url_for('home_page', id_page=id_page_max))
    liste_produit_qte = get_pagination_produits(page=id_page, nb=nb)
    return render_template("home.html", liste_produit_qte=liste_produit_qte, actu_id_page=id_page, total_pages=id_page_max, nbmax=nb)



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
        return redirect(url_for('preparation_reservation_page', id_page=1))

    id_page_max = get_nb_page_max_reservations(nb, current_user)

    if id_page > id_page_max:
        return redirect(url_for('preparation_reservation_page', id_page=id_page_max))

    reservations_etats = get_pagination_reservations(page=id_page, nb=nb, chimiste=current_user)

    return render_template(
        "reservation-preparation.html",
        reservations_etats=reservations_etats,
        actu_id_page=id_page,
        id_page_max=id_page_max,  # On garde cette variable
        total_pages=id_page_max   # Ajout pour éviter l'erreur dans Jinja
    )




# Même chose que pour "/1"
@app.route("/preparation/reservations/1")
@login_required
def preparation_reservation_page_1():
    return redirect("/preparation/reservations")



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
            form.email.errors.append('Cet email est déjà utilisé.')
        else:
            nouveau_chimiste = Chimiste(idChimiste=next_chimiste_id(), prenom=prenom, nom=nom, email=email, mdp=passwd)
            send_mail_activation(nouveau_chimiste)
            flash("Veuillez consulter vos e-mails pour activer votre compte.", "info")
            return redirect(url_for('connection'))
    return render_template('inscription.html', form=form)

@app.route("/settings", methods=('GET', 'POST'))
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        prenom = form.prenom.data
        nom = form.nom.data
        info = form.info.data
        old_mdp = form.old_mdp.data
        mdp = form.mdp.data
        confirm_mdp = form.confirm_mdp.data

        if current_user.nom != nom:
            current_user.changer_nom(nom)
        if current_user.prenom != prenom:
            current_user.changer_prenom(prenom)
        if current_user.info != info:
            current_user.reception_notif()

        if mdp != "":
            m = sha256()
            m.update(old_mdp.encode())
            passwd = m.hexdigest()
            if passwd == current_user.mdp:
                m = sha256()
                m.update(mdp.encode())
                passwd = m.hexdigest()
                current_user.mdp = passwd
                db.session.commit()
                flash("Votre mot de passe à été changé avec succès.","info" )

    return render_template("settings.html", form=form)

@app.route("/inscription-cgu")
def cgu():
    return render_template("inscription-cgu.html")


@app.route('/activation/<token>/<time_in_link>', methods=['GET', 'POST'])
def activation_token(token, time_in_link):

    decoded_time = base64.urlsafe_b64decode(time_in_link).decode()

    user=Chimiste.verify_activation_token(token, decoded_time)
    if user is None:
        flash('Token invalide ou expiré. Veulliez réessayer de vous inscrire.', "info")
        return redirect(url_for('inscrire'))
    
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('connection'))


@app.route("/connection", methods=('GET', 'POST'))
def connection():
    user = None
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect(next)
    
    return render_template("connection.html", form=f)


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
            flash("Regardez vos mail pour réinitialiser votre mot de passe.", "info")
            return redirect(url_for('connection'))
        else:
            form.email.errors.append('Email invalid')
    return render_template("reset_pwd.html", form=form)

@app.route('/reset_pwd/<token>/<time_in_link>', methods=['GET', 'POST'])
def reset_token(token, time_in_link):
    # Décoder plus tard
    decoded_time = base64.urlsafe_b64decode(time_in_link).decode()
    
    user=Chimiste.verify_mdp_token(token=token, time_in_link=decoded_time)
    if user is None:
        flash('Token invalide ou expiré. Veulliez réessayer.', 'info')
        return redirect(url_for('reset_pwd'))
    form=ChangePasswordForm()
    
    if form.validate_on_submit():
        m = sha256()
        m.update(form.mdp.data.encode())
        passwd = m.hexdigest()
        user.mdp = passwd
        db.session.commit()
        flash("Votre mot de passe à été changé avec succès.","info" )
        return redirect(url_for("connection"))
    print("page change password "+decoded_time)
    return render_template('change_password.html', form=form, token=token)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('connection'))


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
    if qte == "":
        qte = 0
    else:
        qte = float(qte)
    res = reserver_prod(id_produit, qte, current_user.idChimiste)
    if res:
        return jsonify(success=True, message="Réservation réussie !"), 200
    else:
        return jsonify(success=False, message="Quantité non valide"), 400   
    

@app.route('/commande/<int:id_commande>', methods=['GET'])
@login_required
def popup_modifier_commande(id_commande, erreur=None):
    commande=Commande.query.get(id_commande).to_dict()
    produit = Produit.query.get(commande["idProduit"]).to_dict()
    stock=Est_Stocker.query.filter(Est_Stocker.idProduit == commande["idProduit"]).first().to_dict()
    return jsonify(commande=commande, produit=produit, stock=stock, erreur=erreur)
    
@app.route('/commande/modif/<int:id_commande>', methods=('GET',))
@login_required
def modifier_reserv(id_commande):
    commande = Commande.query.get(id_commande)
    qte = request.args.get("inputQte")
    if qte == "":
        qte = 0
    else:
        qte = float(qte)
    res = save_modif_reserv(id_commande, qte, commande.qteCommande)
    if res:
        return jsonify(success=True, message="Modification réussie !"), 200
    else:
        return jsonify(success=False, message="Quantité non valide"), 400 

@app.route('/modifier/<int:id_produit>', methods=['GET'])
@login_required
def get_modif_produit(id_produit):
    if current_user.estPreparateur:
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
        if id_fou is None:
            fournisseur = ""
        else:
            fournisseur = Fournisseur.query.filter(Fournisseur.idFou == id_fou).first().to_dict()
        return jsonify(produit=produit, lieu=lieu, fournisseur=fournisseur, est_stocker=est_stocker, les_fournisseurs=les_fournisseurs, les_fonctions=les_fonctions, les_lieux=les_lieux) 
    return redirect("/")    

@app.route('/ajouter', methods=['GET'])
@login_required
def get_fonction_lieux():

    les_four = Fournisseur.query.all()
    les_fournisseurs = []
    for fourn in les_four:
            les_fournisseurs.append(fourn.to_dict())
    
    les_li = Lieu_Stockage.query.all()
    les_lieux = []
    for li in les_li:
        les_lieux.append(li.to_dict())
    return jsonify(les_fournisseurs=les_fournisseurs, les_lieux=les_lieux)

@app.route('/sauvegarder/<int:id_produit>',  methods=['GET'])
@login_required
def sauvegarder_modif(id_produit):
    nom = request.args.get("inputNom")
    four = request.args.get("textFournisseur")
    quantite = request.args.get("textQuantite")
    seuil = request.args.get("textSeuil")
    fonction = request.args.get("textFonction")
    lieu = request.args.get("textLieu")
    res = modif_sauvegarde(id_produit, nom, four, quantite, seuil, fonction, lieu)
    if res:
        return jsonify(success=True, message="Modification réussie !"), 200
    else:
        return jsonify(success=False, message="Quantité non valide"), 400

@app.route("/search/famille/<int:id_produit>", methods=('GET',))
@login_required
@cache.cached(timeout=300)
def searchByButton(id_produit):
    prod = Produit.query.get(id_produit)
    q = str(prod.fonctionProduit)
    results = search_famille_filter(q)
    return render_template("home.html", liste_produit_qte=results, actu_id_page=None)

@app.route('/ajout/sauvegarder/', methods=['POST'])
@login_required
def sauvegarder_ajout():
    data = request.get_json()
    nom = data.get("textNom")
    four = data.get("textFournisseur")
    unite = data.get("textUnite")
    quantite = data.get("textQuantite")
    seuil = data.get("textSeuil")
    fonction = data.get("textFonction")
    lieu = data.get("textLieu")

    res = ajout_sauvegarde(nom, four, unite, quantite, seuil, fonction, lieu)
    if res:
        return jsonify(success=True, message="Produit créé !"), 200
    else:
        return jsonify(success=False, message="Quantité non valide"), 400
    
@app.route('/ajoutLieu/sauvegarder', methods=['POST'])
@login_required
def sauvegarder_ajout_lieu():
    data = request.get_json()
    nom_lieu = data.get("nomLieu")

    if not nom_lieu:
        return jsonify(success=False, message="Nom du lieu requis"), 400

    if ajout_lieu_sauvegarde(nom_lieu):
        return jsonify(success=True, message="Lieu ajouté avec succès !"), 200
    else:
        return jsonify(success=False, message="Le lieu existe déjà ou une erreur est survenue."), 400


@app.route('/ajoutFournisseur/sauvegarder', methods=['POST'])
@login_required
def sauvegarder_ajout_fournisseur():
    data = request.get_json()
    nom_fou = data.get("nomFournisseur")
    adresse_fou = data.get("adresseFournisseur")
    num_tel_fou = data.get("telephoneFournisseur")

    # Validation des données : seul le nom est obligatoire
    if not nom_fou:
        return jsonify(success=False, message="Nom du fournisseur requis"), 400

    # Appel de la fonction pour sauvegarder le fournisseur
    if ajout_fournisseur_sauvegarde(nom_fou, adresse_fou, num_tel_fou):
        return jsonify(success=True, message="Fournisseur ajouté avec succès !"), 200
    else:
        return jsonify(success=False, message="Le fournisseur existe déjà ou une erreur est survenue."), 400


@app.route('/etat/commande/<int:idCommande>', methods=['GET', 'POST'])
def etat_commande(idCommande):
    if current_user.estPreparateur:
        update_etat(idCommande, current_user.idChimiste)
        commande = Commande.query.get(idCommande)
        chimiste = Chimiste.query.get(commande.idChimiste)
        send_mail_etat(chimiste, commande)
    return redirect(url_for("preparation_reservation"))


@app.route('/supprimer/reservation/<int:idCommande>')
@login_required
def suppr_reservation(idCommande):
    if current_user.estPreparateur:
        commande = Commande.query.get(idCommande)
        send_mail_supp(current_user, commande)
    delete_reservation(idCommande, current_user.idChimiste)
    return redirect(url_for("preparation_reservation"))



@app.route('/pop_up_cacher/<int:id_produit>',  methods=['GET'])
@login_required
def pop_up_cacher(id_produit):
    if current_user.estPreparateur:
        produit = Produit.query.get(id_produit)
        return jsonify(id_produit=id_produit, nomProduit=produit.nomProduit)
    return redirect(url_for("home"))


@app.route('/cacher/<int:id_produit>',  methods=['GET'])
@login_required
def cacher(id_produit):
    if current_user.estPreparateur:
        res = cacher_le_produit(id_produit)
        if res:
            return jsonify(success=True, message="Vous avez caché le produit !"), 200
        else:
            return jsonify(success=False, message="Vous n'avez pas caché le produit !"), 400
    return redirect(url_for("home"))


@app.route('/pop_up_montrer/<int:id_produit>',  methods=['GET'])
@login_required
def pop_up_montrer(id_produit):
    if current_user.estPreparateur:
        produit = Produit.query.get(id_produit)
        return jsonify(id_produit=id_produit, nomProduit=produit.nomProduit)
    return redirect(url_for("home"))


@app.route('/montrer/<int:id_produit>',  methods=['GET'])
@login_required
def montrer(id_produit):
    if current_user.estPreparateur:
        res = montrer_le_produit(id_produit)
        if res:
            return jsonify(success=True, message="Vous avez montré le produit !"), 200
        else:
            return jsonify(success=False, message="Vous n'avez pas montré le produit !"), 400
    return redirect(url_for("home"))

@app.errorhandler(404)
def internal_error(error):
    return redirect(url_for('home'))

@app.errorhandler(405)
def method_error(error):
    return redirect(url_for('home'))

@app.route('/generate_pdf', methods=['POST'])
@login_required
def generate_pdf():
    if current_user.estPreparateur:
        pdf_file = creer_pdf_produit_en_dessous_du_seuil()
        return send_file(pdf_file, as_attachment=True)
    return redirect(url_for('home'))


@app.route('/ajout_csv', methods=['POST'])
@login_required
def ajout_csv():
    if 'file' not in request.files:
        return "Aucun fichier envoyé", 400  # Erreur si aucun fichier

    file = request.files['file']
    chemin = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(chemin)
    if current_user.estPreparateur:
        if csv_to_db(chemin):
            os.remove(chemin)
            return jsonify(success=True, message="Données ajoutées !"), 200
        else:
            os.remove(chemin)
            return jsonify(success=False, message="Il y a eu un problème, vérifier que le fichier csv est conforme."), 400
    return redirect(url_for('home'))
