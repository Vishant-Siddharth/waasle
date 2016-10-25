from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from ..emails import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm,\
    PasswordResetRequestForm, PasswordResetForm


@auth.before_app_request        # this is run every time a request is made to the auth app
def before_request():
    if current_user.is_authenticated:       # if the current_user is authenticate
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.':        # endpoint = auth.<function_name>
            return redirect(url_for('auth.unconfirmed'))


@auth.context_processor         # to add variables in template scope
def include_template_variables():
    return {'variable': 'value'}
    pass


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
        if form_login.validate_on_submit():
            user = User.query.filter_by(email=form_login.email.data).first()
            if user is not None and user.verify_password(form_login.password.data):
                login_user(user, form_login.remember_me.data)
                return redirect(request.args.get('next') or url_for('main.index'))
            flash('Invalid username or password.')
        if form_register.validate_on_submit():
            try:
                user = User()
                user.name = form_register.name.data
                user.email = form_register.email.data
                user.mob = form_register.number.data
                user.password = form_register.password.data
                user.address_1 = form_register.address_1.data
                user.address_2 = form_register.address_2.data
                user.city = form_register.city.data
                user.pincode = form_register.pincode.data
                db.session.add(user)
                db.session.commit()
                token = user.generate_confirmation_token()
                send_email(user.email, 'Confirm Your Account',
                           'auth/email/confirm', user=user, token=token)
                flash('A confirmation email has been sent to you by email.')
                return redirect(url_for('auth.account'))
            except:
                db.session.rollback()
                flash('Something Went Wrong. Please try again')
        return render_template('auth/login.html')
    else:
        return render_template('auth/account.html')


@auth.route('/account')
def account():
    return render_template('auth/account.html')


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
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
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
#@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            try:
                current_user.password = form.password.data
                db.session.add(current_user)
                db.session.commit()
                flash('Your password has been updated.')
            except:
                db.session.rollback()
                flash('Something Went Wrong. Please try again')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
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
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            flash('Something Went Wrong. Please try again')
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)
