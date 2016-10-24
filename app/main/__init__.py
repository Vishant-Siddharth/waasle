from flask import Blueprint     # Importing Blueprint for multiple apps


main = Blueprint('main', __name__)      #Blueprint of the main app
# to be added in manage
from . import views     # Views of main app
#from . import errors    # Errors of main app
