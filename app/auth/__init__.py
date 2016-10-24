from flask import Blueprint     # Importing Blueprint for multiple apps


auth = Blueprint('auth', __name__)      #Blueprint of the auth app
# to be added in app

from . import views     # Views of auth app
from . import errors    # Errors of auth app
