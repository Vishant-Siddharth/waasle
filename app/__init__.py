import os
from flask import Flask
from flask_mail import Mail         # To send mails, wrapper around smtplib module
from flask_moment import Moment     # for date and time using jquery
from flask_sqlalchemy import SQLAlchemy     # using orm wrapper around sqlalchemy
from flask_login import LoginManager        # for login sessions
from flask_bcrypt import Bcrypt             # for hashing method used is bcrypt
from . import config              # config file having different configurations


db = SQLAlchemy()
mail = Mail()
moment = Moment()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'     # Default login page, after any bad requests


import app.models


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.config[config_name])
    config.config[config_name].init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # attach routes and custom error pages herereturn app
    return app


app = create_app(os.environ.get('FLASKY_CONFIG'))
