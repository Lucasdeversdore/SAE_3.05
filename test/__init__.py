import os, sys
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(os.path.abspath(ROOT))

# Connexion à la base de données myapp
myapp_engine = create_engine('sqlite:///myapp.db')
myapp_metadata = MetaData()  # Utilise l'initialisation par défaut
myapp_metadata.reflect(bind=myapp_engine)  # Récupère les informations sur les tables existantes

# Connexion à la base de données cible
test_engine = create_engine('sqlite:///test.db')
test_metadata = MetaData()

# Crée les tables dans la base de données cible
myapp_metadata.create_all(test_engine)

# Pas sûr de faire ça,
# # peut-être juste copier les tables sans le contenu puis charger des données constantes

# # Crée une session pour la base de données source
# MyappSession = sessionmaker(bind=myapp_engine)
# myapp_session = MyappSession()

# # Crée une session pour la base de données cible
# TestSession = sessionmaker(bind=test_engine)
# test_session = TestSession()

# # Copier les données de chaque table de la base source vers la base cible
# for table in myapp_metadata.sorted_tables:
#     data = myapp_session.query(table).all()
#     for row in data:
#         test_session.execute(table.insert(), row._asdict())

# # Commit les modifications
# test_session.commit()

# # Ferme les sessions
# myapp_session.close()
# test_session.close()
