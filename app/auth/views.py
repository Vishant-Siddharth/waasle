from flask import render_template, redirect, request, url_for, flash, g
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User, Mobile, Subscription, Order
from ..emails import send_email
from ..decorators import only_confirmed
from .forms import LoginForm, RegistrationForm, ChangePasswordForm,\
    PasswordResetRequestForm, PasswordResetForm, SubscriptionForm, \
    BookNowForm, RescheduleForm
from ..main.forms import MobileForm
import datetime

'''
@auth.before_app_request        # this is run every time a request is made to the auth app
def before_request():
    if current_user.is_authenticated:       # if the current_user is authenticate
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':        # endpoint = auth.<function_name>
            return redirect(url_for('auth.unconfirmed'))
'''


@auth.context_processor         # to add variables in template scope
def include_template_variables():
    return {'form_sub': SubscriptionForm(), 'form_mob': MobileForm()}


@auth.context_processor         # to add variables in template scope
def include_template_function():
    def length(x):
        return len(x)
    return dict(len=length)


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form_register = RegistrationForm()
    form_login = LoginForm()
    if not current_user.is_authenticated:
        if request.args.get('type') == 'login':
            if form_login.validate_on_submit():
                user = User.query.filter_by(email=form_login.email.data).first()
                if user is not None and user.verify_password(form_login.password.data):
                    login_user(user, form_login.remember_me.data)
                    return redirect(request.args.get('next') or url_for('auth.account'))
                else:
                    flash('Invalid email or password')
            else:
                flash('Invalid email or password')
        elif request.args.get('type') == 'register':
            if form_register.validate_on_submit():
                user = User()
                try:
                    if form_register.terms.data is True:
                        user.name = form_register.name.data.title()
                        user.email = form_register.email.data
                        user.mob = form_register.number.data
                        user.password_hash(form_register.password.data)
                        user.address_1 = form_register.address_1.data
                        user.address_2 = form_register.address_2.data
                        user.city = form_register.city.data
                        user.pincode = int(form_register.pincode.data)
                        db.session.add(user)
                        db.session.commit()
                        try:
                            mobile = Mobile()
                            mobile.number = user.mob
                            subscription = Subscription()
                            subscription.email = user.email
                            db.session.add(mobile)
                            db.session.add(subscription)
                            db.seesion.commit()
                        except:
                            db.session.rollback()
                        token = user.generate_confirmation_token()
                        send_email(user.email, 'Confirm Your Account',
                                   'auth/email/confirm', user=user, token=token)
                        flash('A confirmation email has been sent to you by email.')
                        return redirect(url_for('main.index'))
                    else:
                        flash('Please accept the terms and conditions.')
                except :
                    db.session.rollback()
                    flash('Something Went Wrong. Please try again')
            else:
                for i, v in form_register.errors.items():
                    flash(v[0])
        elif request.args.get('next'):
            tmp = request.args.get('next')
            return render_template('auth/login.html', form_reg=form_register, form_log=form_login, next=tmp)
        return render_template('auth/login.html', form_reg=form_register, form_log=form_login, next=None)
    else:
        return redirect(url_for('auth.account'))


@auth.route('/account')
@login_required
def account():
    return render_template('auth/account.html', user_name=current_user.name)


@auth.route('/book-now', methods=['GET', 'POST'])
@login_required
@only_confirmed
def book_now():
    form_book = BookNowForm()
    date = request.args.get('date', default=None)
    if (request.args.get('submit', None) == 'Book Now') and date != '':
        tmp = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        if tmp >= datetime.date.today():
            order = Order()
            try:
                order.pick_up = tmp
                order.user_id = current_user.id
                order.status = 'Processing'
                order.service = request.args.get('service')
                db.session.add(order)
                db.session.commit()
                if request.args.get('choice') == 'new':
                    user = User.query.filter_by(id=current_user.id).first()
                    user.mob = request.args.get('number') if request.args.get('number') != '' else user.mob
                    user.address_1 = request.args.get('address_1') if request.args.get('address_1') else user.address_1
                    user.address_2 = request.args.get('address_2') if request.args.get('address_2') else user.address_2
                    user.city = request.args.get('city') if request.args.get('city') else user.city
                    user.pincode = request.args.get('pincode') if request.args.get('pincode') else user.pincode
                    db.session.add(user)
                    db.session.commit()
                send_email(current_user.email, 'Scheduled Pickup',
                           'auth/email/pickup', user=current_user, order=order)
                flash("Your order has been placed")
                return redirect(url_for('auth.orders'))
            except:
                db.session.rollback()
                flash('Something Went Wrong. Please try again')
        else:
            flash('Wrong choice. Please try again.')
    return render_template('auth/book_now.html', form_book=form_book)


@auth.route('/orders')
@login_required
@only_confirmed
def orders():
    return render_template('auth/orders.html')


@auth.route('/reschedule')
@login_required
@only_confirmed
def reschedule():
    form_re = RescheduleForm()
    order = Order()
    id = request.args.get('order', None)
    if request.args.get('submit', None) == 'Confirm':
        date = request.args.get('date', default=None)
        if date != '':
            tmp = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            if tmp >= datetime.date.today():
                order = Order.query.filter_by(id=request.args.get('order', None)).first()
                try:
                    order.pick_up = tmp
                    order.status = 'Rescheduled'
                    order.service = request.args.get('service')
                    db.session.add(order)
                    db.session.commit()
                    if request.args.get('choice') == 'new':
                        user = User.query.filter_by(id=current_user.id).first()
                        user.mob = request.args.get('number') if request.args.get('number') != '' else user.mob
                        user.address_1 = request.args.get('address_1') if request.args.get('address_1') else user.address_1
                        user.address_2 = request.args.get('address_2') if request.args.get('address_2') else user.address_2
                        user.city = request.args.get('city') if request.args.get('city') else user.city
                        user.pincode = request.args.get('pincode') if request.args.get('pincode') else user.pincode
                        db.session.add(user)
                        db.session.commit()
                    flash("Your order has been rescheduled")
                    return redirect(url_for('auth.orders'))
                except:
                    db.session.rollback()
                    flash('Something Went Wrong. Please try again')
        else:
            flash('Wrong choice. Please try again.')
        return render_template('auth/reschedule.html', form_re=form_re, order=id)
    elif request.args.get('submit', None) == 'Reschedule':
        return render_template('auth/reschedule.html', form_re=form_re, order=id)
    elif request.args.get('submit', None) == 'Delete':
        order = Order.query.filter_by(id=id).first()
        if order:
            try:
                order.status = 'Cancelled'
                db.session.add(order)
                db.session.commit()
                flash('Your order has been cancelled')
            except:
                db.session.rollback()
                flash('Something Went Wrong. Please try again')
        return redirect(url_for('auth.orders'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out.')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('auth.account'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
        return redirect(url_for('auth.account'))
    else:
        flash('The confirmation link is invalid or has expired.')
        return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if current_user.verify_password(form.old_password.data):
                try:
                    current_user.password_hash(form.password.data)
                    db.session.add(current_user)
                    db.session.commit()
                    flash('Your password has been updated.')
                except:
                    db.session.rollback()
                    flash('Something Went Wrong. Please try again')
                return redirect(url_for('main.index'))
            else:
                flash('Invalid password.')
        else:
            for i, v in form.errors.items():
                flash(v[0])
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if request.method == 'GET':
        return render_template('auth/reset_password.html', form=form)
    else:
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                token = user.generate_reset_token()
                send_email(user.email, 'Reset Your Password',
                           'auth/email/reset_password',
                           user=user, token=token,
                           next=request.args.get('next'))
            flash('An email with instructions to reset your password has been '
                  'sent to you.')
            return redirect(url_for('auth.login'))
        flash('Entered email address is not registered')
        return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        tmp = user.reset_password(token, form.password.data)        # storing the result
        if tmp == 'True':
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            flash(tmp)
            return redirect(url_for('main.index'))
    else:
        for i, v in form.errors.items():
            flash(v[0])
    return render_template('auth/resetting_password.html', form=form, token=token)
