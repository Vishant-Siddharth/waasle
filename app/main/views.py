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
    return render_template('base.html')


@main.route('/login')
def login():
    return render_template('account.html')


@main.route('/pricing', methods=['GET', 'POST'])
def pricing():
    return render_template('base.html')


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = QueryForm()
    return render_template('contact.html', form=form)


@main.route('/faq', methods=['GET', 'POST'])
def faq():
    return render_template('faq.html')


@main.route('/location', methods=['GET', 'POST'])
def location():
    return render_template('location.html')


@main.route('/services', methods=['GET', 'POST'])
def services():
    return render_template('services.html')


@main.route('/mission', methods=['GET', 'POST'])
def mission():
    return render_template('mission.html')


@main.route('/vision', methods=['GET', 'POST'])
def vision():
    return render_template('vision.html')


@main.route('/blog', methods=['GET', 'POST'])
def blog():
    return render_template('blog.html')


@main.route('/why-us', methods=['GET', 'POST'])
def why_us():
    return render_template('why-us.html')
