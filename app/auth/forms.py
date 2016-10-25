from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, \
    PasswordField, RadioField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.recaptcha import RecaptchaField  # enabling google re-captcha automatically
from ..models import User
from wtforms import ValidationError


class RegistrationForm(FlaskForm):       # The first form to be filled by user
    name = StringField('Your Name', validators=[DataRequired(), Length(4, 25), ])
    # Validators with min and max length
    email = StringField('Email', validators=[Email(), Length(1, 64)])
    number = StringField('Phone number', validators=[DataRequired(), Length(8, 15,
                                                                            message='length 8-15')])
    # Use of StringField so as to maintain the value of zero in front of the number
    password = PasswordField('Password', validators=[EqualTo('password_confirm',
                                                             message='Password must match.'),
                                                     DataRequired(message='Field is Required'),
                                                     Length(8, 20,
                                                     message='Minimum 8 length and maximum 20')])
    # To make the user enter at least 8 digit long password
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    address_1 = StringField('Address Line 1', validators=[DataRequired(), Length(4, 256), ])
    address_2 = StringField('Address Line 2', validators=[DataRequired(), Length(4, 256), ])
    city = StringField('City', validators=[DataRequired(), Length(4, 25), ])
    pincode = IntegerField('Pin Code', validators=[DataRequired()])
    terms = BooleanField('Term & Conditions.', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Get Your Purchase ID')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match'), Length(8, 20,
                        message='Minimum 8 length and maximum 20')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email_id=field.data).first() is None:
            raise ValidationError('Unknown email address.')
