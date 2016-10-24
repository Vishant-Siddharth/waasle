from flask import render_template, session, redirect, url_for, request, flash
from ..main import main
import json
from .forms import QueryForm
from ..auth.forms import RegistrationForm
from ..models import User, Contact
from app import db
from datetime import datetime
from urllib.request import urlopen


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
