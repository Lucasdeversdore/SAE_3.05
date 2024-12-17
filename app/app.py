

from flask import Flask
from flask_bootstrap import Bootstrap5
import os.path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

import nomDB


app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = "8e202471-f369-40b7-a917-516553e1b4c3"
bootstrap = Bootstrap5(app)
def mkpath (p):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), p))
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../'+nomDB.nomDB)) 
db = SQLAlchemy(app)
login_manager = LoginManager(app)

login_manager.login_view = "connecter"


app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None

mail = Mail()
mail.init_app(app)
mail=Mail(app)


