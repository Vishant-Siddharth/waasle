from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, length, optional
from flask_wtf.recaptcha import RecaptchaField


class QueryForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), length(4, 25)])
    email = StringField('Email', validators=[Email(), length(1, 35)])
    number = StringField('Phone number', validators=[DataRequired(), length(8, 15, message='Length 8-15')])
    description = TextAreaField('Description', validators=[optional()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Send your query')
