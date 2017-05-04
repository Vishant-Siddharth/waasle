from flask import render_template, session, redirect, url_for, request, flash
from ..main import main
from flask_login import current_user
from .forms import QueryForm, SubscriptionForm, MobileForm
from ..models import Contact, Subscription, Mobile
from app import db


@main.context_processor         # to add variables in template scope
def include_template_variables():
    return {'form_sub': SubscriptionForm(), 'form_mob': MobileForm(), 'w_f': 49, 'w_i': 59, 'dc': 79}


@main.context_processor         # to add variables in template scope
def include_template_function():
    def typ(x):
        return type(x)
    return dict(type=typ)


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/pricing', methods=['GET', 'POST'])
def pricing():
    return render_template('pricing.html')


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = QueryForm()
    if form.validate_on_submit():
        user = Contact()
        try:
            user.name = form.name.data.title()
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


@main.route('/our_mission', methods=['GET', 'POST'])
def mission():
    return render_template('mission.html')


@main.route('/our_vision', methods=['GET', 'POST'])
def vision():
    return render_template('vision.html')


@main.route('/blog')
def blog():
    return redirect(url_for('main.index'))


@main.route('/why-us', methods=['GET', 'POST'])
def why_us():
    return render_template('why-us.html')


@main.route('/about-us', methods=['GET', 'POST'])
def about_us():
    return render_template('about_us.html')


@main.route('/terms-&-conditions')
def t_and_q():
    return 'terms-&-conditions'


@main.route('/subscribe', methods=['Get', 'POST'])
def subscribe():
    if request.method == 'GET':
        return redirect(url_for('main.index'))
    else:
        form_sub = SubscriptionForm()
        if form_sub.validate_on_submit():
            sub = Subscription()
            try:
                sub.email = form_sub.email.data
                db.session.add(sub)
                db.session.commit()
                flash("Thank you for subscribing to us. You'll get our latest offers right in your email box.")
                return redirect(url_for('main.index'))
            except:
                db.session.rollback()
                flash("You are already subscribed to us.")
        else:
            for i, v in form_sub.errors.items():
                flash(v[0])
        return redirect(url_for('main.index'))


@main.route('/app', methods=['Get', 'POST'])
def mobile_app():
    if request.method == 'GET':
        return redirect(url_for('main.index'))
    else:
        form_mob = MobileForm()
        if form_mob.validate_on_submit():
            mob = Mobile()
            try:
                mob.number = form_mob.number.data
                db.session.add(mob)
                db.session.commit()
                return redirect(url_for('main.app_link'))
            except:
                db.session.rollback()
                return redirect(url_for('main.app_link'))
        else:
            for i, v in form_mob.errors.items():
                flash(v[0])
        return redirect(url_for('main.index'))


@main.route('/app/get-app', methods=['Get', 'POST'])
def app_link():
    return redirect("http://bit.ly/1K38IWh")


@main.route('/unsubscribe/<token>')         # Will implement it afterwards
def unsubscribe():
    if request.method == 'GET':
        return redirect(url_for('main.index'))
    else:
        form_sub = SubscriptionForm()
        if form_sub.validate_on_submit():
            sub = Subscription()
            try:
                sub.email = form_sub.email.data
                db.session.add(sub)
                db.session.commit()
                flash("Thank you for subscribing to us. You'll get our latest offers right in your email box.")
                return redirect(url_for('main.index'))
            except:
                db.session.rollback()
                flash("You are already subscribed to us.")
        else:
            for i, v in form_sub.errors.items():
                flash(v[0])
        return redirect(url_for('main.index'))
