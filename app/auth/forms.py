from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, \
    PasswordField, RadioField, BooleanField, DateField, SelectField
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
    city = SelectField('City', validators=[DataRequired()], choices=[('Lucknow', 'Lucknow')])
    pincode = SelectField('Pin Code', validators=[DataRequired()], choices=[('226001', '226001'), ('226002', '226002'),
        ('226003', '226003'), ('226004', '226004'), ('226005', '226005'), ('226006', '226006'), ('226007', '226007'),
        ('226008', '226008'), ('226009', '226009'), ('226010', '226010'), ('226011', '226011'), ('226012', '226012'),
        ('226013', '226013'), ('226014', '226014'), ('226015', '226015'), ('226016', '226016'), ('226017', '226017'),
        ('226018', '226018'), ('226020', '226020'), ('226021', '226021'), ('226022', '226022'), ('226023', '226023'),
        ('226024', '226024'), ('226025', '226025'), ('226026', '226026'), ('227005', '227005'), ('227101', '227101'),
        ('227105', '227105'), ('227107', '227107'), ('227111', '227111'), ('227115', '227115'), ('227116', '227116'),
        ('227125', '227125'), ('227132', '227132'), ('227202', '227202'), ('227207', '227207'), ('227305', '227305'),
        ('227308', '227308'), ('227309', '227309')])
    terms = BooleanField('I agree the ', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Create Your Account')


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
                                                                                     message=
                                                                                     'Minimum 8 length and maximum 20')])
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
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class SubscriptionForm(FlaskForm):
    email = StringField('Email', validators=[Email(), Length(1, 35)])
    submit = SubmitField('Subscribe')


class BookNowForm(FlaskForm):
    date = DateField('Date and Time', format='%d/%m/%Y')
    number = StringField('Phone number', validators=[DataRequired(), Length(8, 15,
                                                                            message='length 8-15')])
    choice = RadioField(validators=[DataRequired()],
                        choices=[('same', 'Same'), ('new', 'New')], default='same')
    address_1 = StringField('Address Line 1', validators=[DataRequired(), Length(4, 256), ])
    address_2 = StringField('Address Line 2', validators=[DataRequired(), Length(4, 256), ])
    city = SelectField('City', validators=[DataRequired()], choices=[('Lucknow', 'Lucknow')])
    pincode = SelectField('Pin Code', validators=[DataRequired()], choices=[('226001', '226001'), ('226002', '226002'),
        ('226003', '226003'), ('226004', '226004'), ('226005', '226005'), ('226006', '226006'), ('226007', '226007'),
        ('226008', '226008'), ('226009', '226009'), ('226010', '226010'), ('226011', '226011'), ('226012', '226012'),
        ('226013', '226013'), ('226014', '226014'), ('226015', '226015'), ('226016', '226016'), ('226017', '226017'),
        ('226018', '226018'), ('226020', '226020'), ('226021', '226021'), ('226022', '226022'), ('226023', '226023'),
        ('226024', '226024'), ('226025', '226025'), ('226026', '226026'), ('227005', '227005'), ('227101', '227101'),
        ('227105', '227105'), ('227107', '227107'), ('227111', '227111'), ('227115', '227115'), ('227116', '227116'),
        ('227125', '227125'), ('227132', '227132'), ('227202', '227202'), ('227207', '227207'), ('227305', '227305'),
        ('227308', '227308'), ('227309', '227309')])
    submit = SubmitField('Book Now')


class RescheduleForm(FlaskForm):
    date = DateField('Date and Time', format='%d/%m/%Y')
    order = IntegerField('order')
    number = StringField('Phone number', validators=[DataRequired(), Length(8, 15,
                                                                            message='length 8-15')])
    choice = RadioField(validators=[DataRequired()],
                        choices=[('same', 'Same'), ('new', 'New')], default='same')
    address_1 = StringField('Address Line 1', validators=[DataRequired(), Length(4, 256), ])
    address_2 = StringField('Address Line 2', validators=[DataRequired(), Length(4, 256), ])
    city = SelectField('City', validators=[DataRequired()], choices=[('Lucknow', 'Lucknow')])
    pincode = SelectField('Pin Code', validators=[DataRequired()], choices=[('226001', '226001'), ('226002', '226002'),
        ('226003', '226003'), ('226004', '226004'), ('226005', '226005'), ('226006', '226006'), ('226007', '226007'),
        ('226008', '226008'), ('226009', '226009'), ('226010', '226010'), ('226011', '226011'), ('226012', '226012'),
        ('226013', '226013'), ('226014', '226014'), ('226015', '226015'), ('226016', '226016'), ('226017', '226017'),
        ('226018', '226018'), ('226020', '226020'), ('226021', '226021'), ('226022', '226022'), ('226023', '226023'),
        ('226024', '226024'), ('226025', '226025'), ('226026', '226026'), ('227005', '227005'), ('227101', '227101'),
        ('227105', '227105'), ('227107', '227107'), ('227111', '227111'), ('227115', '227115'), ('227116', '227116'),
        ('227125', '227125'), ('227132', '227132'), ('227202', '227202'), ('227207', '227207'), ('227305', '227305'),
        ('227308', '227308'), ('227309', '227309')])
    submit = SubmitField('Confirm')
