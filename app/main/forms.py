from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional
from flask_wtf.recaptcha import RecaptchaField


class QueryForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(4, 25)])
    email = StringField('Email', validators=[Email(), Length(1, 35)])
    number = StringField('Phone number', validators=[DataRequired(), Length(8, 15, message='Length 8-15')])
    description = TextAreaField('Description', validators=[Optional()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Send your query')


class SubscriptionForm(FlaskForm):
    email = StringField('Email', validators=[Email(), Length(1, 35)])
    submit = SubmitField('Subscribe')
