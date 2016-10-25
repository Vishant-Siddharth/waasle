from flask import render_template
from ..main import main


@main.app_errorhandler(404)     # Will route all the errors
def page_not_found(e):
    return render_template('404.html'), 404