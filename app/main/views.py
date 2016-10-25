from flask import render_template, session, redirect, url_for, request, flash
from ..main import main
from .forms import QueryForm
from ..models import User, Contact
from app import db


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/pricing', methods=['GET', 'POST'])
def pricing():
    return render_template('base.html')


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = QueryForm()
    if form.validate_on_submit():
        user = Contact()
        try:
            user.name = form.name.data
            user.email = form.email.data
            user.mob = form.number.data
            user.description = form.description.data
            db.session.add(user)
            db.session.commit()
            flash('Your query has been successfully submitted.')
            return redirect(url_for('main.index'))
        except:
            db.session.rollback()
            flash('Something Went Wrong. Please try again')
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


@main.route('/typo')
def typo():
    return render_template('typo.html')
